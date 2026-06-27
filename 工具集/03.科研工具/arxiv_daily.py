#!/usr/bin/env python3
"""
arXiv 每日论文推送
📌 根据类别和关键词获取最新论文，输出为 Markdown 或终端显示
⚠️ 基于 arXiv API，无需额外安装依赖
"""

import argparse
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime

# Windows 终端 UTF-8 输出
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")


# arXiv API 基础 URL
ARXIV_API = "http://export.arxiv.org/api/query"

# 常用类别
CATEGORIES = {
    "cs.AI": "人工智能",
    "cs.CV": "计算机视觉",
    "cs.CL": "计算语言学（NLP）",
    "cs.LG": "机器学习",
    "cs.AR": "硬件架构",
    "cs.DC": "分布式计算",
    "cs.SE": "软件工程",
    "cs.DB": "数据库",
    "cs.OS": "操作系统",
    "cs.NE": "神经网络与进化计算",
    "stat.ML": "统计机器学习",
    "eess.SP": "信号处理",
}


def fetch_arxiv(category: str, max_results: int = 50) -> list:
    """
    从 arXiv API 获取最新论文

    参数:
        category: arXiv 类别（如 cs.CV）
        max_results: 最大返回数量
    """
    query = f"cat:{category}"
    url = f"{ARXIV_API}?search_query={query}&sortBy=submittedDate&sortOrder=descending&max_results={max_results}"

    print(f"🔍 正在查询: {category}（{CATEGORIES.get(category, '未知')}）")
    print(f"   URL: {url}")

    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=30) as resp:
            xml_data = resp.read().decode("utf-8")
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        return []

    # 解析 XML
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    root = ET.fromstring(xml_data)
    papers = []

    for entry in root.findall("atom:entry", ns):
        title = entry.find("atom:title", ns).text.strip().replace("\n", " ")
        title = re.sub(r"\s+", " ", title)

        summary = entry.find("atom:summary", ns).text.strip().replace("\n", " ")
        summary = re.sub(r"\s+", " ", summary)

        authors = [
            a.find("atom:name", ns).text
            for a in entry.findall("atom:author", ns)
        ]

        link = entry.find("atom:id", ns).text
        published = entry.find("atom:published", ns).text[:10]

        # 提取 PDF 链接
        pdf_link = ""
        for l in entry.findall("atom:link", ns):
            if l.get("title") == "pdf":
                pdf_link = l.get("href", "")

        papers.append({
            "title": title,
            "authors": authors,
            "summary": summary[:300] + "..." if len(summary) > 300 else summary,
            "link": link,
            "pdf": pdf_link,
            "published": published,
        })

    return papers


def filter_by_keywords(papers: list, keywords: list) -> list:
    """按关键词过滤论文"""
    if not keywords:
        return papers

    filtered = []
    for p in papers:
        text = (p["title"] + " " + p["summary"]).lower()
        if any(kw.lower() in text for kw in keywords):
            filtered.append(p)
    return filtered


def display_papers(papers: list, fmt: str = "text"):
    """显示论文列表"""
    if not papers:
        print("📭 没有找到匹配的论文")
        return

    if fmt == "md":
        print(f"\n## arXiv 每日论文 — {datetime.now().strftime('%Y-%m-%d')}\n")
        for i, p in enumerate(papers, 1):
            print(f"### {i}. {p['title']}\n")
            print(f"- **作者**: {', '.join(p['authors'][:3])}" +
                  (f" 等 {len(p['authors'])} 人" if len(p['authors']) > 3 else ""))
            print(f"- **日期**: {p['published']}")
            print(f"- **链接**: [{p['link']}]({p['link']})")
            if p['pdf']:
                print(f"- **PDF**: [{p['pdf']}]({p['pdf']})")
            print(f"\n> {p['summary']}\n")
    else:
        for i, p in enumerate(papers, 1):
            print(f"\n{'='*60}")
            print(f"[{i}] {p['title']}")
            print(f"    作者: {', '.join(p['authors'][:3])}" +
                  (f" 等" if len(p['authors']) > 3 else ""))
            print(f"    日期: {p['published']}")
            print(f"    链接: {p['link']}")
            print(f"    摘要: {p['summary'][:150]}...")


def main():
    parser = argparse.ArgumentParser(
        description="arXiv 每日论文推送",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
常用类别:
  cs.AI    人工智能          cs.CV    计算机视觉
  cs.CL    NLP              cs.LG    机器学习
  cs.AR    硬件架构          cs.SE    软件工程

示例:
  python arxiv_daily.py --category cs.CV
  python arxiv_daily.py --category cs.AI --keywords "transformer,LLM"
  python arxiv_daily.py --category cs.AR --format md -o 今日论文.md
        """,
    )
    parser.add_argument("--category", default="cs.AI", help="arXiv 类别（默认 cs.AI）")
    parser.add_argument("--keywords", default="", help="关键词过滤（逗号分隔）")
    parser.add_argument("--max", type=int, default=20, help="最大论文数（默认 20）")
    parser.add_argument("--format", choices=["text", "md"], default="text", help="输出格式")
    parser.add_argument("-o", "--output", help="输出文件路径")

    args = parser.parse_args()

    papers = fetch_arxiv(args.category, args.max)

    if args.keywords:
        kw_list = [k.strip() for k in args.keywords.split(",")]
        papers = filter_by_keywords(papers, kw_list)
        print(f"🔑 关键词过滤: {kw_list} → {len(papers)} 篇匹配")

    if args.output:
        import io
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        display_papers(papers, args.format)
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout

        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"✅ 已保存 {len(papers)} 篇论文 → {args.output}")
    else:
        display_papers(papers, args.format)

    print(f"\n📊 共获取 {len(papers)} 篇论文")


if __name__ == "__main__":
    main()
