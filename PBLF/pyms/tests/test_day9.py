from __future__ import annotations

import json
import shutil
import time
import unittest
import uuid
from pathlib import Path

from app import db
from app.cleaning import RawItem
from app.command_engine import execute_command
from app.service import get_task, list_event_logs
from app.worker import CrawlResult, reset_fetcher, set_fetcher, shutdown_queue_runner
from tests.helpers import shared_client as client


class DayNineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = Path("tests/.tmp") / uuid.uuid4().hex
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        db.DB_PATH = self.temp_dir / "app.db"
        db.init_db()

    def tearDown(self) -> None:
        reset_fetcher()
        shutdown_queue_runner()
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_event_stream_replays_existing_events_until_terminal(self) -> None:
        set_fetcher(
            lambda url: CrawlResult(
                discovered_urls=[],
                status_code=200,
                page_title="Root",
                raw_items=[
                    RawItem(
                        news_id="n-001",
                        news_date="2026-04-10",
                        news_title="Alpha",
                        news_content="alpha body",
                        source_url=url,
                        raw_payload={"kind": "alpha"},
                    )
                ],
            )
        )

        started = execute_command("crawl start url=https://example.com/news")
        self._wait_for_terminal_status(started["task_id"])

        _, response = client.get("/v1/events/stream", params={"task_id": started["task_id"]})
        body = response.text

        self.assertEqual(response.status, 200)
        events = self._parse_sse_body(body)
        event_types = [event["event_type"] for event in events]

        self.assertIn("task_created", event_types)
        self.assertIn("crawl_item_success", event_types)
        self.assertIn("task_finished", event_types)

    def test_event_stream_after_id_returns_only_newer_events(self) -> None:
        set_fetcher(
            lambda url: CrawlResult(
                discovered_urls=[],
                status_code=200,
                page_title="Root",
                raw_items=[
                    RawItem(
                        news_id="n-001",
                        news_date="2026-04-10",
                        news_title="Alpha",
                        news_content="alpha body",
                        source_url=url,
                        raw_payload={"kind": "alpha"},
                    )
                ],
            )
        )

        started = execute_command("crawl start url=https://example.com/news")
        self._wait_for_terminal_status(started["task_id"])

        existing_events = list_event_logs(started["task_id"])
        cutoff_id = existing_events[-1]["id"]

        _, response = client.get(
            "/v1/events/stream",
            params={"task_id": started["task_id"], "after_id": cutoff_id},
        )
        body = response.text

        self.assertEqual(response.status, 200)
        events = self._parse_sse_body(body)
        # 任务已完成，没有新事件
        self.assertEqual(len(events), 0)

    def test_event_stream_returns_not_found_for_unknown_task(self) -> None:
        _, response = client.get("/v1/events/stream", params={"task_id": "task_missing"})

        self.assertEqual(response.status, 404)
        body = response.json
        self.assertEqual(body["code"], 2001)
        self.assertIsNone(body["data"])

    def _wait_for_terminal_status(self, task_id: str, timeout_seconds: float = 3) -> dict[str, object]:
        deadline = time.time() + timeout_seconds
        while time.time() < deadline:
            task = get_task(task_id)
            if task["status"] in {"success", "failed", "stopped"}:
                return task
            time.sleep(0.05)
        self.fail(f"task did not reach terminal status: {task_id}")

    def _parse_sse_body(self, body: str) -> list[dict[str, object]]:
        events: list[dict[str, object]] = []
        for block in body.split("\n\n"):
            if not block.strip() or block.startswith(":"):
                continue
            data_line = next((line for line in block.splitlines() if line.startswith("data: ")), None)
            if data_line is None:
                continue
            events.append(json.loads(data_line[6:]))
        return events


if __name__ == "__main__":
    unittest.main()
