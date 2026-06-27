#!/usr/bin/env python3
"""
Anki 闪卡生成器
📌 从 Markdown 笔记中提取 Q/A 对，生成 Anki 可导入的制表符分隔文件
📌 支持多种提取模式：标题分隔、marker 过滤、Callout 语法
"""

import argparse
import re
import sys
from pathlib import Path

# Windows 终端 UTF-8 输出
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")


def extract_by_headings(content: str, min_level: int = 2, max_level: int = 3):
    """
    按 Markdown 标题层级提取 Q/A 对
    - Q = 标题行
    - A = 标题下方的内容（直到下一个同级或更高级标题）
    """
    lines = content.split("\n")
    cards = []
    current_question = None
    current_answer = []

    for line in lines:
        heading_match = re.match(r"^(#{1,6})\s+(.+)", line)
        if heading_match:
            level = len(heading_match.group(1))
            title = heading_match.group(2).strip()

            # 跳过太深或太浅的标题
            if level < min_level or level > max_level:
                if current_question:
                    current_answer.append(line)
                continue

            # 保存上一张卡片
            if current_question and current_answer:
                answer = "\n".join(current_answer).strip()
                if answer:
                    cards.append((current_question, answer))

            current_question = title
            current_answer = []
        elif current_question:
            current_answer.append(line)

    # 保存最后一张
    if current_question and current_answer:
        answer = "\n".join(current_answer).strip()
        if answer:
            cards.append((current_question, answer))

    return cards


def extract_by_marker(content: str, marker: str = "📌"):
    """
    按 marker 符号提取知识点
    - Q = marker 所在行的内容
    - A = 紧跟其后的内容（直到下一个 marker 或空行段落结束）
    """
    lines = content.split("\n")
    cards = []
    current_question = None
    current_answer = []

    for line in lines:
        if marker in line:
            # 保存上一张
            if current_question and current_answer:
                answer = "\n".join(current_answer).strip()
                if answer:
                    cards.append((current_question, answer))

            # 提取 marker 后的文字作为问题
            question = line.replace(marker, "").strip().strip(":：")
            current_question = question
            current_answer = []
        elif current_question:
            # 空行且已有内容 → 段落结束
            if line.strip() == "" and current_answer:
                # 检查下一行是否还是内容（连续空行才结束）
                pass
            current_answer.append(line)

    # 保存最后一张
    if current_question and current_answer:
        answer = "\n".join(current_answer).strip()
        if answer:
            cards.append((current_question, answer))

    return cards


def extract_by_callout(content: str, callout_type: str = "tip"):
    """
    从 Obsidian Callout 语法中提取 Q/A
    - Q = Callout 标题
    - A = Callout 内容
    """
    pattern = re.compile(
        rf">\s*\[!{callout_type}\]\s*(.*)\n((?:>.*\n)*)",
        re.IGNORECASE,
    )
    cards = []
    for match in pattern.finditer(content):
        title = match.group(1).strip()
        body = match.group(2).strip()
        # 去掉行首的 >
        body = re.sub(r"^>\s?", "", body, flags=re.MULTILINE).strip()
        if title and body:
            cards.append((title, body))
    return cards


def sanitize(text: str) -> str:
    """清理文本，移除可能干扰 Anki 导入的字符"""
    # 移除内部链接 [[]]
    text = re.sub(r"\[\[([^\]]+)\]\]", r"\1", text)
    # 移除图片链接
    text = re.sub(r"!\[\[.*?\]\]", "", text)
    # 移除 HTML 标签
    text = re.sub(r"<[^>]+>", "", text)
    # 压缩多余空白
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def generate_anki_file(cards: list, output: str, separator: str = "tab"):
    """生成 Anki 可导入的文件"""
    if not cards:
        print("⚠️ 没有提取到任何卡片")
        return

    sep = "\t" if separator == "tab" else separator

    with open(output, "w", encoding="utf-8") as f:
        for question, answer in cards:
            q = sanitize(question).replace("\n", "<br>")
            a = sanitize(answer).replace("\n", "<br>")
            f.write(f"{q}{sep}{a}\n")

    print(f"✅ 已生成 {len(cards)} 张卡片 → {output}")
    print(f"💡 导入方式: Anki → 文件 → 导入 → 选择 {output}")


def main():
    parser = argparse.ArgumentParser(
        description="从 Markdown 笔记生成 Anki 闪卡",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python anki_card_generator.py 笔记.md -o 卡片.txt
  python anki_card_generator.py 笔记.md --mode marker --marker "📌" -o 重点.txt
  python anki_card_generator.py 笔记.md --mode callout -o callout卡片.txt
        """,
    )
    parser.add_argument("input", help="输入的 Markdown 文件")
    parser.add_argument("-o", "--output", default="anki_cards.txt", help="输出文件路径")
    parser.add_argument(
        "--mode", choices=["heading", "marker", "callout"], default="heading",
        help="提取模式: heading(按标题) | marker(按标记) | callout(按Callout)"
    )
    parser.add_argument("--marker", default="📌", help="marker 符号（默认 📌）")
    parser.add_argument("--min-level", type=int, default=2, help="标题最小层级（heading 模式）")
    parser.add_argument("--max-level", type=int, default=3, help="标题最大层级（heading 模式）")
    parser.add_argument("--separator", default="tab", help="Q/A 分隔符（默认 tab）")

    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.is_file():
        print(f"❌ 文件不存在: {args.input}")
        sys.exit(1)

    content = input_path.read_text(encoding="utf-8")

    if args.mode == "heading":
        cards = extract_by_headings(content, args.min_level, args.max_level)
    elif args.mode == "marker":
        cards = extract_by_marker(content, args.marker)
    elif args.mode == "callout":
        cards = extract_by_callout(content)

    generate_anki_file(cards, args.output, args.separator)


if __name__ == "__main__":
    main()
