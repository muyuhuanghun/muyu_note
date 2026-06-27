#!/usr/bin/env python3
"""
密码生成与强度检测工具
📌 生成安全密码、评估密码强度、支持易记忆模式
"""

import argparse
import math
import random
import re
import string
import sys

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

# 易记忆单词库
WORDS = [
    "apple", "banana", "cherry", "dragon", "eagle", "falcon", "grape",
    "harbor", "island", "jungle", "knight", "lemon", "mango", "noble",
    "ocean", "pearl", "queen", "river", "storm", "tiger", "ultra",
    "vivid", "wolf", "xenon", "yield", "zenith", "amber", "blaze",
    "coral", "delta", "ember", "frost", "glow", "haze", "ivory",
    "jade", "karma", "lunar", "mist", "nova", "orbit", "pixel",
    "quartz", "ridge", "spark", "torch", "unity", "vault", "wave",
    "axiom", "brisk", "cedar", "drift", "flint", "grove", "helix",
]


def generate_password(length: int = 16, no_symbols: bool = False) -> str:
    """生成随机密码"""
    chars = string.ascii_letters + string.digits
    if not no_symbols:
        chars += "!@#$%^&*"
    return "".join(random.choices(chars, k=length))


def generate_memorable(word_count: int = 4, separator: str = "-") -> str:
    """生成易记忆密码（单词组合）"""
    words = random.sample(WORDS, word_count)
    # 首字母大写，加一个数字和特殊字符
    words = [w.capitalize() for w in words]
    num = random.randint(10, 99)
    symbol = random.choice("!@#$%&")
    return separator.join(words) + str(num) + symbol


def check_strength(password: str) -> dict:
    """
    检测密码强度

    返回:
        {score, level, feedback, entropy}
    """
    score = 0
    feedback = []

    # 长度
    length = len(password)
    if length >= 8:
        score += 1
    if length >= 12:
        score += 1
    if length >= 16:
        score += 1
    if length < 8:
        feedback.append("⚠️ 长度不足 8 位")

    # 字符类型
    has_lower = bool(re.search(r"[a-z]", password))
    has_upper = bool(re.search(r"[A-Z]", password))
    has_digit = bool(re.search(r"\d", password))
    has_symbol = bool(re.search(r"[^a-zA-Z0-9]", password))

    types = sum([has_lower, has_upper, has_digit, has_symbol])
    score += types
    if not has_lower:
        feedback.append("💡 建议添加小写字母")
    if not has_upper:
        feedback.append("💡 建议添加大写字母")
    if not has_digit:
        feedback.append("💡 建议添加数字")
    if not has_symbol:
        feedback.append("💡 建议添加特殊字符")

    # 重复字符
    if re.search(r"(.)\1{2,}", password):
        score -= 1
        feedback.append("⚠️ 包含连续重复字符")

    # 常见模式
    common_patterns = ["123456", "qwerty", "password", "abc123", "admin"]
    for pattern in common_patterns:
        if pattern in password.lower():
            score -= 2
            feedback.append(f"⚠️ 包含常见弱密码模式: {pattern}")

    # 计算熵
    charset_size = 0
    if has_lower: charset_size += 26
    if has_upper: charset_size += 26
    if has_digit: charset_size += 10
    if has_symbol: charset_size += 32
    entropy = length * math.log2(charset_size) if charset_size > 0 else 0

    # 评级
    score = max(0, min(score, 7))
    if score <= 2:
        level = "🔴 弱"
    elif score <= 4:
        level = "🟡 中"
    elif score <= 6:
        level = "🟢 强"
    else:
        level = "🟢 非常强"

    return {
        "score": score,
        "level": level,
        "feedback": feedback,
        "entropy": round(entropy, 1),
    }


def main():
    parser = argparse.ArgumentParser(
        description="密码生成与强度检测工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python password_gen.py
  python password_gen.py --length 32 --count 5
  python password_gen.py --check "MyP@ssw0rd!"
  python password_gen.py --memorable --count 3
        """,
    )
    parser.add_argument("--length", type=int, default=16, help="密码长度（默认 16）")
    parser.add_argument("--count", type=int, default=1, help="生成数量（默认 1）")
    parser.add_argument("--no-symbols", action="store_true", help="不包含特殊字符")
    parser.add_argument("--memorable", action="store_true", help="生成易记忆密码")
    parser.add_argument("--words", type=int, default=4, help="易记忆模式的单词数（默认 4）")
    parser.add_argument("--check", help="检测指定密码的强度")

    args = parser.parse_args()

    if args.check:
        result = check_strength(args.check)
        print(f"🔑 密码强度检测")
        print(f"   密码: {'*' * len(args.check)}")
        print(f"   强度: {result['level']}（{result['score']}/7）")
        print(f"   熵值: {result['entropy']} bits")
        if result["feedback"]:
            print(f"   建议:")
            for f in result["feedback"]:
                print(f"     {f}")
    elif args.memorable:
        print(f"🔑 易记忆密码:")
        for i in range(args.count):
            pwd = generate_memorable(args.words)
            strength = check_strength(pwd)
            print(f"   {pwd:<40} {strength['level']}")
    else:
        print(f"🔑 随机密码:")
        for i in range(args.count):
            pwd = generate_password(args.length, args.no_symbols)
            strength = check_strength(pwd)
            print(f"   {pwd:<40} {strength['level']}")


if __name__ == "__main__":
    main()
