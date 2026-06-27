#!/bin/bash
# ============================================================
# SLURM 集群任务提交模板
# 📌 提交 GPU/CPU 训练任务到 SLURM 调度系统
# 📌 适用于高校 HPC 集群（如 UESTC 超算中心）
# ============================================================

# ============================================================
# 使用方法
# ============================================================
# 1. 直接运行（会生成并提交 sbatch 脚本）:
#    bash slurm_job_submit.sh --gpu 1 --mem 16G --time 24:00:00 --cmd "python train.py"
#
# 2. 只生成脚本（不提交）:
#    bash slurm_job_submit.sh --gpu 1 --mem 16G --time 24:00:00 --cmd "python train.py" --generate-only
#
# 3. 查看任务状态:
#    squeue -u $USER
#
# 4. 取消任务:
#    scancel <job_id>
# ============================================================

set -e

# 默认参数
GPU_COUNT=1
CPU_COUNT=4
MEMORY="16G"
TIME="24:00:00"
PARTITION="gpu"          # 分区名（需要根据集群修改）
JOB_NAME="train_job"
COMMAND=""
OUTPUT_DIR="slurm_logs"
GENERATE_ONLY=false
NOTIFY_EMAIL=""          # 通知邮箱

usage() {
    echo "SLURM 任务提交工具"
    echo ""
    echo "用法: bash slurm_job_submit.sh [选项]"
    echo ""
    echo "选项:"
    echo "  --gpu N           GPU 数量（默认 1）"
    echo "  --cpu N           CPU 核数（默认 4）"
    echo "  --mem SIZE        内存大小（默认 16G）"
    echo "  --time TIME       最大运行时间（默认 24:00:00）"
    echo "  --partition NAME  分区名（默认 gpu）"
    echo "  --name NAME       任务名称（默认 train_job）"
    echo "  --cmd COMMAND     要执行的命令（必需）"
    echo "  --email ADDRESS   任务完成通知邮箱"
    echo "  --generate-only   只生成脚本，不提交"
    echo ""
    echo "示例:"
    echo "  bash slurm_job_submit.sh --gpu 1 --mem 16G --time 24:00:00 --cmd \"python train.py\""
    echo "  bash slurm_job_submit.sh --cpu 8 --mem 32G --time 4:00:00 --cmd \"python inference.py\""
}

# 解析参数
while [[ $# -gt 0 ]]; do
    case $1 in
        --gpu)           GPU_COUNT="$2"; shift 2 ;;
        --cpu)           CPU_COUNT="$2"; shift 2 ;;
        --mem)           MEMORY="$2"; shift 2 ;;
        --time)          TIME="$2"; shift 2 ;;
        --partition)     PARTITION="$2"; shift 2 ;;
        --name)          JOB_NAME="$2"; shift 2 ;;
        --cmd)           COMMAND="$2"; shift 2 ;;
        --email)         NOTIFY_EMAIL="$2"; shift 2 ;;
        --generate-only) GENERATE_ONLY=true; shift ;;
        *)               usage; exit 1 ;;
    esac
done

if [ -z "$COMMAND" ]; then
    echo "❌ 必须指定 --cmd 参数"
    usage
    exit 1
fi

# 创建日志目录
mkdir -p "$OUTPUT_DIR"

# 生成 sbatch 脚本
SCRIPT_FILE="${OUTPUT_DIR}/${JOB_NAME}.sh"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_FILE="${OUTPUT_DIR}/${JOB_NAME}_${TIMESTAMP}.log"

cat > "$SCRIPT_FILE" << EOF
#!/bin/bash
#SBATCH --job-name=${JOB_NAME}
#SBATCH --partition=${PARTITION}
#SBATCH --gres=gpu:${GPU_COUNT}
#SBATCH --cpus-per-task=${CPU_COUNT}
#SBATCH --mem=${MEMORY}
#SBATCH --time=${TIME}
#SBATCH --output=${LOG_FILE}
#SBATCH --error=${LOG_FILE}
EOF

# 添加通知邮箱（如果指定）
if [ -n "$NOTIFY_EMAIL" ]; then
    echo "#SBATCH --mail-type=END,FAIL" >> "$SCRIPT_FILE"
    echo "#SBATCH --mail-user=${NOTIFY_EMAIL}" >> "$SCRIPT_FILE"
fi

cat >> "$SCRIPT_FILE" << 'EOF'

# ============================================================
# 环境配置
# ============================================================

# 加载 CUDA 模块（根据集群配置修改）
# module load cuda/11.8
# module load anaconda3

# 激活 conda 环境
# source activate your_env

# ============================================================
# 运行信息
# ============================================================

echo "========================================"
echo "Job ID: $SLURM_JOB_ID"
echo "Job Name: $SLURM_JOB_NAME"
echo "Node: $SLURM_NODELIST"
echo "GPU: $SLURM_GPUS_ON_NODE"
echo "CPU: $SLURM_CPUS_ON_NODE"
echo "Start Time: $(date)"
echo "========================================"

EOF

# 添加用户命令
echo "# 执行用户命令" >> "$SCRIPT_FILE"
echo "$COMMAND" >> "$SCRIPT_FILE"

cat >> "$SCRIPT_FILE" << 'EOF'

echo ""
echo "========================================"
echo "End Time: $(date)"
echo "========================================"
EOF

chmod +x "$SCRIPT_FILE"
echo "📄 脚本已生成: $SCRIPT_FILE"

# 提交任务
if [ "$GENERATE_ONLY" = true ]; then
    echo "🔍 仅生成模式，未提交任务"
else
    JOB_ID=$(sbatch "$SCRIPT_FILE" | awk '{print $NF}')
    echo "✅ 任务已提交: Job ID = $JOB_ID"
    echo ""
    echo "💡 常用命令:"
    echo "   查看状态: squeue -u $USER"
    echo "   查看日志: tail -f $LOG_FILE"
    echo "   取消任务: scancel $JOB_ID"
fi
