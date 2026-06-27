#!/usr/bin/env python3
"""
SQLite 数据库查看器
📌 查看表结构、执行查询、导出数据、交互式 SQL 终端
"""

import argparse
import csv
import sqlite3
import sys

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")


def list_tables(db_path: str):
    """列出所有表"""
    conn = sqlite3.connect(db_path)
    cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = [row[0] for row in cursor.fetchall()]
    conn.close()

    print(f"📊 数据库: {db_path}")
    print(f"📋 表数量: {len(tables)}\n")
    for t in tables:
        print(f"  - {t}")


def show_schema(db_path: str, table: str):
    """查看表结构"""
    conn = sqlite3.connect(db_path)
    cursor = conn.execute(f"PRAGMA table_info('{table}')")
    columns = cursor.fetchall()

    # 行数
    cursor = conn.execute(f"SELECT COUNT(*) FROM '{table}'")
    row_count = cursor.fetchone()[0]
    conn.close()

    print(f"📋 表: {table}（{row_count} 行）\n")
    print(f"{'序号':<6} {'列名':<20} {'类型':<15} {'非空':<6} {'默认值':<15} {'主键':<6}")
    print("-" * 70)
    for col in columns:
        cid, name, dtype, notnull, default, pk = col
        print(f"  {cid:<4} {name:<20} {dtype:<15} {'是' if notnull else '否':<6} {str(default or ''):<15} {'是' if pk else '否'}")


def query_db(db_path: str, sql: str, fmt: str = "text", output: str = None):
    """执行查询"""
    conn = sqlite3.connect(db_path)
    try:
        cursor = conn.execute(sql)
        rows = cursor.fetchall()
        headers = [desc[0] for desc in cursor.description] if cursor.description else []
    except sqlite3.Error as e:
        print(f"❌ SQL 错误: {e}")
        conn.close()
        return
    finally:
        conn.close()

    if not headers:
        print("✅ 查询执行成功（无返回数据）")
        return

    if output:
        with open(output, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(rows)
        print(f"✅ 导出 {len(rows)} 行 → {output}")
        return

    if fmt == "md":
        print(f"| {' | '.join(headers)} |")
        print(f"|{'|'.join(['------'] * len(headers))}|")
        for row in rows[:50]:
            print(f"| {' | '.join(str(v) for v in row)} |")
    else:
        # 计算列宽
        widths = [len(h) for h in headers]
        for row in rows[:50]:
            for i, val in enumerate(row):
                widths[i] = max(widths[i], len(str(val)))

        # 表头
        header_line = " | ".join(h.ljust(widths[i]) for i, h in enumerate(headers))
        print(header_line)
        print("-" * len(header_line))

        # 数据
        for row in rows[:50]:
            print(" | ".join(str(v).ljust(widths[i]) for i, v in enumerate(row)))

    if len(rows) > 50:
        print(f"\n... 共 {len(rows)} 行，只显示前 50 行")
    else:
        print(f"\n📊 共 {len(rows)} 行")


def interactive_mode(db_path: str):
    """交互式 SQL 终端"""
    conn = sqlite3.connect(db_path)
    print(f"🗄️ SQLite 交互终端: {db_path}")
    print(f"💡 输入 SQL 语句执行，输入 .quit 退出，.tables 查看表\n")

    while True:
        try:
            sql = input("sqlite> ").strip()
        except (EOFError, KeyboardInterrupt):
            break

        if not sql:
            continue
        if sql == ".quit":
            break
        if sql == ".tables":
            list_tables(db_path)
            continue
        if sql.startswith(".schema "):
            table = sql.split(" ", 1)[1]
            show_schema(db_path, table)
            continue

        try:
            cursor = conn.execute(sql)
            if cursor.description:
                rows = cursor.fetchall()
                headers = [d[0] for d in cursor.description]
                if rows:
                    widths = [max(len(h), max(len(str(r[i])) for r in rows[:20])) for i, h in enumerate(headers)]
                    print(" | ".join(h.ljust(widths[i]) for i, h in enumerate(headers)))
                    print("-" * sum(w + 3 for w in widths))
                    for row in rows[:20]:
                        print(" | ".join(str(v).ljust(widths[i]) for i, v in enumerate(row)))
                    if len(rows) > 20:
                        print(f"... 共 {len(rows)} 行")
                else:
                    print("(空结果集)")
            else:
                conn.commit()
                print("✅ 执行成功")
        except sqlite3.Error as e:
            print(f"❌ {e}")

    conn.close()
    print("👋 再见")


def main():
    parser = argparse.ArgumentParser(description="SQLite 数据库查看器")
    parser.add_argument("db", help="数据库文件路径")
    parser.add_argument("--tables", action="store_true", help="列出所有表")
    parser.add_argument("--schema", help="查看表结构")
    parser.add_argument("--query", "-q", help="执行 SQL 查询")
    parser.add_argument("--export", help="导出表为 CSV")
    parser.add_argument("--format", choices=["text", "md"], default="text", help="输出格式")
    parser.add_argument("-o", "--output", help="输出文件")
    parser.add_argument("--interactive", "-i", action="store_true", help="交互式终端")

    args = parser.parse_args()

    if args.tables:
        list_tables(args.db)
    elif args.schema:
        show_schema(args.db, args.schema)
    elif args.query:
        query_db(args.db, args.query, args.format, args.output)
    elif args.export:
        query_db(args.db, f"SELECT * FROM '{args.export}'", output=args.output or f"{args.export}.csv")
    elif args.interactive:
        interactive_mode(args.db)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
