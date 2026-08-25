---
source_repo: cann-learning-hub
source_path: tutorials/llm_inference/qwen3_8b/03_profiling_analysis.ipynb
source_commit: 1bf85454ed7c41e184a96fb51d109b6bb83b7c0d
note_kind: notebook_to_markdown
---

# 3 Profiling 分析

> 📚 上游 Notebook：[tutorials/llm_inference/qwen3_8b/03_profiling_analysis.ipynb](https://gitcode.com/cann/cann-learning-hub/blob/master/tutorials/llm_inference/qwen3_8b/03_profiling_analysis.ipynb)
> 🧪 整理方式：保留 Markdown 与代码单元；省略 Jupyter 执行输出，避免把一次性环境结果误当成可复现结论。

## 🧭 学习目标

- 先跑通功能正确的 Baseline，再用 Profiling 定位瓶颈；
- 理解图模式、融合算子、量化和端到端收益验证。

# ==========================================
## 📖 课程内容

本章在第 2 章同一条 Baseline 推理链路上打开 `torch_npu.profiler`，观察一次短推理中的算子分布。这里不做性能结论，而是为后续优化选择一个可验证的切入点。

### 1 环境与工作区准备
定位教程目录、准备运行目录，并把 CANN 环境变量导入当前 Notebook 进程。若已经跑过第 2 章，模型权重会直接复用下载工具默认缓存。

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

### 2 查看 Profiling YAML 并运行

本节沿用 recipes 的 YAML + `infer.sh` 工作流，只是在 Baseline 配置基础上打开 Profiling。流程同样分为三步：准备 Profiling YAML、启动 recipes 推理、读取结果目录。

#### 2.1 准备 Profiling YAML

Profiling YAML 位于 `models/qwen/config/qwen3_8b_1tp_profile.yaml`。手工运行时，将 `model_config.enable_profiler` 设为 `true`，其余推理参数保持和 Baseline 一致。下面的 Python 单元会复制课程 YAML 到运行目录，写入当前模型路径，并打印关键字段。

```python
import os
import time
from inference_scripts.recipe_workflow import (
    collect_recipe_metrics,
    discover_profile_artifacts,
    find_recipe_case_dir,
    prepare_runtime_yaml,
    print_yaml_focus,
    resolve_model_path,
)
from inference_scripts.inference_qwen3_8b import ensure_recipe_log_ok

PROFILE_WORK_DIR = SOURCE_DIR / 'run_outputs' / 'baseline_profile'
PROFILE_YAML = SOURCE_DIR / 'recipe_yaml' / 'baseline_profile.yaml'
PROFILE_WORK_DIR.mkdir(parents=True, exist_ok=True)
print('[Profiling 采集] 开始', flush=True)
resolved_model_path, model_source = resolve_model_path(str(MODEL_ID), quiet_model_io=False)
prepare_runtime_yaml(PROFILE_YAML_TEMPLATE, PROFILE_YAML, model_path=resolved_model_path)
print('[YAML 准备] Profiling 配置', flush=True)
print('参考 YAML =', PROFILE_YAML_TEMPLATE)
print('运行 YAML =', PROFILE_YAML)
print_yaml_focus(PROFILE_YAML)

profile_log_dir = PROFILE_WORK_DIR / 'recipe_logs'
profile_log_dir.mkdir(parents=True, exist_ok=True)
os.environ['QWEN3_RECIPE_ROOT'] = str(RECIPE_ROOT)
os.environ['QWEN3_RUN_YAML'] = str(PROFILE_YAML)
os.environ['QWEN3_RUN_LOG'] = str(profile_log_dir / 'baseline_profile_infer_stdout.log')
os.environ['QWEN3_RUN_START_TIME'] = str(time.perf_counter())
```

#### 2.2 使用 recipes 命令启动 Profiling

这部分仍然使用 recipes 原生命令：进入 `recipe_qwen3_8b` 目录后执行 `executor/scripts/infer.sh`。由于 YAML 已打开 Profiling，推理结束后会在 recipes 结果目录中生成 `prof/` 产物。

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

#### 2.3 读取 Profiling 结果目录

recipes 推理完成后，先定位本次结果目录和 `prof/` 目录，再把推理日志、生成文本和 Profiling 摘要整理到课程运行目录，供后续单元查看。

```python
case_dir = find_recipe_case_dir(RECIPE_ROOT, PROFILE_YAML)
if case_dir is None:
    raise RuntimeError(f'未找到 recipes 结果目录：{PROFILE_YAML.stem}')
recipe_log_path = case_dir / 'log_0.log'
ensure_recipe_log_ok(recipe_log_path)
run_info = {
    'stdout_path': os.environ['QWEN3_RUN_LOG'],
    'stderr_path': os.environ['QWEN3_RUN_LOG'],
    'wall_time_s': time.perf_counter() - float(os.environ['QWEN3_RUN_START_TIME']),
    'recipe_case_dir': str(case_dir),
    'recipe_log_path': str(recipe_log_path),
}
profile_metrics = collect_recipe_metrics(
    RECIPE_ROOT,
    PROFILE_WORK_DIR,
    'baseline_profile',
    PROFILE_YAML,
    run_info,
    model_id=str(MODEL_ID),
    resolved_model_path=resolved_model_path,
    model_source=model_source,
    optimization_mode='none',
    max_new_tokens=64,
    max_input_tokens=256,
    enable_thinking=False,
)
profile_artifacts = profile_metrics.get('profiler_artifacts') or discover_profile_artifacts(Path(profile_metrics['profiler_dir']))
print('Profile 目录 =', profile_metrics.get('profiler_dir'))
print('[Profiling 采集] 完成', flush=True)
```

### 3 查看 Profiler 产物

Profiling 运行结束后，recipes 结果目录下会生成 `prof/`，其中通常包含 `prof/prefill/` 和 `prof/decode/` 两个阶段目录。需重点关注 `kernel_details.csv` 和 `trace_view.json`：前者记录具体算子耗时、次数等信息，后者可使用 Chrome 的 `chrome://tracing` 或 MindStudio 打开，可视化查看推理过程的时间线。

```python
print('[Profiler 产物] 开始', flush=True)
def status_cn(status):
    return {'ok': '通过', 'warning': '告警', 'failed': '失败'}.get(status, status)

def find_phase_dir(profile_root, phase):
    direct = profile_root / phase
    if direct.is_dir():
        return direct
    matches = sorted(path for path in profile_root.rglob(phase) if path.is_dir())
    return matches[0] if matches else None

def direct_dirs(path):
    if not path or not path.is_dir():
        return []
    return sorted(item.name for item in path.iterdir() if item.is_dir())

def has_focus_file(paths, phase, keyword):
    for item in paths or []:
        path = Path(item)
        if keyword in path.name.lower() and phase in path.parts:
            return True
    return False

metrics_path = Path(PROFILE_WORK_DIR) / 'metrics' / 'baseline_profile_summary.json'
profile_metrics = json.loads(metrics_path.read_text(encoding='utf-8'))
profile_artifacts = profile_metrics.get('profiler_artifacts') or {}
profile_root = Path(profile_metrics['profiler_dir'])
print('指标文件 =', metrics_path)
print('生成 token 数 =', profile_metrics.get('generated_tokens'))
print('Profiler 开启 =', '是' if profile_metrics.get('profiler_enabled') else '否')
print('Profile 目录 =', profile_root)

for phase in ('prefill', 'decode'):
    phase_dir = find_phase_dir(profile_root, phase)
    print(f'prof/{phase} =', phase_dir if phase_dir else '未找到')
    if phase_dir:
        dirs = direct_dirs(phase_dir)
        if dirs:
            print('  一级目录 =', '、'.join(dirs[:8]) + (f' 等 {len(dirs)} 个' if len(dirs) > 8 else ''))
        else:
            print('  一级目录 = 无')
    kernel_ready = has_focus_file(profile_artifacts.get('kernel_details', []), phase, 'kernel_details')
    trace_ready = has_focus_file(profile_artifacts.get('trace', []), phase, 'trace_view') or has_focus_file(profile_artifacts.get('trace', []), phase, 'trace')
    print('  kernel_details.csv =', '已生成' if kernel_ready else '未找到')
    print('  trace_view.json =', '已生成' if trace_ready else '未找到')

sanity = profile_metrics.get('generation_text_sanity')
if sanity:
    print('吐字检查 =', status_cn(sanity.get('status')), f"警告={sanity.get('num_with_warnings')}", f"失败={sanity.get('num_failed')}")
summary_path = Path(profile_metrics['profiler_summary_path'])
summary_lines = summary_path.read_text(encoding='utf-8').splitlines()
print()
print('Profiler 摘要文件 =', summary_path)
print('\n'.join(summary_lines[:24]))
if len(summary_lines) > 24:
    print(f'... 仅显示前 24 行，共 {len(summary_lines)} 行')
print('[Profiler 产物] 完成', flush=True)
```

### 4 分析结论

这里基于真实 Profiler 摘要、Baseline YAML 和 QwenRMSNorm 的计算链路选择优化点。Baseline 关闭 Dense RMSNorm 融合时，Profiler 更常见的是底层 elementwise/reduction 小算子，而不是一个已经融合好的 RMSNorm 算子。

```python
print('[分析结论] 开始')
summary_text = summary_path.read_text(encoding='utf-8')
first_line = summary_text.splitlines()[0] if summary_text.splitlines() else ''
summary_kind = first_line.replace('Profiler summary from ', '') if first_line else 'Profiler 摘要'

operator_rows = []
for line in summary_text.splitlines():
    parts = line.split()
    if len(parts) >= 4:
        try:
            count = int(float(parts[-3]))
            total_us = float(parts[-2])
            ratio = float(parts[-1])
        except ValueError:
            continue
        op_type = ' '.join(parts[:-3])
        operator_rows.append({'op_type': op_type, 'count': count, 'total_us': total_us, 'ratio_pct': ratio})
operator_rows = sorted(operator_rows, key=lambda row: row['total_us'], reverse=True)
if not operator_rows:
    raise RuntimeError('Profiler 摘要中没有可解析的算子行，请重新执行 Profiling 采集。')

def match_norm_chain_op(name):
    lower = name.lower()
    if 'rmsnorm' in lower:
        return True
    if 'matmul' in lower or 'batchmatmul' in lower:
        return False
    if any(key in lower for key in ('pow', 'reduce', 'rsqrt', 'sqrt', 'cast')):
        return True
    return lower in {'mul', 'muls'} or lower.startswith('mul_')

def match_residual_add_op(name):
    lower = name.lower()
    return 'add' in lower and 'rmsnorm' not in lower

top_ops = operator_rows[:10]
rmsnorm_status = profile_metrics.get('rmsnorm_status') or {}
op_names = [row['op_type'] for row in operator_rows]
direct_rmsnorm_ops = sorted(name for name in op_names if 'rmsnorm' in name.lower())
norm_chain_ops = sorted(name for name in op_names if match_norm_chain_op(name))
residual_add_ops = sorted(name for name in op_names if match_residual_add_op(name))
analysis = {
    'profiler_summary_path': str(summary_path),
    'profiler_dir': profile_metrics.get('profiler_dir'),
    'profiler_artifacts': profile_artifacts,
    'baseline_metrics_path': str(PROFILE_WORK_DIR / 'metrics' / 'baseline_profile_summary.json'),
    'baseline_rmsnorm_fused': rmsnorm_status.get('rmsnorm_fused'),
    'baseline_add_rmsnorm_fused': rmsnorm_status.get('add_rmsnorm_fused'),
    'metrics': {
        'generated_tokens': profile_metrics.get('generated_tokens'),
        'generation_text_sanity': profile_metrics.get('generation_text_sanity'),
    },
    'summary_kind': summary_kind,
    'top_operators': top_ops,
    'direct_rmsnorm_ops': direct_rmsnorm_ops,
    'norm_chain_ops': norm_chain_ops,
    'residual_add_ops': residual_add_ops,
    'notes': [],
}

print('摘要类型 =', summary_kind)
print('生成 token 数 =', analysis['metrics']['generated_tokens'])
print('Baseline RMSNorm 融合 =', '是' if analysis['baseline_rmsnorm_fused'] else '否')
print('Baseline Add+RMSNorm 融合 =', '是' if analysis['baseline_add_rmsnorm_fused'] else '否')
print()
print('Top 算子:')
for row in top_ops:
    print(f"- {row['op_type']}: 次数={row['count']}，总耗时(us)={row['total_us']:.3f}，占比={row['ratio_pct']:.3f}%")

analysis['notes'].append('Baseline YAML 中 Dense RMSNorm 两个融合开关均为关闭，因此本章看到的是融合前的执行链路。')
if direct_rmsnorm_ops:
    analysis['notes'].append('摘要中出现名称含 RMSNorm 的条目：' + '、'.join(direct_rmsnorm_ops[:8]) + '。这里仅作为命名线索，是否启用融合仍以 YAML 开关和第 4 章 A/B 指标为准。')
else:
    analysis['notes'].append('摘要中没有直接出现融合后的 RMSNorm 算子名，说明 Baseline 仍按小算子链路执行。')
if norm_chain_ops:
    analysis['notes'].append('结合 QwenRMSNorm 的计算式，摘要中的归一化相关小算子包括：' + '、'.join(norm_chain_ops[:8]) + '。')
else:
    analysis['notes'].append('当前摘要 Top 行未完整呈现归一化小算子，后续仍以同一 YAML 口径做整网 A/B 验证。')
if residual_add_ops:
    analysis['notes'].append('摘要中也可以看到残差 Add 相关算子：' + '、'.join(residual_add_ops[:8]) + '。')
else:
    analysis['notes'].append('当前摘要中未直接列出残差 Add 名称，优化验证阶段继续用关闭/开启融合的同口径实验观察收益。')
analysis['notes'].append('下一章保持 recipes 的 YAML + infer.sh 工作流，只切换 Dense RMSNorm NPU 融合开关，对比精度、吐字健康和吞吐变化。')

print()
print('结论:')
for note in analysis['notes']:
    print('-', note)
analysis_path = SOURCE_DIR / 'run_outputs' / 'profiling_analysis_summary.json'
analysis_path.write_text(json.dumps(analysis, indent=2, ensure_ascii=False), encoding='utf-8')
print('分析文件 =', analysis_path)
print('[分析结论] 完成')
```

# ==========================================
## 📝 练习与验证

> 📌 原 Notebook 中的练习、编译命令和校验代码已按原顺序保留在上文。需要 CANN 运行时、Ascend NPU 或 CANNLab 环境的单元，执行前请先核对版本和设备条件。
