#!/usr/bin/env python3
"""
进程资源监控工具
📌 监控指定进程的 CPU/内存使用，支持定时采样和 CSV 导出
📌 可用于监控训练任务的资源瓶颈
"""

import argparse
import csv
import sys
import time
from datetime import datetime

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")


def find_processes(name: str = None, pid: int = None) -> list:
    """查找进程"""
    import subprocess

    if pid:
        # 按 PID 查找
        if sys.platform == "win32":
            output = subprocess.run(
                f"tasklist /FI \"PID eq {pid}\" /FO CSV /NH",
                shell=True, capture_output=True, text=True
            ).stdout
        else:
            output = subprocess.run(
                f"ps -p {pid} -o pid,user,%cpu,%mem,rss,comm --no-headers",
                shell=True, capture_output=True, text=True
            ).stdout
        return output.strip().split("\n") if output.strip() else []
    elif name:
        # 按名称查找
        if sys.platform == "win32":
            output = subprocess.run(
                f'tasklist /FI "IMAGENAME eq {name}*" /FO CSV /NH',
                shell=True, capture_output=True, text=True
            ).stdout
        else:
            output = subprocess.run(
                f"ps aux | grep -i {name} | grep -v grep",
                shell=True, capture_output=True, text=True
            ).stdout
        return output.strip().split("\n") if output.strip() else []
    return []


def get_process_info(pid: int) -> dict:
    """获取进程详细信息"""
    import subprocess

    info = {"pid": pid, "cpu": 0, "memory": 0, "memory_mb": 0}

    try:
        if sys.platform == "win32":
            output = subprocess.run(
                f'wmic process where "ProcessId={pid}" get WorkingSetSize,Name /format:list',
                shell=True, capture_output=True, text=True, timeout=5
            ).stdout
            for line in output.strip().split("\n"):
                if "WorkingSetSize" in line and "=" in line:
                    bytes_val = int(line.split("=", 1)[1].strip())
                    info["memory_mb"] = bytes_val / 1024 / 1024
        else:
            output = subprocess.run(
                f"ps -p {pid} -o %cpu,%mem,rss --no-headers",
                shell=True, capture_output=True, text=True, timeout=5
            ).stdout
            parts = output.strip().split()
            if len(parts) >= 3:
                info["cpu"] = float(parts[0])
                info["memory"] = float(parts[1])
                info["memory_mb"] = float(parts[2]) / 1024
    except Exception:
        pass

    return info


def monitor_process(
    name: str = None,
    pid: int = None,
    interval: float = 2.0,
    count: int = 60,
    csv_output: str = None,
):
    """监控进程资源使用"""
    if not name and not pid:
        print("❌ 必须指定 --name 或 --pid")
        sys.exit(1)

    print(f"🔍 监控目标: {name or pid}")
    print(f"⏱️ 采样间隔: {interval}s")
    print(f"📊 采样次数: {count}")
    print(f"⏹️ 按 Ctrl+C 停止\n")

    # CSV 输出
    csv_file = None
    csv_writer = None
    if csv_output:
        csv_file = open(csv_output, "w", newline="", encoding="utf-8")
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["时间", "PID", "CPU(%)", "内存(MB)"])

    records = []
    try:
        for i in range(count):
            timestamp = datetime.now().strftime("%H:%M:%S")

            if pid:
                pids = [pid]
            else:
                # 按名称查找 PID
                import subprocess
                if sys.platform == "win32":
                    output = subprocess.run(
                        f'tasklist /FI "IMAGENAME eq {name}*" /FO CSV /NH',
                        shell=True, capture_output=True, text=True
                    ).stdout
                    pids = []
                    for line in output.strip().split("\n"):
                        if line.strip():
                            parts = line.strip().strip('"').split('","')
                            if len(parts) >= 2:
                                try:
                                    pids.append(int(parts[1]))
                                except ValueError:
                                    pass
                else:
                    output = subprocess.run(
                        f"pgrep -f {name}",
                        shell=True, capture_output=True, text=True
                    ).stdout
                    pids = [int(p) for p in output.strip().split("\n") if p.strip().isdigit()]

            if not pids:
                print(f"  [{timestamp}] ⚠️ 未找到进程")
                time.sleep(interval)
                continue

            for p in pids:
                info = get_process_info(p)
                cpu = info.get("cpu", 0)
                mem = info.get("memory_mb", 0)

                bar_cpu = "█" * min(int(cpu / 2), 40)
                bar_mem = "█" * min(int(mem / 100), 40)

                print(f"  [{timestamp}] PID={p:<8} CPU: {cpu:>5.1f}% {bar_cpu}  MEM: {mem:>8.1f} MB {bar_mem}")

                if csv_writer:
                    csv_writer.writerow([timestamp, p, cpu, f"{mem:.1f}"])

                records.append({"time": timestamp, "pid": p, "cpu": cpu, "mem": mem})

            time.sleep(interval)

    except KeyboardInterrupt:
        print(f"\n⏹️ 监控已停止")

    if csv_file:
        csv_file.close()
        print(f"\n💾 数据已保存: {csv_output}")

    # 统计
    if records:
        cpus = [r["cpu"] for r in records]
        mems = [r["mem"] for r in records]
        print(f"\n📊 统计:")
        print(f"   CPU: 平均 {sum(cpus)/len(cpus):.1f}%, 最大 {max(cpus):.1f}%")
        print(f"   内存: 平均 {sum(mems)/len(mems):.1f} MB, 最大 {max(mems):.1f} MB")


def main():
    parser = argparse.ArgumentParser(
        description="进程资源监控工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python process_monitor.py --name python
  python process_monitor.py --pid 12345
  python process_monitor.py --name train --interval 5 --count 60
  python process_monitor.py --name python --csv -o monitor.csv
        """,
    )
    parser.add_argument("--name", help="进程名称")
    parser.add_argument("--pid", type=int, help="进程 PID")
    parser.add_argument("--interval", type=float, default=2.0, help="采样间隔秒数（默认 2）")
    parser.add_argument("--count", type=int, default=60, help="采样次数（默认 60）")
    parser.add_argument("--csv", action="store_true", help="输出为 CSV")
    parser.add_argument("-o", "--output", help="CSV 输出路径")

    args = parser.parse_args()
    csv_path = args.output if args.csv else None
    monitor_process(args.name, args.pid, args.interval, args.count, csv_path)


if __name__ == "__main__":
    main()
