"""命令引擎：解析并执行控制台命令。"""
from __future__ import annotations

import base64
import shlex
from typing import Any

from app.cleaning import generate_wordcloud, run_cleaning
from app.errors import AppError
from app.service import (
    DEFAULT_DEPTH, DEFAULT_LIMIT,
    delete_task, get_task, list_queue_items, submit_task, transition_task,
)


def execute_command(command: str) -> dict[str, Any]:
    """执行一条命令，返回结果。"""
    tokens = shlex.split(command)
    if not tokens:
        raise AppError(1001, "command is required")

    head = tuple(t.lower() for t in tokens[:2])
    params = _parse_params(tokens[2:]) if len(tokens) > 2 else {}

    if len(tokens) == 1 and tokens[0].lower() == "help":
        return {"output": _help_text(), "task_id": None}
    if head == ("crawl", "start"):
        return _cmd_crawl_start(params)
    if head == ("crawl", "pause"):
        return _cmd_transition(params, "paused", "task paused")
    if head == ("crawl", "resume"):
        return _cmd_transition(params, "running", "task resumed")
    if head == ("crawl", "stop"):
        return _cmd_transition(params, "stopped", "task stopped")
    if head == ("task", "status"):
        return _cmd_task_status(params)
    if head == ("task", "delete"):
        return _cmd_task_delete(params)
    if head == ("queue", "list"):
        return _cmd_queue_list(params)
    if head == ("clean", "run"):
        return _cmd_clean_run(params)
    if head == ("wordcloud", "run"):
        return _cmd_wordcloud_run(params)
    raise AppError(1003)


def _cmd_crawl_start(params: dict[str, str]) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "url": _require(params, "url"),
        "limit": params.get("limit", DEFAULT_LIMIT),
        "depth": params.get("depth", DEFAULT_DEPTH),
    }
    if "task_name" in params:
        payload["task_name"] = params["task_name"]
    if "keyword" in params:
        payload["keyword"] = params["keyword"]
    created = submit_task(payload)
    task = transition_task(created["task_id"], "running")
    return {"output": f"task started: {task['task_id']} url={task['root_url']} status={task['status']}", "task_id": task["task_id"]}


def _cmd_transition(params: dict[str, str], target: str, msg: str) -> dict[str, Any]:
    task_id = _require(params, "task_id")
    task = transition_task(task_id, target)
    return {"output": f"{msg}: {task['task_id']} status={task['status']}", "task_id": task["task_id"]}


def _cmd_task_status(params: dict[str, str]) -> dict[str, Any]:
    task_id = _require(params, "task_id")
    task = get_task(task_id)
    return {"output": f"task {task['task_id']} status={task['status']} progress={task['progress']}% done={task['done_count']} failed={task['failed_count']} total={task['total_count']}", "task_id": task["task_id"]}


def _cmd_task_delete(params: dict[str, str]) -> dict[str, Any]:
    task_id = _require(params, "task_id")
    delete_task(task_id)
    return {"output": f"task deleted: {task_id}", "task_id": task_id}


def _cmd_queue_list(params: dict[str, str]) -> dict[str, Any]:
    task_id = _require(params, "task_id")
    queue = list_queue_items(task_id, params.get("state"))
    preview = ", ".join(f"{i['id']}:{i['state']}" for i in queue["items"][:5]) or "empty"
    return {"output": f"queue task_id={task_id} total={queue['total']} preview=[{preview}]", "task_id": task_id}


def _cmd_clean_run(params: dict[str, str]) -> dict[str, Any]:
    task_id = _require(params, "task_id")
    result = run_cleaning(task_id)
    return {"output": f"clean finished: {task_id} raw={result['raw_total']} clean_done={result['clean_done_count']} clean_failed={result['clean_failed_count']}", "task_id": task_id}


def _cmd_wordcloud_run(params: dict[str, str]) -> dict[str, Any]:
    task_id = _require(params, "task_id")
    result = generate_wordcloud(task_id)
    # 将图片转为 base64 以便前端显示
    img_b64 = base64.b64encode(result["content"]).decode("ascii")
    return {
        "output": f"wordcloud generated: {task_id} ({len(result['content'])} bytes)",
        "task_id": task_id,
        "wordcloud": img_b64,
    }


def _parse_params(tokens: list[str]) -> dict[str, str]:
    params: dict[str, str] = {}
    for token in tokens:
        if "=" not in token:
            raise AppError(1001, f"invalid argument: {token}")
        key, value = token.split("=", 1)
        key, value = key.strip().lower(), value.strip()
        if not key or not value:
            raise AppError(1001, f"invalid argument: {token}")
        params[key] = value
    return params


def _require(params: dict[str, str], name: str) -> str:
    value = params.get(name)
    if not value:
        raise AppError(1001, f"{name} is required")
    return value


def _help_text() -> str:
    return (
        "commands: help | "
        "crawl start url=<...> limit=<1-1000> depth=<1-5> [task_name=<...>] [keyword=<...>] | "
        "crawl pause task_id=<...> | crawl resume task_id=<...> | crawl stop task_id=<...> | "
        "task status task_id=<...> | task delete task_id=<...> | "
        "queue list task_id=<...> [state=<pending|running|done|failed|canceled|all>] | "
        "clean run task_id=<...> | "
        "wordcloud run task_id=<...>"
    )
