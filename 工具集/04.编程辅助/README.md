# 04.编程辅助

📌 编程效率工具，从项目初始化到测试运行。

# ==========================================
# 📁 脚本列表
# ==========================================

| 脚本 | 功能 | 适用场景 |
|------|------|----------|
| `code_template_gen.py` | 常用数据结构/算法代码模板生成 | 刷题、竞赛、课程作业 |
| `auto_test_runner.py` | 批量运行测试用例并对拍 | OJ题目验证、Debug |
| `project_scaffold.py` | 项目目录脚手架生成 | 新项目快速启动 |

# ==========================================
# 🚀 使用示例
# ==========================================

## code_template_gen.py — 代码模板

```bash
# 生成 Python 快速排序模板
python code_template_gen.py --lang python --template quicksort

# 生成 C++ 图论模板（邻接表 + BFS/DFS）
python code_template_gen.py --lang cpp --template graph

# 列出所有可用模板
python code_template_gen.py --list
```

📌 支持的模板类型：排序算法、树、图、DP、字符串、数学

## auto_test_runner.py — 自动测试

```bash
# 对拍：对比两个程序的输出
python auto_test_runner.py --prog1 "./solution.exe" --prog2 "./brute.exe" --cases 100

# 批量运行测试用例
python auto_test_runner.py --prog "./solution.exe" --input-dir tests/ --output-dir outputs/

# 生成随机测试数据
python auto_test_runner.py --generate --template "rand_array(n=100, range=1..1000)"
```

## project_scaffold.py — 项目脚手架

```bash
# 生成 Python 项目结构
python project_scaffold.py my_project --type python

# 生成 C++ CMake 项目
python project_scaffold.py my_cpp_project --type cpp-cmake

# 生成 PyTorch 深度学习项目
python project_scaffold.py my_dl_project --type pytorch
```

# ==========================================
# 💡 Tips
# ==========================================

- 代码模板可以直接复制到 LeetCode/icoding 等平台使用
- 对拍脚本是竞赛 Debug 的利器——先写暴力解，再对比优化解
- PyTorch 项目模板包含 train/eval/logging/checkpoint 的标准结构
