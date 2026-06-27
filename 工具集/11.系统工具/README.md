# 11.系统工具

📌 系统信息收集、资源监控、环境管理工具。

# ==========================================
# 📁 脚本列表
# ==========================================

| 脚本 | 功能 | 适用场景 |
|------|------|----------|
| `system_info.py` | 系统信息一键收集 | 排查环境问题、写实验报告的环境描述 |
| `disk_usage.py` | 磁盘使用分析 | 找出大文件、清理磁盘空间 |
| `process_monitor.py` | 进程资源监控 | 监控训练任务的 CPU/GPU/内存占用 |

# ==========================================
# 🚀 使用示例
# ==========================================

## system_info.py — 系统信息

```bash
# 显示完整系统信息
python system_info.py

# 输出为 Markdown（可直接粘贴到实验报告）
python system_info.py --format md

# 只显示硬件信息
python system_info.py --hardware

# 只显示 Python/conda 环境
python system_info.py --env
```

## disk_usage.py — 磁盘分析

```bash
# 分析当前目录
python disk_usage.py .

# 显示最大的 20 个文件
python disk_usage.py . --top 20

# 按文件类型统计
python disk_usage.py . --by-type

# 只扫描特定深度
python disk_usage.py . --depth 2
```

## process_monitor.py — 进程监控

```bash
# 监控指定进程（按名称）
python process_monitor.py --name python

# 监控指定 PID
python process_monitor.py --pid 12345

# 每 5 秒刷新，共监控 60 次
python process_monitor.py --name train --interval 5 --count 60

# 输出为 CSV（方便后续画图）
python process_monitor.py --name python --csv -o monitor.csv
```

# ==========================================
# 💡 Tips
# ==========================================

- `system_info.py` 可以直接生成 Markdown 格式，粘贴到论文的「实验环境」章节
- `disk_usage.py` 在清理 Docker 镜像/conda 环境时特别有用
- `process_monitor.py` 可以在训练时后台运行，事后分析资源瓶颈
