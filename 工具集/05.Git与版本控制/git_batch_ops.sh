#!/bin/bash
# ============================================================
# Git 批量操作工具
# 📌 清理分支、安全拉取、子模块同步、仓库统计
# ============================================================

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

usage() {
    echo "Git 批量操作工具"
    echo ""
    echo "用法: bash git_batch_ops.sh <命令>"
    echo ""
    echo "命令:"
    echo "  clean-merged      清理已合并到当前分支的本地分支"
    echo "  safe-pull          stash → pull → pop（安全拉取远端更新）"
    echo "  pull-submodules    批量拉取所有子模块"
    echo "  stats              显示仓库统计信息"
    echo "  stash-all          暂存所有修改"
    echo "  unstash-all        恢复暂存的修改"
    echo "  sync-fork          同步 fork 的上游仓库"
    echo ""
    echo "示例:"
    echo "  bash git_batch_ops.sh clean-merged"
    echo "  bash git_batch_ops.sh safe-pull"
}

# ============================================================
# clean-merged: 清理已合并的本地分支
# ============================================================
clean_merged() {
    echo -e "${GREEN}🧹 清理已合并的本地分支${NC}"
    current_branch=$(git branch --show-current)
    echo "   当前分支: $current_branch"
    echo ""

    merged_branches=$(git branch --merged "$current_branch" | grep -v "^\*" | grep -v "main" | grep -v "master" || true)

    if [ -z "$merged_branches" ]; then
        echo "   ✅ 没有需要清理的分支"
        return
    fi

    echo "   以下分支已合并到 $current_branch:"
    echo "$merged_branches"
    echo ""
    read -p "   确认删除？(y/N) " confirm
    if [ "$confirm" = "y" ] || [ "$confirm" = "Y" ]; then
        echo "$merged_branches" | xargs git branch -d
        echo -e "   ${GREEN}✅ 清理完成${NC}"
    else
        echo "   ⏹️ 已取消"
    fi
}

# ============================================================
# safe-pull: stash → pull → pop
# ============================================================
safe_pull() {
    echo -e "${GREEN}🔄 安全拉取远端更新${NC}"
    current_branch=$(git branch --show-current)
    echo "   当前分支: $current_branch"

    # 检查是否有未提交的修改
    if git diff --quiet && git diff --cached --quiet; then
        echo "   工作区干净，直接拉取"
        git pull origin "$current_branch"
    else
        echo "   ⚠️ 检测到未提交的修改，先 stash"
        git stash push -m "auto-stash before pull $(date +%Y%m%d_%H%M%S)"
        git pull origin "$current_branch"
        git stash pop
        echo -e "   ${GREEN}✅ 拉取完成，已恢复暂存的修改${NC}"
    fi
}

# ============================================================
# pull-submodules: 批量拉取子模块
# ============================================================
pull_submodules() {
    echo -e "${GREEN}📦 更新所有子模块${NC}"
    git submodule update --init --recursive
    echo -e "${GREEN}✅ 子模块更新完成${NC}"
}

# ============================================================
# stats: 仓库统计
# ============================================================
show_stats() {
    echo -e "${GREEN}📊 仓库统计${NC}"
    echo ""

    # 基本信息
    echo "   远程仓库: $(git remote get-url origin 2>/dev/null || echo '无')"
    echo "   当前分支: $(git branch --show-current)"
    echo ""

    # 提交统计
    total_commits=$(git rev-list --all --count 2>/dev/null || echo "0")
    echo "   总提交数: $total_commits"

    # 今日提交
    today_commits=$(git log --since="midnight" --oneline 2>/dev/null | wc -l || echo "0")
    echo "   今日提交: $today_commits"

    # 文件统计
    total_files=$(git ls-files | wc -l)
    echo "   跟踪文件: $total_files"

    # 仓库大小
    repo_size=$(du -sh .git 2>/dev/null | cut -f1 || echo "未知")
    echo "   仓库大小: $repo_size"

    # 最近活动
    echo ""
    echo "   最近 5 次提交:"
    git log --oneline -5 --pretty=format="     %h %s (%ar)" 2>/dev/null || echo "     无提交记录"
    echo ""
}

# ============================================================
# stash-all / unstash-all
# ============================================================
stash_all() {
    echo -e "${GREEN}📦 暂存所有修改${NC}"
    git stash push -m "manual-stash $(date +%Y%m%d_%H%M%S)" --include-untracked
    echo -e "${GREEN}✅ 已暂存${NC}"
}

unstash_all() {
    echo -e "${GREEN}📦 恢复暂存的修改${NC}"
    git stash pop
    echo -e "${GREEN}✅ 已恢复${NC}"
}

# ============================================================
# sync-fork: 同步上游仓库
# ============================================================
sync_fork() {
    echo -e "${GREEN}🔄 同步上游仓库${NC}"

    # 检查是否有 upstream
    if ! git remote get-url upstream &>/dev/null; then
        echo -e "   ${YELLOW}⚠️ 未配置 upstream 远程仓库${NC}"
        echo "   请先运行: git remote add upstream <上游仓库URL>"
        return
    fi

    current_branch=$(git branch --show-current)
    git fetch upstream
    git merge upstream/main --no-edit
    git push origin "$current_branch"
    echo -e "${GREEN}✅ 同步完成${NC}"
}

# ============================================================
# 主入口
# ============================================================
case "$1" in
    clean-merged)    clean_merged ;;
    safe-pull)       safe_pull ;;
    pull-submodules) pull_submodules ;;
    stats)           show_stats ;;
    stash-all)       stash_all ;;
    unstash-all)     unstash_all ;;
    sync-fork)       sync_fork ;;
    *)               usage ;;
esac
