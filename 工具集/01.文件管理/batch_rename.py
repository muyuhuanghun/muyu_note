#!/usr/bin/env python3
"""
批量重命名工具
📌 支持前缀/后缀、序号模板、扩展名过滤，附带 --dry-run 预览模式
"""

import argparse
import os
import sys
from pathlib import Path

# Windows 终端 UTF-8 输出
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")


def batch_rename(
    directory: str,
    prefix: str = "",
    suffix: str = "",
    ext: str = None,
    pattern: str = None,
    start: int = 1,
    dry_run: bool = False,
):
    """
    批量重命名目录中的文件

    参数:
        directory: 目标目录
        prefix: 文件名前缀
        suffix: 文件名后缀（在扩展名之前）
        ext: 只处理指定扩展名的文件（如 .pdf）
        pattern: 序号模板，如 "photo_{n:03d}"，n 为序号
        start: 序号起始值
        dry_run: 预览模式，不实际修改
    """
    dir_path = Path(directory)
    if not dir_path.is_dir():
        print(f"❌ 目录不存在: {directory}")
        sys.exit(1)

    # 收集目标文件
    files = sorted(
        f for f in dir_path.iterdir()
        if f.is_file() and (ext is None or f.suffix.lower() == ext.lower())
    )

    if not files:
        print("⚠️ 没有找到匹配的文件")
        return

    print(f"📂 目标目录: {dir_path}")
    print(f"📝 匹配文件: {len(files)} 个")
    if dry_run:
        print("🔍 预览模式（不会实际修改）")
    print("-" * 60)

    renamed_count = 0
    for i, file_path in enumerate(files):
        old_name = file_path.name
        stem = file_path.stem
        extension = file_path.suffix

        # 生成新文件名
        if pattern:
            # 使用序号模板
            new_stem = pattern.format(n=start + i)
        else:
            new_stem = f"{prefix}{stem}{suffix}"

        new_name = f"{new_stem}{extension}"
        new_path = file_path.parent / new_name

        # 跳过同名文件
        if old_name == new_name:
            continue

        # 处理冲突
        if new_path.exists():
            print(f"  ⚠️ 冲突跳过: {old_name} → {new_name}（目标已存在）")
            continue

        if dry_run:
            print(f"  {old_name}  →  {new_name}")
        else:
            file_path.rename(new_path)
            print(f"  ✅ {old_name}  →  {new_name}")

        renamed_count += 1

    print("-" * 60)
    action = "将重命名" if dry_run else "已重命名"
    print(f"📊 {action} {renamed_count} 个文件")


def main():
    parser = argparse.ArgumentParser(
        description="批量重命名文件工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python batch_rename.py ./课件/ --prefix "数据结构_" --ext .pdf
  python batch_rename.py ./photos/ --pattern "photo_{n:03d}" --ext .png
  python batch_rename.py ./下载/ --prefix "DL_" --dry-run
        """,
    )
    parser.add_argument("directory", help="目标目录路径")
    parser.add_argument("--prefix", default="", help="文件名前缀")
    parser.add_argument("--suffix", default="", help="文件名后缀（扩展名之前）")
    parser.add_argument("--ext", default=None, help="只处理指定扩展名（如 .pdf）")
    parser.add_argument("--pattern", default=None, help="序号模板，如 photo_{n:03d}")
    parser.add_argument("--start", type=int, default=1, help="序号起始值（默认 1）")
    parser.add_argument("--dry-run", action="store_true", help="预览模式，不实际修改")

    args = parser.parse_args()
    batch_rename(
        directory=args.directory,
        prefix=args.prefix,
        suffix=args.suffix,
        ext=args.ext,
        pattern=args.pattern,
        start=args.start,
        dry_run=args.dry_run,
    )


if __name__ == "__main__":
    main()
