"""Web 服务器：定义所有 API 路由。"""
from __future__ import annotations

import asyncio
import json
import uuid
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from io import BytesIO
from pathlib import Path
from typing import Any

import uvicorn
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, ConfigDict, Field

from app.cleaning import export_results, generate_sentiment_analysis, generate_wordcloud, list_results
from app.command_engine import execute_command
from app.config import get_settings
from app.db import init_db
from app.errors import AppError, ERROR_MESSAGES
from app.service import (
    DEFAULT_DEPTH, DEFAULT_LIMIT,
    delete_task, get_task, list_event_logs, list_queue_items,
    list_tasks, log_command, submit_task,
)
from app.worker import start_queue_runtime


STATIC_DIR = Path(__file__).resolve().parent / "static"


class SubmitTaskRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    url: str
    limit: int = Field(default=DEFAULT_LIMIT, ge=1, le=1000)
    depth: int = Field(default=DEFAULT_DEPTH, ge=1, le=5)
    task_name: str | None = None
    keyword: str | None = None


class CommandRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    command: str = Field(min_length=1)
    request_id: str | None = None


class ExportRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    format: str = Field(min_length=1)


@asynccontextmanager
async def _lifespan(_: FastAPI) -> Any:
    init_db()
    start_queue_runtime()
    yield


def create_app() -> FastAPI:
    settings = get_settings()
    api = FastAPI(title="PyMS 爬虫控制台", version="0.1.0", lifespan=_lifespan)
    api.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

    @api.middleware("http")
    async def attach_request_id(request: Request, call_next: Any) -> Any:
        request.state.request_id = request.headers.get("X-Request-Id") or f"req_{uuid.uuid4().hex[:12]}"
        return await call_next(request)

    # API Key 校验（可选）
    @api.middleware("http")
    async def check_api_key(request: Request, call_next: Any) -> Any:
        path = request.url.path
        if not settings.api_key_enabled or path == "/" or path.startswith("/static/"):
            return await call_next(request)
        if not path.startswith("/v1/"):
            return await call_next(request)
        api_key = _read_api_key(request)
        if api_key != settings.api_key:
            return JSONResponse(status_code=401, content=_err(_rid(request), 1004, "unauthorized"))
        return await call_next(request)

    # 错误处理
    @api.exception_handler(AppError)
    async def handle_app_error(_: Request, exc: AppError) -> JSONResponse:
        code = 400 if exc.code < 5000 else 500
        if exc.code == 1004:
            code = 401
        if exc.code == 2001:
            code = 404
        return JSONResponse(status_code=code, content=_err(_rid(None), exc.code, exc.message))

    @api.exception_handler(Exception)
    async def handle_unexpected(_: Request, exc: Exception) -> JSONResponse:
        return JSONResponse(status_code=500, content=_err(_rid(None), 5000, ERROR_MESSAGES[5000]))

    @api.exception_handler(RequestValidationError)
    async def handle_validation(request: Request, exc: RequestValidationError) -> JSONResponse:
        return JSONResponse(status_code=400, content=_err(_rid(request), 1001, str(exc.errors())))

    # ---- 路由 ----

    @api.get("/", response_class=FileResponse)
    async def index() -> FileResponse:
        return FileResponse(STATIC_DIR / "index.html")

    @api.get("/v1/health")
    async def health(request: Request) -> dict[str, Any]:
        return _ok(_rid(request), {
            "status": "ok",
            "version": "0.1.0",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })

    @api.get("/v1/tasks")
    async def tasks(request: Request, task_id: str | None = None) -> dict[str, Any]:
        data = get_task(task_id) if task_id else list_tasks()
        return _ok(_rid(request), data)

    @api.get("/v1/tasks/{task_id}")
    async def task_detail(task_id: str, request: Request) -> dict[str, Any]:
        return _ok(_rid(request), get_task(task_id))

    @api.delete("/v1/tasks/{task_id}")
    async def task_delete(task_id: str, request: Request) -> dict[str, Any]:
        return _ok(_rid(request), delete_task(task_id), message="task deleted")

    @api.get("/v1/tasks/{task_id}/queue")
    async def task_queue(task_id: str, request: Request, state: str | None = None, page: int = 1) -> dict[str, Any]:
        return _ok(_rid(request), list_queue_items(task_id, state, page=page))

    @api.get("/v1/tasks/{task_id}/results")
    async def task_results(
        task_id: str, request: Request,
        view: str = "clean", page: int = 1, page_size: int = 20, q: str | None = None,
    ) -> dict[str, Any]:
        return _ok(_rid(request), list_results(task_id=task_id, view=view, page=page, page_size=page_size, query=q))

    @api.post("/v1/tasks/{task_id}/export")
    async def task_export(task_id: str, payload: ExportRequest) -> StreamingResponse:
        exported = export_results(task_id, payload.format)
        return StreamingResponse(
            BytesIO(exported["content"]),
            media_type=exported["media_type"],
            headers={"Content-Disposition": f'attachment; filename="{exported["filename"]}"'},
        )

    @api.get("/v1/tasks/{task_id}/wordcloud")
    async def task_wordcloud(task_id: str) -> StreamingResponse:
        result = generate_wordcloud(task_id)
        return StreamingResponse(
            BytesIO(result["content"]),
            media_type=result["media_type"],
            headers={"Content-Disposition": f'attachment; filename="{result["filename"]}"'},
        )

    @api.get("/v1/tasks/{task_id}/sentiment")
    async def task_sentiment(task_id: str, request: Request) -> dict[str, Any]:
        result = generate_sentiment_analysis(task_id)
        return _ok(_rid(request), result)

    @api.get("/v1/events/stream")
    async def event_stream(task_id: str, request: Request, after_id: int = 0) -> StreamingResponse:
        get_task(task_id)

        async def generate() -> Any:
            last_id = after_id
            idle_at = asyncio.get_running_loop().time()
            while True:
                if await request.is_disconnected():
                    break
                events = list_event_logs(task_id=task_id, after_id=last_id, limit=100)
                if events:
                    idle_at = asyncio.get_running_loop().time()
                    for ev in events:
                        last_id = ev["id"]
                        yield _sse_frame("message", ev, event_id=ev["id"])
                else:
                    task = get_task(task_id)
                    idle_sec = asyncio.get_running_loop().time() - idle_at
                    if task["status"] in {"success", "failed", "stopped"} and idle_sec >= 0.2:
                        return
                    if idle_sec >= 5:
                        yield _sse_frame("keepalive", {"task_id": task_id})
                        return
                    yield ": keepalive\n\n"
                    await asyncio.sleep(0.1)

        return StreamingResponse(generate(), media_type="text/event-stream")

    @api.post("/v1/crawl/submit", status_code=201)
    async def crawl_submit(payload: SubmitTaskRequest, request: Request) -> dict[str, Any]:
        data = submit_task(payload.model_dump())
        return _ok(_rid(request), data, message="task created")

    @api.post("/v1/command")
    async def command(payload: CommandRequest, request: Request) -> Any:
        request_id = payload.request_id or _rid(request)
        try:
            data = execute_command(payload.command)
        except AppError as exc:
            log_command(request_id, payload.command, exc.code, exc.message)
            code = 400 if exc.code < 5000 else 500
            if exc.code == 2001:
                code = 404
            return JSONResponse(status_code=code, content=_err(request_id, exc.code, exc.message))
        log_command(request_id, payload.command, 0, "ok")
        return _ok(request_id, data)

    return api


