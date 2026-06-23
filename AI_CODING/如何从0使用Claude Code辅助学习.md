# 如何从0使用 Claude Code 辅助学习

Claude Code 是 Anthropic 官方推出的 AI 编程 CLI 工具，直接在终端里和 Claude 对话，能读写文件、执行命令、搜索代码。相比网页版 ChatGPT/Claude，它的核心优势是**能直接操作你的本地项目**——读代码、改文件、跑命令、管理 Git，全部在一个终端里完成。

本文覆盖从安装到深度集成的完整流程。

# 一.前置准备

## 1.Node.js

Claude Code 基于 Node.js 运行，需要 **18+** 版本。

```
# 📌 下载安装 Node.js
# 官网：https://nodejs.org/zh-cn
# 安装时勾选"Add to PATH"

# 验证安装
node -v    # 应显示 v18.x.x 或更高
npm -v     # 应显示 9.x.x 或更高
```

## 2.Git for Windows

Claude Code 依赖 Git 进行版本控制操作，Windows 用户需要安装 Git for Windows。

```
# 📌 下载安装 Git for Windows
# 官网：https://git-scm.com/download/win
# 安装时选择"Use Git from the Windows Command Line"

# 验证安装
git --version    # 应显示 git version 2.x.x
```

## 3.终端环境

推荐使用 **PowerShell 7+** 或 **Windows Terminal**，自带的 cmd 也可以但体验较差。

```
# 📌 PowerShell 7 安装（可选但推荐）
# Microsoft Store 搜索 "PowerShell" 安装即可
# 或：winget install Microsoft.PowerShell
```

# 二.安装 Claude Code

前置准备就绪后，一条命令搞定安装：

```
# 🌟 全局安装 Claude Code
npm install -g @anthropic-ai/claude-code

# 验证安装
claude --version
```

⚠️ 如果遇到权限错误（Windows 上较少见），用管理员权限运行终端重试。

安装完成后，在任意项目目录下输入 `claude` 即可启动。

# 三.认证配置

Claude Code 需要 API Key 才能使用。有两种方式：官方 API 和第三方中转。

## 1.官方 API（推荐，最稳定）

```
# 📌 方式一：首次启动时交互式登录
claude
# → 会自动打开浏览器，登录 Anthropic 账号并授权

# 📌 方式二：手动设置 API Key
export ANTHROPIC_API_KEY="sk-ant-xxxxxxxxxxxxxxxx"
# Windows PowerShell：
$env:ANTHROPIC_API_KEY="sk-ant-xxxxxxxxxxxxxxxx"
```

💡 官方 API 注册地址：https://console.anthropic.com
- 需要海外手机号验证
- 按 token 计费，Sonnet 4 性价比最高
- 支持 Claude 全系列模型

## 2.使用 ccswitch 管理 API（推荐）

📌 **ccswitch** 是一个统一的 API 供应商管理工具，可以一键切换不同的 API 供应商（官方、中转站、DeepSeek 等），免去手动配置环境变量的麻烦。

### 安装 ccswitch

```
# 📌 下载安装
# GitHub: https://github.com/farion1231/cc-switch
# 在 Release 页面下载对应系统版本（Windows/macOS/Linux）
# 解压后将可执行文件放到 PATH 目录下，或直接双击运行

# 验证安装
ccswitch --version
```

### 添加 API 供应商

ccswitch 支持管理多个供应商，每个供应商可以配置不同的 API Key 和请求地址：

```
# 📌 添加供应商（交互式配置）
ccswitch add

# 配置项说明：
# - 供应商名称：自定义标识，如 "anthropic官方"、"某某中转站"、"deepseek"
# - API Key：从供应商后台获取
# - 请求地址（Base URL）：
#   · 官方：https://api.anthropic.com
#   · 中转站：供应商提供的地址
#   · DeepSeek：https://api.deepseek.com/anthropic
# - 认证字段：ANTHROPIC_API_KEY 或 ANTHROPIC_AUTH_TOKEN（取决于供应商）
```

### 常用命令

