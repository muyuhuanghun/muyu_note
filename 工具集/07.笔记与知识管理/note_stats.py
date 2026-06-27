#!/usr/bin/env python3
"""
笔记库统计工具
📌 统计 Obsidian vault 的文件数、字数、更新频率等
📌 支持按目录统计、最近活跃度分析
"""

import argparse
import os
import sys
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path

# Windows 终端 UTF-8 输出
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")


def scan_notes(vault_path: str, ignore_dirs: list = None) -> list:
    """扫描 vault 中的所有 .md 文件"""
    vault = Path(vault_path)
    ignore_dirs = ignore_dirs or [".obsidian", ".git", ".claude", "node_modules"]

    notes = []
    for md in vault.rglob("*.md"):
        rel = md.relative_to(vault)
        if any(part in ignore_dirs for part in rel.parts):
            continue

        stat = md.stat()
        try:
            content = md.read_text(encoding="utf-8")
            char_count = len(content)
            word_count = len(content.split())
            line_count = content.count("\n") + 1
        except Exception:
            char_count = word_count = line_count = 0

        notes.append({
            "path": str(rel),
            "stem": md.stem,
            "size": stat.st_size,
            "chars": char_count,
            "words": word_count,
            "lines": line_count,
            "modified": datetime.fromtimestamp(stat.st_mtime),
            "created": datetime.fromtimestamp(stat.st_ctime),
            "top_dir": rel.parts[0] if len(rel.parts) > 1 else "(根目录)",
        })

    return notes


def overall_stats(notes: list) -> dict:
    """整体统计"""
    total_chars = sum(n["chars"] for n in notes)
    total_words = sum(n["words"] for n in notes)
    total_lines = sum(n["lines"] for n in notes)
    total_size = sum(n["size"] for n in notes)

    return {
        "file_count": len(notes),
        "total_chars": total_chars,
        "total_words": total_words,
        "total_lines": total_lines,
        "total_size": total_size,
        "avg_chars": total_chars / len(notes) if notes else 0,
        "avg_words": total_words / len(notes) if notes else 0,
    }


def by_directory_stats(notes: list) -> dict:
    """按目录统计"""
    by_dir = defaultdict(lambda: {"count": 0, "chars": 0, "words": 0, "size": 0})

    for n in notes:
        d = by_dir[n["top_dir"]]
        d["count"] += 1
        d["chars"] += n["chars"]
        d["words"] += n["words"]
        d["size"] += n["size"]

    return dict(sorted(by_dir.items(), key=lambda x: -x[1]["count"]))


def recent_activity(notes: list, days: int = 7) -> dict:
    """最近活跃度"""
    cutoff = datetime.now() - timedelta(days=days)
    recent = [n for n in notes if n["modified"] >= cutoff]

    # 按日期分组
    by_date = defaultdict(list)
    for n in recent:
        date_str = n["modified"].strftime("%Y-%m-%d")
        by_date[date_str].append(n)

    return {
        "count": len(recent),
        "days": days,
        "by_date": dict(sorted(by_date.items())),
    }


def largest_notes(notes: list, top_n: int = 10) -> list:
    """最大的 N 篇笔记"""
    return sorted(notes, key=lambda n: n["chars"], reverse=True)[:top_n]


def most_recently_modified(notes: list, top_n: int = 10) -> list:
    """最近修改的 N 篇笔记"""
    return sorted(notes, key=lambda n: n["modified"], reverse=True)[:top_n]


