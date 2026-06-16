"""Web 服务器：定义所有 API 路由（Sanic 框架）。"""
from __future__ import annotations

import asyncio
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from sanic import Sanic, Request
from sanic.response import JSONResponse, json as sanic_json, raw, file_stream

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

Sanic._app_registry.clear()
app = Sanic("PyMS")

# 静态文件
app.static("/static", STATIC_DIR)
app.static("/favicon.ico", STATIC_DIR / "favicon.ico", name="favicon")


# ---- 中间件 ----

@app.middleware("request")
async def attach_request_id(request: Request) -> None:
    request.ctx.request_id = request.headers.get("X-Request-Id") or f"req_{uuid.uuid4().hex[:12]}"


@app.middleware("request")
async def check_api_key(request: Request) -> None:
    settings = get_settings()
    path = request.path
    if not settings.api_key_enabled or path == "/" or path.startswith("/static/"):
        return
    if not path.startswith("/v1/"):
        return
    api_key = _read_api_key(request)
    if api_key != settings.api_key:
        return sanic_json(_err(_rid(request), 1004, "unauthorized"), status=401)


# ---- 生命周期 ----

@app.before_server_start
async def init_application(app: Sanic, loop: Any) -> None:
    init_db()
    start_queue_runtime()


# ---- 错误处理 ----

@app.exception(AppError)
async def handle_app_error(request: Request, exc: AppError) -> JSONResponse:
    code = 400 if exc.code < 5000 else 500
    if exc.code == 1004:
        code = 401
    if exc.code == 2001:
        code = 404
    return sanic_json(_err(_rid(request), exc.code, exc.message), status=code)


@app.exception(Exception)
async def handle_unexpected(request: Request, exc: Exception) -> JSONResponse:
    import traceback
    print(f"[ERROR] {type(exc).__name__}: {exc}")
    traceback.print_exc()
    return sanic_json(_err(_rid(request), 5000, ERROR_MESSAGES[5000]), status=500)


# ---- 路由 ----

@app.get("/")
async def index(request: Request) -> Any:
    return await file_stream(STATIC_DIR / "index.html", mime_type="text/html")


@app.get("/v1/health")
async def health(request: Request) -> JSONResponse:
    return sanic_json(_ok(_rid(request), {
        "status": "ok",
        "version": "0.1.0",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }))


@app.get("/v1/tasks")
async def tasks(request: Request) -> JSONResponse:
    task_id = request.args.get("task_id")
    data = get_task(task_id) if task_id else list_tasks()
    return sanic_json(_ok(_rid(request), data))


@app.get("/v1/tasks/<task_id:str>")
async def task_detail(request: Request, task_id: str) -> JSONResponse:
    return sanic_json(_ok(_rid(request), get_task(task_id)))


@app.delete("/v1/tasks/<task_id:str>")
async def task_delete(request: Request, task_id: str) -> JSONResponse:
    return sanic_json(_ok(_rid(request), delete_task(task_id), message="task deleted"))


@app.get("/v1/tasks/<task_id:str>/queue")
async def task_queue(request: Request, task_id: str) -> JSONResponse:
    state = request.args.get("state")
    page = int(request.args.get("page", 1))
    return sanic_json(_ok(_rid(request), list_queue_items(task_id, state, page=page)))


@app.get("/v1/tasks/<task_id:str>/results")
async def task_results(request: Request, task_id: str) -> JSONResponse:
    view = request.args.get("view", "clean")
    page = int(request.args.get("page", 1))
    page_size = int(request.args.get("page_size", 20))
    q = request.args.get("q")
    return sanic_json(_ok(_rid(request), list_results(task_id=task_id, view=view, page=page, page_size=page_size, query=q)))


@app.post("/v1/tasks/<task_id:str>/export")
async def task_export(request: Request, task_id: str) -> Any:
    payload = request.json
    exported = export_results(task_id, payload["format"])
    return raw(
        exported["content"],
        content_type=exported["media_type"],
        headers={"Content-Disposition": f'attachment; filename="{exported["filename"]}"'},
    )


