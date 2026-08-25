---
source_repo: cann-learning-hub
source_path: reference_practice/model_inference_optimization/sana_video/03_profiling_analysis.ipynb
source_commit: 1bf85454ed7c41e184a96fb51d109b6bb83b7c0d
note_kind: notebook_to_markdown
---

# 3 Profiling 分析

> 📚 上游 Notebook：[reference_practice/model_inference_optimization/sana_video/03_profiling_analysis.ipynb](https://gitcode.com/cann/cann-learning-hub/blob/master/reference_practice/model_inference_optimization/sana_video/03_profiling_analysis.ipynb)
> 🧪 整理方式：保留 Markdown 与代码单元；省略 Jupyter 执行输出，避免把一次性环境结果误当成可复现结论。

## 🧭 学习目标

- 先读懂概念，再运行代码片段验证关键结论；
- 把本节内容接入后续 CANN / Ascend NPU 实践。

# ==========================================
## 📖 课程内容

本节使用 `torch_npu.profiler` 采集 Baseline 路径的性能数据。默认已完成上一节的依赖安装。

---

### 1 环境与工作区准备
如需独立执行本 Notebook，会重复完成环境初始化、源码拉取和教程文件覆盖。为加速模型下载，教程默认使用 HF-Mirror 镜像源。

```python
import os
import shutil
import subprocess
import sys
from pathlib import Path

os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
def locate_repo_root():
    candidates = []
    if os.environ.get('GITCODE_REPO_ROOT'):
        candidates.append(Path(os.environ['GITCODE_REPO_ROOT']))
    candidates.extend([
        Path('/opt/atomgit/cann-learning-hub'),
    ])
    try:
        cwd = Path.cwd()
        candidates.extend([cwd, *cwd.parents])
    except FileNotFoundError:
        pass

    seen = set()
    for candidate in candidates:
        key = str(candidate)
        if key in seen:
            continue
        seen.add(key)
        if (candidate / 'reference_practice/model_inference_optimization/sana_video/src').exists():
            return candidate
    raise FileNotFoundError('Cannot locate cann-learning-hub repository root.')

REPO_ROOT = locate_repo_root()
os.chdir(REPO_ROOT)
TUTORIAL_DIR = REPO_ROOT / 'reference_practice' / 'model_inference_optimization' / 'sana_video'
SOURCE_DIR = REPO_ROOT / 'Sources' / 'model_inference_optimization' / 'sana_video'
UPSTREAM_SANA_DIR = SOURCE_DIR / 'Sana_upstream'
WORKSPACE = SOURCE_DIR / 'Sana'
SOURCE_DIR.mkdir(parents=True, exist_ok=True)

if not os.environ.get('ASCEND_TOOLKIT_HOME'):
    raise EnvironmentError('ASCEND_TOOLKIT_HOME is not set. Please activate the CANN environment before running this notebook.')
cann_script = Path(os.environ['ASCEND_TOOLKIT_HOME']) / 'set_env.sh'
env_cmd = f'source {cann_script} && env'
env = subprocess.check_output(f"bash -lc '{env_cmd}'", shell=True, text=True, cwd=REPO_ROOT)
for line in env.splitlines():
    if '=' in line:
        os.environ.__setitem__(*line.split('=', 1))

import time

if not UPSTREAM_SANA_DIR.exists():
    max_retries = 3
    clone_success = False
    for attempt in range(max_retries):
        try:
            print(f'Cloning Sana repository (attempt {attempt + 1}/{max_retries})...')
            subprocess.run(
                ['git', 'clone', 'https://github.com/NVlabs/Sana.git', str(UPSTREAM_SANA_DIR)],
                check=True,
                timeout=300,
            )
            clone_success = True
            break
        except subprocess.TimeoutExpired:
            print(f'Clone timed out after 300 seconds')
            if attempt < max_retries - 1:
                print('Retrying in 5 seconds...')
                time.sleep(5)
        except subprocess.CalledProcessError as e:
            print(f'Clone failed with exit code {e.returncode}')
            if attempt < max_retries - 1:
                print('Retrying in 5 seconds...')
                time.sleep(5)
    if not clone_success:
        print('\nERROR: Failed to clone after 3 attempts.')
        print('Please try running manually in a terminal:')
        print(f'  git clone https://github.com/NVlabs/Sana.git {UPSTREAM_SANA_DIR}')
        raise RuntimeError('Failed to clone Sana repository')
subprocess.run(['git', 'checkout', '08c656c3'], cwd=UPSTREAM_SANA_DIR, check=True)
WORKSPACE.mkdir(parents=True, exist_ok=True)
(WORKSPACE / 'inference_video_scripts').mkdir(parents=True, exist_ok=True)
(WORKSPACE / 'asset' / 'samples').mkdir(parents=True, exist_ok=True)
shutil.copy2(TUTORIAL_DIR / 'src' / 'pyproject.toml', WORKSPACE / 'pyproject.toml')
shutil.copy2(TUTORIAL_DIR / 'src' / 'sana_npu_adaptation.py', WORKSPACE / 'sana_npu_adaptation.py')
shutil.copy2(TUTORIAL_DIR / 'src' / 'inference_video_scripts' / 'inference_sana_video.py', WORKSPACE / 'inference_video_scripts' / 'inference_sana_video.py')
shutil.copy2(TUTORIAL_DIR / 'src' / 'samples' / 'video_prompts_samples.txt', WORKSPACE / 'asset' / 'samples' / 'tutorial_video_prompts_samples.txt')
subprocess.run(
    ['bash', '-lc', f'cp -rn "{UPSTREAM_SANA_DIR}/." "{WORKSPACE}"'],
    check=True,
)
print('Workspace ready:', WORKSPACE)
```

### 2 采集 Baseline Profiling
这里启用 `torch_npu.profiler`，同时关闭视频保存，避免编码阶段干扰模型采样分析，这里使用 10 个 sample step，本节的时间结果主要用于profiling分析。

```python
PROFILE_WORK_DIR = SOURCE_DIR / 'run_outputs' / 'baseline_profile'
PROFILE_DIR = SOURCE_DIR / 'profiler' / 'baseline'
PROFILE_WORK_DIR.mkdir(parents=True, exist_ok=True)
PROFILE_DIR.mkdir(parents=True, exist_ok=True)
cmd = [
    sys.executable,
    str(WORKSPACE / 'inference_video_scripts' / 'inference_sana_video.py'),
    '--config', str(WORKSPACE / 'configs' / 'sana_video_config' / 'Sana_2000M_480px_AdamW_fsdp.yaml'),
    '--model_path', 'hf://Efficient-Large-Model/SANA-Video_2B_480p/checkpoints/SANA_Video_2B_480p.pth',
    '--txt_file', str(WORKSPACE / 'asset' / 'samples' / 'tutorial_video_prompts_samples.txt'),
    '--cfg_scale', '6',
    '--motion_score', '30',
    '--flow_shift', '8',
    '--work_dir', str(PROFILE_WORK_DIR),
    '--sample_nums', '1',
    '--step', '10',
    '--metrics_tag', 'baseline_profile',
    '--skip_save', 'True',
    '--enable_torch_profiler', 'True',
    '--profiler_dir', str(PROFILE_DIR),
    '--profiler_active', '1',
    '--profiler_with_stack', 'True',
    '--model.fp32_attention', 'False',
]
subprocess.run(cmd, cwd=WORKSPACE, check=True)
```

### 3 查看 Profiler 摘要
先观察整网 step 级时间与全局热点，再结合下一节的 `RMSNorm` 源码理解为什么值得尝试融合替换。

说明：
- `mean_single_step_latency_s` 统计的是 `solver.sample(...)` 总采样时间除以 `sample_steps`，只反映采样阶段。
- `Step trace` 中的 `Stage / Computing / Free` 对应一次 profiler step 的整段 batch 时间，会包含采样前后的其他 batch 内开销。
- 运行时 tqdm 显示的 `xx s/it` 只反映 DPM-Solver multistep 主循环中可见迭代的耗时；由于前面还有初始化和 warmup，因此不会与最终平均值完全一致。

```python
import csv
import json
from collections import defaultdict

profile_metrics_path = PROFILE_WORK_DIR / 'metrics' / 'baseline_profile_summary.json'
profile_metrics = json.loads(profile_metrics_path.read_text(encoding='utf-8'))
prof_output = next(PROFILE_DIR.rglob('ASCEND_PROFILER_OUTPUT'))
print('profiler output =', prof_output)
print()
print('Single-step latency baseline:')
print(f"  sample_steps: {profile_metrics['sample_steps']}")
print(f"  mean_sampling_time_s: {profile_metrics['mean_sampling_time_s']:.2f} s")
print(f"  mean_single_step_latency_s: {profile_metrics['mean_single_step_latency_s']:.4f} s")
print()
with (prof_output / 'step_trace_time.csv').open(newline='', encoding='utf-8') as f:
    step_trace = next(csv.DictReader(f))

print('Step trace:')
for key in ['Stage', 'Computing', 'Free', 'Preparing']:
    print(f"  {key}: {float(step_trace[key]) / 1000:.2f} ms")

agg = defaultdict(lambda: {'count': 0, 'total_us': 0.0, 'ratio': 0.0})
with (prof_output / 'op_statistic.csv').open(newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        op = row['OP Type']
        agg[op]['count'] += int(row['Count'])
        agg[op]['total_us'] += float(row['Total Time(us)'])
        agg[op]['ratio'] += float(row['Ratio(%)'])

rows = sorted(
    ({'op': op, **stats} for op, stats in agg.items()),
    key=lambda r: r['total_us'],
    reverse=True,
)

print()
print('Top 10 ops by total time:')
for row in rows[:10]:
    print(
        f"{row['op']:<15} count={row['count']:>5} total={row['total_us']/1000:>10.2f} ms ratio={row['ratio']:.3f}%"
    )

focus_ops = ['TransData', 'Mul', 'Cast', 'Pows', 'RealDiv', 'Rsqrt']
print()
print('Ops relevant to decomposed RMSNorm:')
for name in focus_ops:
    row = next((r for r in rows if r['op'] == name), None)
    if row:
        print(
            f"{row['op']:<15} count={row['count']:>5} total={row['total_us']/1000:>10.2f} ms ratio={row['ratio']:.3f}%"
        )
```

```python
print('profiler_dir =', PROFILE_DIR)
sorted(str(path.relative_to(PROFILE_DIR)) for path in PROFILE_DIR.rglob('*') if path.is_file())[:20]
```

### 4 查看 Baseline `RMSNorm` 源码
上游 `Sana` 的 `RMSNorm` 在 Baseline 中仍是原始实现，会拆解为 `pow`、`mean`、`rsqrt`、`mul` 等小算子。

```python
norms_lines = (WORKSPACE / 'diffusion' / 'model' / 'norms.py').read_text(encoding='utf-8').splitlines()
for line_no in range(182, 232):
    print(f'{line_no}: {norms_lines[line_no - 1]}')
```

### 5 分析结论
从 Baseline 的 Profiling 结果和 `RMSNorm` 源码可以看到：
- 当前 `mean_single_step_latency_s` 仅作为 profiling 场景下的采样参考值；正式性能对比以下一节关闭 profiler 后的同口径指标为准。
- 整网中 `Mul`、`Cast`、`Pows`、`TransData` 等小算子存在可见开销。
- 结合 Baseline `RMSNorm` 源码，可以看到它仍是分解实现，因此适合在保持其余流程不变的前提下，尝试替换为 `torch_npu.npu_rms_norm`。

下一节会在相同 prompt、seed 和 step 设置下，对比优化前后的性能变化。

# ==========================================
## 📝 练习与验证

> 📌 原 Notebook 中的练习、编译命令和校验代码已按原顺序保留在上文。需要 CANN 运行时、Ascend NPU 或 CANNLab 环境的单元，执行前请先核对版本和设备条件。
