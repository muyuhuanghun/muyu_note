"""任务服务：创建、查询、删除任务，管理队列和事件日志。"""
from __future__ import annotations

import json
import uuid
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any

from app.db import get_connection
from app.errors import AppError
from app.security import validate_target_url
from app.state_machine import TaskStatus, can_transition


DEFAULT_LIMIT = 50
DEFAULT_DEPTH = 1
MAX_LIMIT = 1000
MAX_DEPTH = 5
QUEUE_STATES = {"pending", "running", "done", "failed", "canceled"}
DELETABLE_STATUSES = {"success", "failed", "stopped"}


@dataclass
class TaskRecord:
    task_id: str
    task_name: str | None
    root_url: str
    keyword: str | None
    status: str
    limit: int
    depth: int
    total_count: int
    done_count: int
    failed_count: int
    clean_done_count: int
    created_at: str
    started_at: str | None
    ended_at: str | None

    @property
    def progress(self) -> float:
        if self.total_count <= 0:
            return 0.0
        return round(((self.done_count + self.failed_count) / self.total_count) * 100, 2)


def submit_task(payload: dict[str, Any]) -> dict[str, Any]:
    """创建新任务并放入队列。"""
    url = validate_target_url(_require_str(payload, "url"))
    limit = _clamp_int(payload.get("limit", DEFAULT_LIMIT), "limit", 1, MAX_LIMIT)
    depth = _clamp_int(payload.get("depth", DEFAULT_DEPTH), "depth", 1, MAX_DEPTH)
    task_name = payload.get("task_name")
    if task_name is not None and not isinstance(task_name, str):
        raise AppError(1001, "task_name must be a string")
    keyword = payload.get("keyword")
    if keyword is not None and not isinstance(keyword, str):
        raise AppError(1001, "keyword must be a string")

    task_id = f"task_{uuid.uuid4().hex[:12]}"
    now = _now()

    conn = get_connection()
    try:
        conn.execute(
            "INSERT INTO tasks (task_id, task_name, root_url, keyword, status, limit_count, depth, total_count, done_count, failed_count, clean_done_count, created_at, started_at, ended_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (task_id, task_name or task_id, url, keyword, TaskStatus.PENDING.value, limit, depth, 1, 0, 0, 0, now, None, None),
        )
        conn.execute(
            "INSERT INTO queue_items (task_id, url, state, hop_count, retry_count, priority, last_error, created_at, updated_at) VALUES (?, ?, 'pending', ?, 0, 100, NULL, ?, ?)",
            (task_id, url, 0, now, now),
        )
        conn.execute(
            "INSERT INTO event_logs (task_id, event_type, payload_json, created_at) VALUES (?, ?, ?, ?)",
            (task_id, "task_created", json.dumps({"root_url": url, "keyword": keyword, "queued_count": 1}, ensure_ascii=True), now),
        )
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

    return {"task_id": task_id, "status": TaskStatus.PENDING.value, "queued_count": 1}


def list_tasks() -> list[dict[str, Any]]:
    """列出所有任务。"""
    conn = get_connection()
    try:
        rows = conn.execute(
            "SELECT task_id, task_name, root_url, keyword, status, limit_count, depth, total_count, done_count, failed_count, clean_done_count, created_at, started_at, ended_at FROM tasks ORDER BY created_at DESC"
        ).fetchall()
    finally:
        conn.close()
    return [_serialize_task(_row_to_task(r)) for r in rows]


def get_task(task_id: str) -> dict[str, Any]:
    """查询单个任务。"""
    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT task_id, task_name, root_url, keyword, status, limit_count, depth, total_count, done_count, failed_count, clean_done_count, created_at, started_at, ended_at FROM tasks WHERE task_id = ?",
            (task_id,),
        ).fetchone()
    finally:
        conn.close()
    if row is None:
        raise AppError(2001)
    return _serialize_task(_row_to_task(row))


def delete_task(task_id: str) -> dict[str, Any]:
    """删除已结束的任务。"""
    task = _get_task_record(task_id)
    if task.status not in DELETABLE_STATUSES:
        raise AppError(2002, f"task status {task.status} is not deletable")
    conn = get_connection()
    try:
        conn.execute("DELETE FROM tasks WHERE task_id = ?", (task_id,))
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
    return {"task_id": task_id, "deleted": True}


