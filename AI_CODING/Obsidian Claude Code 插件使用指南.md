# Obsidian Claude Code 插件使用指南

## 📦 插件安装

插件已安装在 `.obsidian/plugins/obsidian-claude-code/` 目录下。

### 启用插件

1. 打开 Obsidian
2. 进入 设置 → 第三方插件
3. 找到 **Claude Code** 并启用

## 🚀 快速开始

### 打开方式

- **侧边栏图标**: 点击左侧边栏的终端图标
- **命令面板**: `Ctrl/Cmd + P` → 输入 "Open Claude Code"

### 界面布局

```
┌─────────────────────────────────────┐
│  📁 Vault Information               │
│  显示笔记数量、大小、分支等信息      │
├─────────────────────────────────────┤
│  Claude Code                    [🗑][⚙]│
├─────────────────────────────────────┤
│                                     │
│  [C] 👋 Welcome to Claude Code!     │
│                                     │
├─────────────────────────────────────┤
│  ┌─────────────────────────┐ [➤]   │
│  │ Type your message...     │       │
│  └─────────────────────────┘       │
│  [📎] [💻] [🔌]                    │
│  ┌─────────────────────────────────┐│
│  │ Model: [Claude Sonnet 4 ▼]      ││
│  │ Effort: [Medium ▼]              ││
│  │ Permission: [Manual ▼]          ││
│  └─────────────────────────────────┘│
└─────────────────────────────────────┘
```

## 💬 使用方法

### 与 Claude 对话

直接在输入框中输入问题，按 `Enter` 发送：

```
你: 帮我写一个 Python 快速排序算法
Claude: 好的，这是一个 Python 快速排序实现...
```

### 执行终端命令

使用 `/terminal` 前缀执行命令：

```
/terminal ls -la
/terminal git status
/terminal python --version
```

### 快捷命令

| 命令 | 说明 |
|------|------|
| `/help` | 显示帮助信息 |
| `/clear` | 清空聊天记录 |
| `/repo` | 刷新仓库信息 |
| `/terminal <cmd>` | 执行终端命令 |

## 🔄 模型与参数控制

输入框下方有三个下拉选择器，可以实时调整 Claude 的行为：

### Model (模型选择)

| 模型 | 说明 | 适用场景 |
|------|------|----------|
| `Claude Sonnet 4` | 平衡性能与速度 | 日常使用 (默认) |
| `Claude Opus 4` | 最强能力 | 复杂任务、代码生成 |
| `Claude Haiku 4` | 最快速度 | 简单问题、快速回复 |

### Effort (思考深度)

| 级别 | max-turns | 说明 |
|------|-----------|------|
| `Low` | 3 | 快速响应，较少思考 |
| `Medium` | 默认 | 平衡模式 |
| `High` | 20 | 深度思考，更准确 |

### Permission (审批模式)

| 模式 | CLI 参数 | 说明 |
|------|----------|------|
| `Auto` | `--dangerously-skip-permissions` | 自动批准所有操作 |
| `Manual` | 默认 | 手动批准每个操作 |
| `Plan` | `--permission-mode plan` | 先规划再执行 |

## ⚙️ 设置选项

进入 设置 → Claude Code 进行配置：

- **Claude Code Path**: Claude CLI 路径（默认: `claude`）
- **Shell Path**: 终端 Shell 路径
- **Auto-scroll**: 自动滚动到最新消息
- **Show Line Numbers**: 代码块显示行号
- **Max History**: 最大消息保留数量
- **Theme**: 界面主题
- **Model**: 默认使用的模型
- **Effort**: 默认思考深度
- **Permission Mode**: 默认审批模式

## 🎯 使用场景

### 1. 代码生成

```
你: 帮我写一个 Obsidian 插件的 main.ts 模板
Claude: 好的，这是一个基础的 Obsidian 插件模板...
```

### 2. 代码解释

```
你: 解释一下这段代码的作用
[粘贴代码]
Claude: 这段代码实现了...
```

### 3. 笔记辅助

```
你: 帮我整理一下深度学习的笔记结构
Claude: 建议按照以下结构组织...
```

### 4. Git 操作

```
你: 帮我查看最近的 git 提交
/terminal git log --oneline -10
```

## 🔧 前置要求

确保已安装 Claude Code CLI：

```bash
npm install -g @anthropic-ai/claude-code
```

验证安装：

```bash
claude --version
```

## 📝 注意事项

1. **安全性**: 命令会在 Vault 目录下执行，请注意安全
2. **性能**: 长时间运行的命令可能会影响 Obsidian 性能
3. **兼容性**: 仅支持桌面端

## 🐛 常见问题

### Q: Claude Code 无法连接？

A: 检查 Claude Code 是否正确安装：
```bash
claude --version
```

### Q: 命令执行失败？

A: 检查 Shell 路径设置是否正确。

### Q: 如何更新插件？

A: 进入插件目录，拉取最新代码后重新构建：
```bash
cd .obsidian/plugins/obsidian-claude-code
git pull
npm install
npm run build
```

## 🔗 相关链接

- [Claude Code 官方文档](https://docs.anthropic.com/claude-code)
- [Obsidian 插件开发文档](https://docs.obsidian.md/Plugins/Getting+started)

---

*最后更新: 2026-06-24*
