#!/usr/bin/env python3
"""
磁盘使用分析工具
📌 扫描目录，找出大文件、按类型统计、可视化磁盘占用
"""

import argparse
import os
import sys
from collections import defaultdict
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")


def scan_directory(path: str, depth: int = None, ignore_hidden: bool = True) -> list:
    """扫描目录，返回文件信息列表"""
    root = Path(path)
    files = []

    for f in root.rglob("*"):
        if not f.is_file():
            continue
        if ignore_hidden and any(part.startswith(".") for part in f.relative_to(root).parts):
            continue

        rel = f.relative_to(root)
        current_depth = len(rel.parts)

        if depth is not None and current_depth > depth:
            continue

        try:
            size = f.stat().st_size
        except OSError:
            size = 0

        files.append({
            "path": str(rel),
            "name": f.name,
            "size": size,
            "ext": f.suffix.lower() or "(无扩展名)",
            "depth": current_depth,
        })

    return files


def format_size(size: int) -> str:
    """格式化文件大小"""
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} PB"


def analyze_disk(
    directory: str,
    top_n: int = 20,
    by_type: bool = False,
    depth: int = None,
    min_size: int = 0,
):
    """分析磁盘使用"""
    dir_path = Path(directory)
    if not dir_path.is_dir():
        print(f"❌ 目录不存在: {directory}")
        sys.exit(1)

    print(f"🔍 扫描目录: {dir_path}")
    files = scan_directory(directory, depth)
    print(f"📊 文件数: {len(files)}")

    if not files:
        print("⚠️ 没有找到文件")
        return

    total_size = sum(f["size"] for f in files)

    # 按类型统计
    if by_type:
        by_ext = defaultdict(lambda: {"count": 0, "size": 0})
        for f in files:
            by_ext[f["ext"]]["count"] += 1
            by_ext[f["ext"]]["size"] += f["size"]

        sorted_exts = sorted(by_ext.items(), key=lambda x: -x[1]["size"])

        print(f"\n📋 按文件类型统计:")
        print(f"{'扩展名':<15} {'数量':>8} {'大小':>12} {'占比':>8}")
        print("-" * 45)
        for ext, info in sorted_exts[:15]:
            pct = info["size"] / total_size * 100 if total_size > 0 else 0
            bar = "█" * min(int(pct / 2), 30)
            print(f"  {ext:<13} {info['count']:>6}  {format_size(info['size']):>10}  {pct:>5.1f}%  {bar}")

    # 最大文件
    largest = sorted(files, key=lambda f: -f["size"])
    if min_size > 0:
        largest = [f for f in largest if f["size"] >= min_size]

    print(f"\n📁 最大文件 Top {top_n}:")
    print(f"{'大小':>12}  {'文件路径'}")
    print("-" * 60)
    for f in largest[:top_n]:
        print(f"  {format_size(f['size']):>10}  {f['path']}")

    # 总计
    print(f"\n{'='*60}")
    print(f"📊 总计: {len(files)} 个文件, {format_size(total_size)}")

    # 目录大小 Top 10
    dir_sizes = defaultdict(int)
    for f in files:
        top_dir = f["path"].split(os.sep)[0] if os.sep in f["path"] else "(根目录)"
        dir_sizes[top_dir] += f["size"]

    sorted_dirs = sorted(dir_sizes.items(), key=lambda x: -x[1])
    if len(sorted_dirs) > 1:
        print(f"\n📂 目录大小 Top 10:")
        for d, size in sorted_dirs[:10]:
            pct = size / total_size * 100 if total_size > 0 else 0
            bar = "█" * min(int(pct / 2), 30)
            print(f"  {format_size(size):>10}  {pct:>5.1f}%  {d:<20} {bar}")


def main():
    parser = argparse.ArgumentParser(
        description="磁盘使用分析工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python disk_usage.py .
  python disk_usage.py . --top 20
  python disk_usage.py . --by-type
  python disk_usage.py . --depth 2 --min-size 1048576
        """,
    )
    parser.add_argument("directory", help="目标目录")
    parser.add_argument("--top", type=int, default=20, help="显示前 N 个最大文件")
    parser.add_argument("--by-type", action="store_true", help="按文件类型统计")
    parser.add_argument("--depth", type=int, help="扫描深度")
    parser.add_argument("--min-size", type=int, default=0, help="最小文件大小（字节）")

    args = parser.parse_args()
    analyze_disk(args.directory, args.top, args.by_type, args.depth, args.min_size)


if __name__ == "__main__":
    main()
