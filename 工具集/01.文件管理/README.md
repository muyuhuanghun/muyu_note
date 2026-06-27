# 01.文件管理

📌 文件管理类脚本，解决日常文件整理的痛点。

# ==========================================
# 📁 脚本列表
# ==========================================

| 脚本 | 功能 | 适用场景 |
|------|------|----------|
| `batch_rename.py` | 批量重命名文件 | 课件、照片、下载文件规范化 |
| `file_organizer.py` | 按类型/日期自动分类文件 | 下载文件夹、桌面清理 |
| `duplicate_finder.py` | 查找重复文件 | 释放磁盘空间、去重 |

# ==========================================
# 🚀 使用示例
# ==========================================

## batch_rename.py — 批量重命名

```bash
# 给所有 .pdf 文件加上课程前缀
python batch_rename.py ./课件/ --prefix "数据结构_" --ext .pdf

# 按序号重命名图片
python batch_rename.py ./photos/ --pattern "photo_{n:03d}" --ext .png

# 预览模式（不实际修改）
python batch_rename.py ./下载/ --prefix "DL_" --dry-run
```

## file_organizer.py — 自动分类

```bash
# 按文件类型分类（文档/图片/视频/代码/压缩包）
python file_organizer.py ~/Downloads

# 按修改日期分类（年-月子目录）
python file_organizer.py ~/Downloads --by-date

# 预览模式
python file_organizer.py ~/Downloads --dry-run
```

## duplicate_finder.py — 查找重复文件

```bash
# 扫描目录中的重复文件
python duplicate_finder.py ~/Documents

# 只显示重复文件（不交互删除）
python duplicate_finder.py ~/Documents --list-only
```

# ==========================================
# ⚠️ 注意事项
# ==========================================

- 所有脚本默认支持 `--dry-run`，建议先预览再执行
- 文件操作不可逆，建议在操作前备份重要文件
- 脚本仅使用 Python 标准库，无需额外安装
