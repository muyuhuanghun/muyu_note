"""简单配置：从环境变量读取运行参数。"""
from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass
class Settings:
    host: str
    port: int
    db_path: str
    api_key: str | None

    @property
    def api_key_enabled(self) -> bool:
        return bool(self.api_key)


def get_settings() -> Settings:
    return Settings(
        host=os.getenv("PYMS_HOST", "127.0.0.1").strip() or "127.0.0.1",
        port=_read_int("PYMS_PORT", 8000),
        db_path=os.getenv("PYMS_DB_PATH", "data/app.db").strip() or "data/app.db",
        api_key=os.getenv("PYMS_API_KEY", "").strip() or None,
    )


def _read_int(name: str, default: int) -> int:
    raw = os.getenv(name)
    if raw is None or not raw.strip():
        return default
    return int(raw.strip())
