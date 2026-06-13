from __future__ import annotations

import shutil
import unittest
import uuid
from pathlib import Path

from app import db
from app.errors import AppError
from app.security import validate_target_url
from app.service import get_task, list_tasks, submit_task
from app.state_machine import can_transition


class DayOneDayTwoTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = Path("tests/.tmp") / uuid.uuid4().hex
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        db.DB_PATH = self.temp_dir / "app.db"
        db.init_db()

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_task_state_machine(self) -> None:
        self.assertTrue(can_transition("pending", "running"))
        self.assertTrue(can_transition("running", "paused"))
        self.assertFalse(can_transition("pending", "success"))

    def test_validate_forbids_private_targets(self) -> None:
        with self.assertRaises(AppError) as context:
            validate_target_url("http://127.0.0.1/admin")
        self.assertEqual(context.exception.code, 1002)

    def test_validate_forbids_localhost(self) -> None:
        with self.assertRaises(AppError) as context:
            validate_target_url("http://localhost/test")
        self.assertEqual(context.exception.code, 1002)

    def test_submit_task_initializes_queue_and_detail(self) -> None:
        result = submit_task(
            {
                "url": "https://example.com/news",
                "limit": 20,
                "depth": 2,
                "task_name": "daily-news",
            }
        )

        self.assertEqual(result["status"], "pending")
        self.assertEqual(result["queued_count"], 1)

        task = get_task(result["task_id"])
        self.assertEqual(task["task_name"], "daily-news")
        self.assertEqual(task["root_url"], "https://example.com/news")
        self.assertEqual(task["total_count"], 1)
        self.assertEqual(task["progress"], 0.0)

    def test_list_tasks_returns_newest_first(self) -> None:
        first = submit_task({"url": "https://example.com/1"})
        second = submit_task({"url": "https://example.com/2"})

        items = list_tasks()

        self.assertEqual(items[0]["task_id"], second["task_id"])
        self.assertEqual(items[1]["task_id"], first["task_id"])


if __name__ == "__main__":
    unittest.main()
