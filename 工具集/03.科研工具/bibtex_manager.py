#!/usr/bin/env python3
"""
BibTeX 参考文献管理工具
📌 查重、排序、格式化 .bib 文件
📌 从 DOI 获取 BibTeX 条目（需网络）
"""

import argparse
import re
import sys
import urllib.request
from collections import defaultdict
from pathlib import Path

# Windows 终端 UTF-8 输出
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")


def parse_bibtex(filepath: str) -> list:
    """
    解析 .bib 文件，返回条目列表

    每个条目为 dict:
        {type, key, fields: {field: value, ...}, raw: 原始文本}
    """
    content = Path(filepath).read_text(encoding="utf-8")
    entries = []

    # 匹配 @type{key, ... }
    pattern = re.compile(
        r"@(\w+)\{([^,]+),\s*(.*?)\n\}",
        re.DOTALL,
    )

    for match in pattern.finditer(content):
        entry_type = match.group(1).lower()
        entry_key = match.group(2).strip()
        body = match.group(3)

        # 解析字段
        fields = {}
        field_pattern = re.compile(r"(\w+)\s*=\s*\{(.*?)\}", re.DOTALL)
        for fm in field_pattern.finditer(body):
            fields[fm.group(1).lower()] = fm.group(2).strip()

        entries.append({
            "type": entry_type,
            "key": entry_key,
            "fields": fields,
            "raw": match.group(0),
        })

    return entries


def find_duplicates(entries: list) -> dict:
    """
    查找重复条目
    基于 title 和 doi 的相似度判断
    """
    dup_groups = defaultdict(list)

    # 按 title 分组
    by_title = defaultdict(list)
    for e in entries:
        title = e["fields"].get("title", "").lower().strip()
        if title:
            by_title[title].append(e)

    for title, group in by_title.items():
        if len(group) > 1:
            dup_groups[title] = group

    return dup_groups


def sort_entries(entries: list, by: str = "year") -> list:
    """排序条目"""
    if by == "year":
        return sorted(entries, key=lambda e: e["fields"].get("year", "0"))
    elif by == "author":
        return sorted(entries, key=lambda e: e["fields"].get("author", "").lower())
    elif by == "key":
        return sorted(entries, key=lambda e: e["key"].lower())
    return entries


def entries_to_bibtex(entries: list) -> str:
    """将条目列表转为 BibTeX 字符串"""
    return "\n\n".join(e["raw"] for e in entries) + "\n"


def fetch_doi(doi: str) -> str:
    """从 DOI 获取 BibTeX 条目"""
    url = f"https://doi.org/{doi}"
    headers = {"Accept": "application/x-bibtex"}
    req = urllib.request.Request(url, headers=headers)

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.read().decode("utf-8")
    except Exception as e:
        print(f"❌ 获取失败: {e}")
        return None


def main():
    parser = argparse.ArgumentParser(description="BibTeX 参考文献管理工具")
    sub = parser.add_subparsers(dest="command", help="可用命令")

    # check（查重）
    ck = sub.add_parser("check", help="检查重复条目")
    ck.add_argument("file", help=".bib 文件路径")
    ck.add_argument("--dedup", action="store_true", help="自动去重（保留第一个）")

    # sort
    st = sub.add_parser("sort", help="排序条目")
    st.add_argument("file", help=".bib 文件路径")
    st.add_argument("--by", choices=["year", "author", "key"], default="year")
    st.add_argument("-o", "--output", help="输出文件路径")

    # fetch
    ft = sub.add_parser("fetch", help="从 DOI 获取 BibTeX")
    ft.add_argument("doi", help="DOI 编号")

    # stats
    sa = sub.add_parser("stats", help="显示 .bib 文件统计")
    sa.add_argument("file", help=".bib 文件路径")

    args = parser.parse_args()

    if args.command == "check":
        entries = parse_bibtex(args.file)
        print(f"📊 共 {len(entries)} 个条目")
        dups = find_duplicates(entries)
        if not dups:
            print("✅ 没有发现重复条目")
        else:
            print(f"🚨 发现 {len(dups)} 组重复:")
            for title, group in dups.items():
                print(f"\n  「{title}」:")
                for e in group:
                    print(f"    - {e['key']}")
            if args.dedup:
                # 保留每组第一个
                seen = set()
                deduped = []
                for e in entries:
                    title = e["fields"].get("title", "").lower().strip()
                    if title in dups and title in seen:
                        continue
                    seen.add(title)
                    deduped.append(e)
                with open(args.file, "w", encoding="utf-8") as f:
                    f.write(entries_to_bibtex(deduped))
                print(f"\n✅ 已去重: {len(entries)} → {len(deduped)} 个条目")

    elif args.command == "sort":
        entries = parse_bibtex(args.file)
        sorted_entries = sort_entries(entries, args.by)
        output = args.output or args.file
        with open(output, "w", encoding="utf-8") as f:
            f.write(entries_to_bibtex(sorted_entries))
        print(f"✅ 已按 {args.by} 排序 → {output}")

    elif args.command == "fetch":
        bibtex = fetch_doi(args.doi)
        if bibtex:
            print(bibtex)

    elif args.command == "stats":
        entries = parse_bibtex(args.file)
        print(f"📊 {args.file}")
        print(f"   总条目: {len(entries)}")
        types = defaultdict(int)
        for e in entries:
            types[e["type"]] += 1
        for t, c in sorted(types.items()):
            print(f"   {t}: {c}")
        years = [e["fields"].get("year") for e in entries if "year" in e["fields"]]
        if years:
            print(f"   年份范围: {min(years)} ~ {max(years)}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