@app.get("/v1/tasks/<task_id:str>/wordcloud")
async def task_wordcloud(request: Request, task_id: str) -> Any:
    result = generate_wordcloud(task_id)
    return raw(
        result["content"],
        content_type=result["media_type"],
        headers={"Content-Disposition": f'attachment; filename="{result["filename"]}"'},
    )


@app.get("/v1/tasks/<task_id:str>/sentiment")
async def task_sentiment(request: Request, task_id: str) -> JSONResponse:
    result = generate_sentiment_analysis(task_id)
    return sanic_json(_ok(_rid(request), result))


@app.get("/v1/events/stream")
async def event_stream(request: Request) -> Any:
    task_id = request.args.get("task_id")
    if not task_id:
        return sanic_json(_err(_rid(request), 1001, "task_id is required"), status=400)
    after_id = int(request.args.get("after_id", 0))

    try:
        task = get_task(task_id)
    except AppError as exc:
        return sanic_json(_err(_rid(request), exc.code, exc.message), status=404)

    # 任务已结束时直接返回全部事件（非流式）
    if task["status"] in {"success", "failed", "stopped"}:
        events = list_event_logs(task_id=task_id, after_id=after_id, limit=1000)
        body = ""
        for ev in events:
            body += _sse_frame("message", ev, event_id=ev["id"])
        if not body:
            body = ": no new events\n\n"
        return raw(body.encode("utf-8"), content_type="text/event-stream")

    # 任务进行中时使用流式响应
    import time as _time

    async def generate():
        last_id = after_id
        idle_at = _time.monotonic()
        while True:
            events = list_event_logs(task_id=task_id, after_id=last_id, limit=100)
            if events:
                idle_at = _time.monotonic()
                for ev in events:
                    last_id = ev["id"]
                    yield _sse_frame("message", ev, event_id=ev["id"]).encode("utf-8")
            else:
                cur_task = get_task(task_id)
                idle_sec = _time.monotonic() - idle_at
                if cur_task["status"] in {"success", "failed", "stopped"} and idle_sec >= 0.2:
                    return
                if idle_sec >= 5:
                    yield _sse_frame("keepalive", {"task_id": task_id}).encode("utf-8")
                    return
                yield b": keepalive\n\n"
                await asyncio.sleep(0.1)

    return raw(generate(), content_type="text/event-stream")


@app.post("/v1/crawl/submit")
async def crawl_submit(request: Request) -> JSONResponse:
    payload = request.json
    data = submit_task(payload)
    return sanic_json(_ok(_rid(request), data, message="task created"), status=201)


@app.post("/v1/command")
async def command(request: Request) -> JSONResponse:
    payload = request.json
    request_id = payload.get("request_id") or _rid(request)
    try:
        data = execute_command(payload["command"])
    except AppError as exc:
        log_command(request_id, payload["command"], exc.code, exc.message)
        code = 400 if exc.code < 5000 else 500
        if exc.code == 2001:
            code = 404
        return sanic_json(_err(request_id, exc.code, exc.message), status=code)
    log_command(request_id, payload["command"], 0, "ok")
    return sanic_json(_ok(request_id, data))


# ---- 启动入口 ----

def run(host: str | None = None, port: int | None = None) -> None:
    settings = get_settings()
    app.run(host=host or settings.host, port=port or settings.port, debug=False, access_log=False)


# ---- 辅助函数 ----

def _read_api_key(request: Request) -> str | None:
    auth = request.headers.get("Authorization", "")
    if auth.lower().startswith("bearer "):
        return auth[7:].strip() or None
    key = request.headers.get("X-API-Key")
    if key and key.strip():
        return key.strip()
    q = request.args.get("api_key")
    if q and q.strip():
        return q.strip()
    return None


def _rid(request: Request | None) -> str:
    if request is None:
        return f"req_{uuid.uuid4().hex[:12]}"
    return getattr(request.ctx, "request_id", None) or f"req_{uuid.uuid4().hex[:12]}"


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
