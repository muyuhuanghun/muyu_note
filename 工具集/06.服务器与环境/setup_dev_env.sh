#!/bin/bash
# ============================================================
# 开发环境一键配置脚本
# 📌 支持 Ubuntu/Debian，配置 Python + Git + 终端美化
# ⚠️ 仅适用于 Linux 系统
# ============================================================

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info()  { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn()  { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }
log_step()  { echo -e "\n${BLUE}==>${NC} $1"; }

# ============================================================
# 基础工具
# ============================================================
install_base() {
    log_step "安装基础工具"
    sudo apt update
    sudo apt install -y \
        build-essential \
        curl \
        wget \
        git \
        vim \
        htop \
        tree \
        unzip \
        software-properties-common \
        apt-transport-https \
        ca-certificates
    log_info "基础工具安装完成"
}

# ============================================================
# Python 环境（Miniconda）
# ============================================================
install_python() {
    log_step "安装 Python 环境（Miniconda）"

    if command -v conda &>/dev/null; then
        log_info "Miniconda 已安装，跳过"
    else
        log_info "下载 Miniconda..."
        wget -q https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /tmp/miniconda.sh
        bash /tmp/miniconda.sh -b -p "$HOME/miniconda3"
        rm /tmp/miniconda.sh

        # 初始化
        "$HOME/miniconda3/bin/conda" init bash
        log_info "Miniconda 安装完成"
    fi

    # 常用 Python 包
    log_info "安装常用 Python 包..."
    pip install --upgrade pip
    pip install \
        numpy \
        pandas \
        matplotlib \
        seaborn \
        scikit-learn \
        jupyter \
        tqdm \
        rich \
        httpx \
        pyyaml
    log_info "Python 包安装完成"
}

# ============================================================
# 终端美化
# ============================================================
install_terminal() {
    log_step "安装终端美化工具"

    # zsh
    if ! command -v zsh &>/dev/null; then
        sudo apt install -y zsh
    fi

    # oh-my-zsh
    if [ ! -d "$HOME/.oh-my-zsh" ]; then
        log_info "安装 oh-my-zsh..."
        sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended
    fi

    # starship prompt
    if ! command -v starship &>/dev/null; then
        log_info "安装 starship..."
        curl -sS https://starship.rs/install.sh | sh -s -- -y
    fi

    # 配置 .zshrc
    if ! grep -q "starship" "$HOME/.zshrc" 2>/dev/null; then
        echo 'eval "$(starship init zsh)"' >> "$HOME/.zshrc"
    fi

    # zsh 插件
    ZSH_CUSTOM="${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}"
    if [ ! -d "$ZSH_CUSTOM/plugins/zsh-autosuggestions" ]; then
        git clone https://github.com/zsh-users/zsh-autosuggestions "$ZSH_CUSTOM/plugins/zsh-autosuggestions"
    fi
    if [ ! -d "$ZSH_CUSTOM/plugins/zsh-syntax-highlighting" ]; then
        git clone https://github.com/zsh-users/zsh-syntax-highlighting "$ZSH_CUSTOM/plugins/zsh-syntax-highlighting"
    fi

    log_info "终端美化完成"
}

# ============================================================
# Node.js（用于一些 CLI 工具）
# ============================================================
install_nodejs() {
    log_step "安装 Node.js"
    if command -v node &>/dev/null; then
        log_info "Node.js 已安装: $(node --version)"
    else
        curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
        sudo apt install -y nodejs
        log_info "Node.js 安装完成"
    fi
}

# ============================================================
# Docker
# ============================================================
install_docker() {
    log_step "安装 Docker"
    if command -v docker &>/dev/null; then
        log_info "Docker 已安装，跳过"
    else
        curl -fsSL https://get.docker.com | sh
        sudo usermod -aG docker "$USER"
        log_info "Docker 安装完成（需要重新登录生效）"
    fi
}

# ============================================================
# 主入口
# ============================================================
usage() {
    echo "开发环境一键配置脚本"
    echo ""
    echo "用法: bash setup_dev_env.sh [选项]"
    echo ""
    echo "选项:"
    echo "  --full            完整安装（所有组件）"
    echo "  --python-only     只安装 Python 环境"
    echo "  --terminal-only   只安装终端美化"
    echo "  --base            只安装基础工具"
    echo "  --docker          安装 Docker"
}

case "$1" in
    --full)
        install_base
        install_python
        install_terminal
        install_nodejs
        install_docker
        echo -e "\n${GREEN}🎉 完整安装完成！请重新登录终端${NC}"
        ;;
    --python-only)
        install_base
        install_python
        echo -e "\n${GREEN}🎉 Python 环境安装完成！${NC}"
        ;;
    --terminal-only)
        install_terminal
        echo -e "\n${GREEN}🎉 终端美化完成！${NC}"
        ;;
    --base)
        install_base
        echo -e "\n${GREEN}🎉 基础工具安装完成！${NC}"
        ;;
    --docker)
        install_docker
        echo -e "\n${GREEN}🎉 Docker 安装完成！${NC}"
        ;;
    *)
        usage
        ;;
esac