```
# 📌 ccswitch 日常操作

ccswitch list          # 查看已配置的所有供应商
ccswitch use <名称>    # 切换到指定供应商（自动设置环境变量）
ccswitch current       # 查看当前使用的供应商
ccswitch remove <名称> # 删除某个供应商配置
ccswitch edit <名称>   # 修改供应商配置
```

### 与 Claude Code 配合

```
# 📌 典型工作流

# 1. 配置好多个供应商后，切换到目标供应商
ccswitch use anthropic官方

# 2. 直接启动 Claude Code，自动读取环境变量
claude

# 3. 需要切换时，退出 Claude Code → 切换供应商 → 重新启动
ccswitch use deepseek
claude
```

💡 **ccswitch 的优势**：
- 一次配置，永久生效，不用每次手动 export 环境变量
- 多供应商随时切换，方便对比不同模型的效果
- 配置文件本地存储，API Key 不会泄露到终端历史

## 3.其他第三方中转站

如果不想用 ccswitch，也可以手动配置环境变量。市面上常见中转站大多基于 sub2api，操作基本一致：

```
# 📌 手动配置中转站

# Step 1: 在中转站创建 API Key
# Step 2: 设置环境变量
export ANTHROPIC_API_KEY="sk-xxxxxxxxxxxxxxxx"
export ANTHROPIC_BASE_URL="https://中转站地址/v1"

# Windows PowerShell：
$env:ANTHROPIC_API_KEY="sk-xxxxxxxxxxxxxxxx"
$env:ANTHROPIC_BASE_URL="https://中转站地址/v1"

# Step 3: 启动 Claude Code
claude
```

## 4.使用 DeepSeek 替代（省钱方案）

📌 DeepSeek 原生兼容 Anthropic API 格式，可以直接接入 Claude Code：

```
# 📌 DeepSeek 配置（通过 ccswitch 或手动设置环境变量）

# 供应商名称：DeepSeek
# 官网链接：https://platform.deepseek.com
# 请求地址：https://api.deepseek.com/anthropic
# API 格式：Anthropic Messages（原生）
# 认证字段：ANTHROPIC_AUTH_TOKEN

# 手动配置（PowerShell）
$env:ANTHROPIC_AUTH_TOKEN="sk-xxxxxxxxxxxxxxxx"
$env:ANTHROPIC_BASE_URL="https://api.deepseek.com/anthropic"
$env:ANTHROPIC_MODEL="deepseek-v4-pro[1m]"
```

💡 DeepSeek 的优势：
- 价格约为 Claude 官方的 **1/10**
- 原生支持 Claude Code 的 websearch 功能
- 国内直连，无需科学上网

# 四.基础使用

## 1.启动与对话

```
# 📌 进入项目目录，启动 Claude Code
cd D:\Obsidian\muyu_note
claude

# 启动后进入交互式终端，直接打字对话
# Ctrl+C 退出
```

## 2.常用斜杠命令

```
# 📌 Claude Code 内置命令

/help           → 查看帮助
/clear          → 清空当前对话上下文
/compact        → 压缩对话历史，节省 token
/memory         → 查看/编辑持久化记忆
/config         → 查看/修改配置
/model          → 切换模型
/cost           → 查看本次会话的 token 消耗
/exit           → 退出
```

## 3.常用操作示例

```
# 📌 在 Claude Code 中可以做的事

# 直接对话
> 帮我解释一下这个仓库的目录结构

# 读文件
> 读一下 01.前期准备.md，帮我检查有没有错误

# 搜索
> 搜索仓库里所有提到 "Flash Attention" 的文件

# 执行命令
> 帮我执行 git status 看看当前状态

# 写文件
> 帮我写一篇关于 xxx 的笔记，保存到 xxx 目录下
```

# 五.核心机制：CLAUDE.md

📌 CLAUDE.md 是 Claude Code 的**项目级指令文件**，放在仓库根目录下。Claude 每次启动时会自动读取它，相当于给 AI 一份"项目说明书"。

## 1.这个仓库的 CLAUDE.md 做了什么

