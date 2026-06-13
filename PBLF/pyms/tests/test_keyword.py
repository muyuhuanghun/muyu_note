"""关键字过滤功能测试。"""
from __future__ import annotations

import shutil
import time
import unittest
import uuid
from pathlib import Path

from fastapi.testclient import TestClient

from app import db
from app.cleaning import RawItem, run_cleaning
from app.command_engine import execute_command
from app.server import create_app
from app.service import get_task
from app.worker import CrawlResult, reset_fetcher, set_fetcher, shutdown_queue_runner


class KeywordTests(unittest.TestCase):
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

    def test_keyword_stored_in_task(self) -> None:
        """测试关键字保存到任务中。"""
        set_fetcher(lambda url: CrawlResult(discovered_urls=[], status_code=200, page_title="Test", raw_items=[]))
        started = execute_command("crawl start url=https://example.com keyword=python,爬虫")
        task_id = started["task_id"]
        task = get_task(task_id)
        self.assertEqual(task["keyword"], "python,爬虫")

    def test_keyword_none_when_not_provided(self) -> None:
        """测试不提供关键字时为 None。"""
        set_fetcher(lambda url: CrawlResult(discovered_urls=[], status_code=200, page_title="Test", raw_items=[]))
        started = execute_command("crawl start url=https://example.com")
        task_id = started["task_id"]
        task = get_task(task_id)
        self.assertIsNone(task["keyword"])

    def test_keyword_filters_content_by_title(self) -> None:
        """测试关键字根据标题筛选内容。"""
        def mock_fetch(url: str) -> CrawlResult:
            if url == "https://example.com":
                return CrawlResult(
                    discovered_urls=["https://example.com/page1", "https://example.com/page2"],
                    status_code=200, page_title="Root",
                    raw_items=[RawItem(news_id=url, news_date=None, news_title="Root", news_content="root content", source_url=url, raw_payload={})],
                )
            elif "page1" in url:
                return CrawlResult(
                    discovered_urls=[], status_code=200, page_title="Python教程",
                    raw_items=[RawItem(news_id=url, news_date=None, news_title="Python教程", news_content="学习Python编程", source_url=url, raw_payload={})],
                )
            else:
                return CrawlResult(
                    discovered_urls=[], status_code=200, page_title="Java教程",
                    raw_items=[RawItem(news_id=url, news_date=None, news_title="Java教程", news_content="学习Java编程", source_url=url, raw_payload={})],
                )

        set_fetcher(mock_fetch)
        started = execute_command("crawl start url=https://example.com keyword=python depth=2")
        task_id = started["task_id"]
        self._wait_for_terminal_status(task_id)
        # 执行清洗
        run_cleaning(task_id)
        task = get_task(task_id)
        # 所有页面都被爬取（total_count=3）
        self.assertEqual(task["total_count"], 3)
        # 但只有包含 "python" 的内容被保存（clean_done_count=1，因为根URL的标题"Root"不包含python）
        self.assertEqual(task["clean_done_count"], 1)

    def test_keyword_filters_content_by_content(self) -> None:
        """测试关键字根据正文内容筛选。"""
        def mock_fetch(url: str) -> CrawlResult:
            return CrawlResult(
                discovered_urls=[], status_code=200, page_title="新闻列表",
                raw_items=[RawItem(news_id=url, news_date=None, news_title="新闻列表", news_content="今天学习了Python爬虫技术", source_url=url, raw_payload={})],
            )

        set_fetcher(mock_fetch)
        started = execute_command("crawl start url=https://example.com keyword=爬虫")
        task_id = started["task_id"]
        self._wait_for_terminal_status(task_id)
        run_cleaning(task_id)
        task = get_task(task_id)
        # 内容包含"爬虫"，应该被保存
        self.assertEqual(task["clean_done_count"], 1)

    def test_keyword_case_insensitive(self) -> None:
        """测试关键字匹配不区分大小写。"""
        def mock_fetch(url: str) -> CrawlResult:
            return CrawlResult(
                discovered_urls=[], status_code=200, page_title="PYTHON Guide",
                raw_items=[RawItem(news_id=url, news_date=None, news_title="PYTHON Guide", news_content="Learn Python", source_url=url, raw_payload={})],
            )

        set_fetcher(mock_fetch)
        started = execute_command("crawl start url=https://example.com keyword=python")
        task_id = started["task_id"]
        self._wait_for_terminal_status(task_id)
        run_cleaning(task_id)
        task = get_task(task_id)
        # 大写 "PYTHON" 应该匹配小写 "python"
        self.assertEqual(task["clean_done_count"], 1)

    def test_keyword_no_match_skips_content(self) -> None:
        """测试不匹配关键字的内容被跳过。"""
        def mock_fetch(url: str) -> CrawlResult:
            return CrawlResult(
                discovered_urls=[], status_code=200, page_title="Java教程",
                raw_items=[RawItem(news_id=url, news_date=None, news_title="Java教程", news_content="学习Java编程", source_url=url, raw_payload={})],
            )

        set_fetcher(mock_fetch)
        started = execute_command("crawl start url=https://example.com keyword=python")
        task_id = started["task_id"]
        self._wait_for_terminal_status(task_id)
        run_cleaning(task_id)
        task = get_task(task_id)
        # 标题和内容都不包含 "python"，不保存
        self.assertEqual(task["clean_done_count"], 0)

    def test_keyword_via_api(self) -> None:
        """测试通过 API 提交带关键字的任务。"""
        set_fetcher(lambda url: CrawlResult(discovered_urls=[], status_code=200, page_title="Test", raw_items=[]))
        response = self.client.post("/v1/crawl/submit", json={
            "url": "https://example.com",
            "keyword": "python,test",
        })
        self.assertEqual(response.status_code, 201)
        data = response.json()["data"]
        task = get_task(data["task_id"])
        self.assertEqual(task["keyword"], "python,test")

    def test_keyword_multiple_keywords(self) -> None:
        """测试多个关键字（任一匹配即可）。"""
        def mock_fetch(url: str) -> CrawlResult:
            return CrawlResult(
                discovered_urls=[], status_code=200, page_title="Go语言教程",
                raw_items=[RawItem(news_id=url, news_date=None, news_title="Go语言教程", news_content="学习Go编程", source_url=url, raw_payload={})],
            )

        set_fetcher(mock_fetch)
        started = execute_command("crawl start url=https://example.com keyword=python,go,java")
        task_id = started["task_id"]
        self._wait_for_terminal_status(task_id)
        run_cleaning(task_id)
        task = get_task(task_id)
        # 标题包含 "go"（不区分大小写），应该匹配
        self.assertEqual(task["clean_done_count"], 1)

    def test_crawl_all_links_without_keyword(self) -> None:
        """测试没有关键字时爬取所有链接。"""
        def mock_fetch(url: str) -> CrawlResult:
            if url == "https://example.com":
                return CrawlResult(
                    discovered_urls=["https://example.com/page1", "https://example.com/page2"],
                    status_code=200, page_title="Root",
                    raw_items=[RawItem(news_id=url, news_date=None, news_title="Root", news_content="root", source_url=url, raw_payload={})],
                )
            else:
                return CrawlResult(
                    discovered_urls=[], status_code=200, page_title="Page",
                    raw_items=[RawItem(news_id=url, news_date=None, news_title="Page", news_content="content", source_url=url, raw_payload={})],
                )

        set_fetcher(mock_fetch)
        started = execute_command("crawl start url=https://example.com depth=2")
        task_id = started["task_id"]
        self._wait_for_terminal_status(task_id)
        task = get_task(task_id)
        # 没有关键字，爬取所有页面
        self.assertEqual(task["total_count"], 3)
        self.assertEqual(task["done_count"], 3)

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
