from __future__ import annotations

import shutil
import unittest
import uuid
from pathlib import Path

from fastapi.testclient import TestClient

from app import db
from app.command_engine import execute_command
from app.server import create_app
from app.service import get_task, submit_task
from app.worker import CrawlResult, reset_fetcher, set_fetcher, shutdown_queue_runner


class DayThreeDayFourTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = Path("tests/.tmp") / uuid.uuid4().hex
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        db.DB_PATH = self.temp_dir / "app.db"
        self.client = TestClient(create_app())
        db.init_db()

    def tearDown(self) -> None:
        self.client.close()
        reset_fetcher()
        shutdown_queue_runner()
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_help_command(self) -> None:
        result = execute_command("help")

        self.assertIn("commands", result["output"])
        self.assertIsNone(result["task_id"])

    def test_crawl_start_creates_running_task(self) -> None:
        set_fetcher(lambda url: CrawlResult(discovered_urls=[], status_code=200, page_title=url))
        result = execute_command("crawl start url=https://example.com/news limit=10 depth=2 task_name=daily")

        task = get_task(result["task_id"])
        self.assertIn(task["status"], {"running", "success"})
        self.assertIsNotNone(task["started_at"])
        self.assertEqual(task["task_name"], "daily")

    def test_pause_resume_stop_commands_change_status(self) -> None:
        created = execute_command("crawl start url=https://example.com/news")

        paused = execute_command(f"crawl pause task_id={created['task_id']}")
        self.assertIn("task paused", paused["output"])
        self.assertEqual(get_task(created["task_id"])["status"], "paused")

        resumed = execute_command(f"crawl resume task_id={created['task_id']}")
        self.assertIn("task resumed", resumed["output"])
        self.assertEqual(get_task(created["task_id"])["status"], "running")

        stopped = execute_command(f"crawl stop task_id={created['task_id']}")
        self.assertIn("task stopped", stopped["output"])
        task = get_task(created["task_id"])
        self.assertEqual(task["status"], "stopped")
        self.assertIsNotNone(task["ended_at"])

    def test_queue_list_command_returns_preview(self) -> None:
        created = submit_task({"url": "https://example.com/news"})

        result = execute_command(f"queue list task_id={created['task_id']} state=pending")

        self.assertIn("total=1", result["output"])

    def test_command_endpoint_uses_supplied_request_id_and_logs_result(self) -> None:
        response = self.client.post(
            "/v1/command",
            json={
                "command": "crawl start url=https://example.com/news limit=5 depth=1",
                "request_id": "req_manual_001",
            },
        )

        body = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(body["request_id"], "req_manual_001")
        self.assertIn("task started", body["data"]["output"])

    def test_command_endpoint_returns_app_error_payload(self) -> None:
        response = self.client.post(
            "/v1/command",
            json={"command": "crawl pause task_id=task_missing", "request_id": "req_missing"},
        )

        body = response.json()
        self.assertEqual(response.status_code, 404)
        self.assertEqual(body["request_id"], "req_missing")
        self.assertEqual(body["code"], 2001)


if __name__ == "__main__":
    unittest.main()
