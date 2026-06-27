#!/usr/bin/env python3
"""
仓库分析工具
📌 分析 Git 仓库结构、贡献者统计、代码行数
"""

import argparse
import os
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

# Windows 终端 UTF-8 输出
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")


def run_git(repo_path: str, *args) -> str:
    """在指定仓库执行 git 命令"""
    try:
        result = subprocess.run(
            ["git", "-c", "core.quotepath=false"] + list(args),
            capture_output=True, text=True, encoding="utf-8",
            cwd=repo_path,
        )
        return result.stdout.strip()
    except Exception:
        return ""


def analyze_structure(repo_path: str) -> dict:
    """分析仓库文件结构"""
    files = run_git(repo_path, "ls-files").split("\n")
    files = [f for f in files if f]

    # 按扩展名统计
    by_ext = defaultdict(int)
    by_dir = defaultdict(int)
    total_size = 0

    for f in files:
        ext = Path(f).suffix or "(无扩展名)"
        by_ext[ext] += 1

        top_dir = f.split("/")[0] if "/" in f else "(根目录)"
        by_dir[top_dir] += 1

        full_path = Path(repo_path) / f
        if full_path.exists():
            total_size += full_path.stat().st_size

    return {
        "total_files": len(files),
        "total_size": total_size,
        "by_ext": dict(sorted(by_ext.items(), key=lambda x: -x[1])),
        "by_dir": dict(sorted(by_dir.items(), key=lambda x: -x[1])),
    }


def analyze_contributors(repo_path: str) -> list:
    """分析贡献者统计"""
    log = run_git(repo_path, "log", "--format=%aN|%aE")
    if not log:
        return []

    contributors = defaultdict(int)
    for line in log.split("\n"):
        if "|" in line:
            name, email = line.split("|", 1)
            contributors[name] += 1

    return sorted(contributors.items(), key=lambda x: -x[1])


def count_loc(repo_path: str, by_type: bool = False) -> dict:
    """统计代码行数"""
    files = run_git(repo_path, "ls-files").split("\n")
    files = [f for f in files if f]

    # 代码文件扩展名
    code_exts = {
        ".py", ".c", ".cpp", ".h", ".hpp", ".java", ".js", ".ts",
        ".html", ".css", ".sh", ".bash", ".rs", ".go", ".rb",
        ".md", ".txt", ".json", ".yaml", ".yml", ".toml",
    }

    loc_by_type = defaultdict(int)
    total_loc = 0

    for f in files:
        ext = Path(f).suffix.lower()
        if by_type and ext not in code_exts:
            continue

        full_path = Path(repo_path) / f
        if not full_path.exists():
            continue

        try:
            with open(full_path, "r", encoding="utf-8", errors="ignore") as fh:
                lines = len(fh.readlines())
                loc_by_type[ext] += lines
                total_loc += lines
        except Exception:
            pass

    return {
        "total_loc": total_loc,
        "by_type": dict(sorted(loc_by_type.items(), key=lambda x: -x[1])),
    }


def print_report(structure: dict, contributors: list, loc: dict, fmt: str = "text"):
    """输出分析报告"""
    if fmt == "md":
        print("# 仓库分析报告\n")
        print(f"## 文件概览\n")
        print(f"- 总文件数: {structure['total_files']}")
        print(f"- 仓库大小: {structure['total_size'] / 1024 / 1024:.2f} MB")
        print(f"- 总代码行: {loc['total_loc']}\n")

        print("## 文件类型分布\n")
        print("| 扩展名 | 数量 |")
        print("|--------|------|")
        for ext, count in list(structure["by_ext"].items())[:15]:
            print(f"| {ext} | {count} |")

        print("\n## 目录结构\n")
        print("| 目录 | 文件数 |")
        print("|------|--------|")
        for d, count in list(structure["by_dir"].items())[:15]:
            print(f"| {d} | {count} |")

        if contributors:
            print("\n## 贡献者\n")
            print("| 贡献者 | 提交数 |")
            print("|--------|--------|")
            for name, count in contributors:
                print(f"| {name} | {count} |")
    else:
        print(f"\n{'='*50}")
        print(f"📊 仓库分析报告")
        print(f"{'='*50}")

        print(f"\n📁 文件概览:")
        print(f"   总文件数: {structure['total_files']}")
        print(f"   仓库大小: {structure['total_size'] / 1024 / 1024:.2f} MB")
        print(f"   总代码行: {loc['total_loc']}")

        print(f"\n📋 文件类型 Top 10:")
        for ext, count in list(structure["by_ext"].items())[:10]:
            bar = "█" * min(count, 30)
            print(f"   {ext:<12} {count:>4}  {bar}")

        print(f"\n📂 目录文件数 Top 10:")
        for d, count in list(structure["by_dir"].items())[:10]:
            bar = "█" * min(count, 30)
            print(f"   {d:<20} {count:>4}  {bar}")

        if contributors:
            print(f"\n👥 贡献者:")
            for name, count in contributors[:10]:
                bar = "█" * min(count, 30)
                print(f"   {name:<20} {count:>4}  {bar}")


def main():
    parser = argparse.ArgumentParser(description="仓库分析工具")
    parser.add_argument("repo", nargs="?", default=".", help="仓库路径（默认当前目录）")
    parser.add_argument("--contributors", action="store_true", help="显示贡献者统计")
    parser.add_argument("--loc-by-type", action="store_true", help="按文件类型统计代码行数")
    parser.add_argument("--format", choices=["text", "md"], default="text", help="输出格式")
    parser.add_argument("-o", "--output", help="输出到文件")

    args = parser.parse_args()

    structure = analyze_structure(args.repo)
    contributors = analyze_contributors(args.repo) if args.contributors else []
    loc = count_loc(args.repo, by_type=args.loc_by_type)

    if args.output:
        import io
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        print_report(structure, contributors, loc, args.format)
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"✅ 报告已保存: {args.output}")
    else:
        print_report(structure, contributors, loc, args.format)


if __name__ == "__main__":
    main()
