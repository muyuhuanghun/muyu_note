# 08.网络与安全

📌 网络调试、安全工具，覆盖日常开发和学习中的网络需求。

# ==========================================
# 📁 脚本列表
# ==========================================

| 脚本 | 功能 | 适用场景 |
|------|------|----------|
| `port_scanner.py` | TCP 端口扫描器 | 检测服务器开放端口、学习网络编程 |
| `http_file_server.py` | 一键 HTTP 文件服务器 | 局域网传文件、本地调试前端 |
| `network_info.py` | 网络信息收集 | 查看本机 IP、路由、DNS、连通性 |
| `password_gen.py` | 密码生成与强度检测 | 生成安全密码、评估密码强度 |

# ==========================================
# 🚀 使用示例
# ==========================================

## port_scanner.py — 端口扫描

```bash
# 扫描 localhost 常用端口
python port_scanner.py 127.0.0.1

# 扫描指定端口范围
python port_scanner.py 192.168.1.1 --ports 80,443,3306,6379,8080

# 扫描端口段
python port_scanner.py 192.168.1.1 --range 8000-9000

# 多线程加速
python port_scanner.py 10.0.0.1 --range 1-1024 --threads 100
```

## http_file_server.py — HTTP 文件服务器

```bash
# 在当前目录启动 HTTP 服务器（默认 8000 端口）
python http_file_server.py

# 指定端口和目录
python http_file_server.py --port 9090 --dir ./share

# 带基础认证
python http_file_server.py --port 8080 --user admin --password 123456
```

💡 启动后其他设备通过 `http://你的IP:端口` 即可访问文件

## network_info.py — 网络信息

```bash
# 显示完整网络信息
python network_info.py

# 只显示 IP 地址
python network_info.py --ip-only

# 测试连通性
python network_info.py --ping 8.8.8.8
```

## password_gen.py — 密码工具

```bash
# 生成随机密码（默认 16 位）
python password_gen.py

# 生成 5 个 32 位密码
python password_gen.py --length 32 --count 5

# 检测密码强度
python password_gen.py --check "MyP@ssw0rd!"

# 生成易记忆密码（单词组合）
python password_gen.py --memorable --count 3
```

# ==========================================
# ⚠️ 注意事项
# ==========================================

- 端口扫描仅用于授权的网络环境，未经授权扫描他人服务器可能违法
- HTTP 文件服务器不要在公网暴露敏感文件
- 密码工具仅使用标准库，不会外传任何数据
