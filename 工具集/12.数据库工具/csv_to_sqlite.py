#!/usr/bin/env python3
"""
CSV 批量导入 SQLite 工具
📌 自动推断列类型、支持批量导入、指定主键
"""

import argparse
import csv
import sqlite3
import sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")


def infer_type(value: str):
    """推断值的 SQLite 类型"""
    if not value or value.strip() == "":
        return "TEXT"
    try:
        int(value)
        return "INTEGER"
    except ValueError:
        pass
    try:
        float(value)
        return "REAL"
    except ValueError:
        pass
    return "TEXT"


def infer_column_types(rows: list, headers: list) -> list:
    """推断每列的类型"""
    types = ["TEXT"] * len(headers)
    for row in rows[:100]:  # 采样前 100 行
        for i, val in enumerate(row):
            t = infer_type(val)
            if t == "REAL" and types[i] == "INTEGER":
                types[i] = "REAL"
            elif t == "TEXT":
                types[i] = "TEXT"
    return types


def import_csv(
    csv_path: str,
    db_path: str,
    table_name: str = None,
    primary_key: str = None,
    overwrite: bool = False,
    delimiter: str = ",",
):
    """导入单个 CSV 文件到 SQLite"""
    path = Path(csv_path)
    if not table_name:
        table_name = path.stem

    # 读取 CSV
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=delimiter)
        headers = next(reader)
        rows = list(reader)

    if not rows:
        print(f"⚠️ {path.name}: 空文件，跳过")
        return

    # 清理列名
    clean_headers = [h.strip().replace(" ", "_").replace("-", "_") for h in headers]

    # 推断类型
    col_types = infer_column_types(rows, clean_headers)

    # 连接数据库
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 删除已有表
    if overwrite:
        cursor.execute(f"DROP TABLE IF EXISTS '{table_name}'")

    # 建表
    columns = []
    for h, t in zip(clean_headers, col_types):
        col_def = f"'{h}' {t}"
        if h == primary_key:
            col_def += " PRIMARY KEY"
        columns.append(col_def)

    create_sql = f"CREATE TABLE IF NOT EXISTS '{table_name}' ({', '.join(columns)})"
    try:
        cursor.execute(create_sql)
    except sqlite3.OperationalError as e:
        print(f"❌ {path.name}: 建表失败 — {e}")
        conn.close()
        return

    # 插入数据
    placeholders = ", ".join(["?"] * len(clean_headers))
    insert_sql = f"INSERT INTO '{table_name}' VALUES ({placeholders})"

    try:
        cursor.executemany(insert_sql, rows)
        conn.commit()
        print(f"✅ {path.name} → {table_name}: {len(rows)} 行, {len(clean_headers)} 列")
    except sqlite3.Error as e:
        print(f"❌ {path.name}: 插入失败 — {e}")

    conn.close()


def batch_import(
    directory: str,
    db_path: str,
    primary_key: str = None,
    overwrite: bool = False,
):
    """批量导入目录下所有 CSV"""
    dir_path = Path(directory)
    csv_files = sorted(dir_path.glob("*.csv"))

    if not csv_files:
        print("⚠️ 没有找到 CSV 文件")
        return

    print(f"📂 目录: {dir_path}")
    print(f"📊 文件: {len(csv_files)} 个")
    print(f"🗄️ 数据库: {db_path}")
    print("-" * 50)

    for csv_file in csv_files:
        import_csv(str(csv_file), db_path, primary_key=primary_key, overwrite=overwrite)

    print("-" * 50)
    print(f"✅ 导入完成")


def main():
    parser = argparse.ArgumentParser(
        description="CSV 批量导入 SQLite",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python csv_to_sqlite.py data.csv --db data.db --table users
  python csv_to_sqlite.py ./csv_files/ --db data.db
  python csv_to_sqlite.py data.csv --db data.db --table items --primary-key id
        """,
    )
    parser.add_argument("input", help="CSV 文件或目录")
    parser.add_argument("--db", required=True, help="SQLite 数据库路径")
    parser.add_argument("--table", help="表名（默认使用文件名）")
    parser.add_argument("--primary-key", help="主键列名")
    parser.add_argument("--overwrite", action="store_true", help="覆盖已有表")
    parser.add_argument("--delimiter", default=",", help="CSV 分隔符")

    args = parser.parse_args()

    p = Path(args.input)
    if p.is_dir():
        batch_import(args.input, args.db, args.primary_key, args.overwrite)
    else:
        import_csv(args.input, args.db, args.table, args.primary_key, args.overwrite, args.delimiter)


if __name__ == "__main__":
    main()