app = create_app()


def run(host: str | None = None, port: int | None = None) -> None:
    settings = get_settings()
    uvicorn.run(app, host=host or settings.host, port=port or settings.port)


# ---- 辅助函数 ----

def _read_api_key(request: Request) -> str | None:
    auth = request.headers.get("Authorization", "")
    if auth.lower().startswith("bearer "):
        return auth[7:].strip() or None
    key = request.headers.get("X-API-Key")
    if key and key.strip():
        return key.strip()
    q = request.query_params.get("api_key")
    if q and q.strip():
        return q.strip()
    return None


def _rid(request: Request | None) -> str:
    if request is None:
        return f"req_{uuid.uuid4().hex[:12]}"
    return getattr(request.state, "request_id", None) or f"req_{uuid.uuid4().hex[:12]}"


def _ok(request_id: str, data: Any, message: str = "ok") -> dict[str, Any]:
    return {"code": 0, "message": message, "request_id": request_id, "data": data}


def _err(request_id: str, code: int, message: str) -> dict[str, Any]:
    return {"code": code, "message": message, "request_id": request_id, "data": None}


def _sse_frame(event: str, data: dict[str, Any], event_id: int | None = None) -> str:
    lines = []
    if event_id is not None:
        lines.append(f"id: {event_id}")
    lines.append(f"event: {event}")
    lines.append(f"data: {json.dumps(data, ensure_ascii=True)}")
    return "\n".join(lines) + "\n\n"
