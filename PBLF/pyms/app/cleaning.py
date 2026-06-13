"""数据清洗：规范化、去重、导出、词云图。"""
from __future__ import annotations

import csv
import hashlib
import html
import io
import json
import os
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

import jieba
from bs4 import BeautifulSoup
from wordcloud import WordCloud

from app.db import get_connection
from app.errors import AppError


@dataclass
class RawItem:
    """一条原始抓取数据。"""
    news_id: str | None
    news_date: str | None
    news_title: str | None
    news_content: str | None
    source_url: str
    raw_payload: dict[str, Any]


def save_raw_items(task_id: str, items: list[RawItem], fetched_at: str, connection: Any = None) -> int:
    """保存原始抓取数据到数据库。"""
    if not items:
        return 0
    if connection is None:
        conn = get_connection()
        try:
            return save_raw_items(task_id, items, fetched_at, connection=conn)
        finally:
            conn.close()

    for item in items:
        connection.execute(
            "INSERT INTO raw_items (task_id, news_id, news_date, news_title, news_content, source_url, fetched_at, raw_payload_json) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (task_id, item.news_id, item.news_date, item.news_title, item.news_content, item.source_url, fetched_at, json.dumps(item.raw_payload, ensure_ascii=True)),
        )
    return len(items)


def run_cleaning(task_id: str) -> dict[str, Any]:
    """对任务的原始数据执行清洗和去重。"""
    _ensure_task_exists(task_id)
    cleaned_at = _now()

    conn = get_connection()
    try:
        rows = conn.execute(
            "SELECT id, news_id, news_date, news_title, news_content, source_url FROM raw_items WHERE task_id = ? ORDER BY id ASC",
            (task_id,),
        ).fetchall()
        conn.execute("DELETE FROM clean_items WHERE task_id = ?", (task_id,))

        done_count = 0
        fail_count = 0
        for row in rows:
            try:
                date = _normalize_date(row["news_date"])
                title = _normalize_text(row["news_title"])
                content = _normalize_text(row["news_content"])
                dedup_key = _build_dedup_key(row["news_id"], title, date)
                inserted = conn.execute(
                    "INSERT OR IGNORE INTO clean_items (raw_id, task_id, clean_news_date, clean_news_title, clean_news_content, dedup_key, clean_status, cleaned_at) VALUES (?, ?, ?, ?, ?, ?, 'clean_done', ?)",
                    (row["id"], task_id, date, title, content, dedup_key, cleaned_at),
                )
                if inserted.rowcount == 1:
                    done_count += 1
            except Exception:
                fail_count += 1
                conn.execute(
                    "INSERT INTO clean_items (raw_id, task_id, clean_news_date, clean_news_title, clean_news_content, dedup_key, clean_status, cleaned_at) VALUES (?, ?, ?, ?, ?, ?, 'clean_failed', ?)",
                    (row["id"], task_id, None, None, None, f"failed:{row['id']}", cleaned_at),
                )

        conn.execute("UPDATE tasks SET clean_done_count = ? WHERE task_id = ?", (done_count, task_id))
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

    return {"task_id": task_id, "raw_total": len(rows), "clean_done_count": done_count, "clean_failed_count": fail_count}


def list_results(task_id: str, view: str = "clean", page: int = 1, page_size: int = 20, query: str | None = None) -> dict[str, Any]:
    """查询任务的结果数据（分页）。"""
    _ensure_task_exists(task_id)
    if view not in ("raw", "clean"):
        raise AppError(1001, "view must be raw or clean")
    page = max(1, int(page))
    page_size = max(1, min(100, int(page_size)))
    offset = (page - 1) * page_size
    keyword = (query or "").strip()

    conn = get_connection()
    try:
        if view == "raw":
            where = "WHERE task_id = ?"
            params: list[Any] = [task_id]
            if keyword:
                where += " AND (COALESCE(news_title, '') LIKE ? OR COALESCE(news_content, '') LIKE ?)"
                params.extend([f"%{keyword}%", f"%{keyword}%"])
            total = conn.execute(f"SELECT COUNT(*) AS c FROM raw_items {where}", params).fetchone()["c"]
            rows = conn.execute(f"SELECT id, news_id, news_date, news_title, news_content, source_url, fetched_at FROM raw_items {where} ORDER BY id DESC LIMIT ? OFFSET ?", [*params, page_size, offset]).fetchall()
            items = [dict(r) for r in rows]
        else:
            where = "WHERE task_id = ?"
            params = [task_id]
            if keyword:
                where += " AND (COALESCE(clean_news_title, '') LIKE ? OR COALESCE(clean_news_content, '') LIKE ?)"
                params.extend([f"%{keyword}%", f"%{keyword}%"])
            total = conn.execute(f"SELECT COUNT(*) AS c FROM clean_items {where}", params).fetchone()["c"]
            rows = conn.execute(f"SELECT id, raw_id, clean_news_date, clean_news_title, clean_news_content, dedup_key, clean_status, cleaned_at FROM clean_items {where} ORDER BY id DESC LIMIT ? OFFSET ?", [*params, page_size, offset]).fetchall()
            items = [dict(r) for r in rows]
    finally:
        conn.close()

    return {"task_id": task_id, "view": view, "page": page, "page_size": page_size, "total": total, "items": items}


