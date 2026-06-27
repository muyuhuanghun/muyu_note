# 05.Git与版本控制

📌 Git 效率工具，处理重复性版本控制操作。

# ==========================================
# 📁 脚本列表
# ==========================================

| 脚本 | 功能 | 适用场景 |
|------|------|----------|
| `git_batch_ops.sh` | Git 批量操作（清理、同步、统计） | 仓库维护 |
| `repo_analyzer.py` | 仓库结构与贡献分析 | 项目管理、代码审计 |

# ==========================================
# 🚀 使用示例
# ==========================================

## git_batch_ops.sh — 批量操作

```bash
# 清理已合并的本地分支
bash git_batch_ops.sh clean-merged

# 批量拉取所有子模块
bash git_batch_ops.sh pull-submodules

# 显示仓库统计（提交数、文件数、大小）
bash git_batch_ops.sh stats

# 批量 stash → pull → pop（安全拉取远端更新）
bash git_batch_ops.sh safe-pull
```

## repo_analyzer.py — 仓库分析

```bash
# 分析仓库结构（文件类型、目录大小）
python repo_analyzer.py .

# 生成贡献者统计
python repo_analyzer.py . --contributors

# 按文件类型统计代码行数
python repo_analyzer.py . --loc-by-type

# 输出为 Markdown 报告
python repo_analyzer.py . --format md -o 分析报告.md
```

# ==========================================
# 💡 Tips
# ==========================================

- `git_batch_ops.sh` 在 Windows 上需要 Git Bash 环境
- `repo_analyzer.py` 可以分析任意 Git 仓库，不限于当前项目
- 建议定期运行 `clean-merged` 保持本地分支整洁
