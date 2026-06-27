# 12.数据库工具

📌 SQLite 轻量级数据库操作工具，适合课程作业和小规模数据管理。

# ==========================================
# 📁 脚本列表
# ==========================================

| 脚本 | 功能 | 适用场景 |
|------|------|----------|
| `sqlite_viewer.py` | SQLite 数据库查看器 | 查看表结构、执行查询、导出数据 |
| `csv_to_sqlite.py` | CSV 批量导入 SQLite | 数据库课程作业、数据分析 |
| `db_diff.py` | 数据库结构差异对比 | 数据库迁移、版本管理 |

# ==========================================
# 🚀 使用示例
# ==========================================

## sqlite_viewer.py — 数据库查看

```bash
# 列出所有表
python sqlite_viewer.py data.db --tables

# 查看表结构
python sqlite_viewer.py data.db --schema users

# 查询数据
python sqlite_viewer.py data.db --query "SELECT * FROM users LIMIT 10"

# 导出为 CSV
python sqlite_viewer.py data.db --export users -o users.csv

# 交互式 SQL 终端
python sqlite_viewer.py data.db --interactive
```

## csv_to_sqlite.py — CSV 导入

```bash
# 导入单个 CSV
python csv_to_sqlite.py data.csv --db data.db --table users

# 批量导入目录下所有 CSV（文件名即表名）
python csv_to_sqlite.py ./csv_files/ --db data.db

# 指定主键
python csv_to_sqlite.py data.csv --db data.db --table items --primary-key id

# 覆盖已有表
python csv_to_sqlite.py data.csv --db data.db --table users --overwrite
```

## db_diff.py — 结构对比

```bash
# 对比两个数据库的表结构差异
python db_diff.py old.db new.db

# 只对比指定表
python db_diff.py old.db new.db --tables users,orders

# 输出 SQL 迁移脚本
python db_diff.py old.db new.db --migration -o migrate.sql
```

# ==========================================
# 💡 Tips
# ==========================================

- SQLite 是 Python 内置的，无需安装任何数据库服务器
- `csv_to_sqlite.py` 自动推断列类型（INTEGER/REAL/TEXT）
- `sqlite_viewer.py` 的交互式终端支持 Tab 补全和历史记录
