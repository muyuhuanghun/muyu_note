from __future__ import annotations

import shutil
import unittest
import uuid
from pathlib import Path

from app import db
from app.worker import shutdown_queue_runner
from tests.helpers import shared_client as client


class DayElevenTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = Path("tests/.tmp") / uuid.uuid4().hex
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        db.DB_PATH = self.temp_dir / "app.db"
        db.init_db()

    def tearDown(self) -> None:
        shutdown_queue_runner()
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_index_route_serves_console_html(self) -> None:
        _, response = client.get("/")

        self.assertEqual(response.status, 200)
        self.assertIn("text/html", response.content_type)
        self.assertIn("网页爬虫控制台", response.text)
        self.assertIn("/static/app.js", response.text)

    def test_static_assets_are_served(self) -> None:
        _, response = client.get("/static/app.js")

        self.assertEqual(response.status, 200)
        self.assertIn("javascript", response.content_type)
        self.assertIn("startEventStream", response.text)


if __name__ == "__main__":
    unittest.main()
