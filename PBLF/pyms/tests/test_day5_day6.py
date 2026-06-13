from __future__ import annotations

import shutil
import threading
import time
import unittest
import uuid
from pathlib import Path

from app import db
from app.command_engine import execute_command
from app.service import get_task, submit_task, transition_task
from app.worker import CrawlResult, reset_fetcher, set_fetcher, shutdown_queue_runner


class DayFiveDaySixTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = Path("tests/.tmp") / uuid.uuid4().hex
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        db.DB_PATH = self.temp_dir / "app.db"
        db.init_db()

    def tearDown(self) -> None:
        reset_fetcher()
        shutdown_queue_runner()
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_worker_consumes_queue_and_marks_task_success(self) -> None:
        set_fetcher(lambda url: CrawlResult(discovered_urls=[], status_code=200, page_title="root"))

        started = execute_command("crawl start url=https://example.com/news limit=5 depth=1")
        task = self._wait_for_terminal_status(started["task_id"])

        self.assertEqual(task["status"], "success")
        self.assertEqual(task["done_count"], 1)
        self.assertEqual(task["failed_count"], 0)

    def test_worker_enqueues_discovered_urls_with_limit_and_depth(self) -> None:
        def fetcher(url: str) -> CrawlResult:
            if url.endswith("/news"):
                return CrawlResult(
                    discovered_urls=["https://example.com/a", "https://example.com/b", "https://example.com/c"],
                    status_code=200, page_title="root",
                )
            return CrawlResult(discovered_urls=[], status_code=200, page_title="child")

        set_fetcher(fetcher)

        started = execute_command("crawl start url=https://example.com/news limit=3 depth=2")
        task = self._wait_for_terminal_status(started["task_id"])

        self.assertEqual(task["status"], "success")
        self.assertEqual(task["total_count"], 3)
        self.assertEqual(task["done_count"], 3)

    def test_worker_marks_task_failed_when_fetcher_raises(self) -> None:
        set_fetcher(lambda url: (_ for _ in ()).throw(RuntimeError("boom")))

        started = execute_command("crawl start url=https://example.com/news")
        task = self._wait_for_terminal_status(started["task_id"])

        self.assertEqual(task["status"], "failed")
        self.assertEqual(task["done_count"], 0)
        self.assertEqual(task["failed_count"], 1)

    def test_pause_and_resume_control_remaining_queue_items(self) -> None:
        release_fetch = threading.Event()

        def fetcher(url: str) -> CrawlResult:
            if url.endswith("/news"):
                release_fetch.wait(timeout=2)
            return CrawlResult(discovered_urls=[], status_code=200, page_title="page")

        set_fetcher(fetcher)

        created = submit_task({"url": "https://example.com/news", "limit": 2, "depth": 1})
        now = "2026-04-10T00:00:00+00:00"
        with db.get_connection() as connection:
            connection.execute(
                "INSERT INTO queue_items (task_id, url, state, hop_count, retry_count, priority, last_error, created_at, updated_at) VALUES (?, ?, 'pending', 0, 0, 100, NULL, ?, ?)",
                (created["task_id"], "https://example.com/extra", now, now),
            )
            connection.execute("UPDATE tasks SET total_count = 2 WHERE task_id = ?", (created["task_id"],))
            connection.commit()

        transition_task(created["task_id"], "running")

        paused = execute_command(f"crawl pause task_id={created['task_id']}")
        self.assertIn("task paused", paused["output"])

        release_fetch.set()
        time.sleep(0.2)

        task = get_task(created["task_id"])
        self.assertEqual(task["status"], "paused")

        resumed = execute_command(f"crawl resume task_id={created['task_id']}")
        self.assertIn("task resumed", resumed["output"])

        task = self._wait_for_terminal_status(created["task_id"])
        self.assertEqual(task["status"], "success")
        self.assertEqual(task["done_count"], 2)

    def _wait_for_terminal_status(self, task_id: str, timeout_seconds: float = 3) -> dict[str, object]:
        deadline = time.time() + timeout_seconds
        while time.time() < deadline:
            task = get_task(task_id)
            if task["status"] in {"success", "failed", "stopped"}:
                return task
            time.sleep(0.05)
        self.fail(f"task did not reach terminal status: {task_id}")


if __name__ == "__main__":
    unittest.main()
