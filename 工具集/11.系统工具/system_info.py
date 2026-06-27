#!/usr/bin/env python3
"""
系统信息收集工具
📌 一键收集 CPU/内存/磁盘/GPU/Python 环境等信息
📌 支持输出为 Markdown，可直接粘贴到论文「实验环境」章节
"""

import argparse
import platform
import sys

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

import os
import subprocess


def run_cmd(cmd: str) -> str:
    """执行命令并返回输出"""
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
        return r.stdout.strip()
    except Exception:
        return ""


def get_cpu_info() -> dict:
    """CPU 信息"""
    info = {
        "处理器": platform.processor() or "未知",
        "架构": platform.machine(),
        "物理核心": "未知",
        "逻辑核心": str(os.cpu_count()),
    }

    if platform.system() == "Windows":
        output = run_cmd("wmic cpu get Name,NumberOfCores /format:list")
        for line in output.split("\n"):
            if "Name" in line and "=" in line:
                info["处理器"] = line.split("=", 1)[1].strip()
            if "NumberOfCores" in line and "=" in line:
                info["物理核心"] = line.split("=", 1)[1].strip()
    elif platform.system() == "Linux":
        output = run_cmd("nproc")
        if output:
            info["逻辑核心"] = output
        output = run_cmd("lscpu | grep 'Model name'")
        if ":" in output:
            info["处理器"] = output.split(":", 1)[1].strip()

    return info


def get_memory_info() -> dict:
    """内存信息"""
    if platform.system() == "Windows":
        output = run_cmd("wmic os get TotalVisibleMemorySize /format:list")
        for line in output.split("\n"):
            if "TotalVisibleMemorySize" in line and "=" in line:
                kb = int(line.split("=", 1)[1].strip())
                return {"总内存": f"{kb / 1024 / 1024:.1f} GB"}
    elif platform.system() == "Linux":
        output = run_cmd("free -h | grep Mem")
        parts = output.split()
        if len(parts) >= 2:
            return {"总内存": parts[1]}

    # Python 层面
    try:
        import psutil
        mem = psutil.virtual_memory()
        return {"总内存": f"{mem.total / 1024**3:.1f} GB", "可用": f"{mem.available / 1024**3:.1f} GB"}
    except ImportError:
        pass

    return {"总内存": "未知"}


def get_disk_info() -> list:
    """磁盘信息"""
    disks = []
    if platform.system() == "Windows":
        output = run_cmd("wmic logicaldisk get DeviceID,Size,FreeSpace /format:list")
        current = {}
        for line in output.split("\n"):
            line = line.strip()
            if "=" in line:
                key, val = line.split("=", 1)
                current[key.strip()] = val.strip()
            elif current:
                if "DeviceID" in current:
                    total = int(current.get("Size", 0))
                    free = int(current.get("FreeSpace", 0))
                    if total > 0:
                        disks.append({
                            "盘符": current["DeviceID"],
                            "总容量": f"{total / 1024**3:.1f} GB",
                            "可用": f"{free / 1024**3:.1f} GB",
                        })
                current = {}
    elif platform.system() == "Linux":
        output = run_cmd("df -h | grep -E '^/dev/'")
        for line in output.split("\n"):
            parts = line.split()
            if len(parts) >= 6:
                disks.append({"设备": parts[0], "总容量": parts[1], "已用": parts[2], "可用": parts[3]})

    return disks


def get_gpu_info() -> list:
    """GPU 信息（通过 nvidia-smi）"""
    gpus = []
    output = run_cmd("nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader")
    if output:
        for line in output.split("\n"):
            parts = [p.strip() for p in line.split(",")]
            if len(parts) >= 3:
                gpus.append({"型号": parts[0], "显存": parts[1], "驱动": parts[2]})
    return gpus


def get_python_info() -> dict:
    """Python 环境信息"""
    info = {
        "Python 版本": platform.python_version(),
        "实现": platform.python_implementation(),
    }

    # conda 环境
    conda_env = os.environ.get("CONDA_DEFAULT_ENV", "")
    if conda_env:
        info["Conda 环境"] = conda_env

    # 关键包版本
    packages = ["torch", "numpy", "pandas", "tensorflow", "keras", "scikit-learn"]
    for pkg in packages:
        try:
            mod = __import__(pkg)
            ver = getattr(mod, "__version__", "已安装")
            info[pkg] = ver
        except ImportError:
            pass

    return info


def get_os_info() -> dict:
    """操作系统信息"""
    return {
        "系统": platform.system(),
        "版本": platform.version(),
        "发行版": platform.platform(),
        "主机名": platform.node(),
    }


def collect_all() -> dict:
    """收集所有信息"""
    return {
        "操作系统": get_os_info(),
        "CPU": get_cpu_info(),
        "内存": get_memory_info(),
        "磁盘": get_disk_info(),
        "GPU": get_gpu_info(),
        "Python": get_python_info(),
    }


def print_report(data: dict, sections: list = None, fmt: str = "text"):
    """输出报告"""
    if fmt == "md":
        print("# 实验环境\n")
        for section, info in data.items():
            if sections and section not in sections:
                continue
            print(f"## {section}\n")
            if isinstance(info, dict):
                print(f"| 项目 | 值 |")
                print(f"|------|-----|")
                for k, v in info.items():
                    print(f"| {k} | {v} |")
            elif isinstance(info, list):
                if info:
                    keys = info[0].keys()
                    print(f"| {' | '.join(keys)} |")
                    print(f"|{'|'.join(['------'] * len(keys))}|")
                    for item in info:
                        print(f"| {' | '.join(str(v) for v in item.values())} |")
                else:
                    print("无信息")
            print()
    else:
        print(f"{'='*50}")
        print(f"🖥️ 系统信息")
        print(f"{'='*50}")

        for section, info in data.items():
            if sections and section not in sections:
                continue
            print(f"\n📋 {section}:")
            if isinstance(info, dict):
                for k, v in info.items():
                    print(f"   {k}: {v}")
            elif isinstance(info, list):
                if info:
                    for item in info:
                        print(f"   {' | '.join(str(v) for v in item.values())}")
                else:
                    print("   无信息")


def main():
    parser = argparse.ArgumentParser(description="系统信息收集工具")
    parser.add_argument("--hardware", action="store_true", help="只显示硬件信息")
    parser.add_argument("--env", action="store_true", help="只显示 Python 环境")
    parser.add_argument("--format", choices=["text", "md"], default="text", help="输出格式")

    args = parser.parse_args()

    data = collect_all()
    sections = None
    if args.hardware:
        sections = ["操作系统", "CPU", "内存", "磁盘", "GPU"]
    elif args.env:
        sections = ["Python"]

    print_report(data, sections, args.format)


if __name__ == "__main__":
    main()