本仓库的 CLAUDE.md 定义了以下内容：

```
# 📌 CLAUDE.md 的核心配置

## Repository overview
# → 告诉 Claude 这是一个 Obsidian 学习笔记仓库，中文为主，Git 托管

## Directory structure
# → 列出每个文件夹的用途，Claude 就知道去哪找什么文件

## File types
# → .md 是笔记、.canvas 是画布、.png 是图片

## Git conventions
# → commit 用中文、推送前审查敏感信息、PR 审批流程

## Note writing style ← 最关键的部分
# → 代码驱动式笔记、中英混写、emoji 标记、渐进式迭代
# → Claude 写笔记时会严格遵循这些规范
```

💡 没有 CLAUDE.md，Claude 只是一个通用助手。有了它，Claude 就变成了**了解你项目结构和写作风格的专属助手**。

## 2.如何写自己的 CLAUDE.md

```markdown
# 📌 CLAUDE.md 模板

## 项目描述
用一两句话说明这个仓库是什么

## 目录结构
列出主要文件夹及其用途

## 写作规范
说明你的笔记风格（代码驱动？纯文字？图文并茂？）

## Git 约定
commit 语言、分支策略、审查要求

## 注意事项
Claude 需要知道的特殊规则
```

# 六.核心机制：Memory 系统

📌 Memory 是 Claude Code 的**跨会话持久化记忆**。普通对话结束后上下文就丢了，但 Memory 可以让 Claude 在下次对话时"记住"之前的关键信息。

## 1.Memory 存在哪里

```
# 📌 Memory 文件位置
# Windows:
C:\Users\<用户名>\.claude\projects\<项目路径>\memory\

# 本仓库的 Memory：
C:\Users\muyuhuanghun\.claude\projects\D--Obsidian-muyu-note\memory\
```

## 2.这个仓库的 Memory 内容

```
# 📌 已配置的 Memory 文件

MEMORY.md                    → 索引文件，列出所有记忆条目
project_vault_context.md     → 仓库背景：Obsidian 学习笔记，PyTorch 课程为核心
feedback_writing_style.md    → 写作风格：代码驱动，中英混写
project_collaborator_role.md → 用户权限：可审批 PR
feedback_push_security.md    → 推送规则：审查敏感信息
project_push_workflow.md     → 工作流：本地审查后直接 push
project_cpp_to_verilog.md    → 研究项目：LLM 驱动的 DSP-HLS 调优
project_rtlhealer.md         → 研究方向：Verilog 语法错误自愈 Agent
```

💡 这些记忆是 Claude 通过 `/memory` 命令或对话中自动积累的，**不需要每次重新交代背景**。

## 3.如何使用 Memory

```
# 📌 在 Claude Code 中管理记忆

/memory              → 查看当前记忆列表
/memory add "xxx"    → 手动添加一条记忆
/memory edit          → 编辑已有记忆

# Claude 也会在对话中自动判断哪些信息值得记住
# 比如你说"以后写笔记都用代码驱动风格"，Claude 会自动存入 Memory
```

# 七.与 Obsidian 笔记仓库的配合方式

📌 这是本仓库的核心价值——**Claude Code + Obsidian + Git 形成完整的学习辅助闭环**。

## 1.协作架构

```
# 📌 三层协作模型

┌─────────────────────────────────────────┐
│           Claude Code (AI 层)            │
│  - 读取 CLAUDE.md 了解项目规范            │
│  - 通过 Memory 记住长期上下文             │
│  - 直接读写 .md 文件、执行 Git 命令        │
└──────────────────┬──────────────────────┘
                   │ 操作
┌──────────────────▼──────────────────────┐
│         Obsidian Vault (笔记层)           │
│  - .md 文件：Markdown 笔记               │
│  - .canvas 文件：可视化知识图谱            │
│  - wikilinks：[[双向链接]]               │
└──────────────────┬──────────────────────┘
                   │ 版本控制
┌──────────────────▼──────────────────────┐
│           Git + GitHub (存储层)           │
│  - 版本历史、分支管理                      │
│  - 多设备同步、协作                        │
│  - 推送前自动审查敏感信息                  │
└─────────────────────────────────────────┘
```

