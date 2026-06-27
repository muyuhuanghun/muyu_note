#!/usr/bin/env python3
"""
一键 HTTP 文件服务器
📌 快速启动一个 HTTP 服务器，用于局域网文件共享或本地调试
📌 支持目录浏览、基础认证、自定义端口
"""

import argparse
import base64
import os
import sys
from functools import partial
from http.server import HTTPServer, SimpleHTTPRequestHandler

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")


class AuthHandler(SimpleHTTPRequestHandler):
    """带基础认证的 HTTP 请求处理器"""

    def __init__(self, username, password, *args, **kwargs):
        self.username = username
        self.password = password
        super().__init__(*args, **kwargs)

    def do_AUTHHEAD(self):
        self.send_response(401)
        self.send_header("WWW-Authenticate", 'Basic realm="File Server"')
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"401 Unauthorized")

    def do_GET(self):
        if self.username and self.password:
            auth_header = self.headers.get("Authorization")
            if auth_header is None:
                self.do_AUTHHEAD()
                return

            try:
                auth_type, credentials = auth_header.split(" ", 1)
                if auth_type.lower() != "basic":
                    self.do_AUTHHEAD()
                    return
                decoded = base64.b64decode(credentials).decode("utf-8")
                user, pwd = decoded.split(":", 1)
                if user != self.username or pwd != self.password:
                    self.do_AUTHHEAD()
                    return
            except Exception:
                self.do_AUTHHEAD()
                return

        super().do_GET()


def run_server(port: int, directory: str, username: str = None, password: str = None):
    """启动 HTTP 文件服务器"""
    os.chdir(directory)

    if username and password:
        handler = partial(AuthHandler, username, password)
    else:
        handler = SimpleHTTPRequestHandler

    server = HTTPServer(("0.0.0.0", port), handler)

    print(f"🌐 HTTP 文件服务器已启动")
    print(f"📁 服务目录: {os.path.abspath(directory)}")
    print(f"🔗 访问地址: http://localhost:{port}")
    if username:
        print(f"🔐 认证: {username} / {'*' * len(password)}")
    print(f"⏹️ 按 Ctrl+C 停止\n")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n⏹️ 服务器已停止")
        server.server_close()


def main():
    parser = argparse.ArgumentParser(
        description="一键 HTTP 文件服务器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python http_file_server.py
  python http_file_server.py --port 9090 --dir ./share
  python http_file_server.py --port 8080 --user admin --password 123456
        """,
    )
    parser.add_argument("--port", type=int, default=8000, help="端口号（默认 8000）")
    parser.add_argument("--dir", default=".", help="服务目录（默认当前目录）")
    parser.add_argument("--user", help="认证用户名")
    parser.add_argument("--password", help="认证密码")

    args = parser.parse_args()
    run_server(args.port, args.dir, args.user, args.password)


if __name__ == "__main__":
    main()
