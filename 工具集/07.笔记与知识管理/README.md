# 07.笔记与知识管理

📌 Obsidian 知识库维护和笔记质量检查工具。

# ==========================================
# 📁 脚本列表
# ==========================================

| 脚本 | 功能 | 适用场景 |
|------|------|----------|
| `obsidian_link_checker.py` | 检查 Obsidian 断链和孤岛笔记 | 知识库健康检查 |
| `note_stats.py` | 笔记库统计分析 | 学习进度追踪 |

# ==========================================
# 🚀 使用示例
# ==========================================

## obsidian_link_checker.py — 链接检查

```bash
# 检查所有断链
python obsidian_link_checker.py /path/to/vault

# 只显示断链（不含孤岛）
python obsidian_link_checker.py /path/to/vault --broken-only

# 输出为 Markdown 报告
python obsidian_link_checker.py /path/to/vault --format md -o 链接报告.md

# 自动修复常见断链（大小写、空格差异）
python obsidian_link_checker.py /path/to/vault --auto-fix
```

## note_stats.py — 笔记统计

```bash
# 显示笔记库整体统计
python note_stats.py /path/to/vault

# 按目录统计文件数和字数
python note_stats.py /path/to/vault --by-dir

# 统计最近 N 天的新增/修改笔记
python note_stats.py /path/to/vault --recent 7

# 生成 Markdown 报告
python note_stats.py /path/to/vault --format md -o 统计报告.md
```

# ==========================================
# 💡 Tips
# ==========================================

- 建议每周运行一次链接检查，保持知识库健康
- `note_stats.py` 可以配合 cron/Task Scheduler 自动生成周报
- 这两个脚本就是本仓库「仓库结构地图.md」中审计报告的通用化版本
