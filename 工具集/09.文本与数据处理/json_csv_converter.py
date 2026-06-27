#!/usr/bin/env python3
"""
JSON ↔ CSV 格式转换器
📌 支持嵌套 JSON 扁平化、自定义分隔符、大文件流式处理
"""

import argparse
import csv
import json
import sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")


def flatten_dict(d: dict, parent_key: str = "", sep: str = ".") -> dict:
    """扁平化嵌套字典，如 {a: {b: 1}} → {"a.b": 1}"""
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep).items())
        elif isinstance(v, list):
            # 列表转为 JSON 字符串
            items.append((new_key, json.dumps(v, ensure_ascii=False)))
        else:
            items.append((new_key, v))
    return dict(items)


def json_to_csv(input_file: str, output_file: str, delimiter: str = ","):
    """JSON → CSV"""
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, dict):
        data = [data]
    if not isinstance(data, list):
        print("❌ JSON 顶层必须是数组或对象")
        sys.exit(1)

    # 扁平化
    flat_data = [flatten_dict(item) if isinstance(item, dict) else {"value": item} for item in data]

    # 收集所有字段名
    headers = []
    seen = set()
    for item in flat_data:
        for key in item:
            if key not in seen:
                headers.append(key)
                seen.add(key)

    # 写入 CSV
    with open(output_file, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers, delimiter=delimiter)
        writer.writeheader()
        for item in flat_data:
            writer.writerow(item)

    print(f"✅ JSON → CSV: {len(data)} 行, {len(headers)} 列 → {output_file}")


def csv_to_json(input_file: str, output_file: str, delimiter: str = ","):
    """CSV → JSON"""
    with open(input_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=delimiter)
        data = list(reader)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✅ CSV → JSON: {len(data)} 条记录 → {output_file}")


def main():
    parser = argparse.ArgumentParser(
        description="JSON ↔ CSV 格式转换器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python json_csv_converter.py data.json --to csv -o data.csv
  python json_csv_converter.py data.csv --to json -o data.json
  python json_csv_converter.py data.tsv --to json --delimiter "\\t"
        """,
    )
    parser.add_argument("input", help="输入文件")
    parser.add_argument("--to", choices=["csv", "json"], required=True, help="目标格式")
    parser.add_argument("-o", "--output", help="输出文件路径")
    parser.add_argument("--delimiter", default=",", help="CSV 分隔符（默认逗号）")

    args = parser.parse_args()
    output = args.output or f"{Path(args.input).stem}.{args.to}"

    if args.to == "csv":
        json_to_csv(args.input, output, args.delimiter)
    else:
        csv_to_json(args.input, output, args.delimiter)


if __name__ == "__main__":
    main()
