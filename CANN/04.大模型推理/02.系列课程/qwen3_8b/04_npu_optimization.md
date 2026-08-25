---
source_repo: cann-learning-hub
source_path: tutorials/llm_inference/qwen3_8b/04_npu_optimization.ipynb
source_commit: 1bf85454ed7c41e184a96fb51d109b6bb83b7c0d
note_kind: notebook_to_markdown
---

# 4 Dense RMSNorm NPU 融合路径优化验证

> 📚 上游 Notebook：[tutorials/llm_inference/qwen3_8b/04_npu_optimization.ipynb](https://gitcode.com/cann/cann-learning-hub/blob/master/tutorials/llm_inference/qwen3_8b/04_npu_optimization.ipynb)
> 🧪 整理方式：保留 Markdown 与代码单元；省略 Jupyter 执行输出，避免把一次性环境结果误当成可复现结论。

## 🧭 学习目标

- 先跑通功能正确的 Baseline，再用 Profiling 定位瓶颈；
- 理解图模式、融合算子、量化和端到端收益验证。

# ==========================================
## 📖 课程内容

本章承接第 3 章的 Profiler 摘要，将 Add 与 RMSNorm 小算子链路作为基础优化点进行验证。验证时只切换 Dense RMSNorm NPU 融合开关，对比关闭融合与开启融合两条路径，并记录精度、吐字、文本一致性和整网 A/B 指标。

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

### 2 确认 A/B 口径

第 4 章仍使用 recipes 的 YAML + `infer.sh` 工作流。手工运行时，可以先打开 Baseline YAML `qwen3_8b_1tp.yaml`，确认 `custom_params.enable_npu_rmsnorm=false`、`custom_params.enable_add_rmsnorm=false`；再打开优化版 YAML `qwen3_8b_1tp_add_rmsnorm.yaml`，确认这两个开关为 `true`。两次运行只改变 Dense RMSNorm NPU 融合开关，其余 prompt、batch、输出长度、thinking 和采样参数保持一致。

```python
print('[Dense RMSNorm 精度检查] 开始')
from qwen3_npu_adaptation import run_add_rmsnorm_precision_check, run_rmsnorm_precision_check

precision_rows = {
    'RMSNorm': run_rmsnorm_precision_check(
        shapes=([1, 1, 4096], [1, 16, 4096], [1, 16, 32, 128]),
        dtype='bfloat16',
        device='npu:0',
        seed=2026,
    ),
    'Add+RMSNorm': run_add_rmsnorm_precision_check(
        shapes=([1, 1, 4096], [1, 16, 4096], [1, 16, 32, 128]),
        dtype='bfloat16',
        device='npu:0',
        seed=2026,
    ),
}
all_precision_rows = [row for group_rows in precision_rows.values() for row in group_rows]
PRECISION_CHECK_OK = all(row.get('status') == 'ok' for row in all_precision_rows)
PRECISION_CHECK_HAS_WARNING = any(row.get('status') == 'warning' for row in all_precision_rows)
PRECISION_CHECK_HARD_FAILED = any(row.get('status') == 'failed' for row in all_precision_rows)
PRECISION_CHECK_CAN_RUN = not PRECISION_CHECK_HARD_FAILED
precision_path = SOURCE_DIR / 'run_outputs' / 'add_rmsnorm_precision_check.json'
precision_path.parent.mkdir(parents=True, exist_ok=True)
precision_path.write_text(json.dumps(precision_rows, indent=2, ensure_ascii=False), encoding='utf-8')
for group_name, group_rows in precision_rows.items():
    ok_count = sum(row.get('status') == 'ok' for row in group_rows)
    warning_count = sum(row.get('status') == 'warning' for row in group_rows)
    failed_count = sum(row.get('status') == 'failed' for row in group_rows)
    max_diff = max(
        row.get('max_abs_diff', row.get('max_norm_abs_diff', 0.0))
        for row in group_rows
    )
    print(f'{group_name}: 通过 {ok_count}/{len(group_rows)}，告警 {warning_count}，失败 {failed_count}，最大误差={max_diff}')
print('精度阈值 = 0.01')
print('精度检查通过 =', '是' if PRECISION_CHECK_OK else '否')
print('精度检查告警 =', '是' if PRECISION_CHECK_HAS_WARNING else '否')
print('存在硬失败 =', '是' if PRECISION_CHECK_HARD_FAILED else '否')
print('继续 A/B =', '是' if PRECISION_CHECK_CAN_RUN else '否')
print('精度检查文件 =', precision_path)
print('[Dense RMSNorm 精度检查] 完成')
```

### 3 记录 Baseline 指标

先运行 Baseline YAML。下方单元会复制 YAML、填入当前模型路径，然后按 recipes 原生方式执行 `cd <recipes目录>` 与 `bash executor/scripts/infer.sh ...`，记录关闭融合时的指标。

#### 3.1 准备 Baseline YAML

运行 Baseline 前先准备 YAML：从课程模板复制配置到运行目录，写入当前模型路径，并打印关键字段，方便确认本次实验使用的是关闭融合的配置。

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

BASELINE_WORK_DIR = SOURCE_DIR / 'run_outputs' / 'benchmark_baseline'
BASELINE_YAML = SOURCE_DIR / 'recipe_yaml' / 'addrmsnorm_baseline.yaml'
BASELINE_WORK_DIR.mkdir(parents=True, exist_ok=True)

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

def prepare_recipe_run(work_dir, yaml_path, template_path, log_name):
    resolved_path, source = resolve_model_path(str(MODEL_ID), quiet_model_io=False)
    prepare_runtime_yaml(template_path, yaml_path, model_path=resolved_path)
    print('参考 YAML =', template_path)
    print('运行 YAML =', yaml_path)
    print_yaml_focus(yaml_path)
    log_dir = work_dir / 'recipe_logs'
    log_dir.mkdir(parents=True, exist_ok=True)
    os.environ['QWEN3_RECIPE_ROOT'] = str(RECIPE_ROOT)
    os.environ['QWEN3_RUN_YAML'] = str(yaml_path)
    os.environ['QWEN3_RUN_LOG'] = str(log_dir / log_name)
    os.environ['QWEN3_RUN_START_TIME'] = str(time.perf_counter())
    os.environ['QWEN3_SKIP_RECIPE_RUN'] = '0'
    return resolved_path, source

def collect_recipe_run(work_dir, metrics_tag, yaml_path, resolved_path, source, optimization_mode):
    case_dir = find_recipe_case_dir(RECIPE_ROOT, yaml_path)
    if case_dir is None:
        raise RuntimeError(f'未找到 recipes 结果目录：{yaml_path.stem}')
    recipe_log_path = case_dir / 'log_0.log'
    ensure_recipe_log_ok(recipe_log_path)
    run_info = {
        'stdout_path': os.environ['QWEN3_RUN_LOG'],
        'stderr_path': os.environ['QWEN3_RUN_LOG'],
        'wall_time_s': time.perf_counter() - float(os.environ['QWEN3_RUN_START_TIME']),
        'recipe_case_dir': str(case_dir),
        'recipe_log_path': str(recipe_log_path),
    }
    return collect_recipe_metrics(
        RECIPE_ROOT,
        work_dir,
        metrics_tag,
        yaml_path,
        run_info,
        model_id=str(MODEL_ID),
        resolved_model_path=resolved_path,
        model_source=source,
        optimization_mode=optimization_mode,
        max_new_tokens=64,
        max_input_tokens=256,
        enable_thinking=False,
    )

print('[Baseline 指标] 开始', flush=True)
print('[YAML 准备] Baseline 关闭 Dense RMSNorm NPU 融合', flush=True)
baseline_resolved_model_path, baseline_model_source = prepare_recipe_run(
    BASELINE_WORK_DIR,
    BASELINE_YAML,
    BASELINE_YAML_TEMPLATE,
    'addrmsnorm_baseline_infer_stdout.log',
)
```

#### 3.2 使用 recipes 命令启动 Baseline

这部分是真正的 recipes 启动命令。执行时先 `cd` 到 `recipe_qwen3_8b`，再调用 `executor/scripts/infer.sh`，其中 `--yaml` 指向刚才准备好的 Baseline 配置。

```bash
%%bash
set -euo pipefail

if [ "${QWEN3_SKIP_RECIPE_RUN:-0}" = "1" ]; then
  echo '跳过本次 recipes 推理。'
  exit 0
fi

echo 'recipes 启动命令:'
echo "cd ${QWEN3_RECIPE_ROOT}"
echo "bash executor/scripts/infer.sh --model qwen --mode offline --yaml ${QWEN3_RUN_YAML}"
cd "${QWEN3_RECIPE_ROOT}"
bash executor/scripts/infer.sh --model qwen --mode offline --yaml "${QWEN3_RUN_YAML}" 2>&1 | tee "${QWEN3_RUN_LOG}"
```

#### 3.3 读取 Baseline 结果

推理完成后，读取 recipes 输出目录中的 `log_0.log`，提取生成耗时和模型输出，并保存为后续 A/B 对比使用的指标文件。

```python
baseline_metrics = collect_recipe_run(
    BASELINE_WORK_DIR,
    'addrmsnorm_baseline',
    BASELINE_YAML,
    baseline_resolved_model_path,
    baseline_model_source,
    'none',
)
print('[Baseline 指标] 完成', flush=True)
baseline_metrics = load_metrics(BASELINE_WORK_DIR, 'addrmsnorm_baseline')
```

### 4 运行 Dense RMSNorm NPU 融合版本

随后运行开启 Dense RMSNorm NPU 融合的 YAML。启动方式保持不变，只切换 YAML 中的融合开关，便于和 Baseline 做同口径对比。

#### 4.1 准备优化版 YAML

运行优化版本前，同样先准备 YAML：复制开启 Dense RMSNorm NPU 融合的配置，写入相同模型路径，并保持输入长度、输出长度、batch 和解码设置与 Baseline 一致。

```python
OPT_WORK_DIR = SOURCE_DIR / 'run_outputs' / 'benchmark_add_rmsnorm'
OPT_YAML = SOURCE_DIR / 'recipe_yaml' / 'addrmsnorm_optimized.yaml'
OPT_WORK_DIR.mkdir(parents=True, exist_ok=True)
if PRECISION_CHECK_CAN_RUN:
    if PRECISION_CHECK_HAS_WARNING:
        print('[Dense RMSNorm 指标] 精度检查存在告警，继续执行 A/B。', flush=True)
    print('[Dense RMSNorm 指标] 开始', flush=True)
    print('[YAML 准备] 优化版本开启 Dense RMSNorm NPU 融合', flush=True)
    optimized_resolved_model_path, optimized_model_source = prepare_recipe_run(
        OPT_WORK_DIR,
        OPT_YAML,
        OPTIMIZED_YAML_TEMPLATE,
        'addrmsnorm_optimized_infer_stdout.log',
    )
    os.environ['QWEN3_SKIP_RECIPE_RUN'] = '0'
else:
    optimized_metrics = None
    os.environ['QWEN3_SKIP_RECIPE_RUN'] = '1'
    print('精度检查存在硬失败，跳过 Dense RMSNorm 基准测试。')
```

#### 4.2 使用 recipes 命令启动优化版

优化版本的启动命令与 Baseline 保持一致，只将 `--yaml` 切换为融合配置。这样实验差异集中在 YAML 中的融合开关，便于做同口径对比。

```bash
%%bash
set -euo pipefail

if [ "${QWEN3_SKIP_RECIPE_RUN:-0}" = "1" ]; then
  echo '跳过本次 recipes 推理。'
  exit 0
fi

echo 'recipes 启动命令:'
echo "cd ${QWEN3_RECIPE_ROOT}"
echo "bash executor/scripts/infer.sh --model qwen --mode offline --yaml ${QWEN3_RUN_YAML}"
cd "${QWEN3_RECIPE_ROOT}"
bash executor/scripts/infer.sh --model qwen --mode offline --yaml "${QWEN3_RUN_YAML}" 2>&1 | tee "${QWEN3_RUN_LOG}"
```

#### 4.3 读取优化版结果

优化版完成后，继续从 recipes 日志提取指标与生成文本，保存到 `benchmark_add_rmsnorm` 目录，供最后的 A/B 对比单元读取。

```python
if PRECISION_CHECK_CAN_RUN:
    optimized_metrics = collect_recipe_run(
        OPT_WORK_DIR,
        'addrmsnorm_optimized',
        OPT_YAML,
        optimized_resolved_model_path,
        optimized_model_source,
        'add_rmsnorm',
    )
    print('[Dense RMSNorm 指标] 完成', flush=True)
    optimized_metrics = load_metrics(OPT_WORK_DIR, 'addrmsnorm_optimized')
else:
    optimized_metrics = None
```

### 5 结果对比

最后汇总单算子精度、吞吐、时延、吐字健康和文本相似度。BF16 融合路径允许轻微措辞差异，重点确认输出可读、语义稳定，并观察性能指标是否改善。

```python
print('[结果对比] 开始')
from difflib import SequenceMatcher
from qwen3_npu_adaptation import run_generation_text_sanity_check

def status_cn(status):
    return {'ok': '通过', 'warning': '告警', 'failed': '失败'}.get(status, status)

def decision_cn(decision):
    return {'adopt': '建议开启', 'do_not_adopt': '暂不建议开启', 'not_run': '未运行'}.get(decision, decision)

def yes_no(value):
    if value is None:
        return '未记录'
    return '是' if value else '否'

def precision_summary_cn():
    if PRECISION_CHECK_HARD_FAILED:
        return '硬失败'
    if PRECISION_CHECK_HAS_WARNING:
        return '告警'
    return '通过'

def read_generation_rows(metrics):
    rows = []
    for line in Path(metrics['outputs_path']).read_text(encoding='utf-8').splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows

def rmsnorm_fused(metrics):
    return (metrics.get('rmsnorm_status') or {}).get('rmsnorm_fused')

def add_rmsnorm_fused(metrics):
    return (metrics.get('rmsnorm_status') or {}).get('add_rmsnorm_fused')

def text_similarity_ratio(left_texts, right_texts):
    if len(left_texts) != len(right_texts) or not left_texts:
        return 0.0
    ratios = [SequenceMatcher(None, left, right).ratio() for left, right in zip(left_texts, right_texts)]
    return min(ratios)

baseline_rows = read_generation_rows(baseline_metrics)
baseline_text_sanity = run_generation_text_sanity_check(
    baseline_rows,
    max_new_tokens=baseline_metrics.get('max_new_tokens'),
)

if optimized_metrics is None:
    comparison = {
        'status': 'skipped',
        'reason': 'Dense RMSNorm 精度检查存在硬失败，跳过优化版基准测试。',
        'optimization_decision': 'not_run',
        'precision_check_ok': PRECISION_CHECK_OK,
        'precision_check_has_warning': PRECISION_CHECK_HAS_WARNING,
        'precision_check_hard_failed': PRECISION_CHECK_HARD_FAILED,
        'precision_check_can_run': PRECISION_CHECK_CAN_RUN,
        'precision_check_path': str(precision_path),
        'baseline_generation_text_sanity': baseline_text_sanity,
    }
else:
    optimized_rows = read_generation_rows(optimized_metrics)
    optimized_text_sanity = run_generation_text_sanity_check(
        optimized_rows,
        max_new_tokens=optimized_metrics.get('max_new_tokens'),
    )
    baseline_texts = [row.get('generated_text', '') for row in baseline_rows]
    optimized_texts = [row.get('generated_text', '') for row in optimized_rows]
    output_similarity_ratio = text_similarity_ratio(baseline_texts, optimized_texts)
    outputs_consistent = output_similarity_ratio >= 0.95
    baseline_tps = baseline_metrics['tokens_per_second']
    optimized_tps = optimized_metrics['tokens_per_second']
    baseline_latency = baseline_metrics['mean_per_token_latency_s']
    optimized_latency = optimized_metrics['mean_per_token_latency_s']
    throughput_gain_pct = (optimized_tps / baseline_tps - 1.0) * 100 if baseline_tps else None
    latency_reduction_pct = (1.0 - optimized_latency / baseline_latency) * 100 if baseline_latency else None
    adopt = (
        PRECISION_CHECK_CAN_RUN
        and throughput_gain_pct is not None
        and throughput_gain_pct > 0
        and baseline_text_sanity.get('status') == 'ok'
        and optimized_text_sanity.get('status') == 'ok'
        and outputs_consistent
    )
    comparison = {
        'status': 'ok',
        'baseline_rmsnorm_fused': rmsnorm_fused(baseline_metrics),
        'baseline_add_rmsnorm_fused': add_rmsnorm_fused(baseline_metrics),
        'optimized_rmsnorm_fused': rmsnorm_fused(optimized_metrics),
        'optimized_add_rmsnorm_fused': add_rmsnorm_fused(optimized_metrics),
        'baseline_tokens_per_second': baseline_tps,
        'optimized_tokens_per_second': optimized_tps,
        'throughput_gain_pct': throughput_gain_pct,
        'baseline_mean_per_token_latency_s': baseline_latency,
        'optimized_mean_per_token_latency_s': optimized_latency,
        'latency_reduction_pct': latency_reduction_pct,
        'precision_check_ok': PRECISION_CHECK_OK,
        'precision_check_has_warning': PRECISION_CHECK_HAS_WARNING,
        'precision_check_hard_failed': PRECISION_CHECK_HARD_FAILED,
        'precision_check_can_run': PRECISION_CHECK_CAN_RUN,
        'precision_check_path': str(precision_path),
        'baseline_generation_text_sanity': baseline_text_sanity,
        'optimized_generation_text_sanity': optimized_text_sanity,
        'baseline_optimized_output_similarity_ratio': output_similarity_ratio,
        'baseline_optimized_outputs_consistent': outputs_consistent,
        'optimization_decision': 'adopt' if adopt else 'do_not_adopt',
        'decision_reason': '精度无硬失败、吞吐提升、生成文本健康且文本相似度达标时，建议开启 Dense RMSNorm NPU 融合路径。',
    }

comparison_path = SOURCE_DIR / 'run_outputs' / 'optimization_comparison.json'
comparison_path.write_text(json.dumps(comparison, indent=2, ensure_ascii=False), encoding='utf-8')
print('对比文件 =', comparison_path)
print('精度检查 =', precision_summary_cn())
print('Baseline 融合状态 =', yes_no(comparison.get('baseline_rmsnorm_fused')), '/', yes_no(comparison.get('baseline_add_rmsnorm_fused')))
print('优化版融合状态 =', yes_no(comparison.get('optimized_rmsnorm_fused')), '/', yes_no(comparison.get('optimized_add_rmsnorm_fused')))
print('吞吐(tokens/s) =', comparison.get('baseline_tokens_per_second'), '->', comparison.get('optimized_tokens_per_second'))
print('吞吐提升(%) =', comparison.get('throughput_gain_pct'))
print('吐字检查 =', status_cn(comparison.get('baseline_generation_text_sanity', {}).get('status')), '/', status_cn(comparison.get('optimized_generation_text_sanity', {}).get('status')))
print('文本相似度 =', comparison.get('baseline_optimized_output_similarity_ratio'))
print('文本一致性达标 =', yes_no(comparison.get('baseline_optimized_outputs_consistent')))
if optimized_metrics is not None:
    print('Baseline 文本 =', baseline_texts[0] if baseline_texts else '')
    print('优化版文本 =', optimized_texts[0] if optimized_texts else '')
print('优化建议 =', decision_cn(comparison.get('optimization_decision')))
if comparison.get('optimization_decision') == 'adopt':
    print('结论：本轮指标支持开启 Dense RMSNorm NPU 融合路径。')
elif comparison.get('optimization_decision') == 'do_not_adopt':
    print('结论：本轮指标暂不支持开启 Dense RMSNorm NPU 融合路径。')
else:
    print('结论：本轮未完成 Dense RMSNorm NPU 融合路径 A/B。')
print('[结果对比] 完成')
```

# ==========================================
## 📝 练习与验证

> 📌 原 Notebook 中的练习、编译命令和校验代码已按原顺序保留在上文。需要 CANN 运行时、Ascend NPU 或 CANNLab 环境的单元，执行前请先核对版本和设备条件。
