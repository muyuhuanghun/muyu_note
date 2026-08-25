---
source_repo: cann-learning-hub
source_path: reference_practice/model_inference_optimization/sana_video/02_baseline_run.ipynb
source_commit: 1bf85454ed7c41e184a96fb51d109b6bb83b7c0d
note_kind: notebook_to_markdown
---

# 2 Baseline 跑通

> 📚 上游 Notebook：[reference_practice/model_inference_optimization/sana_video/02_baseline_run.ipynb](https://gitcode.com/cann/cann-learning-hub/blob/master/reference_practice/model_inference_optimization/sana_video/02_baseline_run.ipynb)
> 🧪 整理方式：保留 Markdown 与代码单元；省略 Jupyter 执行输出，避免把一次性环境结果误当成可复现结论。

## 🧭 学习目标

- 先读懂概念，再运行代码片段验证关键结论；
- 把本节内容接入后续 CANN / Ascend NPU 实践。

# ==========================================
## 📖 课程内容

本节将跑通 `Sana-Video`，只覆盖模型在 NPU 上运行所需的最小兼容适配。

**硬件要求**：
- NPU 显存：32GB（910B 满足要求）
- 主机内存：**最低 16GB**，**推荐 32GB**（模型加载峰值约 20GB）

---

### 1 环境准备
定位教程目录、准备运行工作区，并把 CANN 环境变量导入当前 Notebook 进程。为加速模型下载，教程默认使用 HF-Mirror 镜像源。在线体验请直接在 GitCode Notebook 环境中执行，本地运行时再使用独立 Python/conda 环境。

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

print('REPO_ROOT =', REPO_ROOT)
print('UPSTREAM_SANA_DIR =', UPSTREAM_SANA_DIR)
print('WORKSPACE =', WORKSPACE)
```

### 2 拉取上游 Sana 源码并构建教程工作区
Notebook 会先拉取上游 `Sana` 指定版本，再以教程目录自身为主体构建工作区。工作区中的 `pyproject.toml` 使用教程自带配置，上游代码以非覆盖方式复制进来。

```python
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
subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=UPSTREAM_SANA_DIR, check=True)

WORKSPACE.mkdir(parents=True, exist_ok=True)
(WORKSPACE / 'inference_video_scripts').mkdir(parents=True, exist_ok=True)
(WORKSPACE / 'asset' / 'samples').mkdir(parents=True, exist_ok=True)
shutil.copy2(TUTORIAL_DIR / 'src' / 'pyproject.toml', WORKSPACE / 'pyproject.toml')
shutil.copy2(TUTORIAL_DIR / 'src' / 'sana_npu_adaptation.py', WORKSPACE / 'sana_npu_adaptation.py')
shutil.copy2(
    TUTORIAL_DIR / 'src' / 'inference_video_scripts' / 'inference_sana_video.py',
    WORKSPACE / 'inference_video_scripts' / 'inference_sana_video.py',
)
shutil.copy2(
    TUTORIAL_DIR / 'src' / 'samples' / 'video_prompts_samples.txt',
    WORKSPACE / 'asset' / 'samples' / 'tutorial_video_prompts_samples.txt',
)
subprocess.run(
    ['bash', '-lc', f'cp -rn "{UPSTREAM_SANA_DIR}/." "{WORKSPACE}"'],
    check=True,
)
print('Workspace ready:', WORKSPACE)
```

### 3 安装依赖
首次执行可能耗时较长（mmcv 编译约需 10 分钟）。为加速下载，教程默认使用清华 PyPI 镜像源。GitCode Notebook 环境会直接复用已预装的 `torch`、`torch_npu`、`torchvision` 与 `torchaudio`，这里只安装教程工作区的其余 Python 依赖。

**注意**：安装过程中部分依赖（如 mmcv、clip 等）需从 GitHub 拉取源码，可能由于网络不稳定拉取失败，通常可通过**重新执行 cell 解决**。

```bash
PIP_INDEX_URL = 'https://pypi.tuna.tsinghua.edu.cn/simple'
PIP_TRUSTED_HOST = 'pypi.tuna.tsinghua.edu.cn'

