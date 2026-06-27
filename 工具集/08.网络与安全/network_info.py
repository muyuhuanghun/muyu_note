#!/usr/bin/env python3
"""
网络信息收集工具
📌 一键查看本机 IP、网卡、DNS、路由、连通性等网络信息
"""

import argparse
import platform
import socket
import subprocess
import sys

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")


def get_local_ip() -> str:
    """获取本机局域网 IP"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "无法获取"


def get_hostname() -> str:
    """获取主机名"""
    return socket.gethostname()


def get_all_ips() -> list:
    """获取所有网卡 IP"""
    hostname = get_hostname()
    try:
        results = socket.getaddrinfo(hostname, None)
        ips = list(set(r[4][0] for r in results))
        return sorted(ips)
    except Exception:
        return []


def run_cmd(cmd: str) -> str:
    """执行系统命令并返回输出"""
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=10
        )
        return result.stdout.strip()
    except Exception:
        return "(命令执行失败)"


def ping_host(host: str, count: int = 4) -> str:
    """Ping 测试"""
    flag = "-n" if platform.system() == "Windows" else "-c"
    return run_cmd(f"ping {flag} {count} {host}")


def show_network_info(ip_only: bool = False, ping_target: str = None, fmt: str = "text"):
    """显示网络信息"""
    local_ip = get_local_ip()
    hostname = get_hostname()
    all_ips = get_all_ips()

    if ip_only:
        print(local_ip)
        return

    if fmt == "md":
        print("# 网络信息\n")
        print(f"| 项目 | 值 |")
        print(f"|------|-----|")
        print(f"| 主机名 | {hostname} |")
        print(f"| 局域网 IP | {local_ip} |")
        print(f"| 系统 | {platform.system()} {platform.release()} |")
        print(f"\n## 所有 IP 地址\n")
        for ip in all_ips:
            print(f"- {ip}")

        if ping_target:
            print(f"\n## Ping {ping_target}\n")
            print(f"```\n{ping_host(ping_target)}\n```")
    else:
        print(f"{'='*50}")
        print(f"🌐 网络信息")
        print(f"{'='*50}")
        print(f"  主机名:     {hostname}")
        print(f"  局域网 IP:  {local_ip}")
        print(f"  系统:       {platform.system()} {platform.release()}")
        print(f"  架构:       {platform.machine()}")

        print(f"\n📡 所有 IP 地址:")
        for ip in all_ips:
            print(f"  - {ip}")

        # DNS 信息
        print(f"\n🔤 DNS 解析测试:")
        test_domains = ["google.com", "baidu.com", "github.com"]
        for domain in test_domains:
            try:
                ip = socket.gethostbyname(domain)
                print(f"  {domain:<20} → {ip}")
            except Exception:
                print(f"  {domain:<20} → 解析失败")

        # 路由信息
        print(f"\n🛤️ 路由表:")
        if platform.system() == "Windows":
            route = run_cmd("route print | findstr 0.0.0.0")
        else:
            route = run_cmd("route -n | head -10")
        for line in route.split("\n")[:8]:
            print(f"  {line}")

        if ping_target:
            print(f"\n🏓 Ping {ping_target}:")
            result = ping_host(ping_target)
            for line in result.split("\n"):
                print(f"  {line}")


def main():
    parser = argparse.ArgumentParser(description="网络信息收集工具")
    parser.add_argument("--ip-only", action="store_true", help="只显示本机 IP")
    parser.add_argument("--ping", help="Ping 测试目标")
    parser.add_argument("--format", choices=["text", "md"], default="text", help="输出格式")

    args = parser.parse_args()
    show_network_info(ip_only=args.ip_only, ping_target=args.ping, fmt=args.format)


if __name__ == "__main__":
    main()
