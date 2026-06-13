"""任务状态机：定义状态和允许的状态迁移。"""
from __future__ import annotations

from enum import Enum


class TaskStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    PAUSED = "paused"
    STOPPED = "stopped"
    SUCCESS = "success"
    FAILED = "failed"


TRANSITIONS: dict[TaskStatus, set[TaskStatus]] = {
    TaskStatus.PENDING: {TaskStatus.RUNNING},
    TaskStatus.RUNNING: {TaskStatus.PAUSED, TaskStatus.STOPPED, TaskStatus.SUCCESS, TaskStatus.FAILED},
    TaskStatus.PAUSED: {TaskStatus.RUNNING, TaskStatus.STOPPED},
    TaskStatus.STOPPED: set(),
    TaskStatus.SUCCESS: set(),
    TaskStatus.FAILED: set(),
}


def can_transition(current: str, target: str) -> bool:
    return TaskStatus(target) in TRANSITIONS[TaskStatus(current)]
