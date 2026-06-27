#!/usr/bin/env python3
"""
文件自动整理工具
📌 按文件类型或修改日期自动分类到子目录，附带 --dry-run 预览模式
"""

import argparse
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path

# Windows 终端 UTF-8 输出
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

# 文件类型 → 子目录名 映射
TYPE_MAP = {
    # 文档
    ".pdf": "文档", ".doc": "文档", ".docx": "文档",
    ".xls": "文档", ".xlsx": "文档", ".ppt": "文档", ".pptx": "文档",
    ".txt": "文档", ".md": "文档", ".tex": "文档", ".csv": "文档",
    # 图片
    ".jpg": "图片", ".jpeg": "图片", ".png": "图片",
    ".gif": "图片", ".bmp": "图片", ".svg": "图片", ".webp": "图片",
    # 视频
    ".mp4": "视频", ".avi": "视频", ".mkv": "视频",
    ".mov": "视频", ".wmv": "视频", ".flv": "视频",
    # 音频
    ".mp3": "音频", ".wav": "音频", ".flac": "音频",
    ".aac": "音频", ".ogg": "音频",
    # 压缩包
    ".zip": "压缩包", ".rar": "压缩包", ".7z": "压缩包",
    ".tar": "压缩包", ".gz": "压缩包", ".bz2": "压缩包",
    # 代码
    ".py": "代码", ".c": "代码", ".cpp": "代码", ".h": "代码",
    ".java": "代码", ".js": "代码", ".ts": "代码",
    ".html": "代码", ".css": "代码", ".sh": "代码",
    # 可执行文件
    ".exe": "程序", ".msi": "程序", ".dmg": "程序",
    ".deb": "程序", ".rpm": "程序",
}


def get_type_dir(filename: str) -> str:
    """根据文件扩展名返回分类目录名"""
    ext = Path(filename).suffix.lower()
    return TYPE_MAP.get(ext, "其他")


def get_date_dir(filepath: Path) -> str:
    """根据文件修改日期返回 YYYY-MM 格式目录名"""
    mtime = datetime.fromtimestamp(filepath.stat().st_mtime)
    return mtime.strftime("%Y-%m")


def organize_files(
    directory: str,
    by_date: bool = False,
    dry_run: bool = False,
    ignore_hidden: bool = True,
):
    """
    整理目录中的文件

    参数:
        directory: 目标目录
        by_date: True 按日期分类，False 按类型分类
        dry_run: 预览模式
        ignore_hidden: 忽略隐藏文件
    """
    dir_path = Path(directory)
    if not dir_path.is_dir():
        print(f"❌ 目录不存在: {directory}")
        sys.exit(1)

    # 收集文件（不递归子目录）
    files = [
        f for f in dir_path.iterdir()
        if f.is_file()
        and (not ignore_hidden or not f.name.startswith("."))
        and f.name != "desktop.ini"
    ]

    if not files:
        print("⚠️ 没有找到需要整理的文件")
        return

    mode = "按日期" if by_date else "按类型"
    print(f"📂 目标目录: {dir_path}")
    print(f"📝 待整理文件: {len(files)} 个（{mode}分类）")
    if dry_run:
        print("🔍 预览模式（不会实际移动）")
    print("-" * 60)

    moved_count = 0
    for file_path in sorted(files):
        if by_date:
            target_dir = get_date_dir(file_path)
        else:
            target_dir = get_type_dir(file_path.name)

        target_path = dir_path / target_dir / file_path.name

        # 跳过已在正确目录的文件
        if target_path.parent == file_path.parent:
            continue

        # 处理冲突
        if target_path.exists():
            print(f"  ⚠️ 冲突跳过: {file_path.name}（目标目录已存在同名文件）")
            continue

        if dry_run:
            print(f"  {file_path.name}  →  {target_dir}/")
        else:
            target_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(file_path), str(target_path))
            print(f"  ✅ {file_path.name}  →  {target_dir}/")

        moved_count += 1

    print("-" * 60)
    action = "将移动" if dry_run else "已整理"
    print(f"📊 {action} {moved_count} 个文件")


def main():
    parser = argparse.ArgumentParser(
        description="文件自动整理工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python file_organizer.py ~/Downloads
  python file_organizer.py ~/Downloads --by-date
  python file_organizer.py ~/Downloads --dry-run
        """,
    )
    parser.add_argument("directory", help="目标目录路径")
    parser.add_argument("--by-date", action="store_true", help="按修改日期分类（YYYY-MM）")
    parser.add_argument("--dry-run", action="store_true", help="预览模式，不实际移动")
    parser.add_argument("--include-hidden", action="store_true", help="包含隐藏文件")

    args = parser.parse_args()
    organize_files(
        directory=args.directory,
        by_date=args.by_date,
        dry_run=args.dry_run,
        ignore_hidden=not args.include_hidden,
    )


if __name__ == "__main__":
    main()
