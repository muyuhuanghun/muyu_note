from __future__ import annotations

import shutil
import time
import unittest
import uuid
from pathlib import Path

from fastapi.testclient import TestClient

from app import db
from app.cleaning import RawItem
from app.command_engine import execute_command
from app.server import create_app
from app.service import get_task
from app.worker import CrawlResult, reset_fetcher, set_fetcher, shutdown_queue_runner


class DaySevenDayEightTests(unittest.TestCase):
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

    def test_worker_persists_raw_items(self) -> None:
        set_fetcher(
            lambda url: CrawlResult(
                discovered_urls=[],
                status_code=200,
                page_title="Root",
                raw_items=[
                    RawItem(
                        news_id="n-001",
                        news_date="2026/04/10",
                        news_title="<b> Alpha </b>",
                        news_content=" Hello   world ",
                        source_url=url,
                        raw_payload={"source": "test"},
                    )
                ],
            )
        )

        started = execute_command("crawl start url=https://example.com/news")
        self._wait_for_terminal_status(started["task_id"])

        with db.get_connection() as connection:
            row = connection.execute(
                """
                SELECT news_id, news_date, news_title, news_content, source_url
                FROM raw_items
                WHERE task_id = ?
                """,
                (started["task_id"],),
            ).fetchone()

        self.assertEqual(row["news_id"], "n-001")
        self.assertEqual(row["news_date"], "2026/04/10")
        self.assertEqual(row["news_title"], "<b> Alpha </b>")
        self.assertEqual(row["source_url"], "https://example.com/news")

    def test_clean_run_deduplicates_and_normalizes_items(self) -> None:
        def fetcher(url: str) -> CrawlResult:
            return CrawlResult(
                discovered_urls=[],
                status_code=200,
                page_title="Root",
                raw_items=[
                    RawItem(
                        news_id="same-id",
                        news_date="2026/04/10",
                        news_title="<h1>Alpha</h1>",
                        news_content=" First   content ",
                        source_url=url,
                        raw_payload={"idx": 1},
                    ),
                    RawItem(
                        news_id="same-id",
                        news_date="2026-04-10",
                        news_title=" Alpha ",
                        news_content="<p>Second</p>",
                        source_url=url,
                        raw_payload={"idx": 2},
                    ),
                    RawItem(
                        news_id=None,
                        news_date="2026年04月11日",
                        news_title="Beta",
                        news_content="Next item",
                        source_url=url,
                        raw_payload={"idx": 3},
                    ),
                ],
            )

        set_fetcher(fetcher)

        started = execute_command("crawl start url=https://example.com/news")
        self._wait_for_terminal_status(started["task_id"])

        result = execute_command(f"clean run task_id={started['task_id']}")
        self.assertIn("raw=3", result["output"])
        self.assertIn("clean_done=2", result["output"])

        task = get_task(started["task_id"])
        self.assertEqual(task["clean_done_count"], 2)

        with db.get_connection() as connection:
            rows = connection.execute(
                """
                SELECT clean_news_date, clean_news_title, clean_news_content, dedup_key, clean_status
                FROM clean_items
                WHERE task_id = ?
                ORDER BY id ASC
                """,
                (started["task_id"],),
            ).fetchall()

        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["clean_news_date"], "2026-04-10")
        self.assertEqual(rows[0]["clean_news_title"], "Alpha")
        self.assertEqual(rows[0]["clean_news_content"], "First content")
        self.assertEqual(rows[0]["dedup_key"], "news_id:same-id")
        self.assertEqual(rows[0]["clean_status"], "clean_done")
        self.assertEqual(rows[1]["clean_news_date"], "2026-04-11")

    def test_results_endpoint_returns_raw_and_clean_views(self) -> None:
        set_fetcher(
            lambda url: CrawlResult(
                discovered_urls=[],
                status_code=200,
                page_title="Root",
                raw_items=[
                    RawItem(
                        news_id="n-001",
                        news_date="2026-04-10",
                        news_title="Alpha News",
                        news_content="alpha body",
                        source_url=url,
                        raw_payload={"kind": "alpha"},
                    ),
                    RawItem(
                        news_id="n-002",
                        news_date="2026-04-11",
                        news_title="Beta News",
                        news_content="beta body",
                        source_url=url,
                        raw_payload={"kind": "beta"},
                    ),
                ],
            )
        )

        started = execute_command("crawl start url=https://example.com/news")
        self._wait_for_terminal_status(started["task_id"])
        execute_command(f"clean run task_id={started['task_id']}")

        raw_response = self.client.get(
            f"/v1/tasks/{started['task_id']}/results",
            params={"view": "raw", "q": "Alpha"},
        )
        clean_response = self.client.get(
            f"/v1/tasks/{started['task_id']}/results",
            params={"view": "clean", "page": 1, "page_size": 1},
        )

        raw_body = raw_response.json()
        clean_body = clean_response.json()

        self.assertEqual(raw_response.status_code, 200)
        self.assertEqual(raw_body["data"]["view"], "raw")
        self.assertEqual(raw_body["data"]["total"], 1)
        self.assertEqual(raw_body["data"]["items"][0]["news_title"], "Alpha News")

        self.assertEqual(clean_response.status_code, 200)
        self.assertEqual(clean_body["data"]["view"], "clean")
        self.assertEqual(clean_body["data"]["page_size"], 1)
        self.assertEqual(len(clean_body["data"]["items"]), 1)
        self.assertEqual(clean_body["data"]["total"], 2)

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