def transition_task(task_id: str, target_status: str) -> dict[str, Any]:
    """迁移任务状态。"""
    task = _get_task_record(task_id)
    if not can_transition(task.status, target_status):
        raise AppError(2002, f"cannot transition from {task.status} to {target_status}")

    target = TaskStatus(target_status)
    now = _now()
    started_at = task.started_at
    ended_at = task.ended_at
    event_type = "task_updated"

    if target == TaskStatus.RUNNING:
        started_at = task.started_at or now
        ended_at = None
        event_type = "task_started" if task.status == TaskStatus.PENDING.value else "task_resumed"
    elif target == TaskStatus.PAUSED:
        event_type = "task_paused"
    elif target == TaskStatus.STOPPED:
        ended_at = now
        event_type = "task_stopped"

    conn = get_connection()
    try:
        conn.execute("UPDATE tasks SET status = ?, started_at = ?, ended_at = ? WHERE task_id = ?", (target.value, started_at, ended_at, task_id))
        if target == TaskStatus.STOPPED:
            conn.execute("UPDATE queue_items SET state = 'canceled', updated_at = ? WHERE task_id = ? AND state IN ('pending', 'running')", (now, task_id))
        elif target == TaskStatus.PAUSED:
            # 暂停时将 running 状态的队列项重置为 pending
            conn.execute("UPDATE queue_items SET state = 'pending', updated_at = ? WHERE task_id = ? AND state = 'running'", (now, task_id))
        conn.execute(
            "INSERT INTO event_logs (task_id, event_type, payload_json, created_at) VALUES (?, ?, ?, ?)",
            (task_id, event_type, json.dumps({"from": task.status, "to": target.value}, ensure_ascii=True), now),
        )
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

    if target == TaskStatus.RUNNING:
        from app.worker import notify_queue_runner
        notify_queue_runner()

    return get_task(task_id)


def list_queue_items(task_id: str, state: str | None = None, page: int = 1) -> dict[str, Any]:
    """列出任务的队列项（分页）。"""
    _ensure_task_exists(task_id)
    page = max(1, int(page))
    page_size = 20
    offset = (page - 1) * page_size

    conn = get_connection()
    try:
        total_row = conn.execute("SELECT COUNT(*) AS c FROM queue_items WHERE task_id = ?", (task_id,)).fetchone()
        rows = conn.execute(
            "SELECT id, url, state, hop_count, retry_count, last_error, updated_at FROM queue_items WHERE task_id = ? ORDER BY id ASC LIMIT ? OFFSET ?",
            (task_id, page_size, offset),
        ).fetchall()
        counts = conn.execute(
            "SELECT state, COUNT(*) AS c FROM queue_items WHERE task_id = ? GROUP BY state",
            (task_id,),
        ).fetchall()
    finally:
        conn.close()

    items = [{"id": r["id"], "url": r["url"], "state": r["state"], "hop_count": r["hop_count"], "retry_count": r["retry_count"], "last_error": r["last_error"], "updated_at": r["updated_at"]} for r in rows]
    counts_by_state = {r["state"]: r["c"] for r in counts}
    return {
        "task_id": task_id, "page": page, "page_size": page_size,
        "total": total_row["c"],
        "counts_by_state": {s: counts_by_state.get(s, 0) for s in ("pending", "running", "done", "failed", "canceled")},
        "items": items,
    }


def list_event_logs(task_id: str, after_id: int = 0, limit: int = 100) -> list[dict[str, Any]]:
    """列出任务事件日志。"""
    _ensure_task_exists(task_id)
    conn = get_connection()
    try:
        rows = conn.execute(
            "SELECT id, event_type, payload_json, created_at FROM event_logs WHERE task_id = ? AND id > ? ORDER BY id ASC LIMIT ?",
            (task_id, after_id, limit),
        ).fetchall()
    finally:
        conn.close()
    return [{"id": r["id"], "task_id": task_id, "event_type": r["event_type"], "timestamp": r["created_at"], "payload": json.loads(r["payload_json"])} for r in rows]


def log_command(request_id: str, command: str, result_code: int, result_message: str) -> None:
    conn = get_connection()
    try:
        conn.execute(
            "INSERT INTO command_logs (request_id, command, result_code, result_message, created_at) VALUES (?, ?, ?, ?, ?)",
            (request_id, command, result_code, result_message, _now()),
        )
        conn.commit()
    finally:
        conn.close()


def _serialize_task(task: TaskRecord) -> dict[str, Any]:
    data = asdict(task)
    data["limit"] = data.pop("limit")
    data["progress"] = task.progress
    return data


def _row_to_task(row: Any) -> TaskRecord:
    return TaskRecord(
        task_id=row["task_id"], task_name=row["task_name"], root_url=row["root_url"],
        keyword=row["keyword"], status=row["status"], limit=row["limit_count"], depth=row["depth"],
        total_count=row["total_count"], done_count=row["done_count"],
        failed_count=row["failed_count"], clean_done_count=row["clean_done_count"],
        created_at=row["created_at"], started_at=row["started_at"], ended_at=row["ended_at"],
    )


def _get_task_record(task_id: str) -> TaskRecord:
    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT task_id, task_name, root_url, keyword, status, limit_count, depth, total_count, done_count, failed_count, clean_done_count, created_at, started_at, ended_at FROM tasks WHERE task_id = ?",
            (task_id,),
        ).fetchone()
    finally:
        conn.close()
    if row is None:
        raise AppError(2001)
    return _row_to_task(row)


def _ensure_task_exists(task_id: str) -> None:
    _get_task_record(task_id)


def _require_str(payload: dict[str, Any], field: str) -> str:
    value = payload.get(field)
    if not isinstance(value, str) or not value.strip():
        raise AppError(1001, f"{field} is required")
    return value.strip()


def _clamp_int(value: Any, field: str, lo: int, hi: int) -> int:
    try:
        n = int(value)
    except (TypeError, ValueError):
        raise AppError(1001, f"{field} must be an integer")
    if n < lo or n > hi:
        raise AppError(1001, f"{field} must be between {lo} and {hi}")
    return n


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()