def print_report(
    notes: list,
    stats: dict,
    by_dir: dict,
    recent: dict,
    largest: list,
    recent_modified: list,
    by_directory: bool = False,
    recent_days: int = 7,
    fmt: str = "text",
):
    """输出报告"""
    if fmt == "md":
        print("# 笔记库统计报告\n")
        print(f"## 整体概览\n")
        print(f"| 指标 | 数值 |")
        print(f"|------|------|")
        print(f"| 笔记总数 | {stats['file_count']} |")
        print(f"| 总字数 | {stats['total_chars']:,} |")
        print(f"| 总词数 | {stats['total_words']:,} |")
        print(f"| 总行数 | {stats['total_lines']:,} |")
        print(f"| 总大小 | {stats['total_size'] / 1024 / 1024:.2f} MB |")
        print(f"| 平均字数/篇 | {stats['avg_chars']:.0f} |")

        if by_directory:
            print(f"\n## 按目录统计\n")
            print(f"| 目录 | 文件数 | 字数 | 大小 |")
            print(f"|------|--------|------|------|")
            for d, info in by_dir.items():
                size_kb = info["size"] / 1024
                print(f"| {d} | {info['count']} | {info['chars']:,} | {size_kb:.1f} KB |")

        print(f"\n## 最近 {recent_days} 天活跃度\n")
        print(f"- 修改笔记数: {recent['count']}")
        for date, items in recent["by_date"].items():
            print(f"\n### {date}（{len(items)} 篇）\n")
            for n in items[:5]:
                print(f"- {n['stem']}")
            if len(items) > 5:
                print(f"- ... 还有 {len(items) - 5} 篇")
    else:
        print(f"\n{'='*50}")
        print(f"📊 笔记库统计报告")
        print(f"{'='*50}")

        print(f"\n📈 整体概览:")
        print(f"   笔记总数: {stats['file_count']}")
        print(f"   总字数:   {stats['total_chars']:,}")
        print(f"   总行数:   {stats['total_lines']:,}")
        print(f"   总大小:   {stats['total_size'] / 1024 / 1024:.2f} MB")
        print(f"   平均字数: {stats['avg_chars']:.0f} 字/篇")

        if by_directory:
            print(f"\n📂 按目录统计:")
            for d, info in by_dir.items():
                bar = "█" * min(info["count"], 30)
                print(f"   {d:<25} {info['count']:>4} 篇  {bar}")

        print(f"\n🕐 最近 {recent_days} 天活跃度:")
        print(f"   修改笔记: {recent['count']} 篇")
        for date, items in recent["by_date"].items():
            print(f"   {date}: {len(items)} 篇")

        print(f"\n📝 最大笔记 Top 5:")
        for n in largest[:5]:
            print(f"   {n['chars']:>6} 字  {n['path']}")

        print(f"\n🔄 最近修改 Top 5:")
        for n in recent_modified[:5]:
            mod = n["modified"].strftime("%m-%d %H:%M")
            print(f"   {mod}  {n['path']}")


def main():
    parser = argparse.ArgumentParser(
        description="笔记库统计工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python note_stats.py /path/to/vault
  python note_stats.py /path/to/vault --by-dir
  python note_stats.py /path/to/vault --recent 30 --format md
        """,
    )
    parser.add_argument("vault", help="Obsidian vault 路径")
    parser.add_argument("--by-dir", action="store_true", help="按目录统计")
    parser.add_argument("--recent", type=int, default=7, help="最近活跃天数（默认 7）")
    parser.add_argument("--format", choices=["text", "md"], default="text", help="输出格式")
    parser.add_argument("-o", "--output", help="输出到文件")

    args = parser.parse_args()

    print(f"🔍 扫描 vault: {args.vault}")
    notes = scan_notes(args.vault)
    print(f"   找到 {len(notes)} 个 .md 文件")

    stats = overall_stats(notes)
    by_dir = by_directory_stats(notes)
    recent = recent_activity(notes, args.recent)
    largest = largest_notes(notes)
    recent_mod = most_recently_modified(notes)

    if args.output:
        import io
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        print_report(notes, stats, by_dir, recent, largest, recent_mod,
                     args.by_dir, args.recent, args.format)
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"✅ 报告已保存: {args.output}")
    else:
        print_report(notes, stats, by_dir, recent, largest, recent_mod,
                     args.by_dir, args.recent, args.format)


if __name__ == "__main__":
    main()
