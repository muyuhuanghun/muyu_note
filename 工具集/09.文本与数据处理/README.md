# 09.文本与数据处理

📌 文本格式转换、差异对比、批量替换等日常文本处理工具。

# ==========================================
# 📁 脚本列表
# ==========================================

| 脚本 | 功能 | 适用场景 |
|------|------|----------|
| `json_csv_converter.py` | JSON ↔ CSV 互转 | 数据格式转换、Excel 兼容 |
| `text_diff.py` | 文本差异对比 | 代码审查、笔记版本对比 |
| `encoding_converter.py` | 文件编码转换 | 乱码修复、GBK/UTF-8 批量转换 |
| `batch_text_replace.py` | 批量文本查找替换 | 重构代码、批量修改笔记 |

# ==========================================
# 🚀 使用示例
# ==========================================

## json_csv_converter.py — 格式转换

```bash
# JSON → CSV
python json_csv_converter.py data.json --to csv -o data.csv

# CSV → JSON
python json_csv_converter.py data.csv --to json -o data.json

# 指定分隔符（TSV）
python json_csv_converter.py data.tsv --to json --delimiter "\t"
```

## text_diff.py — 文本对比

```bash
# 对比两个文件
python text_diff.py old.md new.md

# 并排显示差异
python text_diff.py old.md new.md --side-by-side

# 只显示不同行
python text_diff.py old.md new.md --changes-only

# 输出为 HTML（可浏览器查看）
python text_diff.py old.md new.md --html -o diff.html
```

## encoding_converter.py — 编码转换

```bash
# 检测文件编码
python encoding_converter.py --detect *.txt

# 转换为 UTF-8
python encoding_converter.py --to utf-8 *.txt

# 批量转换目录下所有文件
python encoding_converter.py --to utf-8 --recursive ./课件/

# 预览模式
python encoding_converter.py --to utf-8 --dry-run *.txt
```

## batch_text_replace.py — 批量替换

```bash
# 在文件中批量替换
python batch_text_replace.py ./src/ --old "old_func" --new "new_func"

# 使用正则表达式
python batch_text_replace.py ./src/ --old "def \w+\(" --new "def new_name(" --regex

# 只在 .py 文件中替换
python batch_text_replace.py ./src/ --old "TODO" --new "DONE" --ext .py

# 预览模式
python batch_text_replace.py ./src/ --old "foo" --new "bar" --dry-run
```

# ==========================================
# 💡 Tips
# ==========================================

- JSON/CSV 转换支持嵌套 JSON 的扁平化（如 `user.name` → 列名）
- 编码转换器自动检测源编码，支持中文常见的 GBK/GB2312/GB18030
- 批量替换默认跳过二进制文件，安全可靠
