#!/usr/bin/env python3
"""
TCP 端口扫描器
📌 多线程扫描目标主机的开放端口，支持端口范围和服务识别
⚠️ 仅用于授权的网络环境
"""

import argparse
import socket
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

# 常见端口 → 服务名映射
COMMON_SERVICES = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
    53: "DNS", 80: "HTTP", 110: "POP3", 143: "IMAP",
    443: "HTTPS", 993: "IMAPS", 995: "POP3S",
    3306: "MySQL", 3389: "RDP", 5432: "PostgreSQL",
    5900: "VNC", 6379: "Redis", 8080: "HTTP-Alt",
    8443: "HTTPS-Alt", 27017: "MongoDB", 11211: "Memcached",
}


def scan_port(host: str, port: int, timeout: float = 1.0) -> tuple:
    """扫描单个端口，返回 (port, is_open, service)"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            result = s.connect_ex((host, port))
            if result == 0:
                service = COMMON_SERVICES.get(port, "unknown")
                try:
                    service = socket.getservbyport(port)
                except OSError:
                    pass
                return (port, True, service)
    except Exception:
        pass
    return (port, False, "")


def parse_ports(port_str: str) -> list:
    """解析端口参数：支持 80,443,8080 和 80-100 两种格式"""
    ports = []
    for part in port_str.split(","):
        part = part.strip()
        if "-" in part:
            start, end = part.split("-", 1)
            ports.extend(range(int(start), int(end) + 1))
        else:
            ports.append(int(part))
    return sorted(set(ports))


def scan_host(host: str, ports: list, threads: int = 50, timeout: float = 1.0):
    """
    扫描目标主机

    参数:
        host: 目标 IP 或域名
        ports: 端口列表
        threads: 并发线程数
        timeout: 连接超时秒数
    """
    print(f"🔍 扫描目标: {host}")
    print(f"📋 端口范围: {len(ports)} 个端口")
    print(f"⚡ 并发线程: {threads}")
    print(f"⏱️ 超时时间: {timeout}s")
    print("-" * 50)

    open_ports = []
    scanned = 0

    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = {
            executor.submit(scan_port, host, port, timeout): port
            for port in ports
        }

        for future in as_completed(futures):
            port, is_open, service = future.result()
            scanned += 1

            if is_open:
                open_ports.append((port, service))
                print(f"  ✅ {port:>5}/tcp  OPEN  ({service})")

            # 进度显示
            if scanned % 100 == 0:
                print(f"  ... 已扫描 {scanned}/{len(ports)}")

    # 结果汇总
    open_ports.sort()
    print("-" * 50)
    print(f"📊 扫描完成: {len(open_ports)} 个开放端口 / {len(ports)} 个已扫描")

    if open_ports:
        print(f"\n{'端口':<10} {'服务':<15}")
        print("-" * 25)
        for port, service in open_ports:
            print(f"{port:<10} {service:<15}")


def main():
    parser = argparse.ArgumentParser(
        description="TCP 端口扫描器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python port_scanner.py 127.0.0.1
  python port_scanner.py 192.168.1.1 --ports 80,443,3306,6379
  python port_scanner.py 10.0.0.1 --range 1-1024 --threads 100
        """,
    )
    parser.add_argument("host", help="目标 IP 或域名")
    parser.add_argument("--ports", default="21,22,23,25,53,80,110,143,443,993,995,3306,3389,5432,5900,6379,8080,8443,27017",
                        help="端口列表（逗号分隔）")
    parser.add_argument("--range", help="端口范围（如 1-1024）")
    parser.add_argument("--threads", type=int, default=50, help="并发线程数（默认 50）")
    parser.add_argument("--timeout", type=float, default=1.0, help="超时秒数（默认 1.0）")

    args = parser.parse_args()

    if args.range:
        ports = parse_ports(args.range)
    else:
        ports = parse_ports(args.ports)

    scan_host(args.host, ports, args.threads, args.timeout)


if __name__ == "__main__":
    main()
