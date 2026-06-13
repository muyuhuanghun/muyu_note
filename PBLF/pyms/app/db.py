"""SQLite 数据库：建表、连接。"""
from __future__ import annotations

import sqlite3
import threading
from pathlib import Path
from typing import Any

from app.config import get_settings


DB_PATH: Path | None = None
_SCHEMA_INITIALIZED: set[str] = set()
_SCHEMA_LOCK = threading.Lock()

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS tasks (
    task_id TEXT PRIMARY KEY,
    task_name TEXT,
    root_url TEXT NOT NULL,
    keyword TEXT,
    status TEXT NOT NULL,
    limit_count INTEGER NOT NULL,
    depth INTEGER NOT NULL,
    total_count INTEGER NOT NULL DEFAULT 0,
    done_count INTEGER NOT NULL DEFAULT 0,
    failed_count INTEGER NOT NULL DEFAULT 0,
    clean_done_count INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL,
    started_at TEXT,
    ended_at TEXT
);

CREATE TABLE IF NOT EXISTS queue_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id TEXT NOT NULL,
    url TEXT NOT NULL,
    state TEXT NOT NULL,
    hop_count INTEGER NOT NULL DEFAULT 0,
    retry_count INTEGER NOT NULL DEFAULT 0,
    priority INTEGER NOT NULL DEFAULT 100,
    last_error TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    UNIQUE(task_id, url),
    FOREIGN KEY(task_id) REFERENCES tasks(task_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS event_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id TEXT NOT NULL,
    event_type TEXT NOT NULL,
    payload_json TEXT NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY(task_id) REFERENCES tasks(task_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS command_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    request_id TEXT NOT NULL,
    command TEXT NOT NULL,
    result_code INTEGER NOT NULL,
    result_message TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS raw_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id TEXT NOT NULL,
    news_id TEXT,
    news_date TEXT,
    news_title TEXT,
    news_content TEXT,
    source_url TEXT NOT NULL,
    fetched_at TEXT NOT NULL,
    raw_payload_json TEXT,
    FOREIGN KEY(task_id) REFERENCES tasks(task_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS clean_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    raw_id INTEGER NOT NULL,
    task_id TEXT NOT NULL,
    clean_news_date TEXT,
    clean_news_title TEXT,
    clean_news_content TEXT,
    dedup_key TEXT NOT NULL,
    clean_status TEXT NOT NULL,
    cleaned_at TEXT NOT NULL,
    UNIQUE(task_id, dedup_key),
    FOREIGN KEY(raw_id) REFERENCES raw_items(id) ON DELETE CASCADE,
    FOREIGN KEY(task_id) REFERENCES tasks(task_id) ON DELETE CASCADE
);
"""


def get_connection() -> sqlite3.Connection:
    """获取数据库连接，首次调用时自动建表。"""
    db_path = _resolve_db_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    key = str(db_path)
    if key not in _SCHEMA_INITIALIZED:
        with _SCHEMA_LOCK:
            if key not in _SCHEMA_INITIALIZED:
                conn.executescript(SCHEMA_SQL)
                _migrate_schema(conn)
                _SCHEMA_INITIALIZED.add(key)
    return conn


def _migrate_schema(conn: sqlite3.Connection) -> None:
    """简单的数据库迁移：添加缺失的列。"""
    try:
        # 检查 tasks 表是否有 keyword 列
        columns = [row[1] for row in conn.execute("PRAGMA table_info(tasks)").fetchall()]
        if "keyword" not in columns:
            conn.execute("ALTER TABLE tasks ADD COLUMN keyword TEXT")
            conn.commit()
    except Exception:
        pass  # 忽略迁移错误，表可能刚创建


def init_db() -> None:
    """初始化数据库（建表）。"""
    conn = get_connection()
    conn.close()


def _resolve_db_path() -> Path:
    global DB_PATH
    if DB_PATH is not None:
        return DB_PATH
    settings = get_settings()
    return Path(settings.db_path)
