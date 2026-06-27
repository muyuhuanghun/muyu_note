#!/usr/bin/env python3
"""
文本差异对比工具
📌 逐行对比两个文件，支持并排显示、HTML 输出、只显示变更行
"""

import argparse
import difflib
import sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")


def read_file(filepath: str) -> list:
    """读取文件，返回行列表"""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.readlines()
    except UnicodeDecodeError:
        with open(filepath, "r", encoding="gbk") as f:
            return f.readlines()


def diff_files(
    file1: str,
    file2: str,
    side_by_side: bool = False,
    changes_only: bool = False,
    context_lines: int = 3,
    html_output: bool = False,
    output: str = None,
):
    """
    对比两个文件

    参数:
        file1: 文件 1 路径
        file2: 文件 2 路径
        side_by_side: 并排显示
        changes_only: 只显示变更行
        context_lines: 上下文行数
        html_output: 输出 HTML
        output: 输出文件路径
    """
    lines1 = read_file(file1)
    lines2 = read_file(file2)

    name1 = Path(file1).name
    name2 = Path(file2).name

    if html_output:
        diff = difflib.HtmlDiff().make_file(lines1, lines2, name1, name2)
        if output:
            with open(output, "w", encoding="utf-8") as f:
                f.write(diff)
            print(f"✅ HTML 差异报告已保存: {output}")
        else:
            print(diff)
        return

    if side_by_side:
        diff = difflib.ndiff(lines1, lines2)
    elif changes_only:
        diff = difflib.unified_diff(
            lines1, lines2,
            fromfile=name1, tofile=name2,
            n=context_lines,
        )
        # 过滤掉只有空格的行
        diff = list(diff)
    else:
        diff = difflib.unified_diff(
            lines1, lines2,
            fromfile=name1, tofile=name2,
            n=context_lines,
        )

    output_lines = list(diff)

    if not output_lines:
        print(f"✅ 两个文件完全相同")
        return

    # 统计
    added = sum(1 for l in output_lines if l.startswith("+") and not l.startswith("+++"))
    removed = sum(1 for l in output_lines if l.startswith("-") and not l.startswith("---"))

    result = "".join(output_lines)

    if output:
        with open(output, "w", encoding="utf-8") as f:
            f.write(result)
        print(f"✅ 差异已保存: {output}")
    else:
        # 终端着色
        for line in output_lines:
            if line.startswith("+") and not line.startswith("+++"):
                print(f"\033[32m{line.rstrip()}\033[0m")  # 绿色
            elif line.startswith("-") and not line.startswith("---"):
                print(f"\033[31m{line.rstrip()}\033[0m")  # 红色
            elif line.startswith("@@"):
                print(f"\033[36m{line.rstrip()}\033[0m")  # 青色
            else:
                print(line.rstrip())

    print(f"\n📊 统计: +{added} 行新增, -{removed} 行删除")


def main():
    parser = argparse.ArgumentParser(
        description="文本差异对比工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python text_diff.py old.md new.md
  python text_diff.py old.md new.md --side-by-side
  python text_diff.py old.md new.md --changes-only
  python text_diff.py old.md new.md --html -o diff.html
        """,
    )
    parser.add_argument("file1", help="文件 1")
    parser.add_argument("file2", help="文件 2")
    parser.add_argument("--side-by-side", action="store_true", help="并排显示")
    parser.add_argument("--changes-only", action="store_true", help="只显示变更")
    parser.add_argument("--context", type=int, default=3, help="上下文行数（默认 3）")
    parser.add_argument("--html", action="store_true", help="输出 HTML")
    parser.add_argument("-o", "--output", help="输出文件")

    args = parser.parse_args()
    diff_files(
        args.file1, args.file2,
        side_by_side=args.side_by_side,
        changes_only=args.changes_only,
        context_lines=args.context,
        html_output=args.html,
        output=args.output,
    )


if __name__ == "__main__":
    main()