def export_results(task_id: str, export_format: str) -> dict[str, Any]:
    """导出清洗结果为 JSON 或 CSV。"""
    _ensure_task_exists(task_id)
    if export_format not in ("json", "csv"):
        raise AppError(1001, "format must be json or csv")

    conn = get_connection()
    try:
        rows = conn.execute(
            "SELECT id, raw_id, clean_news_date, clean_news_title, clean_news_content, dedup_key, clean_status, cleaned_at FROM clean_items WHERE task_id = ? ORDER BY id ASC",
            (task_id,),
        ).fetchall()
    finally:
        conn.close()

    items = [dict(r) for r in rows]
    filename = f"{task_id}_results.{export_format}"

    if export_format == "json":
        return {"filename": filename, "media_type": "application/json; charset=utf-8", "content": json.dumps(items, ensure_ascii=False, indent=2).encode("utf-8")}

    buf = io.StringIO()
    fields = ["id", "raw_id", "clean_news_date", "clean_news_title", "clean_news_content", "dedup_key", "clean_status", "cleaned_at"]
    writer = csv.DictWriter(buf, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    writer.writerows(items)
    return {"filename": filename, "media_type": "text/csv; charset=utf-8", "content": buf.getvalue().encode("utf-8")}


def generate_wordcloud(task_id: str) -> dict[str, Any]:
    """生成任务清洗结果的词云图，返回 PNG 图片字节。"""
    _ensure_task_exists(task_id)

    conn = get_connection()
    try:
        rows = conn.execute(
            "SELECT clean_news_title, clean_news_content FROM clean_items WHERE task_id = ? AND clean_status = 'clean_done'",
            (task_id,),
        ).fetchall()
    finally:
        conn.close()

    if not rows:
        raise AppError(3001, "no clean data available for wordcloud")

    # 合并所有标题和正文
    texts = []
    for row in rows:
        if row["clean_news_title"]:
            texts.append(row["clean_news_title"])
        if row["clean_news_content"]:
            texts.append(row["clean_news_content"])
    full_text = " ".join(texts)

    # jieba 分词
    words = jieba.cut(full_text, cut_all=False)
    # 过滤停用词和短词
    stopwords = {"的", "了", "在", "是", "我", "有", "和", "就", "不", "人", "都", "一", "一个", "上", "也", "很", "到", "说", "要", "去", "你", "会", "着", "没有", "看", "好", "自己", "这"}
    filtered = " ".join(w for w in words if len(w) > 1 and w not in stopwords)

    if not filtered.strip():
        raise AppError(3001, "no valid words after filtering")

    # 生成词云 - 使用系统字体
    font_path = _find_chinese_font()
    wc = WordCloud(
        font_path=font_path,
        width=800,
        height=400,
        background_color="white",
        max_words=100,
        colormap="viridis",
    )
    wc.generate(filtered)

    # 转为 PNG 字节
    buf = io.BytesIO()
    wc.to_image().save(buf, format="PNG")
    buf.seek(0)

    return {
        "filename": f"{task_id}_wordcloud.png",
        "media_type": "image/png",
        "content": buf.getvalue(),
    }


def generate_sentiment_analysis(task_id: str) -> dict[str, Any]:
    """对任务清洗结果进行情感分析，返回正面/中立/负面计数。"""
    _ensure_task_exists(task_id)

    conn = get_connection()
    try:
        rows = conn.execute(
            "SELECT clean_news_title, clean_news_content FROM clean_items WHERE task_id = ? AND clean_status = 'clean_done'",
            (task_id,),
        ).fetchall()
    finally:
        conn.close()

    if not rows:
        raise AppError(3001, "no clean data available for sentiment analysis")

    positive = 0
    neutral = 0
    negative = 0
    details: list[dict[str, Any]] = []

    for row in rows:
        text = " ".join(filter(None, [row["clean_news_title"], row["clean_news_content"]]))
        score = _sentiment_score(text)
        if score > 0.05:
            label = "正面"
            positive += 1
        elif score < -0.05:
            label = "负面"
            negative += 1
        else:
            label = "中立"
            neutral += 1
        details.append({"title": row["clean_news_title"] or "", "score": round(score, 4), "label": label})

    return {
        "task_id": task_id,
        "total": len(rows),
        "positive": positive,
        "neutral": neutral,
        "negative": negative,
        "details": details,
    }


# 📌 情感关键词词典（基于中文常见情感词）
_POSITIVE_WORDS = {
    "优秀", "成功", "突破", "创新", "增长", "提升", "进步", "发展", "繁荣",
    "利好", "上涨", "盈利", "利润", "收益", "回报", "佳绩", "领先", "冠军",
    "点赞", "好评", "满意", "开心", "快乐", "幸福", "感动", "温暖", "希望",
    "强大", "卓越", "辉煌", "胜利", "赢", "赞", "棒", "好", "美", "善",
    "喜欢", "热爱", "支持", "鼓励", "肯定", "赞美", "优秀", "出色", "杰出",
    "机遇", "合作", "共赢", "和谐", "稳定", "安全", "健康", "积极", "乐观",
    "感谢", "感恩", "惊喜", "精彩", "完美", "高效", "便捷", "友好", "热情",
    "信任", "忠诚", "奉献", "拼搏", "奋斗", "成就", "荣耀", "辉煌",
}

_NEGATIVE_WORDS = {
    "失败", "下跌", "亏损", "损失", "危机", "风险", "问题", "困难", "挑战",
    "下降", "衰退", "萎缩", "恶化", "下滑", "暴跌", "崩盘", "崩溃", "灾难",
    "批评", "质疑", "担忧", "焦虑", "恐惧", "愤怒", "不满", "失望", "悲伤",
    "糟糕", "差", "坏", "烂", "丑", "恶", "假", "骗", "坑", "毒",
    "腐败", "贪污", "违法", "犯罪", "暴力", "冲突", "战争", "恐怖", "污染",
    "失业", "裁员", "破产", "倒闭", "罚款", "处罚", "警告", "召回", "投诉",
    "病", "死", "伤", "亡", "残", "痛", "苦", "累", "烦", "愁",
    "担心", "害怕", "紧张", "压力", "疲惫", "无奈", "无助", "孤独", "冷漠",
}


def _sentiment_score(text: str) -> float:
    """计算文本情感得分 [-1, 1]，正值=正面，负值=负面。"""
    import jieba
    words = list(jieba.cut(text))
    pos_count = sum(1 for w in words if w in _POSITIVE_WORDS)
    neg_count = sum(1 for w in words if w in _NEGATIVE_WORDS)
    total = pos_count + neg_count
    if total == 0:
        return 0.0
    return (pos_count - neg_count) / total


def _find_chinese_font() -> str | None:
    """查找系统中的中文字体。"""
    # Windows 字体路径
    win_fonts = [
        "C:/Windows/Fonts/msyh.ttc",      # 微软雅黑
        "C:/Windows/Fonts/simhei.ttf",     # 黑体
        "C:/Windows/Fonts/simsun.ttc",     # 宋体
    ]
    for font in win_fonts:
        if os.path.exists(font):
            return font
    # Linux/Mac 常见路径
    unix_fonts = [
        "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
        "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf",
        "/System/Library/Fonts/PingFang.ttc",
    ]
    for font in unix_fonts:
        if os.path.exists(font):
            return font
    return None  # wordcloud 会使用默认字体


def _normalize_date(value: str | None) -> str | None:
    text = _normalize_text(value)
    if not text:
        return None
    for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%Y.%m.%d", "%Y年%m月%d日"):
        try:
            return datetime.strptime(text, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return text


def _normalize_text(value: str | None) -> str | None:
    if value is None:
        return None
    stripped = BeautifulSoup(html.unescape(value), "html.parser").get_text(" ", strip=True)
    return re.sub(r"\s+", " ", stripped).strip() or None


def _build_dedup_key(news_id: str | None, title: str | None, date: str | None) -> str:
    if news_id:
        return f"news_id:{news_id.strip()}"
    source = f"{title or ''}|{date or ''}"
    return "title_date:" + hashlib.sha1(source.encode("utf-8")).hexdigest()


def _ensure_task_exists(task_id: str) -> None:
    conn = get_connection()
    try:
        row = conn.execute("SELECT 1 FROM tasks WHERE task_id = ?", (task_id,)).fetchone()
    finally:
        conn.close()
    if row is None:
        raise AppError(2001)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()
