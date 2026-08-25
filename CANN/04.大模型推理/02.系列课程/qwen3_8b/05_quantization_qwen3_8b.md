---
source_repo: cann-learning-hub
source_path: tutorials/llm_inference/qwen3_8b/05_quantization_qwen3_8b.ipynb
source_commit: 1bf85454ed7c41e184a96fb51d109b6bb83b7c0d
note_kind: notebook_to_markdown
---

# 5 量化Qwen3-8B模型

> 📚 上游 Notebook：[tutorials/llm_inference/qwen3_8b/05_quantization_qwen3_8b.ipynb](https://gitcode.com/cann/cann-learning-hub/blob/master/tutorials/llm_inference/qwen3_8b/05_quantization_qwen3_8b.ipynb)
> 🧪 整理方式：保留 Markdown 与代码单元；省略 Jupyter 执行输出，避免把一次性环境结果误当成可复现结论。

## 🧭 学习目标

- 先跑通功能正确的 Baseline，再用 Profiling 定位瓶颈；
- 理解图模式、融合算子、量化和端到端收益验证。

# ==========================================
## 📖 课程内容

大语言模型（LLM）在推理部署时面临显存占用高、计算量大、推理时延长等挑战。以 Qwen3-8B 为例，其原始权重以 BF16 格式存储，单个参数占用 2 字节，模型权重共需约 16GB 显存，再加上 KV Cache 和运行时开销，对硬件资源的要求较高。

**量化**是工业级大模型部署中降低成本的核心手段之一。其核心思想是将模型中高精度的浮点数（如 BF16/FP32）映射为低精度的整数（如 INT8/INT4），在保留模型推理精度的前提下大幅降低资源消耗。量化的收益主要体现在以下几个方面：

- **降低显存占用**：INT8 仅占 1 字节，相比 BF16 的 2 字节，权重显存占用减半，使得更多请求可并发执行
- **提升计算效率**：INT8 运算的算力密度更高，在昇腾 NPU 上可充分利用 INT8 专用计算单元
- **增加吞吐量**：更小的模型体积和更高的计算效率，使得单位时间内可处理更多请求
- **降低推理时延**：减少数据搬运量和计算时间，单次推理响应更快

**W8A8** 是当前工业界最广泛部署的量化方案，其中 "W" 代表权重（Weight），"A" 代表激活（Activation），"8" 表示 INT8。W8A8 将模型权重和激活值统一量化为 INT8 类型，相比仅量化权重的 W8A16 方案，能同时减少权重存储和激活计算的开销，实现更高的加速比。

本章将以 Qwen3-8B 模型为例，使用昇腾量化工具 AMCT（Ascend Model Compression Toolkit）将其 BF16 权重导出为 W8A8 INT8 量化权重，并通过 recipes 推理框架完成量化模型的推理与性能评估。具体内容如下：

- **环境准备**：配置 CANN 环境变量与运行目录
- **模型权重量化**：使用 AMCT 工具将 Qwen3-8B BF16 权重导出为 W8A8 INT8 量化权重
- **量化模型推理**：基于 recipes 框架加载量化权重，验证推理功能
- **量化模型 profiling 结果分析**：通过 profiling 工具分析量化模型的算子执行情况与性能瓶颈

---

### 1 环境准备

准备运行目录，把 CANN 环境变量导入当前 Notebook。

```python
import json
import os
import subprocess
import sys
from pathlib import Path

print('[环境准备] 开始', flush=True)

def locate_repo_root():
    repo_roots = []
    try:
        cwd = Path.cwd()
        lineage = [cwd, *cwd.parents]
        repo_roots.extend(lineage)
        repo_roots.extend(base / 'cann-learning-hub' for base in lineage)
        for base in lineage:
            try:
                repo_roots.extend(base.glob('*/cann-learning-hub'))
            except OSError:
                pass
    except FileNotFoundError:
        pass
    repo_roots.append(Path('/opt/atomgit/cann-learning-hub'))

    seen = set()
    for repo_root in repo_roots:
        key = str(repo_root)
        if key in seen:
            continue
        seen.add(key)
        if (repo_root / 'tutorials/llm_inference/qwen3_8b/src').exists():
            return repo_root
    raise FileNotFoundError('Cannot locate cann-learning-hub repository root.')

REPO_ROOT = locate_repo_root()
os.chdir(REPO_ROOT)
TUTORIAL_DIR = REPO_ROOT / 'tutorials' / 'llm_inference' / 'qwen3_8b'
os.environ['TUTORIAL_DIR'] = str(TUTORIAL_DIR)
TUTORIAL_SRC_DIR = TUTORIAL_DIR / 'src'
if str(TUTORIAL_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(TUTORIAL_SRC_DIR))

if not os.environ.get('ASCEND_TOOLKIT_HOME'):
    raise EnvironmentError('ASCEND_TOOLKIT_HOME is not set. Please activate the CANN environment.')
print('CANN包路径 =', os.environ.get('ASCEND_TOOLKIT_HOME'))
cann_script = Path(os.environ['ASCEND_TOOLKIT_HOME']) / 'set_env.sh'
env_cmd = f'source {cann_script} && env'
env = subprocess.check_output(f"bash -lc '{env_cmd}'", shell=True, text=True, cwd=REPO_ROOT)
for line in env.splitlines():
    if '=' in line:
        os.environ.__setitem__(*line.split('=', 1))

RECIPE_ROOT = TUTORIAL_DIR / 'src/inference_scripts/recipe_qwen3_8b'

print('教程目录 =', TUTORIAL_DIR)
os.environ['RECIPE_ROOT'] = str(RECIPE_ROOT)
print('推理模型目录 =', RECIPE_ROOT)
print('[环境准备] 完成', flush=True)
```

### 2 模型权重量化

本节使用昇腾量化工具 [AMCT(Ascend Model Compression Toolkit)](https://gitcode.com/cann/amct) 将已有的 Qwen3-8B BF16 权重导出为 W8A8 INT8 量化权重，在下一节用 recipes 框架跑通量化模型推理。

W8A8 INT8 量化将模型权重和激活值从 BF16/FP32 压缩为 INT8，减少内存占用和计算量。昇腾官方大模型量化工具 AMCT 支持通过命令行直接导出 Qwen3-8B W8A8 部署权重，输出目录为 HuggingFace 风格的 compressed-tensors 目录结构，recipes 框架可直接加载。

本章需复用前置章节的非量化模型权重。下方的下载命令会将非量化模型的权重下载到 resolved_model_path 路径下, 如该路径下已下载 Qwen3-8B 非量化模型权重，会复用已下载权重。

```python
from inference_scripts.recipe_workflow import resolve_model_path
#下载非量化模型权重
MODEL_ID = os.environ.get('QWEN3_8B_MODEL_PATH') or 'Qwen/Qwen3-8B'
resolved_model_path, model_source = resolve_model_path(str(MODEL_ID), quiet_model_io=False)
```

使用 AMCT 通过命令行直接导出 Qwen3-8B W8A8 INT8 部署权重。流程主要包含如下三步：
1. 获取 AMCT 源码 
2. 安装 AMCT 依赖
3. 导出 Qwen3-8B W8A8 部署权重

运行下方code cell获取AMCT源码并安装AMCT依赖：

```python
import os
import subprocess
import sys
from pathlib import Path

print('[AMCT 量化] 开始')

# 克隆 AMCT 源码
AMCT_DIR = Path(os.environ['TUTORIAL_DIR']) / 'src/amct'
if not AMCT_DIR.exists():
    print('[AMCT] 克隆源码...')
    subprocess.check_call(['git', 'clone', 'https://gitcode.com/cann/amct.git', str(AMCT_DIR)])

# 安装 AMCT 依赖
print('[AMCT] 安装依赖...')
subprocess.check_call([
    sys.executable, '-m', 'pip', 'install', '-r', str(AMCT_DIR / 'requirements.txt'),
    '-i', 'https://pypi.tuna.tsinghua.edu.cn/simple',
    '--trusted-host', 'pypi.tuna.tsinghua.edu.cn',
    '--extra-index-url', 'https://download.pytorch.org/whl/cpu'
])
subprocess.check_call([
    sys.executable, '-m', 'pip', 'install', 'setuptools<82',
    '-i', 'https://pypi.tuna.tsinghua.edu.cn/simple',
    '--trusted-host', 'pypi.tuna.tsinghua.edu.cn',
])
subprocess.check_call([
    sys.executable, '-m', 'pip', 'install',
    '--no-deps', '--ignore-installed', 'torchaudio==2.7.1',
    '-i', 'https://pypi.tuna.tsinghua.edu.cn/simple',
    '--trusted-host', 'pypi.tuna.tsinghua.edu.cn',
])
```

运行下方code cell导出 Qwen3-8B W8A8 部署权重，其中`--model`指定的是非量化模型权重的路径，`--output_dir`指定的是导出的量化模型权重的路径，在执行时可根据实际情况自行修改这两个参数：

**注意：需要将`--model`的参数指定为本地的非量化模型权重的路径**

```python
# 执行 W8A8 量化导出
print('[AMCT] 执行量化导出...')
W8A8_WEIGHT = Path(os.environ['TUTORIAL_DIR']) / 'src/data/models' / 'Qwen3-8B-W8A8'
deploy_env = os.environ.copy()
deploy_env['PYTHONPATH'] = str(AMCT_DIR)
subprocess.check_call([
    sys.executable, '-m', 'amct_pytorch.deploy',
    '--model', resolved_model_path,
    '--model_name', 'qwen3',
    '--granularity', 'block',
    '--quant_target', 'attn-linear', 'mlp',
    '--quant_dtype', 'int',
    '--bit_config', 'amct_pytorch/configs/w8a8.yaml',
    '--output_dir', str(W8A8_WEIGHT),
], cwd=str(AMCT_DIR), env=deploy_env)

print(f'[AMCT 量化] 完成，W8A8 权重目录 = {W8A8_WEIGHT}')
```

### 3 量化模型推理

#### 3.1 依赖安装

安装推理所需的依赖：

```bash
%pip install -r {RECIPE_ROOT}/models/qwen/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn
```

#### 3.2 准备 W8A8 推理 YAML

W8A8 量化推理使用与 BF16 推理相同的 recipes 框架，但需要使用 W8A8 量化模型路径和适配的 YAML 配置。量化配置由权重目录 `config.json` 内嵌的 `quantization_config` 自动加载，YAML 无需显式声明量化参数。

通过如下操作将 YAML 配置中的模型路径指定为量化权重路径 `W8A8_WEIGHT`：

**注意：需要将`W8A8_WEIGHT`指定为本地的量化模型权重的路径**

```python
from inference_scripts.recipe_workflow import prepare_runtime_yaml
# 指定量化模型权重的路径
W8A8_WEIGHT = TUTORIAL_DIR / 'src/data/models/Qwen3-8B-W8A8'
# 指定yaml配置模板的路径
YAML_A8W8_TEMPLATE = RECIPE_ROOT / 'models/qwen/config/qwen3_8b_a8w8_1tp.yaml'
# 指定修改后的yaml配置的路径
YAML_A8W8 = RECIPE_ROOT / 'models/qwen/config/qwen3_8b_a8w8.yaml'
# 设置量化模型yaml配置中的模型权重路径
prepare_runtime_yaml(YAML_A8W8_TEMPLATE, YAML_A8W8, model_path=str(W8A8_WEIGHT))
```

#### 3.3 执行量化推理

调用infer.sh执行量化推理，查看 W8A8 量化模型推理生成的文本，确认量化推理正常运行。

```python
import sys, subprocess, os

env = os.environ.copy()
python_dir = os.path.dirname(sys.executable)
env["PATH"] = python_dir + ":" + env.get("PATH", "")
result = subprocess.run(
    ['bash', 'executor/scripts/infer.sh', '--model', 'qwen', '--yaml', YAML_A8W8],
    cwd=str(RECIPE_ROOT),
    env=env,
    check=True,
)
```

### 4 量化模型 profiling 结果分析

本节使用 profiling 工具观测量化模型的推理性能。完成带 Profiler 的推理后，会在结果目录中生成 `prof/` 产物。

推理完成后，定位 `prof/` 目录，重点关注其中的 `op_statistic.csv` 和 `kernel_details.csv` 这两个文件。`op_statistic.csv` 中展示了模型调用的所有算子的统计信息，`kernel_details.csv` 中展示了详细的接口调用信息。

首先基于 `op_statistic.csv` 分析量化 Qwen3-8B 模型中耗时占比最高的算子，定位性能瓶颈；然后进一步根据 `kernel_details.csv` 分析该算子的输入输出规格，归纳其调用模式，最终推导出自定义算子 `QmmCustom` 的原型定义，从而明确下一章的自定义算子开发的需求来源。

#### 4.1 进行 Profiling 推理

沿用 recipes 的 YAML + `infer.sh` 工作流，在配置中打开 Profiler，运行一次推理并收集性能数据。

通过如下操作将量化模型 YAML 配置中的enable_profiler配置为 True ，并启动带 Profiler 的推理：

```python
from inference_scripts.recipe_workflow import prepare_profiling_yaml

#准备量化模型YAML
YAML_A8W8_PROFILER = RECIPE_ROOT / 'models/qwen/config/qwen3_8b_a8w8_profiler.yaml'
prepare_profiling_yaml(YAML_A8W8, YAML_A8W8_PROFILER, enable_profiler=True)     #打开量化模型yaml配置中的profiler开关

result = subprocess.run(
    ['bash', 'executor/scripts/infer.sh', '--model', 'qwen', '--yaml', YAML_A8W8_PROFILER],
    cwd=str(RECIPE_ROOT),
    env=env,
    check=True,
)
```

#### 4.2 基于op_statistic.csv分析算子调用

生成的profiling结果在 `prof/` 目录下，重点关注其中的 `op_statistic.csv` 和 `kernel_details.csv` 这两个文件。

`op_statistic.csv` 是昇腾 Profiler 生成的算子级统计汇总文件，记录了推理过程中每个算子的调用次数、总耗时、最小/平均/最大耗时及耗时占比（Ratio）。通过分析该文件，我们可以快速定位模型推理的性能瓶颈——即哪些算子消耗了最多的计算时间。

对于量化模型而言，由于权重和激活值从 BF16 压缩为 INT8，矩阵乘法类算子的计算模式发生了变化：原本的 BF16 Matmul 被替换为 INT8 量化矩阵乘法算子 `QuantBatchMatmulV3`。通过 op_statistic.csv 分析量化模型的算子分布，可以直观了解量化后的算子调用特征，并识别出耗时占比最高的关键算子，为后续的自定义算子优化提供方向。

下方代码分别读取 Prefill 和 Decode 阶段的 `op_statistic.csv`，展示按耗时占比排序的前十类算子：

```python
import pandas as pd
from pathlib import Path

RES_DIR = RECIPE_ROOT / 'models/qwen/res'

# 取最新的 profiling 结果目录
result_dirs = sorted([d for d in RES_DIR.iterdir() if d.is_dir()], key=lambda d: d.name, reverse=True)
latest_result = result_dirs[0]

def find_op_statistic_csv(phase_dir):
    matches = sorted(phase_dir.rglob('op_statistic.csv'), key=lambda p: p.parent.parent.name, reverse=True)
    return matches[0] if matches else None

prefill_op_csv = find_op_statistic_csv(latest_result / 'qwen3_8b_qwen3_8b_a8w8_profiler/prof/prefill')
decode_op_csv = find_op_statistic_csv(latest_result / 'qwen3_8b_qwen3_8b_a8w8_profiler/prof/decode')

if prefill_op_csv:
    prefill_op_df = pd.read_csv(prefill_op_csv)
    print(f'Prefill op_statistic.csv 路径: {prefill_op_csv}')
    print(f'Prefill op_statistic.csv 前十行:')
    display(prefill_op_df.head(10))
else:
    print('Prefill op_statistic.csv 未找到')

if decode_op_csv:
    decode_op_df = pd.read_csv(decode_op_csv)
    print(f'Decode op_statistic.csv 路径: {decode_op_csv}')
    print(f'Decode op_statistic.csv 前十行:')
    display(decode_op_df.head(10))
else:
    print('Decode op_statistic.csv 未找到')
```

从op_statistic.csv中统计的算子调用信息可见，QuantBatchMatmulV3(CANN内置的量化matmul算子)是整个模型推理过程中调用耗时占比最高的算子。

#### 4.3 基于kernel_details.csv分析算子原型

在 4.2 节中，我们通过 `op_statistic.csv` 已确认 `QuantBatchMatmulV3` 是量化模型中耗时占比最高的算子。然而 `op_statistic.csv` 仅提供算子级别的宏观统计（调用次数、总耗时），缺少具体的输入输出规格。要理解该算子的完整行为，我们需要从 `kernel_details.csv` 中提取每次调用的详细参数——包括输入输出的 Shape、Data Type 和 Format。

这些信息至关重要：它们构成了算子的"原型定义"，即算子需要接收什么、输出什么。正如软件开发中需要先明确接口规格再进行编码，自定义算子的开发同样需要从实际调用数据中归纳出完整的原型定义，才能确保开发出的算子能无缝接入模型推理流程。

下方代码筛选 `QuantBatchMatmulV3` 的所有调用记录，按 Input Shapes 分组统计其在 Prefill 和 Decode 阶段的输入输出规格与平均耗时：

```python
import pandas as pd
from pathlib import Path

RES_DIR = RECIPE_ROOT / 'models/qwen/res'

# 取最新的 profiling 结果目录
result_dirs = sorted([d for d in RES_DIR.iterdir() if d.is_dir()], key=lambda d: d.name, reverse=True)
latest_result = result_dirs[0]
print(f'最新结果目录: {latest_result}')

def find_kernel_csv(phase_dir):
    matches = sorted(phase_dir.rglob('kernel_details.csv'), key=lambda p: p.parent.parent.name, reverse=True)
    return matches[0] if matches else None

prefill_csv = find_kernel_csv(latest_result / 'qwen3_8b_qwen3_8b_a8w8_profiler/prof/prefill')
decode_csv = find_kernel_csv(latest_result / 'qwen3_8b_qwen3_8b_a8w8_profiler/prof/decode')
assert prefill_csv and decode_csv, 'kernel_details.csv 未找到，请确认 profiling 已完成'
print(f'Prefill CSV: {prefill_csv}')
print(f'Decode CSV: {decode_csv}')

# 读取 CSV 并筛选 QuantBatchMatmulV3 算子
prefill_df = pd.read_csv(prefill_csv)
decode_df = pd.read_csv(decode_csv)

prefill_qmm = prefill_df[prefill_df['Type'] == 'QuantBatchMatmulV3'].copy()
decode_qmm = decode_df[decode_df['Type'] == 'QuantBatchMatmulV3'].copy()

# 按 Input Shapes 分组，统计每种 shape 下的平均 Duration
def qmm_duration_stats(df, phase):
    stats = df.groupby(['Input Shapes', 'Input Data Types','Input Formats','Output Shapes','Output Data Types'])['Duration(us)'].agg(['mean', 'count']).reset_index()
    stats.columns = ['Input Shapes', 'Input Data Types','Input Formats','Output Shapes','Output Data Types', 'Avg Duration(us)', 'Calls']
    stats = stats.sort_values('Avg Duration(us)', ascending=False).reset_index(drop=True)
    stats.insert(0, 'Phase', phase)
    return stats

prefill_stats = qmm_duration_stats(prefill_qmm, 'Prefill')
decode_stats = qmm_duration_stats(decode_qmm, 'Decode')

combined = pd.concat([prefill_stats, decode_stats], ignore_index=True)
display(combined.style.set_caption('QuantBatchMatmulV3 算子调用情况'))
```

从上表的 `QuantBatchMatmulV3` 调用数据中，我们可以归纳出该算子的核心行为模式：

- **输入始终包含三个核心张量**：`x1`（INT8, ND 格式）为激活矩阵 A，`x2`（INT8, **FRACTAL_NZ** 格式）为权重矩阵 B，`scale`（FLOAT32, ND 格式）为 per-channel 缩放系数。其中 FRACTAL_NZ 是昇腾 NPU 针对 INT8 矩阵乘法优化的特殊存储格式，将权重按 16×32 分块重排，以充分利用 AI Core 的 Cube 计算单元。

- **pertoken_scale 决定输出类型**：部分调用模式携带第 4 个输入 `pertoken_scale`（FLOAT32, ND 格式），此时输出为 BF16——INT32 中间结果经 perTokenScale 反量化回低精度浮点；不含该输入时输出为 INT32，保留整型结果供后续算子继续处理。

- **Shape 随推理阶段和模型层级变化**：Prefill 阶段 M 维度较大（如 50），Decode 阶段 M=1；K 和 N 取值取决于具体层的隐藏维度与投影维度。

现在让我们模拟一个实际的需求分析场景：假设我们正在部署一个 W8A8 量化的大语言模型，推理过程中需要调用 INT8 量化矩阵乘法算子。通过 Profiling 分析，我们发现该模型对底层算子的调用规格恰好如上表所示——即需要一种能同时支持"INT32 输出"和"perTokenScale 反量化输出"两种模式的量化 Matmul 算子。

然而，现有框架中可能没有完全匹配该规格的算子实现，或者我们需要针对特定硬件平台进行深度优化。此时，就需要开发一个自定义算子 `QmmCustom` 来满足这一需求。从 Profiling 数据中归纳出的输入输出规格，自然就成为 `QmmCustom` 的原型定义：

| 算子名称 | QmmCustom |
|------|-----|
| 输入 x1 (A) | INT8, ND 格式, shape [M, K] |
| 输入 x2 (B) | INT8, **FRACTAL_NZ** 格式, shape [K, N] |
| 输入 scale | FLOAT32, ND 格式, shape [N] |
| 输入 pertoken_scale | FLOAT32, ND 格式, shape [M]（可选） |
| 输出 y | 有 perTokenScale → BF16，无 → INT32；ND 格式, shape [M, N] |
| 架构 | ascend910b |

---

#### 小结

本章完成了 Qwen3-8B 模型的权重量化，通过 AMCT 工具将 BF16 权重导出为 W8A8 INT8 量化权重，并验证了量化模型的推理功能。随后通过 Profiling 分析定位到耗时占比最高的算子——量化 matmul（`QuantBatchMatmulV3`），并从 `kernel_details.csv` 中归纳出该算子的输入输出规格，推导出自定义算子 `QmmCustom` 的原型定义。

在下一章中，我们将基于本章归纳的算子原型，完成 `QmmCustom` 算子的 Tiling 设计、Kernel 实现、编译与测试，并将其接入 Qwen3-8B 量化模型，验证自定义算子在模型推理中的功能正确性与性能表现。

# ==========================================
## 📝 练习与验证

> 📌 原 Notebook 中的练习、编译命令和校验代码已按原顺序保留在上文。需要 CANN 运行时、Ascend NPU 或 CANNLab 环境的单元，执行前请先核对版本和设备条件。
