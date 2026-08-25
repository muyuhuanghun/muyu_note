---
source_repo: cann-learning-hub
source_path: tutorials/llm_inference/qwen3_8b/02_baseline_inference.ipynb
source_commit: 1bf85454ed7c41e184a96fb51d109b6bb83b7c0d
note_kind: notebook_to_markdown
---

# 2 Baseline 跑通

> 📚 上游 Notebook：[tutorials/llm_inference/qwen3_8b/02_baseline_inference.ipynb](https://gitcode.com/cann/cann-learning-hub/blob/master/tutorials/llm_inference/qwen3_8b/02_baseline_inference.ipynb)
> 🧪 整理方式：保留 Markdown 与代码单元；省略 Jupyter 执行输出，避免把一次性环境结果误当成可复现结论。

## 🧭 学习目标

- 先跑通功能正确的 Baseline，再用 Profiling 定位瓶颈；
- 理解图模式、融合算子、量化和端到端收益验证。

# ==========================================
## 📖 课程内容

本章使用课程内置的 cann-recipes-infer 推理框架在 NPU 上运行 `Qwen3-8B` 离线推理。完成后会得到指标文件和生成文本文件，作为后续 Profiling 分析与优化 A/B 对比的基线。

### 1 环境与工作区准备
定位教程目录，创建本次实验的运行目录，并把 CANN 环境变量导入当前 Notebook 进程。运行目录指 `Sources/model_inference_optimization/qwen3_8b`，用于保存 Notebook 生成的临时 YAML、推理日志、metrics、outputs 和后续 Profiling 结果；课程模板和源码在 `tutorials/llm_inference/qwen3_8b`。模型权重在执行推理前写入 recipes YAML；没有本地权重时，会先通过默认 ModelScope 通道获取 `Qwen/Qwen3-8B`。

```python
import json
import os
import subprocess
import sys
from pathlib import Path

print('[环境准备] 开始', flush=True)
os.environ.setdefault('QWEN3_8B_DOWNLOAD_BACKEND', 'modelscope')
os.environ['TOKENIZERS_PARALLELISM'] = 'false'
os.environ.setdefault('ASCEND_RT_VISIBLE_DEVICES', '0')

def locate_repo_root():
    repo_roots = []
    for env_name in ('GITCODE_REPO_ROOT', 'CANN_LEARNING_HUB_ROOT', 'REPO_ROOT'):
        if os.environ.get(env_name):
            repo_roots.append(Path(os.environ[env_name]))
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
    raise FileNotFoundError('Cannot locate cann-learning-hub repository root. Open this notebook inside cann-learning-hub or set CANN_LEARNING_HUB_ROOT to the repository root.')

REPO_ROOT = locate_repo_root()
os.chdir(REPO_ROOT)
TUTORIAL_DIR = REPO_ROOT / 'tutorials' / 'llm_inference' / 'qwen3_8b'
SRC_DIR = TUTORIAL_DIR / 'src'
SOURCE_DIR = REPO_ROOT / 'Sources' / 'model_inference_optimization' / 'qwen3_8b'
SOURCE_DIR.mkdir(parents=True, exist_ok=True)
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

if not os.environ.get('ASCEND_TOOLKIT_HOME'):
    raise EnvironmentError('ASCEND_TOOLKIT_HOME is not set. Please activate the CANN environment before running this notebook.')
cann_script = Path(os.environ['ASCEND_TOOLKIT_HOME']) / 'set_env.sh'
env_cmd = f'source {cann_script} && env'
env = subprocess.check_output(f"bash -lc '{env_cmd}'", shell=True, text=True, cwd=REPO_ROOT)
for line in env.splitlines():
    if '=' in line:
        os.environ.__setitem__(*line.split('=', 1))

subprocess.run(
    [
        sys.executable, '-m', 'pip', 'install', '-r', str(TUTORIAL_DIR / 'requirements.txt'),
        '-i', 'https://pypi.tuna.tsinghua.edu.cn/simple',
        '--trusted-host', 'pypi.tuna.tsinghua.edu.cn',
    ],
    check=True,
)

RECIPE_ROOT = SRC_DIR / 'inference_scripts' / 'recipe_qwen3_8b'
RECIPE_CONFIG_DIR = RECIPE_ROOT / 'models' / 'qwen' / 'config'
BASELINE_YAML_TEMPLATE = RECIPE_CONFIG_DIR / 'qwen3_8b_1tp.yaml'
PROFILE_YAML_TEMPLATE = RECIPE_CONFIG_DIR / 'qwen3_8b_1tp_profile.yaml'
OPTIMIZED_YAML_TEMPLATE = RECIPE_CONFIG_DIR / 'qwen3_8b_1tp_add_rmsnorm.yaml'
INFER_SH = RECIPE_ROOT / 'executor' / 'scripts' / 'infer.sh'
MODEL_ID = os.environ.get('QWEN3_8B_MODEL_PATH') or 'Qwen/Qwen3-8B'
MODEL_SOURCE_HINT = 'local_path' if os.environ.get('QWEN3_8B_MODEL_PATH') else os.environ['QWEN3_8B_DOWNLOAD_BACKEND']

print('仓库目录 =', REPO_ROOT)
print('教程目录 =', TUTORIAL_DIR)
print('运行目录 =', SOURCE_DIR)
print('recipes 目录 =', RECIPE_ROOT)
print('YAML 目录 =', RECIPE_CONFIG_DIR)
print('推理入口 =', INFER_SH)
print('可见 NPU =', os.environ.get('ASCEND_RT_VISIBLE_DEVICES'))
print('[环境准备] 完成', flush=True)
```

### 2 查看 YAML 并执行 Baseline 推理

本节按 recipes 的常规流程执行 Baseline：先查看并准备 YAML，再通过 `infer.sh` 启动离线推理，最后读取 recipes 运行结果并生成课程指标。

#### 2.1 准备 Baseline YAML

Qwen3-8B 单卡 YAML 位于 `models/qwen/config/qwen3_8b_1tp.yaml`。手工运行时，重点确认 `model_config.model_path`、`model_config.enable_profiler`、`custom_params.enable_npu_rmsnorm`、`custom_params.enable_add_rmsnorm` 和 `scheduler_config.max_new_tokens`。下面的 Python 单元会复制课程 YAML 到运行目录，写入当前模型路径，并打印关键字段。

```python
import os
import time
from inference_scripts.recipe_workflow import (
    collect_recipe_metrics,
    find_recipe_case_dir,
    prepare_runtime_yaml,
    print_yaml_focus,
    resolve_model_path,
)
from inference_scripts.inference_qwen3_8b import ensure_recipe_log_ok

BASELINE_WORK_DIR = SOURCE_DIR / 'run_outputs' / 'baseline_demo'
BASELINE_YAML = SOURCE_DIR / 'recipe_yaml' / 'baseline_demo.yaml'
BASELINE_WORK_DIR.mkdir(parents=True, exist_ok=True)
print('[Baseline 推理] 开始', flush=True)
resolved_model_path, model_source = resolve_model_path(str(MODEL_ID), quiet_model_io=False)
prepare_runtime_yaml(BASELINE_YAML_TEMPLATE, BASELINE_YAML, model_path=resolved_model_path)
print('[YAML 准备] Baseline 配置', flush=True)
print('参考 YAML =', BASELINE_YAML_TEMPLATE)
print('运行 YAML =', BASELINE_YAML)
print_yaml_focus(BASELINE_YAML)

baseline_log_dir = BASELINE_WORK_DIR / 'recipe_logs'
baseline_log_dir.mkdir(parents=True, exist_ok=True)
os.environ['QWEN3_RECIPE_ROOT'] = str(RECIPE_ROOT)
os.environ['QWEN3_RUN_YAML'] = str(BASELINE_YAML)
os.environ['QWEN3_RUN_LOG'] = str(baseline_log_dir / 'baseline_demo_infer_stdout.log')
os.environ['QWEN3_RUN_START_TIME'] = str(time.perf_counter())
```

#### 2.2 使用 recipes 命令启动推理

这部分展示 recipes 的运行方式：先进入 `recipe_qwen3_8b` 工程目录，再通过 `executor/scripts/infer.sh` 加载 YAML 执行离线推理。代码中会显式打印并执行对应命令。

```bash
%%bash
set -euo pipefail

# recipes 原生启动命令
echo 'recipes 启动命令:'
echo "cd ${QWEN3_RECIPE_ROOT}"
echo "bash executor/scripts/infer.sh --model qwen --mode offline --yaml ${QWEN3_RUN_YAML}"
cd "${QWEN3_RECIPE_ROOT}"
bash executor/scripts/infer.sh --model qwen --mode offline --yaml "${QWEN3_RUN_YAML}" 2>&1 | tee "${QWEN3_RUN_LOG}"
```

#### 2.3 读取 recipes 运行结果

推理结束后，recipes 会在 `models/qwen/res/<日期>/<模型名>_<yaml名>/` 下生成日志。下面的单元读取 `log_0.log`，并整理为课程使用的 metrics 与生成文本文件。

```python
case_dir = find_recipe_case_dir(RECIPE_ROOT, BASELINE_YAML)
if case_dir is None:
    raise RuntimeError(f'未找到 recipes 结果目录：{BASELINE_YAML.stem}')
recipe_log_path = case_dir / 'log_0.log'
ensure_recipe_log_ok(recipe_log_path)
run_info = {
    'stdout_path': os.environ['QWEN3_RUN_LOG'],
    'stderr_path': os.environ['QWEN3_RUN_LOG'],
    'wall_time_s': time.perf_counter() - float(os.environ['QWEN3_RUN_START_TIME']),
    'recipe_case_dir': str(case_dir),
    'recipe_log_path': str(recipe_log_path),
}
baseline_metrics = collect_recipe_metrics(
    RECIPE_ROOT,
    BASELINE_WORK_DIR,
    'baseline_demo',
    BASELINE_YAML,
    run_info,
    model_id=str(MODEL_ID),
    resolved_model_path=resolved_model_path,
    model_source=model_source,
    optimization_mode='none',
    max_new_tokens=64,
    max_input_tokens=256,
    enable_thinking=False,
)
print('[Baseline 推理] 完成', flush=True)
```

### 3 查看结果

运行结束后，查看 Baseline 指标、生成文本和 recipes 结果目录。这里重点确认生成文本可读，Dense RMSNorm 融合状态为关闭。

```python
print('[结果查看] 开始', flush=True)
def status_cn(status):
    return {'ok': '通过', 'warning': '告警', 'failed': '失败'}.get(status, status)

def yes_no(value):
    if value is None:
        return '未记录'
    return '是' if value else '否'

def load_metrics(work_dir, tag):
    metrics_path = Path(work_dir) / 'metrics' / f'{tag}_summary.json'
    metrics = json.loads(metrics_path.read_text(encoding='utf-8'))
    print('指标文件 =', metrics_path)
    print('recipes YAML =', metrics.get('recipe_yaml_path'))
    print('recipes 结果目录 =', metrics.get('recipe_case_dir'))
    print('生成文件 =', metrics.get('outputs_path'))
    print('生成 token 数 =', metrics.get('generated_tokens'))
    print('总耗时(s) =', metrics.get('total_time_s'))
    print('吞吐(tokens/s) =', metrics.get('tokens_per_second'))
    rmsnorm_status = metrics.get('rmsnorm_status') or {}
    print('RMSNorm 融合 =', yes_no(rmsnorm_status.get('rmsnorm_fused')))
    print('Add+RMSNorm 融合 =', yes_no(rmsnorm_status.get('add_rmsnorm_fused')))
    sanity = metrics.get('generation_text_sanity')
    if sanity:
        print('吐字检查 =', status_cn(sanity.get('status')), f"警告={sanity.get('num_with_warnings')}", f"失败={sanity.get('num_failed')}")
    return metrics

baseline_metrics = load_metrics(BASELINE_WORK_DIR, 'baseline_demo')
print()
print('生成文本:')
for line in Path(baseline_metrics['outputs_path']).read_text(encoding='utf-8').splitlines():
    if line.strip():
        print(json.loads(line).get('generated_text', ''))
print('[结果查看] 完成', flush=True)
```

# ==========================================
## 📝 练习与验证

> 📌 原 Notebook 中的练习、编译命令和校验代码已按原顺序保留在上文。需要 CANN 运行时、Ascend NPU 或 CANNLab 环境的单元，执行前请先核对版本和设备条件。
