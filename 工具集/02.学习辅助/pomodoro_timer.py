#!/usr/bin/env python3
"""
终端番茄钟
📌 支持自定义工作/休息时长、轮数统计，终端实时倒计时
"""

import argparse
import sys
import time
import os

# Windows 终端 UTF-8 输出
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")


def clear_line():
    """清除当前行"""
    print("\r\033[K", end="", flush=True)


def format_time(seconds: int) -> str:
    """格式化时间为 MM:SS"""
    m, s = divmod(seconds, 60)
    return f"{m:02d}:{s:02d}"


def progress_bar(current: int, total: int, width: int = 30) -> str:
    """生成进度条"""
    filled = int(width * current / total)
    bar = "█" * filled + "░" * (width - filled)
    return f"[{bar}]"


def beep():
    """终端响铃"""
    print("\a", end="", flush=True)


def countdown(seconds: int, label: str):
    """
    倒计时显示

    参数:
        seconds: 倒计时秒数
        label: 显示标签（如"🍅 工作中"）
    """
    total = seconds
    while seconds > 0:
        time_str = format_time(seconds)
        bar = progress_bar(total - seconds, total)
        print(f"\r  {label} {time_str} {bar}", end="", flush=True)
        time.sleep(1)
        seconds -= 1
    clear_line()


def pomodoro(work_min: int = 25, break_min: int = 5, rounds: int = 4):
    """
    番茄钟主循环

    参数:
        work_min: 工作时长（分钟）
        break_min: 休息时长（分钟）
        rounds: 总轮数（0 = 无限）
    """
    print("╔══════════════════════════════════════╗")
    print("║         🍅 番茄钟 Pomodoro           ║")
    print("╠══════════════════════════════════════╣")
    print(f"║  工作时长: {work_min} 分钟                 ║")
    print(f"║  休息时长: {break_min} 分钟                 ║")
    print(f"║  轮    数: {'无限' if rounds == 0 else rounds}                       ║")
    print("╚══════════════════════════════════════╝")
    print("\n按 Ctrl+C 随时退出\n")

    current_round = 0
    total_work_time = 0

    try:
        while rounds == 0 or current_round < rounds:
            current_round += 1
            round_label = f"第 {current_round} 轮" if rounds == 0 else f"第 {current_round}/{rounds} 轮"

            # 🍅 工作阶段
            print(f"🍅 {round_label} — 开始工作！（{work_min} 分钟）")
            countdown(work_min * 60, "🍅 工作中")
            total_work_time += work_min
            beep()
            print(f"✅ {round_label} 工作完成！累计工作 {total_work_time} 分钟")

            # 休息阶段
            if rounds == 0 or current_round < rounds:
                print(f"☕ 休息时间（{break_min} 分钟）")
                countdown(break_min * 60, "☕ 休息中")
                beep()
                print(f"💪 休息结束，准备下一轮！\n")
            else:
                print(f"\n🎉 所有 {rounds} 轮完成！")
                print(f"📊 总工作时长: {total_work_time} 分钟")

    except KeyboardInterrupt:
        print(f"\n\n⏹️ 番茄钟已停止")
        print(f"📊 本次总工作时长: {total_work_time} 分钟")
        print(f"   完成轮数: {current_round - 1} 轮")


def main():
    parser = argparse.ArgumentParser(
        description="终端番茄钟",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python pomodoro_timer.py                    # 默认 25+5，无限轮
  python pomodoro_timer.py --work 45 --break 10
  python pomodoro_timer.py --rounds 4         # 完成 4 轮后自动停止
        """,
    )
    parser.add_argument("--work", type=int, default=25, help="工作时长（分钟，默认 25）")
    parser.add_argument("--break", dest="break_min", type=int, default=5, help="休息时长（分钟，默认 5）")
    parser.add_argument("--rounds", type=int, default=0, help="总轮数（默认 0 = 无限循环）")

    args = parser.parse_args()
    pomodoro(work_min=args.work, break_min=args.break_min, rounds=args.rounds)


if __name__ == "__main__":
    main()
