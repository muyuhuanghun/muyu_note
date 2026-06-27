#!/usr/bin/env python3
"""
简易工作流编排工具
📌 从 YAML 文件加载工作流，按依赖关系串行/并行执行
📌 支持失败重试、超时控制、日志记录
"""

import argparse
import subprocess
import sys
import time
from collections import defaultdict
from datetime import datetime
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")


# 简易 YAML 解析（不依赖 PyYAML）
def parse_yaml_simple(text: str) -> dict:
    """简易 YAML 解析器，只支持基本的 key: value 和列表"""
    result = {}
    current_key = None
    current_list = None
    current_dict = None

    for line in text.split("\n"):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        indent = len(line) - len(line.lstrip())

        if indent == 0 and ":" in stripped:
            key, val = stripped.split(":", 1)
            key = key.strip()
            val = val.strip()
            if val:
                result[key] = val
            else:
                current_key = key
                current_list = []
                result[key] = current_list
            current_dict = None

        elif indent > 0 and current_key and stripped.startswith("- "):
            item = stripped[2:].strip()
            if ":" in item:
                # 字典项
                if current_dict is None:
                    current_dict = {}
                    current_list.append(current_dict)
                k, v = item.split(":", 1)
                current_dict[k.strip()] = v.strip()
            else:
                current_list.append(item)

        elif indent > 0 and current_dict and ":" in stripped:
            k, v = stripped.split(":", 1)
            current_dict[k.strip()] = v.strip()

    return result


def parse_workflow(filepath: str) -> dict:
    """解析工作流 YAML 文件"""
    content = Path(filepath).read_text(encoding="utf-8")

    # 尝试使用 PyYAML
    try:
        import yaml
        return yaml.safe_load(content)
    except ImportError:
        pass

    # 备用：简易解析
    return parse_yaml_simple(content)


def topological_sort(steps: list) -> list:
    """拓扑排序，处理依赖关系"""
    # 构建依赖图
    name_to_step = {s["name"]: s for s in steps}
    in_degree = defaultdict(int)
    graph = defaultdict(list)

    for step in steps:
        name = step["name"]
        deps = step.get("depends_on", [])
        if isinstance(deps, str):
            deps = [deps]
        for dep in deps:
            graph[dep].append(name)
            in_degree[name] += 1
        if name not in in_degree:
            in_degree[name] = 0

    # Kahn 算法
    queue = [n for n, d in in_degree.items() if d == 0]
    result = []

    while queue:
        node = queue.pop(0)
        result.append(node)
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    if len(result) != len(name_to_step):
        print("❌ 检测到循环依赖")
        return []

    return result


def run_step(step: dict, timeout: int = 300) -> bool:
    """执行单个工作流步骤"""
    name = step["name"]
    command = step.get("command", "")
    retries = int(step.get("retries", 0))

    print(f"\n  🚀 [{name}] 开始执行")
    print(f"     命令: {command}")

    for attempt in range(retries + 1):
        if attempt > 0:
            print(f"     🔄 重试 {attempt}/{retries}")

        start = time.time()
        try:
            result = subprocess.run(
                command, shell=True,
                capture_output=True, text=True,
                timeout=timeout,
            )
            elapsed = time.time() - start

            if result.returncode == 0:
                print(f"  ✅ [{name}] 完成 ({elapsed:.1f}s)")
                if result.stdout.strip():
                    for line in result.stdout.strip().split("\n")[:5]:
                        print(f"     {line}")
                return True
            else:
                print(f"  ❌ [{name}] 失败 (退出码 {result.returncode})")
                if result.stderr.strip():
                    for line in result.stderr.strip().split("\n")[:3]:
                        print(f"     {line}")

        except subprocess.TimeoutExpired:
            print(f"  ⏰ [{name}] 超时 ({timeout}s)")

        except Exception as e:
            print(f"  ❌ [{name}] 错误: {e}")

    return False


def execute_workflow(workflow: dict):
    """执行工作流"""
    name = workflow.get("name", "未命名工作流")
    steps = workflow.get("steps", [])

    if not steps:
        print("⚠️ 工作流没有步骤")
        return

    print(f"{'='*50}")
    print(f"🔧 工作流: {name}")
    print(f"📋 步骤数: {len(steps)}")
    print(f"{'='*50}")

    # 拓扑排序
    order = topological_sort(steps)
    if not order:
        return

    name_to_step = {s["name"]: s for s in steps}

    print(f"📌 执行顺序: {' → '.join(order)}")

    total_start = time.time()
    failed = []

    for step_name in order:
        step = name_to_step[step_name]
        timeout = int(step.get("timeout", 300))

        success = run_step(step, timeout)
        if not success:
            failed.append(step_name)
            if step.get("required", False):
                print(f"\n🛑 关键步骤失败，工作流终止")
                break

    total_elapsed = time.time() - total_start

    print(f"\n{'='*50}")
    if failed:
        print(f"⚠️ 工作流完成（有 {len(failed)} 个失败）")
        print(f"   失败步骤: {', '.join(failed)}")
    else:
        print(f"✅ 工作流全部完成！")
    print(f"⏱️ 总耗时: {total_elapsed:.1f}s")


def generate_example():
    """生成示例工作流文件"""
    example = '''# 工作流示例文件
# 支持的字段: name, command, depends_on, retries, timeout, required

name: 数据处理流水线

steps:
  - name: 清洗数据
    command: python clean.py
    timeout: 60

  - name: 训练模型
    command: python train.py
    depends_on: 清洗数据
    timeout: 3600
    retries: 2

  - name: 生成报告
    command: python report.py
    depends_on: 训练模型

  - name: 发送通知
    command: echo "完成！"
    depends_on: 生成报告
'''
    print(example)


def main():
    parser = argparse.ArgumentParser(
        description="简易工作流编排工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python workflow_builder.py workflow.yaml
  python workflow_builder.py --init > my_workflow.yaml
        """,
    )
    parser.add_argument("workflow", nargs="?", help="工作流 YAML 文件")
    parser.add_argument("--init", action="store_true", help="生成示例工作流文件")

    args = parser.parse_args()

    if args.init:
        generate_example()
        return

    if not args.workflow:
        parser.print_help()
        return

    wf = parse_workflow(args.workflow)
    execute_workflow(wf)


if __name__ == "__main__":
    main()
