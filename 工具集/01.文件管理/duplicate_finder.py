#!/usr/bin/env python3
"""
重复文件查找工具
📌 基于文件大小初筛 + MD5 哈希精检，高效找到重复文件
"""

import argparse
import hashlib
import os
import sys
from collections import defaultdict
from pathlib import Path

# Windows 终端 UTF-8 输出
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")


def file_hash(filepath: Path, chunk_size: int = 8192) -> str:
    """计算文件的 MD5 哈希值"""
    h = hashlib.md5()
    with open(filepath, "rb") as f:
        while chunk := f.read(chunk_size):
            h.update(chunk)
    return h.hexdigest()


def find_duplicates(
    directory: str,
    min_size: int = 0,
    list_only: bool = False,
    ignore_hidden: bool = True,
):
    """
    查找重复文件

    参数:
        directory: 扫描目录
        min_size: 最小文件大小（字节），小于此值的文件不检查
        list_only: 只列出，不交互删除
        ignore_hidden: 忽略隐藏文件
    """
    dir_path = Path(directory)
    if not dir_path.is_dir():
        print(f"❌ 目录不存在: {directory}")
        sys.exit(1)

    # 第一步：按文件大小分组
    print("🔍 扫描文件中...")
    size_groups = defaultdict(list)
    file_count = 0
    for f in dir_path.rglob("*"):
        if not f.is_file():
            continue
        if ignore_hidden and any(part.startswith(".") for part in f.parts):
            continue
        size = f.stat().st_size
        if size < min_size:
            continue
        size_groups[size].append(f)
        file_count += 1

    print(f"📊 扫描完成: {file_count} 个文件")

    # 第二步：对大小相同的文件计算哈希
    duplicates = defaultdict(list)
    hash_count = 0
    for size, files in size_groups.items():
        if len(files) < 2:
            continue
        for f in files:
            h = file_hash(f)
            duplicates[h].append(f)
            hash_count += 1

    # 过滤出真正的重复组
    dup_groups = {h: files for h, files in duplicates.items() if len(files) > 1}

    if not dup_groups:
        print("✅ 没有发现重复文件")
        return

    # 显示结果
    total_dup = sum(len(files) - 1 for files in dup_groups.values())
    wasted = sum(
        (len(files) - 1) * files[0].stat().st_size
        for files in dup_groups.values()
    )

    print(f"\n🚨 发现 {len(dup_groups)} 组重复文件")
    print(f"   可释放空间: {wasted / 1024 / 1024:.2f} MB")
    print("=" * 60)

    for i, (h, files) in enumerate(dup_groups.items(), 1):
        size = files[0].stat().st_size
        print(f"\n组 {i}（{len(files)} 个文件，每个 {size / 1024:.1f} KB）：")
        for j, f in enumerate(files):
            marker = "  ← 保留" if j == 0 else "  ← 删除"
            print(f"  [{j}] {f}{marker if not list_only else ''}")

    if list_only:
        return

    # 交互删除
    print("\n" + "=" * 60)
    print("💡 每组中 [0] 为建议保留的文件，其余为建议删除")
    print("   输入 'a' 全部自动删除 | 输入 'q' 退出 | 回车逐组确认")

    choice = input("\n请选择: ").strip().lower()
    if choice == "q":
        return

    deleted = 0
    for h, files in dup_groups.items():
        to_delete = files[1:]  # 保留第一个
        if choice != "a":
            print(f"\n删除以下文件？(y/n)")
            for f in to_delete:
                print(f"  {f}")
            confirm = input("> ").strip().lower()
            if confirm != "y":
                continue

        for f in to_delete:
            try:
                f.unlink()
                print(f"  🗑️ 已删除: {f}")
                deleted += 1
            except Exception as e:
                print(f"  ❌ 删除失败: {f} ({e})")

    print(f"\n📊 共删除 {deleted} 个重复文件")


def main():
    parser = argparse.ArgumentParser(
        description="重复文件查找工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python duplicate_finder.py ~/Documents
  python duplicate_finder.py ~/Documents --list-only
  python duplicate_finder.py ~/Downloads --min-size 1024
        """,
    )
    parser.add_argument("directory", help="扫描目录路径")
    parser.add_argument("--list-only", action="store_true", help="只列出，不交互删除")
    parser.add_argument("--min-size", type=int, default=0, help="最小文件大小（字节）")
    parser.add_argument("--include-hidden", action="store_true", help="包含隐藏文件")

    args = parser.parse_args()
    find_duplicates(
        directory=args.directory,
        min_size=args.min_size,
        list_only=args.list_only,
        ignore_hidden=not args.include_hidden,
    )


if __name__ == "__main__":
    main()