subprocess.run([
    sys.executable, '-m', 'pip', 'install', '-e', str(WORKSPACE),
    '-i', PIP_INDEX_URL,
    '--trusted-host', PIP_TRUSTED_HOST,
], check=True)
subprocess.run([sys.executable, '-m', 'pip', 'uninstall', '-y', 'opencv-python'], check=False)
subprocess.run([
    sys.executable, '-m', 'pip', 'install', 'opencv-python-headless==4.8.0.76',
    '-i', PIP_INDEX_URL,
    '--trusted-host', PIP_TRUSTED_HOST,
], check=True)

MMCV_DIR = SOURCE_DIR / 'mmcv-1x'
if not MMCV_DIR.exists():
    subprocess.run(['git', 'clone', '-b', '1.x', 'https://github.com/open-mmlab/mmcv.git', str(MMCV_DIR)], check=True)
subprocess.run(
    'MMCV_WITH_OPS=1 FORCE_NPU=1 pip install -e . --no-build-isolation',
    cwd=MMCV_DIR,
    shell=True,
    check=True,
)
```

### 4 执行 Baseline 推理
下面脚本将加载模型权重，生成480p 5s的视频，本教程示例使用 20 个 sample step，当前环境下推理时长约为2.5分钟。

首次运行会自动下载模型文件：
- **VAE**: `vae/Wan2.1_VAE.pth` (508 MB)
- **主模型**: `checkpoints/SANA_Video_2B_480p.pth` (8.25 GB)

**预估下载时间**：约 10-20 分钟（取决于网络速度）

**实时监控下载进度**（在 GitCode 终端执行）：
```bash
# 查看已下载文件大小
du -sh ~/.cache/huggingface/hub/models--Efficient-Large-Model--SANA-Video_2B_480p/

# 实时监控下载进度（每 5 秒刷新）
watch -n 5 'du -sh ~/.cache/huggingface/hub/models--Efficient-Large-Model--SANA-Video_2B_480p/'
```

```python
BASELINE_WORK_DIR = SOURCE_DIR / 'run_outputs' / 'baseline_demo'
BASELINE_WORK_DIR.mkdir(parents=True, exist_ok=True)
cmd = [
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
    '--metrics_tag', 'baseline_demo',
    '--model.fp32_attention', 'False',
]
subprocess.run(cmd, cwd=WORKSPACE, check=True)
```

### 5 查看结果
教程版推理入口会在 `metrics/<tag>_summary.json` 中保存平均采样总时长与平均单步时延。生成的视频保存在 `metrics['save_root']` 指向的目录中。

```python
metrics_path = BASELINE_WORK_DIR / 'metrics' / 'baseline_demo_summary.json'
metrics = json.loads(metrics_path.read_text(encoding='utf-8'))
metrics
```

由于平台暂无法直接展示生成的.mp4文件，可执行下面脚本将视频压缩到指定目录，下载到本地并解压查看。

```python
from pathlib import Path

video_dir = Path(metrics['save_root'])
print('video_dir =', video_dir)

mp4_files = sorted(str(path) for path in video_dir.glob('*.mp4'))
print('生成的视频文件：')
for f in mp4_files:
    print(f)

archive_path = (video_dir.parent / "baseline_demo_vis.tar.gz").resolve()
!tar -czf "{archive_path}" -C "{video_dir.parent}" "{video_dir.name}"

print('\n已打包为:', archive_path)
```

# ==========================================
## 📝 练习与验证

> 📌 原 Notebook 中的练习、编译命令和校验代码已按原顺序保留在上文。需要 CANN 运行时、Ascend NPU 或 CANNLab 环境的单元，执行前请先核对版本和设备条件。
