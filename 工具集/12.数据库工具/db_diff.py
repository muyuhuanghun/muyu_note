#!/usr/bin/env python3
"""
数据库结构差异对比工具
📌 对比两个 SQLite 数据库的表结构差异，生成 SQL 迁移脚本
"""

import argparse
import sqlite3
import sys

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")


def get_schema(db_path: str) -> dict:
    """获取数据库所有表的结构"""
    conn = sqlite3.connect(db_path)
    cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = {}

    for (table_name,) in cursor.fetchall():
        cursor2 = conn.execute(f"PRAGMA table_info('{table_name}')")
        columns = {}
        for col in cursor2.fetchall():
            columns[col[1]] = {
                "type": col[2],
                "notnull": bool(col[3]),
                "default": col[4],
                "pk": bool(col[5]),
            }
        tables[table_name] = columns

    conn.close()
    return tables


def diff_databases(db1: str, db2: str, tables_filter: list = None, migration: str = None):
    """对比两个数据库"""
    schema1 = get_schema(db1)
    schema2 = get_schema(db2)

    all_tables = set(list(schema1.keys()) + list(schema2.keys()))
    if tables_filter:
        all_tables = all_tables.intersection(tables_filter)

    diff_found = False
    migration_sql = []

    for table in sorted(all_tables):
        in_db1 = table in schema1
        in_db2 = table in schema2

        if in_db1 and not in_db2:
            print(f"  ➕ 新增表: {table}")
            migration_sql.append(f"-- 新增表 {table}")
            cols = schema2[table]
            col_defs = []
            for col_name, col_info in cols.items():
                parts = [f"'{col_name}' {col_info['type']}"]
                if col_info["pk"]:
                    parts.append("PRIMARY KEY")
                if col_info["notnull"]:
                    parts.append("NOT NULL")
                if col_info["default"] is not None:
                    parts.append(f"DEFAULT {col_info['default']}")
                col_defs.append(" ".join(parts))
            migration_sql.append(f"CREATE TABLE '{table}' ({', '.join(col_defs)});\n")
            diff_found = True

        elif not in_db1 and in_db2:
            print(f"  ➖ 删除表: {table}")
            migration_sql.append(f"DROP TABLE IF EXISTS '{table}';\n")
            diff_found = True

        else:
            # 对比列
            cols1 = schema1[table]
            cols2 = schema2[table]
            all_cols = set(list(cols1.keys()) + list(cols2.keys()))

            table_diff = False
            for col in sorted(all_cols):
                in_c1 = col in cols1
                in_c2 = col in cols2

                if in_c1 and not in_c2:
                    print(f"  📋 {table}: 新增列 {col}")
                    migration_sql.append(f"ALTER TABLE '{table}' ADD COLUMN '{col}' {cols2[col]['type']};")
                    diff_found = True
                    table_diff = True

                elif not in_c1 and in_c2:
                    print(f"  📋 {table}: 删除列 {col}")
                    diff_found = True
                    table_diff = True

                elif cols1[col] != cols2[col]:
                    print(f"  📋 {table}: 修改列 {col}")
                    print(f"      旧: {cols1[col]}")
                    print(f"      新: {cols2[col]}")
                    diff_found = True
                    table_diff = True

            if table_diff:
                migration_sql.append("")

    if not diff_found:
        print("✅ 两个数据库结构完全相同")
    elif migration:
        with open(migration, "w", encoding="utf-8") as f:
            f.write("-- 数据库迁移脚本\n")
            f.write(f"-- 从: {db1}\n")
            f.write(f"-- 到: {db2}\n\n")
            f.write("\n".join(migration_sql))
        print(f"\n📄 迁移脚本已保存: {migration}")


def main():
    parser = argparse.ArgumentParser(
        description="数据库结构差异对比",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python db_diff.py old.db new.db
  python db_diff.py old.db new.db --tables users,orders
  python db_diff.py old.db new.db --migration -o migrate.sql
        """,
    )
    parser.add_argument("db1", help="数据库 1（旧）")
    parser.add_argument("db2", help="数据库 2（新）")
    parser.add_argument("--tables", help="只对比指定表（逗号分隔）")
    parser.add_argument("--migration", action="store_true", help="生成迁移脚本")
    parser.add_argument("-o", "--output", help="迁移脚本输出路径")

    args = parser.parse_args()

    tables = args.tables.split(",") if args.tables else None
    migration = args.output if args.migration else None
    diff_databases(args.db1, args.db2, tables, migration)


if __name__ == "__main__":
    main()
