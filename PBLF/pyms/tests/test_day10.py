from __future__ import annotations

import csv
import io
import json
import shutil
import time
import unittest
import uuid
from pathlib import Path

from app import db
from app.cleaning import RawItem
from app.command_engine import execute_command
from app.service import get_task
from app.worker import CrawlResult, reset_fetcher, set_fetcher, shutdown_queue_runner
from tests.helpers import shared_client as client


class DayTenTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = Path("tests/.tmp") / uuid.uuid4().hex
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        db.DB_PATH = self.temp_dir / "app.db"
        db.init_db()

    def tearDown(self) -> None:
        reset_fetcher()
        shutdown_queue_runner()
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_export_endpoint_returns_json_attachment(self) -> None:
        task_id = self._create_clean_task()

        _, response = client.post(f"/v1/tasks/{task_id}/export", json={"format": "json"})

        self.assertEqual(response.status, 200)
        self.assertIn("application/json", response.content_type)

        payload = json.loads(response.text)
        self.assertEqual(len(payload), 1)
        self.assertEqual(payload[0]["clean_news_title"], "Alpha News")
        self.assertEqual(payload[0]["clean_status"], "clean_done")

    def test_export_endpoint_returns_csv_attachment(self) -> None:
        task_id = self._create_clean_task()

        _, response = client.post(f"/v1/tasks/{task_id}/export", json={"format": "csv"})

        self.assertEqual(response.status, 200)
        self.assertIn("text/csv", response.content_type)

        rows = list(csv.DictReader(io.StringIO(response.text)))
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["clean_news_title"], "Alpha News")
        self.assertEqual(rows[0]["clean_news_date"], "2026-04-10")

    def test_export_endpoint_rejects_invalid_format(self) -> None:
        task_id = self._create_clean_task()

        _, response = client.post(f"/v1/tasks/{task_id}/export", json={"format": "xml"})

        self.assertEqual(response.status, 400)
        body = response.json
        self.assertEqual(body["code"], 1001)

    def test_export_endpoint_returns_not_found_for_unknown_task(self) -> None:
        _, response = client.post("/v1/tasks/task_missing/export", json={"format": "json"})

        self.assertEqual(response.status, 404)
        body = response.json
        self.assertEqual(body["code"], 2001)

    def _create_clean_task(self) -> str:
        set_fetcher(
            lambda url: CrawlResult(
                discovered_urls=[], status_code=200, page_title="Root",
                raw_items=[RawItem(news_id="n-001", news_date="2026-04-10", news_title="Alpha News", news_content="alpha body", source_url=url, raw_payload={"kind": "alpha"})],
            )
        )
        started = execute_command("crawl start url=https://example.com/news")
        self._wait_for_terminal_status(started["task_id"])
        execute_command(f"clean run task_id={started['task_id']}")
        return started["task_id"]

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
