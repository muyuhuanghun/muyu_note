# 02.学习辅助

📌 学习效率工具，覆盖从复习到时间管理的全流程。

# ==========================================
# 📁 脚本列表
# ==========================================

| 脚本 | 功能 | 适用场景 |
|------|------|----------|
| `anki_card_generator.py` | 从 Markdown 笔记生成 Anki 闪卡 | 考试复习、知识巩固 |
| `pomodoro_timer.py` | 终端番茄钟 | 专注学习、时间管理 |
| `deadline_tracker.py` | 课程作业/考试 Deadline 管理 | 多课程并行、避免遗忘 |

# ==========================================
# 🚀 使用示例
# ==========================================

## anki_card_generator.py — 闪卡生成

```bash
# 从笔记生成 Anki 导入格式（制表符分隔）
python anki_card_generator.py 期末复习/近代史/近代史完整复习.md -o 近代史卡片.txt

# 指定分隔符（默认为 Q/A 空行分隔）
python anki_card_generator.py 笔记.md --separator "##" -o 卡片.txt

# 只提取带 📌 标记的知识点
python anki_card_generator.py 笔记.md --marker "📌" -o 重点卡片.txt
```

📌 生成的 .txt 文件可以直接导入 Anki（文件 → 导入 → 选择文件）

## pomodoro_timer.py — 番茄钟

```bash
# 默认 25 分钟工作 + 5 分钟休息
python pomodoro_timer.py

# 自定义时长（45 分钟工作 + 10 分钟休息）
python pomodoro_timer.py --work 45 --break 10

# 设置总轮数
python pomodoro_timer.py --rounds 4
```

## deadline_tracker.py — Deadline 追踪

```bash
# 查看所有待办 Deadline
python deadline_tracker.py list

# 添加新 Deadline
python deadline_tracker.py add --course "数据结构" --task "期末考试" --date "2026-07-10"

# 按紧急程度排序
python deadline_tracker.py list --sort urgency
```

# ==========================================
# 💡 Tips
# ==========================================

- Anki 卡片生成器支持 Obsidian 的 `> [!tip]` Callout 语法作为答案
- 番茄钟会在终端显示倒计时，到时间会发出提示音
- Deadline 数据存储在本地 JSON 文件中，可手动编辑
