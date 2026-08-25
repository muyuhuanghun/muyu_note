---
source_repo: cann-learning-hub
source_path: reference_practice/model_inference_optimization/sana_video/04_rmsnorm_fusion_optimization.ipynb
source_commit: 1bf85454ed7c41e184a96fb51d109b6bb83b7c0d
note_kind: notebook_to_markdown
---

# 4 RMSNorm 融合接入与收益验证

> 📚 上游 Notebook：[reference_practice/model_inference_optimization/sana_video/04_rmsnorm_fusion_optimization.ipynb](https://gitcode.com/cann/cann-learning-hub/blob/master/reference_practice/model_inference_optimization/sana_video/04_rmsnorm_fusion_optimization.ipynb)
> 🧪 整理方式：保留 Markdown 与代码单元；省略 Jupyter 执行输出，避免把一次性环境结果误当成可复现结论。

## 🧭 学习目标

- 先读懂概念，再运行代码片段验证关键结论；
- 把本节内容接入后续 CANN / Ascend NPU 实践。

# ==========================================
## 📖 课程内容

本节在 Baseline 基础上将上游 `Sana` 的原始 `RMSNorm.forward()` 替换为 `torch_npu.npu_rms_norm`，并验证该替换对整网时延的影响。本节只关注 `Sana-Video` 中的接入与收益验证，不展开 `torch_npu.npu_rms_norm` 的接口细节与单算子测试。

---

### 1 环境与工作区准备
如需独立执行本 Notebook，会重复完成环境初始化、源码拉取和教程文件覆盖。默认已完成 `02_baseline_run.ipynb` 的依赖安装。为加速模型下载，教程默认使用 HF-Mirror 镜像源。

```python
import json
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

### 2 记录 Baseline 指标
这里仍然使用原始 `RMSNorm` 实现，关闭视频保存，只保留性能对比需要的 metrics 输出。本节同样使用 20 个 sample step，输出的 `mean_single_step_latency_s` 作为正式 benchmark 基准。

```python
BASELINE_WORK_DIR = SOURCE_DIR / 'run_outputs' / 'benchmark_baseline'
BASELINE_WORK_DIR.mkdir(parents=True, exist_ok=True)
baseline_cmd = [
    sys.executable,
    str(WORKSPACE / 'inference_video_scripts' / 'inference_sana_video.py'),
    '--config', str(WORKSPACE / 'configs' / 'sana_video_config' / 'Sana_2000M_480px_AdamW_fsdp.yaml'),
    '--model_path', 'hf://Efficient-Large-Model/SANA-Video_2B_480p/checkpoints/SANA_Video_2B_480p.pth',
    '--txt_file', str(WORKSPACE / 'asset' / 'samples' / 'tutorial_video_prompts_samples.txt'),
    '--cfg_scale', '6',
    '--motion_score', '30',
    '--flow_shift', '8',
    '--work_dir', str(BASELINE_WORK_DIR),
    '--sample_nums', '1',
    '--step', '20',
    '--metrics_tag', 'baseline_benchmark',
    '--skip_save', 'True',
    '--model.fp32_attention', 'False',
]
subprocess.run(baseline_cmd, cwd=WORKSPACE, check=True)
baseline_metrics = json.loads((BASELINE_WORK_DIR / 'metrics' / 'baseline_benchmark_summary.json').read_text(encoding='utf-8'))
baseline_metrics
```

### 3 替换 `RMSNorm.forward()`
执行下面脚本修改 `diffusion/model/norms.py`，将原本的RMSNorm实现替换为torch_npu.npu_rms_norm。

```python
norms_path = WORKSPACE / 'diffusion' / 'model' / 'norms.py'
source = norms_path.read_text(encoding='utf-8')
if 'import torch_npu' not in source:
    source = source.replace('import torch\n', 'import torch\nimport torch_npu\n')
old_block = '''    def forward(self, x):
        """
        Forward pass through the RMSNorm layer.

        Args:
            x (torch.Tensor): The input tensor.

        Returns:
            torch.Tensor: The output tensor after applying RMSNorm.

        """
        ndim = x.dim()
        weight_shape = [1] * ndim
        weight_shape[self.norm_dim] = -1
        weight = self.weight.view(*weight_shape)
        return (weight * self._norm(x.float())).type_as(x)
'''
new_block = '''    def forward(self, x):
        """
        Forward pass through the RMSNorm layer.

        Args:
            x (torch.Tensor): The input tensor.

        Returns:
            torch.Tensor: The output tensor after applying RMSNorm.

        """
        if hasattr(torch, "npu") and torch.npu.is_available():
            return torch_npu.npu_rms_norm(x, self.weight, epsilon=self.eps)[0]
        ndim = x.dim()
        weight_shape = [1] * ndim
        weight_shape[self.norm_dim] = -1
        weight = self.weight.view(*weight_shape)
        return (weight * self._norm(x.float())).type_as(x)
'''
if old_block not in source:
    raise RuntimeError('Cannot locate the expected RMSNorm.forward block in norms.py.')
norms_path.write_text(source.replace(old_block, new_block), encoding='utf-8')
print('RMSNorm.forward has been replaced with torch_npu.npu_rms_norm.')
```

### 4 确认替换后的实现
阅读替换后的源码，确认优化点只作用于 `RMSNorm`。

```python
norms_lines = norms_path.read_text(encoding='utf-8').splitlines()
for line_no in range(182, 230):
    print(f'{line_no}: {norms_lines[line_no - 1]}')
```

### 5 运行优化版本
保持 prompt、seed 和 step 设置一致，只改变 `RMSNorm` 的实现。

```python
OPT_WORK_DIR = SOURCE_DIR / 'run_outputs' / 'benchmark_optimized'
OPT_WORK_DIR.mkdir(parents=True, exist_ok=True)
optimized_cmd = [
    sys.executable,
    str(WORKSPACE / 'inference_video_scripts' / 'inference_sana_video.py'),
    '--config', str(WORKSPACE / 'configs' / 'sana_video_config' / 'Sana_2000M_480px_AdamW_fsdp.yaml'),
    '--model_path', 'hf://Efficient-Large-Model/SANA-Video_2B_480p/checkpoints/SANA_Video_2B_480p.pth',
    '--txt_file', str(WORKSPACE / 'asset' / 'samples' / 'tutorial_video_prompts_samples.txt'),
    '--cfg_scale', '6',
    '--motion_score', '30',
    '--flow_shift', '8',
    '--work_dir', str(OPT_WORK_DIR),
    '--sample_nums', '1',
    '--step', '20',
    '--metrics_tag', 'optimized_benchmark',
    '--skip_save', 'True',
    '--model.fp32_attention', 'False',
]
subprocess.run(optimized_cmd, cwd=WORKSPACE, check=True)
optimized_metrics = json.loads((OPT_WORK_DIR / 'metrics' / 'optimized_benchmark_summary.json').read_text(encoding='utf-8'))
optimized_metrics
```

### 6 结果对比
下面以 `mean_single_step_latency_s` 为基准计算优化收益。这里比较的是关闭 profiler 后的平均采样单步时延，因此它不直接对应上一节 `Step trace` 的 `Stage` 时间，也不等同于运行时 tqdm 显示的 `xx s/it`。运行完成后，`performance_improvement_pct` 即可直接用于填写性能提升百分比。

```python
from IPython.display import Markdown, display

baseline_latency = baseline_metrics['mean_single_step_latency_s']
optimized_latency = optimized_metrics['mean_single_step_latency_s']
performance_improvement_pct = (baseline_latency - optimized_latency) / baseline_latency * 100
comparison = {
    'baseline_single_step_latency_s': baseline_latency,
    'optimized_single_step_latency_s': optimized_latency,
    'performance_improvement_pct': performance_improvement_pct,
}
display(Markdown(f"""
| 指标 | 数值 |
| --- | ---: |
| Baseline 单步时延 | {baseline_latency:.4f} s ({baseline_latency * 1000:.2f} ms) |
| 优化后单步时延 | {optimized_latency:.4f} s ({optimized_latency * 1000:.2f} ms) |
| 性能提升 | {performance_improvement_pct:.2f}% |
"""))
```

# ==========================================
## 📝 练习与验证

> 📌 原 Notebook 中的练习、编译命令和校验代码已按原顺序保留在上文。需要 CANN 运行时、Ascend NPU 或 CANNLab 环境的单元，执行前请先核对版本和设备条件。
