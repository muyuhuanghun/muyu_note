# 06.服务器与环境

📌 服务器管理和开发环境配置工具。

# ==========================================
# 📁 脚本列表
# ==========================================

| 脚本 | 功能 | 适用场景 |
|------|------|----------|
| `setup_dev_env.sh` | 一键配置开发环境 | 新机器/重装系统后快速部署 |
| `slurm_job_submit.sh` | SLURM 集群任务提交模板 | GPU 服务器训练模型 |

# ==========================================
# 🚀 使用示例
# ==========================================

## setup_dev_env.sh — 环境配置

```bash
# 完整安装（Python + Git + Node.js + 常用工具）
bash setup_dev_env.sh --full

# 只安装 Python 环境（Miniconda + 常用包）
bash setup_dev_env.sh --python-only

# 只安装终端工具（zsh + starship + nerd font）
bash setup_dev_env.sh --terminal-only
```

⚠️ 仅支持 Ubuntu/Debian 系 Linux 发行版

## slurm_job_submit.sh — SLURM 提交

```bash
# 提交 GPU 训练任务
bash slurm_job_submit.sh --gpu 1 --mem 16G --time 24:00:00 --cmd "python train.py"

# 提交 CPU 推理任务
bash slurm_job_submit.sh --cpu 4 --mem 8G --time 2:00:00 --cmd "python inference.py"

# 查看任务状态
squeue -u $USER
```

📌 SLURM 是学术界 GPU 集群的标准任务调度系统，几乎所有高校 HPC 都使用

# ==========================================
# 💡 Tips
# ==========================================

- `setup_dev_env.sh` 会自动检测系统版本并适配包管理器
- SLURM 脚本中的参数需要根据集群配置调整（分区名、GPU 型号等）
- 建议将常用环境配置存为 dotfiles 仓库，方便跨机器同步
