"""词云图生成功能测试。"""
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


class WordcloudTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = Path("tests/.tmp") / uuid.uuid4().hex
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        db.DB_PATH = self.temp_dir / "app.db"
        self.client = TestClient(create_app())
        self.client.__enter__()

    def tearDown(self) -> None:
        self.client.__exit__(None, None, None)
        reset_fetcher()
        shutdown_queue_runner()
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_wordcloud_returns_png_image(self) -> None:
        """测试词云图接口返回 PNG 图片。"""
        task_id = self._create_clean_task()

        response = self.client.get(f"/v1/tasks/{task_id}/wordcloud")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["content-type"], "image/png")
        # PNG 文件头
        self.assertTrue(response.content[:4] == b'\x89PNG')

    def test_wordcloud_returns_not_found_for_unknown_task(self) -> None:
        """测试不存在的任务返回 404。"""
        response = self.client.get("/v1/tasks/task_missing/wordcloud")

        self.assertEqual(response.status_code, 404)
        body = response.json()
        self.assertEqual(body["code"], 2001)

    def test_wordcloud_returns_error_when_no_clean_data(self) -> None:
        """测试没有清洗数据时返回错误。"""
        set_fetcher(
            lambda url: CrawlResult(
                discovered_urls=[], status_code=200, page_title="Root",
                raw_items=[RawItem(news_id="n-001", news_date="2026-04-10", news_title="Test", news_content="test body", source_url=url, raw_payload={})],
            )
        )
        started = execute_command("crawl start url=https://example.com/news")
        self._wait_for_terminal_status(started["task_id"])
        # 不执行 clean run，直接请求词云图

        response = self.client.get(f"/v1/tasks/{started['task_id']}/wordcloud")

        self.assertEqual(response.status_code, 400)
        body = response.json()
        self.assertEqual(body["code"], 3001)

    def _create_clean_task(self) -> str:
        set_fetcher(
            lambda url: CrawlResult(
                discovered_urls=[], status_code=200, page_title="Root",
                raw_items=[
                    RawItem(news_id="n-001", news_date="2026-04-10", news_title="Python编程入门教程", news_content="Python是一种广泛使用的高级编程语言，具有简洁的语法和强大的功能", source_url=url, raw_payload={}),
                    RawItem(news_id="n-002", news_date="2026-04-11", news_title="数据爬虫技术详解", news_content="网络爬虫是自动获取网页内容的程序，常用于数据采集和分析", source_url=url, raw_payload={}),
                ],
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
