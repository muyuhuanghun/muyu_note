#!/usr/bin/env python3
"""
文件编码转换工具
📌 检测文件编码并批量转换为指定编码，解决中文乱码问题
"""

import argparse
import sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

# 常见编码列表（用于检测）
COMMON_ENCODINGS = [
    "utf-8", "utf-8-sig",  # UTF-8 (with/without BOM)
    "gbk", "gb2312", "gb18030",  # 中文
    "big5",  # 繁体中文
    "shift_jis", "euc-jp",  # 日文
    "euc-kr",  # 韩文
    "latin-1", "ascii",  # 西文
]


def detect_encoding(filepath: str) -> str:
    """
    检测文件编码
    尝试常见编码列表，返回第一个能完整解码的
    """
    raw = Path(filepath).read_bytes()

    # 先试 UTF-8 BOM
    if raw[:3] == b"\xef\xbb\xbf":
        return "utf-8-sig"

    for enc in COMMON_ENCODINGS:
        try:
            raw.decode(enc)
            return enc
        except (UnicodeDecodeError, LookupError):
            continue

    return "unknown"


def convert_encoding(filepath: str, target: str, dry_run: bool = False) -> bool:
    """转换单个文件的编码"""
    path = Path(filepath)
    source = detect_encoding(filepath)

    if source == "unknown":
        print(f"  ⚠️ 无法检测编码: {path.name}")
        return False

    if source == target:
        return False  # 已经是目标编码

    if dry_run:
        print(f"  {path.name}: {source} → {target}")
        return True

    try:
        raw = path.read_bytes()
        text = raw.decode(source)
        path.write_text(text, encoding=target)
        print(f"  ✅ {path.name}: {source} → {target}")
        return True
    except Exception as e:
        print(f"  ❌ {path.name}: {e}")
        return False


def batch_convert(
    directory: str,
    target: str,
    recursive: bool = False,
    extensions: list = None,
    dry_run: bool = False,
):
    """
    批量转换目录下文件的编码

    参数:
        directory: 目标目录
        target: 目标编码
        recursive: 是否递归子目录
        extensions: 文件扩展名过滤（默认 .txt .md .csv .json .py .c .cpp .h）
        dry_run: 预览模式
    """
    dir_path = Path(directory)
    if extensions is None:
        extensions = [".txt", ".md", ".csv", ".json", ".py", ".c", ".cpp", ".h", ".java", ".js", ".html", ".css"]

    # 收集文件
    files = []
    for ext in extensions:
        if recursive:
            files.extend(dir_path.rglob(f"*{ext}"))
        else:
            files.extend(dir_path.glob(f"*{ext}"))

    files = sorted(set(files))

    if not files:
        print("⚠️ 没有找到匹配的文件")
        return

    print(f"📂 目录: {dir_path}")
    print(f"📝 文件: {len(files)} 个")
    print(f"🎯 目标编码: {target}")
    if dry_run:
        print("🔍 预览模式")
    print("-" * 50)

    converted = 0
    for f in files:
        if convert_encoding(str(f), target, dry_run):
            converted += 1

    print("-" * 50)
    action = "将转换" if dry_run else "已转换"
    print(f"📊 {action} {converted} 个文件")


def detect_all(directory: str, extensions: list = None):
    """检测目录下所有文件的编码"""
    dir_path = Path(directory)
    if extensions is None:
        extensions = [".txt", ".md", ".csv", ".json", ".py", ".c", ".cpp", ".h"]

    files = []
    for ext in extensions:
        files.extend(dir_path.rglob(f"*{ext}"))
    files = sorted(set(files))

    if not files:
        print("⚠️ 没有找到匹配的文件")
        return

    print(f"📂 目录: {dir_path}")
    print(f"📝 文件: {len(files)} 个\n")
    print(f"{'文件名':<40} {'编码':<15}")
    print("-" * 55)

    for f in files:
        enc = detect_encoding(str(f))
        print(f"  {f.name:<38} {enc}")


def main():
    parser = argparse.ArgumentParser(
        description="文件编码转换工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python encoding_converter.py --detect *.txt
  python encoding_converter.py --to utf-8 *.txt
  python encoding_converter.py --to utf-8 --recursive ./课件/
  python encoding_converter.py --to utf-8 --dry-run *.txt
        """,
    )
    parser.add_argument("files", nargs="*", help="目标文件或目录")
    parser.add_argument("--detect", action="store_true", help="只检测编码（不转换）")
    parser.add_argument("--to", help="目标编码（如 utf-8, gbk）")
    parser.add_argument("--recursive", action="store_true", help="递归子目录")
    parser.add_argument("--ext", nargs="+", help="文件扩展名过滤")
    parser.add_argument("--dry-run", action="store_true", help="预览模式")

    args = parser.parse_args()

    if not args.files:
        parser.print_help()
        return

    if args.detect:
        for f in args.files:
            p = Path(f)
            if p.is_dir():
                detect_all(str(p), args.ext)
            else:
                enc = detect_encoding(f)
                print(f"{p.name:<40} {enc}")
    elif args.to:
        for f in args.files:
            p = Path(f)
            if p.is_dir():
                batch_convert(str(p), args.to, args.recursive, args.ext, args.dry_run)
            else:
                convert_encoding(f, args.to, args.dry_run)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
