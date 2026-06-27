#!/usr/bin/env python3
"""
Obsidian 链接检查工具
📌 扫描 vault 中的断链和孤岛笔记，生成健康报告
📌 支持自动修复常见断链（大小写、空格差异）
"""

import argparse
import os
import re
import sys
from collections import defaultdict
from pathlib import Path

# Windows 终端 UTF-8 输出
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")


def scan_vault(vault_path: str, ignore_dirs: list = None) -> dict:
    """
    扫描 Obsidian vault

    返回:
        {
            "files": {文件名(不含扩展名): [完整路径, ...]},
            "links": {源文件: [链接目标, ...]},
            "wikilinks": {源文件: [(链接文本, 别名), ...]},
        }
    """
    vault = Path(vault_path)
    ignore_dirs = ignore_dirs or [".obsidian", ".git", ".claude", "node_modules"]

    # 收集所有 .md 文件
    files = defaultdict(list)
    for md in vault.rglob("*.md"):
        # 跳过忽略的目录
        rel = md.relative_to(vault)
        if any(part in ignore_dirs for part in rel.parts):
            continue
        stem = md.stem
        files[stem].append(str(md))

    # 提取 wikilinks
    wikilink_pattern = re.compile(r"\[\[([^\]|]+?)(?:\|([^\]]+?))?\]\]")
    links = {}
    wikilinks = {}

    for md in vault.rglob("*.md"):
        rel = md.relative_to(vault)
        if any(part in ignore_dirs for part in rel.parts):
            continue

        try:
            content = md.read_text(encoding="utf-8")
        except Exception:
            continue

        found_links = []
        found_wikilinks = []
        for match in wikilink_pattern.finditer(content):
            target = match.group(1).strip()
            alias = match.group(2)
            # 跳过图片链接
            if target.endswith((".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".pdf")):
                continue
            # 跳过嵌入链接
            if match.group(0).startswith("![["):
                continue
            found_links.append(target)
            found_wikilinks.append((target, alias))

        if found_links:
            links[str(rel)] = found_links
        if found_wikilinks:
            wikilinks[str(rel)] = found_wikilinks

    return {"files": files, "links": links, "wikilinks": wikilinks}


def find_broken_links(vault_data: dict) -> list:
    """查找断链"""
    files = vault_data["files"]
    broken = []

    for source, targets in vault_data["links"].items():
        for target in targets:
            # 处理带锚点的链接
            clean_target = target.split("#")[0].strip()
            if not clean_target:
                continue

            # 检查是否存在
            if clean_target not in files:
                broken.append({
                    "source": source,
                    "target": target,
                    "clean_target": clean_target,
                })

    return broken


def find_orphan_notes(vault_data: dict) -> list:
    """查找孤岛笔记（没有被任何其他笔记链接到）"""
    # 收集所有被链接到的目标
    linked_targets = set()
    for targets in vault_data["links"].values():
        for t in targets:
            clean = t.split("#")[0].strip()
            if clean:
                linked_targets.add(clean)

    # 找出没有被链接到的文件
    orphans = []
    for stem, paths in vault_data["files"].items():
        if stem not in linked_targets:
            # 检查它是否有出链
            has_outgoing = any(
                stem == Path(src).stem
                for src in vault_data["links"]
            )
            orphans.append({
                "stem": stem,
                "paths": paths,
                "has_outgoing": has_outgoing,
            })

    return orphans


def suggest_fix(target: str, files: dict) -> str:
    """尝试修复断链（大小写、空格差异）"""
    target_lower = target.lower().strip()

    for stem in files:
        if stem.lower().strip() == target_lower:
            return stem

    # 部分匹配
    for stem in files:
        if target_lower in stem.lower() or stem.lower() in target_lower:
            return stem

    return None


def auto_fix_links(vault_path: str, broken: list, files: dict, dry_run: bool = True) -> int:
    """自动修复断链"""
    fixed = 0
    for item in broken:
        suggestion = suggest_fix(item["clean_target"], files)
        if not suggestion:
            continue

        source_path = Path(vault_path) / item["source"]
        try:
            content = source_path.read_text(encoding="utf-8")
        except Exception:
            continue

        old_link = f"[[{item['target']}]]"
        new_link = f"[[{suggestion}]]"

        if old_link in content:
            if dry_run:
                print(f"  🔧 {item['source']}: {old_link} → {new_link}")
            else:
                content = content.replace(old_link, new_link)
                source_path.write_text(content, encoding="utf-8")
                print(f"  ✅ {item['source']}: {old_link} → {new_link}")
            fixed += 1

    return fixed


def print_report(broken: list, orphans: list, total_files: int, fmt: str = "text"):
    """输出报告"""
    if fmt == "md":
        print("# Obsidian 链接检查报告\n")
        print(f"扫描笔记数: {total_files}\n")

        print(f"## 断链（{len(broken)} 条）\n")
        if broken:
            print("| 来源文件 | 断链目标 |")
            print("|----------|----------|")
            for b in broken:
                print(f"| {b['source']} | `[[{b['target']}]]` |")
        else:
            print("✅ 无断链\n")

        print(f"\n## 孤岛笔记（{len(orphans)} 篇）\n")
        if orphans:
            print("| 笔记 | 有出链 |")
            print("|------|--------|")
            for o in orphans:
                has = "是" if o["has_outgoing"] else "否"
                print(f"| {o['stem']} | {has} |")
    else:
        print(f"\n{'='*50}")
        print(f"📋 Obsidian 链接检查报告")
        print(f"{'='*50}")
        print(f"扫描笔记: {total_files}")

        print(f"\n🔗 断链: {len(broken)} 条")
        for b in broken[:20]:
            print(f"   {b['source']}")
            print(f"     → [[{b['target']}]]")
        if len(broken) > 20:
            print(f"   ... 还有 {len(broken) - 20} 条")

        print(f"\n🏝️ 孤岛笔记: {len(orphans)} 篇")
        for o in orphans[:20]:
            out = "有出链" if o["has_outgoing"] else "无出链"
            print(f"   {o['stem']} ({out})")
        if len(orphans) > 20:
            print(f"   ... 还有 {len(orphans) - 20} 篇")


def main():
    parser = argparse.ArgumentParser(
        description="Obsidian 链接检查工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python obsidian_link_checker.py /path/to/vault
  python obsidian_link_checker.py /path/to/vault --broken-only
  python obsidian_link_checker.py /path/to/vault --auto-fix --dry-run
        """,
    )
    parser.add_argument("vault", help="Obsidian vault 路径")
    parser.add_argument("--broken-only", action="store_true", help="只检查断链")
    parser.add_argument("--auto-fix", action="store_true", help="自动修复断链")
    parser.add_argument("--dry-run", action="store_true", help="预览修复（不实际修改）")
    parser.add_argument("--format", choices=["text", "md"], default="text", help="输出格式")
    parser.add_argument("-o", "--output", help="输出到文件")

    args = parser.parse_args()

    print(f"🔍 扫描 vault: {args.vault}")
    vault_data = scan_vault(args.vault)
    total_files = len(vault_data["files"])
    print(f"   找到 {total_files} 个 .md 文件")

    broken = find_broken_links(vault_data)
    orphans = find_orphan_notes(vault_data) if not args.broken_only else []

    if args.auto_fix:
        print(f"\n🔧 自动修复断链:")
        fixed = auto_fix_links(args.vault, broken, vault_data["files"], args.dry_run)
        action = "将修复" if args.dry_run else "已修复"
        print(f"\n📊 {action} {fixed} 条断链")
    elif args.output:
        import io
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        print_report(broken, orphans, total_files, args.format)
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"✅ 报告已保存: {args.output}")
    else:
        print_report(broken, orphans, total_files, args.format)


if __name__ == "__main__":
    main()
