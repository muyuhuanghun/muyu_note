#!/usr/bin/env python3
"""
定时任务管理助手
📌 生成 Linux cron 表达式和 Windows Task Scheduler 配置
📌 支持可视化展示、当前任务列表查看
"""

import argparse
import sys

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")


def parse_interval(interval: str) -> tuple:
    """
    解析间隔表达式
    如 "1h" → ("hourly", 1), "30m" → ("minutely", 30), "2d" → ("daily", 2)
    """
    interval = interval.strip().lower()
    if interval.endswith("m"):
        return ("minutely", int(interval[:-1]))
    elif interval.endswith("h"):
        return ("hourly", int(interval[:-1]))
    elif interval.endswith("d"):
        return ("daily", int(interval[:-1]))
    elif interval.endswith("w"):
        return ("weekly", int(interval[:-1]))
    return ("daily", 1)


WEEKDAY_MAP = {
    "mon": 1, "tue": 2, "wed": 3, "thu": 4,
    "fri": 5, "sat": 6, "sun": 0,
}


def generate_cron(
    every: str = None,
    daily: str = None,
    weekly: str = None,
    monthly: int = None,
    command: str = "",
) -> str:
    """生成 cron 表达式"""
    if every:
        unit, value = parse_interval(every)
        if unit == "minutely":
            return f"*/{value} * * * * {command}"
        elif unit == "hourly":
            return f"0 */{value} * * * {command}"
        elif unit == "daily":
            return f"0 0 */{value} * * {command}"
        elif unit == "weekly":
            return f"0 0 * */{value} * {command}"

    elif daily:
        parts = daily.split(":")
        hour = int(parts[0])
        minute = int(parts[1]) if len(parts) > 1 else 0
        return f"{minute} {hour} * * * {command}"

    elif weekly:
        weekday = WEEKDAY_MAP.get(weekly.lower(), 1)
        return f"0 0 * * {weekday} {command}"

    elif monthly is not None:
        return f"0 0 {monthly} * * {command}"

    return ""


def generate_xml(
    daily: str = None,
    command: str = "",
    task_name: str = "MyTask",
) -> str:
    """生成 Windows Task Scheduler XML"""
    time_str = daily or "02:00"
    parts = time_str.split(":")
    hour = int(parts[0])
    minute = int(parts[1]) if len(parts) > 1 else 0

    xml = f'''<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo>
    <Description>{task_name}</Description>
  </RegistrationInfo>
  <Triggers>
    <CalendarTrigger>
      <StartBoundary>2026-01-01T{hour:02d}:{minute:02d}:00</StartBoundary>
      <Enabled>true</Enabled>
      <ScheduleByDay>
        <DaysInterval>1</DaysInterval>
      </ScheduleByDay>
    </CalendarTrigger>
  </Triggers>
  <Actions>
    <Exec>
      <Command>{command}</Command>
    </Exec>
  </Actions>
</Task>'''
    return xml


def list_cron():
    """列出当前用户的 cron 任务"""
    import subprocess
    if sys.platform == "win32":
        output = subprocess.run("schtasks /query /fo LIST", shell=True, capture_output=True, text=True).stdout
        print(output[:2000] if output else "⚠️ 无法获取任务列表")
    else:
        output = subprocess.run("crontab -l", shell=True, capture_output=True, text=True).stdout
        print(output if output else "📭 没有 cron 任务")


def main():
    parser = argparse.ArgumentParser(
        description="定时任务管理助手",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python cron_helper.py --every 1h --command "python backup.py"
  python cron_helper.py --daily 02:00 --command "python cleanup.py"
  python cron_helper.py --weekly mon --command "python report.py"
  python cron_helper.py --list
        """,
    )
    parser.add_argument("--every", help="每隔多久执行（如 30m, 1h, 2d）")
    parser.add_argument("--daily", help="每天指定时间执行（如 02:00）")
    parser.add_argument("--weekly", help="每周指定天执行（mon/tue/wed/...）")
    parser.add_argument("--monthly", type=int, help="每月指定日执行（1-31）")
    parser.add_argument("--command", default="", help="要执行的命令")
    parser.add_argument("--format", choices=["cron", "xml"], default="cron", help="输出格式")
    parser.add_argument("--list", action="store_true", help="列出当前任务")

    args = parser.parse_args()

    if args.list:
        list_cron()
        return

    if args.format == "xml":
        xml = generate_xml(args.daily, args.command)
        print(xml)
    else:
        cron = generate_cron(
            every=args.every,
            daily=args.daily,
            weekly=args.weekly,
            monthly=args.monthly,
            command=args.command,
        )
        if cron:
            print(f"📋 Cron 表达式:")
            print(f"   {cron}")
            print(f"\n💡 添加方式:")
            print(f"   1. crontab -e")
            print(f"   2. 粘贴上面的表达式")
        else:
            parser.print_help()


if __name__ == "__main__":
    main()