## 2.典型使用场景

### 场景一：让 Claude 帮你写笔记

```
# 📌 示例对话

> 帮我写一篇 llama.cpp 量化类型的笔记，保存到 LLAMA.CPP/03.模型量化与格式转换.md
> 要求：代码驱动风格，中文注释，带 emoji 标记

# Claude 会：
# 1. 读取 CLAUDE.md 了解写作风格
# 2. 参考同目录下已有笔记的格式
# 3. 按照规范生成完整笔记
# 4. 自动保存到指定路径
```

### 场景二：让 Claude 帮你整理知识

```
# 📌 示例对话

> 扫描 基于pytorch的深度学习/ 目录下所有笔记
> 帮我生成一个知识图谱的 canvas 文件，展示各章节之间的依赖关系

# Claude 会：
# 1. 读取所有相关 .md 文件
# 2. 分析章节间的引用关系（wikilinks）
# 3. 生成 .canvas JSON 文件
```

### 场景三：让 Claude 帮你管理 Git

```
# 📌 示例对话

> 帮我看看当前有哪些改动，整理一下准备提交
> commit 信息用中文，描述今天加了什么内容

# Claude 会：
# 1. 执行 git status / git diff
# 2. 审查是否有敏感信息泄露
# 3. 生成中文 commit message
# 4. 执行 git add + git commit
# 5. 如果你要求，还会 git push
```

### 场景四：让 Claude 辅助理解代码

```
# 📌 示例对话

> 我在学 PyTorch，帮我读一下 05.loss_function.md
> 用通俗的语言解释 CrossEntropyLoss 的工作原理，配合代码注释

# Claude 会直接读取笔记，逐段解释，还能帮你补充示例代码
```

## 3.与传统学习方式的对比

```
# 📌 学习效率对比

传统方式：
  遇到问题 → 搜索 → 筛选结果 → 阅读 → 整理笔记
  耗时：30min+ / 问题

Claude Code 方式：
  遇到问题 → 直接问 Claude → 它读你的笔记 + 搜索 + 生成答案 → 自动写入笔记
  耗时：5min / 问题

# 🌟 核心差异：Claude 有你整个仓库的上下文
# 它知道你学了什么、没学什么、笔记风格是什么
# 不是通用搜索，是针对你学习进度的个性化辅助
```

# 八.进阶技巧

## 1.在 VS Code 中使用 Claude Code

```
# 📌 VS Code 集成
# 1. 安装 VS Code 扩展：搜索 "Claude Code"
# 2. 或者直接在 VS Code 的终端中运行 claude
# 3. Claude 可以直接操作 VS Code 中打开的文件
```

## 2.多模型切换

```
# 📌 根据任务选择模型
/model              → 查看当前模型
/model sonnet       → 切换到 Sonnet（速度快，日常使用）
/model opus         → 切换到 Opus（能力强，复杂任务）
/model haiku        → 切换到 Haiku（最便宜，简单任务）

# 💡 日常写笔记用 Sonnet 就够了
# 需要深入分析代码逻辑时切 Opus
# 简单问答用 Haiku 省钱
```

## 3.与本地大模型配合

```
# 📌 Claude Code + llama.cpp 联动

# 场景：用本地模型做初筛，用 Claude Code 做精修
# 1. llama-server 部署本地模型，处理大量重复性工作
# 2. Claude Code 处理需要项目上下文的精细工作（写笔记、整理知识）

# 两者互补：
# 本地模型 → 无审查、无限量、免费、但没有项目上下文
# Claude Code → 有项目上下文、能操作文件、但需要 API 费用
```

---

💡 **总结**：Claude Code 不是一个简单的聊天工具，而是一个**能理解你整个项目的 AI 助手**。配合 Obsidian 的知识管理 + Git 的版本控制，形成了一个从学习、记录到整理的完整闭环。

[[如何在各种ide中使用ai agent进行ai coding]]
