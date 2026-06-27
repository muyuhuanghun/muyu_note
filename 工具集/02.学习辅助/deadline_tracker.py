#!/usr/bin/env python3
"""
Deadline 追踪器
📌 管理课程作业、考试等截止日期，按紧急程度排序提醒
📌 数据存储在本地 JSON 文件中
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Windows 终端 UTF-8 输出
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

# 数据文件路径（与脚本同目录）
DATA_FILE = Path(__file__).parent / "deadlines.json"


def load_data() -> list:
    """加载 Deadline 数据"""
    if not DATA_FILE.exists():
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data: list):
    """保存 Deadline 数据"""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_urgency(deadline: str) -> tuple:
    """
    计算紧急程度
    返回 (等级, 剩余天数)
    等级: 0=已过期, 1=紧急(<3天), 2=较急(<7天), 3=普通(<30天), 4=轻松(>30天)
    """
    now = datetime.now()
    due = datetime.strptime(deadline, "%Y-%m-%d")
    delta = (due - now).days

    if delta < 0:
        return (0, delta)
    elif delta <= 3:
        return (1, delta)
    elif delta <= 7:
        return (2, delta)
    elif delta <= 30:
        return (3, delta)
    else:
        return (4, delta)


URGENCY_LABELS = {
    0: "🔴 已过期",
    1: "🔴 紧急",
    2: "🟡 较急",
    3: "🟢 正常",
    4: "⚪ 轻松",
}


def add_deadline(course: str, task: str, date: str, priority: str = "normal"):
    """添加新 Deadline"""
    data = load_data()
    entry = {
        "course": course,
        "task": task,
        "deadline": date,
        "priority": priority,
        "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "done": False,
    }
    data.append(entry)
    save_data(data)
    print(f"✅ 已添加: [{course}] {task} — 截止 {date}")


def list_deadlines(sort_by: str = "urgency", show_done: bool = False):
    """列出所有 Deadline"""
    data = load_data()

    if not data:
        print("📭 没有 Deadline，可以放松一下！")
        return

    # 过滤已完成
    if not show_done:
        data = [d for d in data if not d.get("done", False)]

    if not data:
        print("✅ 所有 Deadline 已完成！")
        return

    # 排序
    if sort_by == "urgency":
        data.sort(key=lambda d: get_urgency(d["deadline"]))
    elif sort_by == "date":
        data.sort(key=lambda d: d["deadline"])
    elif sort_by == "course":
        data.sort(key=lambda d: d["course"])

    # 显示
    print(f"📋 Deadline 列表（共 {len(data)} 项）\n")
    print(f"{'状态':<10} {'课程':<15} {'任务':<25} {'截止日期':<12} {'剩余':<8}")
    print("-" * 75)

    for d in data:
        urgency, days = get_urgency(d["deadline"])
        label = URGENCY_LABELS[urgency]
        days_str = f"{days}天" if days >= 0 else f"过期{-days}天"
        status = "✅" if d.get("done") else ""

        print(f"{status} {label:<8} {d['course']:<15} {d['task']:<25} {d['deadline']:<12} {days_str}")


def mark_done(index: int):
    """标记 Deadline 为已完成"""
    data = load_data()
    if 0 <= index < len(data):
        data[index]["done"] = True
        save_data(data)
        print(f"✅ 已完成: [{data[index]['course']}] {data[index]['task']}")
    else:
        print(f"❌ 无效序号: {index}")


def delete_deadline(index: int):
    """删除 Deadline"""
    data = load_data()
    if 0 <= index < len(data):
        removed = data.pop(index)
        save_data(data)
        print(f"🗑️ 已删除: [{removed['course']}] {removed['task']}")
    else:
        print(f"❌ 无效序号: {index}")


def main():
    parser = argparse.ArgumentParser(
        description="Deadline 追踪器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python deadline_tracker.py list
  python deadline_tracker.py add --course "数据结构" --task "期末考试" --date "2026-07-10"
  python deadline_tracker.py done 0
  python deadline_tracker.py delete 2
        """,
    )
    sub = parser.add_subparsers(dest="command", help="可用命令")

    # list
    list_parser = sub.add_parser("list", help="列出所有 Deadline")
    list_parser.add_argument("--sort", choices=["urgency", "date", "course"], default="urgency")
    list_parser.add_argument("--show-done", action="store_true", help="显示已完成的")

    # add
    add_parser = sub.add_parser("add", help="添加新 Deadline")
    add_parser.add_argument("--course", required=True, help="课程名称")
    add_parser.add_argument("--task", required=True, help="任务描述")
    add_parser.add_argument("--date", required=True, help="截止日期（YYYY-MM-DD）")
    add_parser.add_argument("--priority", choices=["high", "normal", "low"], default="normal")

    # done
    done_parser = sub.add_parser("done", help="标记为已完成")
    done_parser.add_argument("index", type=int, help="序号")

    # delete
    del_parser = sub.add_parser("delete", help="删除 Deadline")
    del_parser.add_argument("index", type=int, help="序号")

    args = parser.parse_args()

    if args.command == "list":
        list_deadlines(sort_by=args.sort, show_done=args.show_done)
    elif args.command == "add":
        add_deadline(args.course, args.task, args.date, args.priority)
    elif args.command == "done":
        mark_done(args.index)
    elif args.command == "delete":
        delete_deadline(args.index)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
