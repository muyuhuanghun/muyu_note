#!/usr/bin/env python3
"""
批量文本查找替换工具
📌 支持普通文本和正则表达式，可按扩展名过滤，附带 --dry-run
"""

import argparse
import os
import re
import sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")


def batch_replace(
    directory: str,
    old: str,
    new: str,
    use_regex: bool = False,
    extensions: list = None,
    dry_run: bool = False,
    ignore_case: bool = False,
):
    """
    批量替换目录下文件中的文本

    参数:
        directory: 目标目录
        old: 要查找的文本（或正则表达式）
        new: 替换为的文本
        use_regex: 使用正则表达式
        extensions: 文件扩展名过滤
        dry_run: 预览模式
        ignore_case: 忽略大小写
    """
    dir_path = Path(directory)
    if not dir_path.is_dir():
        print(f"❌ 目录不存在: {directory}")
        sys.exit(1)

    if extensions is None:
        extensions = [".txt", ".md", ".py", ".c", ".cpp", ".h", ".java", ".js",
                      ".ts", ".html", ".css", ".json", ".yaml", ".yml", ".toml",
                      ".cfg", ".ini", ".sh", ".bat"]

    # 收集文件
    files = []
    for ext in extensions:
        files.extend(dir_path.rglob(f"*{ext}"))
    files = [f for f in files if f.is_file()]
    files = sorted(set(files))

    if not files:
        print("⚠️ 没有找到匹配的文件")
        return

    # 编译正则
    if use_regex:
        flags = re.IGNORECASE if ignore_case else 0
        try:
            pattern = re.compile(old, flags)
        except re.error as e:
            print(f"❌ 正则表达式错误: {e}")
            sys.exit(1)
    else:
        pattern = None

    print(f"📂 目录: {dir_path}")
    print(f"📝 文件: {len(files)} 个")
    print(f"🔍 查找: {old}")
    print(f"✏️ 替换: {new}")
    if dry_run:
        print("🔍 预览模式")
    print("-" * 60)

    total_replacements = 0
    modified_files = 0

    for filepath in files:
        try:
            content = filepath.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue  # 跳过二进制文件

        if use_regex:
            new_content, count = pattern.subn(new, content)
        else:
            if ignore_case:
                # 不区分大小写的替换
                new_content = re.sub(re.escape(old), new, content, flags=re.IGNORECASE)
                count = len(re.findall(re.escape(old), content, flags=re.IGNORECASE))
            else:
                count = content.count(old)
                new_content = content.replace(old, new)

        if count == 0:
            continue

        rel_path = filepath.relative_to(dir_path)

        if dry_run:
            print(f"  {rel_path}: {count} 处替换")
        else:
            filepath.write_text(new_content, encoding="utf-8")
            print(f"  ✅ {rel_path}: {count} 处替换")

        total_replacements += count
        modified_files += 1

    print("-" * 60)
    action = "将替换" if dry_run else "已替换"
    print(f"📊 {action} {total_replacements} 处（{modified_files} 个文件）")


def main():
    parser = argparse.ArgumentParser(
        description="批量文本查找替换工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python batch_text_replace.py ./src/ --old "old_func" --new "new_func"
  python batch_text_replace.py ./src/ --old "def \\w+\\(" --new "def new_name(" --regex
  python batch_text_replace.py ./src/ --old "TODO" --new "DONE" --ext .py
  python batch_text_replace.py ./src/ --old "foo" --new "bar" --dry-run
        """,
    )
    parser.add_argument("directory", help="目标目录")
    parser.add_argument("--old", required=True, help="查找文本")
    parser.add_argument("--new", required=True, help="替换文本")
    parser.add_argument("--regex", action="store_true", help="使用正则表达式")
    parser.add_argument("--ext", nargs="+", help="文件扩展名过滤")
    parser.add_argument("--ignore-case", "-i", action="store_true", help="忽略大小写")
    parser.add_argument("--dry-run", action="store_true", help="预览模式")

    args = parser.parse_args()
    batch_replace(
        directory=args.directory,
        old=args.old,
        new=args.new,
        use_regex=args.regex,
        extensions=args.ext,
        dry_run=args.dry_run,
        ignore_case=args.ignore_case,
    )


if __name__ == "__main__":
    main()
