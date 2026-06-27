#!/usr/bin/env python3
"""
论文管理工具
📌 下载 arXiv 论文、批量重命名 PDF、按结构化格式归档
"""

import argparse
import os
import re
import sys
import urllib.request
from pathlib import Path

# Windows 终端 UTF-8 输出
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")


def download_arxiv(arxiv_id: str, output_dir: str = "."):
    """
    从 arXiv 下载 PDF

    参数:
        arxiv_id: arXiv ID，如 2301.07041
        output_dir: 保存目录
    """
    # 标准化 ID（去掉版本号）
    clean_id = re.sub(r"v\d+$", "", arxiv_id.strip())
    url = f"https://arxiv.org/pdf/{clean_id}.pdf"

    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    filename = out_path / f"{clean_id.replace('/', '_')}.pdf"

    print(f"📥 正在下载: {url}")
    try:
        urllib.request.urlretrieve(url, str(filename))
        print(f"✅ 已保存: {filename}")
        return filename
    except Exception as e:
        print(f"❌ 下载失败: {e}")
        return None


def rename_papers(directory: str, fmt: str = "{id}", dry_run: bool = False):
    """
    批量重命名 PDF 文件

    参数:
        directory: PDF 所在目录
        fmt: 命名格式，支持 {id}, {year}, {title} 占位符
        dry_run: 预览模式
    """
    dir_path = Path(directory)
    if not dir_path.is_dir():
        print(f"❌ 目录不存在: {directory}")
        sys.exit(1)

    pdfs = sorted(dir_path.glob("*.pdf"))
    if not pdfs:
        print("⚠️ 没有找到 PDF 文件")
        return

    print(f"📂 目录: {dir_path}")
    print(f"📝 PDF 文件: {len(pdfs)} 个")
    if dry_run:
        print("🔍 预览模式")
    print("-" * 60)

    for pdf in pdfs:
        old_name = pdf.stem
        # 尝试从文件名解析信息
        info = {
            "id": old_name,
            "year": "unknown",
            "title": old_name,
        }

        # 尝试匹配 arXiv ID 格式
        arxiv_match = re.match(r"(\d{4}\.\d{4,5})", old_name)
        if arxiv_match:
            info["id"] = arxiv_match.group(1)
            info["year"] = "20" + info["id"][:2]

        new_name = fmt.format(**info) + ".pdf"
        new_path = pdf.parent / new_name

        if pdf.name == new_name:
            continue

        if dry_run:
            print(f"  {pdf.name}  →  {new_name}")
        else:
            if new_path.exists():
                print(f"  ⚠️ 冲突跳过: {pdf.name}")
                continue
            pdf.rename(new_path)
            print(f"  ✅ {pdf.name}  →  {new_name}")


def list_papers(directory: str):
    """列出目录中的所有论文"""
    dir_path = Path(directory)
    if not dir_path.is_dir():
        print(f"❌ 目录不存在: {directory}")
        sys.exit(1)

    pdfs = sorted(dir_path.glob("*.pdf"))
    if not pdfs:
        print("📭 目录中没有 PDF 文件")
        return

    print(f"📂 {dir_path} — {len(pdfs)} 篇论文\n")
    for i, pdf in enumerate(pdfs, 1):
        size_mb = pdf.stat().st_size / 1024 / 1024
        print(f"  {i:>3}. {pdf.name:<50} ({size_mb:.1f} MB)")


def main():
    parser = argparse.ArgumentParser(description="论文管理工具")
    sub = parser.add_subparsers(dest="command", help="可用命令")

    # download
    dl = sub.add_parser("download", help="从 arXiv 下载论文")
    dl.add_argument("arxiv_id", help="arXiv ID（如 2301.07041）")
    dl.add_argument("--dir", default=".", help="保存目录")

    # rename
    rn = sub.add_parser("rename", help="批量重命名 PDF")
    rn.add_argument("directory", help="PDF 所在目录")
    rn.add_argument("--format", default="{id}", dest="fmt", help="命名格式（如 {author}_{year}_{title}）")
    rn.add_argument("--dry-run", action="store_true")

    # list
    ls = sub.add_parser("list", help="列出论文")
    ls.add_argument("directory", help="PDF 所在目录")

    args = parser.parse_args()

    if args.command == "download":
        download_arxiv(args.arxiv_id, args.dir)
    elif args.command == "rename":
        rename_papers(args.directory, args.fmt, args.dry_run)
    elif args.command == "list":
        list_papers(args.directory)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
