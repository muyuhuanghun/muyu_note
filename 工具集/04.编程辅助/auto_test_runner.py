#!/usr/bin/env python3
"""
自动测试运行器
📌 批量运行测试用例、对拍两个程序、生成随机测试数据
"""

import argparse
import os
import random
import subprocess
import sys
import time
from pathlib import Path

# Windows 终端 UTF-8 输出
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")


def run_program(program: str, input_data: str, timeout: int = 5) -> tuple:
    """
    运行程序并返回 (输出, 用时, 错误)

    参数:
        program: 程序路径或命令
        input_data: 输入数据字符串
        timeout: 超时秒数
    """
    try:
        start = time.time()
        result = subprocess.run(
            program,
            input=input_data,
            capture_output=True,
            text=True,
            timeout=timeout,
            shell=True,
        )
        elapsed = time.time() - start
        return (result.stdout.strip(), elapsed, result.stderr.strip() if result.returncode != 0 else None)
    except subprocess.TimeoutExpired:
        return (None, timeout, "TIMEOUT")
    except Exception as e:
        return (None, 0, str(e))


def compare_outputs(out1: str, out2: str, ignore_ws: bool = True) -> bool:
    """比较两个输出是否一致"""
    if ignore_ws:
        return out1.split() == out2.split()
    return out1 == out2


def adversarial_test(prog1: str, prog2: str, generator: str, num_cases: int = 100, timeout: int = 5):
    """
    对拍：用随机数据对比两个程序的输出

    参数:
        prog1: 待测程序
        prog2: 暴力/参考程序
        generator: 数据生成器程序（输出随机测试数据到 stdout）
        num_cases: 测试轮数
        timeout: 超时秒数
    """
    print(f"⚔️  对拍模式")
    print(f"   待测: {prog1}")
    print(f"   参考: {prog2}")
    print(f"   生成器: {generator}")
    print(f"   轮数: {num_cases}")
    print("-" * 60)

    passed = 0
    failed = 0

    for i in range(1, num_cases + 1):
        # 生成测试数据
        gen_out, _, gen_err = run_program(generator, "", timeout=timeout)
        if gen_err:
            print(f"  ❌ 第 {i} 轮: 生成器错误 — {gen_err}")
            continue

        test_input = gen_out

        # 运行两个程序
        out1, t1, err1 = run_program(prog1, test_input, timeout=timeout)
        out2, t2, err2 = run_program(prog2, test_input, timeout=timeout)

        if err1:
            print(f"  ❌ 第 {i} 轮: 待测程序错误 — {err1}")
            failed += 1
            continue

        if err2:
            print(f"  ⚠️ 第 {i} 轮: 参考程序错误 — {err2}，跳过")
            continue

        if compare_outputs(out1, out2):
            passed += 1
            if i % 10 == 0:
                print(f"  ✅ {i}/{num_cases} 轮通过")
        else:
            failed += 1
            print(f"\n  ❌ 第 {i} 轮 FAIL!")
            print(f"     输入:\n{test_input[:200]}")
            print(f"     待测输出: {out1[:100]}")
            print(f"     参考输出: {out2[:100]}")
            print(f"     用时: 待测 {t1:.3f}s / 参考 {t2:.3f}s")
            break

    print("-" * 60)
    print(f"📊 结果: {passed} 通过, {failed} 失败")


def batch_test(program: str, input_dir: str, output_dir: str, timeout: int = 5):
    """
    批量运行测试用例

    参数:
        program: 待测程序
        input_dir: 输入文件目录（*.in）
        output_dir: 输出文件目录（*.out 或 *.ans）
        timeout: 超时秒数
    """
    in_dir = Path(input_dir)
    out_dir = Path(output_dir)

    in_files = sorted(in_dir.glob("*.in"))
    if not in_files:
        in_files = sorted(in_dir.glob("*.txt"))

    if not in_files:
        print("❌ 没有找到输入文件")
        return

    print(f"🧪 批量测试: {len(in_files)} 个用例")
    print(f"   程序: {program}")
    print("-" * 60)

    passed = 0
    total_time = 0

    for in_file in in_files:
        # 找对应的输出文件
        out_file = out_dir / (in_file.stem + ".out")
        if not out_file.exists():
            out_file = out_dir / (in_file.stem + ".ans")
        if not out_file.exists():
            print(f"  ⚠️ {in_file.name}: 找不到答案文件，跳过")
            continue

        input_data = in_file.read_text(encoding="utf-8")
        expected = out_file.read_text(encoding="utf-8").strip()

        actual, elapsed, err = run_program(program, input_data, timeout=timeout)
        total_time += elapsed

        if err:
            print(f"  ❌ {in_file.name}: {err}")
        elif compare_outputs(actual or "", expected):
            passed += 1
            print(f"  ✅ {in_file.name} ({elapsed:.3f}s)")
        else:
            print(f"  ❌ {in_file.name}: 答案错误")
            print(f"     期望: {expected[:80]}")
            print(f"     实际: {(actual or '')[:80]}")

    print("-" * 60)
    print(f"📊 结果: {passed}/{len(in_files)} 通过 | 总耗时: {total_time:.3f}s")


def main():
    parser = argparse.ArgumentParser(description="自动测试运行器")
    sub = parser.add_subparsers(dest="command", help="可用命令")

    # 对拍
    adv = sub.add_parser("adversarial", help="对拍两个程序")
    adv.add_argument("--prog1", required=True, help="待测程序")
    adv.add_argument("--prog2", required=True, help="参考程序")
    adv.add_argument("--generator", required=True, help="数据生成器")
    adv.add_argument("--cases", type=int, default=100, help="测试轮数")
    adv.add_argument("--timeout", type=int, default=5, help="超时秒数")

    # 批量测试
    bt = sub.add_parser("batch", help="批量运行测试用例")
    bt.add_argument("--prog", required=True, help="待测程序")
    bt.add_argument("--input-dir", required=True, help="输入文件目录")
    bt.add_argument("--output-dir", required=True, help="答案文件目录")
    bt.add_argument("--timeout", type=int, default=5, help="超时秒数")

    args = parser.parse_args()

    if args.command == "adversarial":
        adversarial_test(args.prog1, args.prog2, args.generator, args.cases, args.timeout)
    elif args.command == "batch":
        batch_test(args.prog, args.input_dir, args.output_dir, args.timeout)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
