# AI 辅助学习工具补充：DSH / Workbuddy / Codex 使用指南

> 📌 本文是 [[如何从0使用Claude Code辅助学习]] 的**2025 补充文档**。
> 原文档诞生时，很多能力（模型切换、API 配置、记忆管理、插件）需要手动折腾，如今这些功能已经被**打包整合进了各家 agent 或 harness** 里，开箱即用。
> 本文面向新手，先讲「现在用什么、怎么装、怎么用」，再补充 **prompt、skill、agent 原理** 等底层知识。

# ==========================================
# 〇. 为什么需要这篇补充：工具演化史
# ==========================================

```
# 📌 原文档 vs 现在的差距

原文档（Claude Code 时代）需要手动做的事：
  安装 Node.js → 安装 Git → 配置终端
  → npm 装 claude-code → 配 API Key
  → 装 ccswitch 切换供应商 → 写 CLAUDE.md → 配 Memory

现在（agent/harness 时代）：
  🚀 装一个工具 = 一条命令（或下载 App）
  🚀 模型切换、API 配置 = 内置（Settings 里点一点）
  🚀 项目指令 = 仓库根目录放 AGENTS.md / PROJECT.md
  🚀 记忆 = 内置 memory 目录，自动沉淀
  🚀 子任务 = sub-agent / workflow 原生支持
```

💡 **一句话理解**：原文档教的是「拼装积木」，本文教的是「直接用成品」。

工具演进时间线（大致）：

```
ChatGPT/网页问答（2016-2023）   → 纯对话，不能动你的文件
    ↓
Copilot / Cursor（2022-2023）   → 编辑器内补全/侧边栏
    ↓
Claude Code / Codex（2024）     → CLI Agent：能读写文件、跑命令、操作 Git
    ↓
Harness 时代（2024-2025）       → 集成执行环境 + 工具库 + 编排 + GUI
                                 （DSH / Desktop App / Workbuddy 等）
```

# ==========================================
# 一. DeepSeek Harness（DSH）
# ==========================================

## 1.1 DSH 是什么

📌 **DeepSeek Harness（简称 DSH）** 是集成了 **CLI + Web GUI + Desktop 客户端** 的 DeepSeek Agent 工作台。

🌟 它把原文档里散落的环节全部收拢：

```
# 📌 原文档散落的配置 → DSH 内置能力对照

Node.js 环境排查      → 免维护，随 App 打包
ANTHROPIC_API_KEY    → 内置登录（设置页登录/填 key 即可）
ccswitch 多供应商切换  → Settings 里切换，GUI 化
CLAUDE.md 项目指令     → AGENTS.md / PROJECT.md，自动读取
Memory 持久记忆        → 内置 memory 机制
sub-task 手动拆分      → subagent 原生支持
```

## 1.2 安装与启动

### 形态一：Desktop 客户端（新手最友好）

```
# 📌 下载 & 安装
# github获取桌面版安装包 → 双击安装 → 打开即用
# 登录：内置账号体系，不用手动配任何环境变量

# 启动后界面大致包含：
#   - 左侧会话列表
#   - 中间对话区（和 AI 打字聊天）
#   - 底部输入框
```

### 形态二：Web GUI（浏览器访问）

```
# 📌 在任意终端里启动 Web GUI
dsh web

# 启动成功后浏览器打开：
#   http://127.0.0.1:43120
# 浏览器/桌面端通用，同一套界面
```

### 形态三：CLI / TUI（终端内交互，老手最爱）

```
# 📌 终端里直接进入交互模式
dsh

# 或一次性执行任务（非交互）
dsh "帮我读一下 README 并总结"

# 常用子命令
dsh --version        # 版本
dsh web              # 启动 Web GUI
dsh --help           # 全部子命令
```

⚠️ **新手建议**：从 **Desktop 或 Web GUI** 入手，界面能看到 AI 每一步动作（读文件、搜代码、执行命令、写文件都会显示出来），比纯黑终端直观得多。

## 1.3 核心用法：像带实习生一样指挥它

```
# 📌 在 DSH 里能做的事（和原文档 Claude Code 行为对齐）

> 帮我解释一下这个仓库的目录结构
> 读一下 01.前期准备.md，检查有没有错误
> 搜索仓库里所有提到 "Flash Attention" 的笔记
> 帮我执行 git status 看看当前状态
> 帮我写一篇关于 RNN 的笔记，保存到 xxx 目录
```

🌟 DSH 的 Agent 是一台**带工具的全自动机器**，它会自动做：

```
看文件（read）→ 找文件（glob/grep）→ 搜索（web）
→ 改文件（write/edit）→ 跑命令（pwsh）→ 读结果 → 继续
```

这就像请了个实习生：你不必告诉它「第一步 read，第二步 grep」，它自己会编排。

## 1.4 项目指令文件：AGENTS.md / PROJECT.md

📌 这是原文档「CLAUDE.md」章节的**现代升级版**。DSH 会自动读取项目根目录的指令文件，当作「项目说明书」。

```
# 📌 各工具对指令文件的命名映射

Claude Code  →  CLAUDE.md
Codex CLI    →  AGENTS.md
DSH          →  AGENTS.md / PROJECT.md（自动识别读取）
```

💡 **通用原则**：不知道工具读哪个文件？**放 AGENTS.md 最通用**，Claude Code 也能配成读 AGENTS.md，Codex 原生读它。

一个示例 AGENTS.md（贴合本仓库）：

```markdown
# AGENTS.md

## Repository overview
这是一个 Obsidian 学习笔记仓库，中文为主 + 英文技术术语。

## Directory structure
- AI_CODING/          → AI 辅助编程工具与工作流
- 基于pytorch的深度学习/ → PyTorch 深度学习课程笔记
- LLAMA.CPP/          → 本地运行大模型

## Note writing style
1. 代码驱动：核心是代码块，概念用注释解释
2. emoji 标记：📌 关键 / 🚀 启动 / 🌟 亮点 / ⚠️ 坑 / 💡 提示
3. 中英混写，技术术语保留英文

## Git conventions
- commit 用中文
- push 前审查敏感信息
```

## 1.5 把 DSH 变成「主力写笔记工具」的姿势

本仓库实测推荐工作流：

```
# 📌 每天的学习闭环

1. 打开 dsh web（或桌面端），进入本仓库目录
2. 把当天学到的内容丢给它：
   > 我今天学了 CrossEntropyLoss，帮我整理一篇笔记，
   > 放到 基于pytorch的深度学习/ 下，按 AGENTS.md 的风格写
3. 它自动：
   read 参考已有笔记 → 参考 AGENTS.md 规范 → 生成 .md →
   让我确认 → 写入文件
4. 让它顺手 git 提交：
   > commit 用中文，描述今天新增内容并 push
```

⚠️ **新手最大误区**：把 Agent 当搜索引擎用（只问答，不落盘）。正确用法是**让它产出文件**——笔记、知识图谱、代码仓库，全部落到本地，沉淀成自己的资产。

# ==========================================
# 二. Workbuddy（workbuddy.cn）
# ==========================================

## 2.1 它是什么

📌 **Workbuddy** 是一款面向个人开发者的 **国产桌面 AI 助手**，官方地址 https://workbuddy.cn 。

🌟 核心卖点：**默认集成多个主流大模型**（DeepSeek、GLM、K3、HY 等），主打「一键多模型调试」+ 项目级 Agent，定位类似 Claude Code / Codex 的国产替代方案。

```
# 📌 一句话定位

DSH        → DeepSeek 官方全家桶（DeepSeek 模型深度绑定）
Workbuddy  → 多模型聚合桌面助手（谁强用谁）
Claude Code→ Anthropic 官方 CLI
Codex CLI  → OpenAI 官方 CLI
```

## 2.2 典型能力

```
# 📌 打开即用的功能
- 多模型切换：同一个问题，一键切换 GPT / Claude / DeepSeek / Gemini 对比回答
- 项目级 Agent：选定一个文件夹，让 AI 读写文件、执行命令
- 会话管理：多会话并行，像浏览器标签页一样管理
- 桌面集成：不依赖终端，新手零门槛
```

## 2.3 什么时候用 Workbuddy

```
💡 选择建议：
- 想对比各家模型哪个答得更好  → Workbuddy（多模型一键切换）
- 深度依赖 DeepSeek 生态       → DSH
- 想深度自动化、写脚本编排任务 → CLI 类（DSH / Claude Code / Codex）
- 零基础、不想碰终端           → 任一桌面 App 都行，Workbuddy 上手最快之一

⚠️ 注意：工具更新极快，具体支持模型/收费方式以官网为准
```

# ==========================================
# 三. Codex CLI（OpenAI 官方）
# ==========================================

## 3.1 它是什么

📌 **Codex CLI**（https://codex.ai/code）是 OpenAI 官方的终端 AI 编程 Agent，直接对标 Claude Code。2025 年用 **Rust 重写**，速度和稳定性大幅提升，支持在**本地终端**里读写文件、执行命令、操作 Git。

```
# 📌 一句话定位

Claude Code = Anthropic 家的终端 Agent
Codex CLI   = OpenAI 家的终端 Agent
DSH         = DeepSeek 家的全平台工作台
```

## 3.2 安装

```
# 📌 方式一：npm 全局安装（需要 Node.js 18+）
npm install -g @openai/codex

# 方式二：官方安装脚本（自动装最新的二进制，免 Node）
#   见官网 https://codex.ai/code 给出的一行脚本

# 验证
codex --version
```

## 3.3 认证：三种方式

```
# 📌 方式一：ChatGPT 账号登录（官方默认推荐 ⭐）
codex
# 首次运行 → 浏览器打开 ChatGPT 登录授权
# 需要 ChatGPT Plus / Pro / Business 订阅（消耗订阅额度）

# 📌 方式二：OpenAI API Key
codex login
# 或在环境变量里配置
$env:OPENAI_API_KEY="sk-..."
$env:OPENAI_MODEL="gpt-5-codex"     # 按官方命名

# 📌 方式三：自定义兼容 API（第三方中转 / 本地模型）
$env:OPENAI_BASE_URL="https://你的中转站地址/v1"
$env:OPENAI_API_KEY="sk-..."
```

⚠️ 国内网络环境：官方 API / ChatGPT 登录可能需要代理；**中转 + 自定义 Base URL** 是常见省钱方案（和原文档里配 DeepSeek 中转的思路一样）。

## 3.4 核心玩法详解

### 1. 交互模式（和 Claude Code 一样）

```
codex
# 进入交互式终端 → 打字对话
# 它自动规划：读文件 → 改文件 → 跑测试 → 修 bug → 让你确认

# 常用内置命令
/help         查看帮助
/clear        清空上下文
/model        切换模型
/quit         退出
```

### 2. Exec 模式（非交互，一行式执行 ⭐）

```
# 📌 codex exec：适合脚本化、批量、CI
codex exec "帮我把 src 下所有 .py 文件加上 UTF-8 编码头"
codex exec --json "给我一份测试报告"      # 输出 JSON 结构化结果
codex exec --sandbox read-only "列出依赖" # 只读沙箱，禁止改文件
```

💡 **exec 模式 = 把 Agent 变成命令行工具**：可以在 PowerShell 脚本、CI 流水线里调用。DSH 里对应的是一次性 `dsh "任务"`。

### 3. Sandbox 沙箱（安全机制）⭐

```
# 📌 默认阻止 Agent 乱动系统，三种级别
--sandbox read-only     # 只读，改不了任何文件（默认）
--sandbox workspace-write # 可写工作区文件，系统文件不行
--sandbox danger-full-access # 完全放权（慎用！）

# 交互模式下按提示符（y/n）逐条批准危险操作
```

🌟 这和 DSH 的文件沙箱机制是同一套思路：**危险动作要用户批准**。

### 4. 云端任务（cloud tasks）⭐

```
# 📌 Codex 的云端 Agent 模式
# 在本地把任务交给云端跑，不占本地资源，可长时间执行
# 适合：海量重构、大规模测试、夜间批量任务
```

### 5. AGENTS.md 项目指令

```
# 📌 Codex 原生读 AGENTS.md（和 DSH 一致）
# 在仓库根目录放 AGENTS.md，Codex 自动作为项目说明书
```

## 3.5 Codex vs Claude Code vs DSH 速查表

```
# ==========================================
# 对比项       Codex CLI          Claude Code       DSH
# ==========================================
# 厂商         OpenAI             Anthropic         DeepSeek
# 形态         CLI + 云任务       CLI + IDE 插件    CLI + 桌面 + Web GUI
# 默认模型     GPT 系列           Claude 系列       DeepSeek 系列
# 登录         ChatGPT 订阅/Key   官网/Key          内置登录
# 指令文件     AGENTS.md          CLAUDE.md         AGENTS.md / PROJECT.md
# 沙箱         内置              ask-approval      内置
# 多模型       Key 可换          /model 切换       Settings 切换
# 适合         OpenAI 生态、CI    通用 Agent 标杆    国产直连、桌面体验
# ==========================================

💡 三个不冲突：备份笔记给 DSH/Claude Code，批量脚本给 Codex exec，
   对比回答给 Workbuddy——按场景取用。
```

# ==========================================
# 四. 扩展知识 1：Prompt 工程基础
# ==========================================

不管换哪个工具，**底层拼的都是 prompt**。学到的东西放之四海皆准。

## 4.1 一个好 prompt 的四件套

```
# 📌 万能 prompt 骨架（对应英文缩写 CORE 等类似套路）

【角色】  你是一个资深的 PyTorch 老师
【任务】  给我讲解 CrossEntropyLoss 的数学原理
【背景】  我只会 Python 基础，正在学深度学习入门
【输出】  用代码+注释风格，先给公式再给代码示例，最后总结3条易错点
```

```
对比：
❌ 差的 prompt：  "解释一下 CrossEntropyLoss"
✅ 好的 prompt：  "你是深度学习老师，我用 Python 基础学 PyTorch。
                 请用『先公式→再代码→最后易错点』的结构，
                 通俗解释 CrossEntropyLoss，中文为主，英文术语保留"
```

💡 **黄金公式**：`角色 + 任务 + 背景 + 输出格式`。80% 的"AI 答得不好"都是因为缺了后两项。

## 4.2 让 AI 一步步思考（CoT）

```
# 📌 Chain of Thought：要求 AI 分步推理，别直接给结论

❌ "这个代码为什么报错？"          → 容易胡猜
✅ "先分析错误堆栈每一条的含义，
    再列出可能的3个原因和排查顺序，
    最后给出修复方案"              → 想得深、可验证
```

💡 对写笔记尤其好用：**让 AI 先列大纲→再逐节填充→最后检查**，结果质量远超一次生成。

## 4.3 Few-shot：给例子比给描述管用

```
# 📌 给 AI 1-2 个范文，它就能模仿你的风格

> 参考这篇笔记的格式（贴一篇你过去的笔记），
> 按同样的结构写 RNN 的笔记
```

## 4.4 结构化输出

```
# 📌 明确指定输出格式，便于复用
> 用 Markdown 表格返回这5个模型的参数量、上下文长度、价格
> 用 JSON 返回：{"name": "...", "params": "..."}

# Agent 工具里这叫 "schema"：规定 AI 返回的数据结构，
# 下游程序拿到就能直接解析 👉 这是 workflow 编排的基础
```

## 4.5 迭代：一次问不好，就追问修正

```
# 📌 别指望一次到位，把 AI 当同事反复打磨

第一轮 → 生成初稿
第二轮 → "第二小节太啰嗦，压缩到5行"
第三轮 → "把 1.3 和 2.1 合并，加一个实战例子"
```

# ==========================================
# 五. 扩展知识 2：Agent / Harness 原理
# ==========================================

## 5.1 Agent 到底是什么

```
# 📌 三层结构（理解后就懂所有工具了）

┌──────────────────────────────────────┐
│ 你（提需求）                          │
└──────────────┬───────────────────────┘
               ▼
┌──────────────────────────────────────┐
│ Agent 循环（Agent Loop）              │
│  思考(think) → 调用工具(act) → 读结果 │
│        ↑_______________________│     │
│        ↕ 反复执行直到完成目标          │
└──────────────┬───────────────────────┘
               ▼
┌──────────────────────────────────────┐
│ 工具层（Tools）                       │
│ read / write / edit / grep / glob    │
│ pwsh(跑命令) / web_search / ...      │
└──────────────────────────────────────┘
```

🌟 **Claude Code / Codex / DSH 的本质相同**：都是一个「大模型 + 一堆工具 + 一个循环」。区别只在工具集、默认模型、界面包装。

## 5.2 Harness（工具带）指什么

📌 **Harness = 让 Agent 能稳定干活的整套工程**，包括：

```
- 工具集：文件读写、命令执行、搜索、网页抓取
- 沙箱/权限：危险操作要你批准
- 上下文管理：长对话自动压缩、memory 持久化
- 任务编排：subagent 子任务、workflow 流水线
- 界面：CLI / Web / Desktop

💡 为什么说「打包整合」：这些能力原文档要自己配（ccswitch、
    Claude Code 插件、自写脚本），现在 harness 全内置了。
```

## 5.3 上下文窗口与 Token（钱的本质）

```
# 📌 关键概念

Token    = 模型计费/处理的文本单位，1 个汉字≈1-2 token
上下文窗口 = 模型一次能"记住"的最大 token 量（如 1M = 100万）
上下文超了 → 自动压缩(compact)或丢细节

# 省钱/提速心法：
- 无关内容不要贴给 AI
- 长会话及时 /clear 或开新会话
- 用 AGENTS.md 代替重复交代背景
```

## 5.4 子任务：Subagent

```
# 📌 为什么需要 subagent？

主 Agent 上下文是有限的。任务一大：
  "同时调研 A、B、C 三个主题然后汇总"

做法：主 Agent 拆成 3 个子任务，分别交给 3 个子 agent 并行跑
      → 每个子 agent 有独立上下文 → 各自返回结果 → 主 agent 汇总

现象：你会看到界面里同时出现几个 worker 在干活（并行）👈 DSH 里
      "background subagent" 就是这个
```

## 5.5 记忆：从 CLAUDE.md 到 Memory 到 Skill

```
# 📌 记忆分三层（都是新工具内置的）

① 项目指令（长期）：AGENTS.md / CLAUDE.md / PROJECT.md
   → 每次会话自动读，写"这个仓库是什么、什么规矩"
② 持久记忆（中期）：memory 目录，自动沉淀"用户偏好"
   → 比如你说过一次"commit 用中文"，以后都记住
③ Skill（能力包）  ：见下一章
```

# ==========================================
# 六. 扩展知识 3：Skill / 工作流编排
# ==========================================

## 6.1 Skill 是什么

📌 **Skill = 把「一个复杂任务的完整套路」打包成可复用指令**。相当于给 AI 一本"操作手册"：遇到任务时 AI 先读手册，再按手册逐步执行。

```
# 📌 类比
- Prompt   = 口头的临时交代
- Skill    = 标准化的 S.O.P. 文档（随取随用）
- Workflow = 自动化的流水线（多个步骤+多agent）

# 本仓库/工具里就有现成 skill（harness 的技能目录中）：
- pdf-to-markdown      → 把 PDF 转成规范笔记的完整流程
- pptx-to-markdown     → PPT 转笔记流程
- source-command-edit-canvas → 编辑 canvas 画布的规范
- humanizer            → 让 AI 生成文字更像真人写的

💡 这些 skill 由工具提供、随取随用；下一篇：
   你也可以给自己的重复流程（如「每周笔记转 canvas」）写自己的 skill
```

## 6.2 Skill 长什么样

```
# 📌 一个 Skill = 一个目录 + 说明文件

skills/
└── pdf-to-markdown/
    ├── SKILL.md          ← 核心：告诉 AI 怎么做（步骤、要求、门槛）
    └── (参考文件/模板)    ← 可选：范文、脚本、校验清单
```

```
SKILL.md 内部结构（示例心智模型）：
- 什么时候用这个 skill
- 前置准备
- Step 1 / 2 / 3 ... （含每步的验收标准）
- 完成门槛（什么情况算完成，什么情况算失败）
- 常见坑
```

## 6.3 什么时候该写一个 Skill

```
💡 判断标准：同一件事你让 AI 做了 ≥3 次 → 写成 skill
   - "把 PDF 转成我的笔记风格" → 一次
   - "每周把新课转成笔记"       → 值得固化成 skill

好处：
- 每次结果质量稳定（按手册走，不靠运气）
- 换工具/换模型也能用（手册是通用的）
- 团队可共享（AGENTS.md 里引用 skill 名即可）
```

## 6.4 工作流编排（Workflow / 多 Agent 协作）

```
# 📌 从单个 agent 到流水线

单个 prompt  → 一个 agent 做完
subagent     → 主 agent 拆任务，多个子 agent 并行
workflow     → 固定流水线：阶段1 完成任务批量分发 → 阶段2 汇总校验
               例：审计 100 个文件 → 每个文件派一个子 agent 分析
                   → 收集结果 → 汇总报告

💡 新手先用好"单个 agent + 迭代修正"，
   subagent / workflow 等任务量大了再学，不用一上来就上。
```

# ==========================================
# 七. 扩展知识 4：实战套路 + 反模式
# ==========================================

## 7.1 实战套路：把 AI 当前端协作而不是搜索引擎

```
# 📌 三个高频好用场景（开箱即用）

① 学习新知识：
   把笔记仓库当上下文 → "结合我已学的 XX，用我的风格讲 YY"
   → 产出一篇新笔记并落盘

② 调试报错：
   贴报错+相关文件 → "先分析原因再给修复，不要直接改"
   → 让它 read 相关文件自己查，比贴截图更有效

③ 批量整理：
   "扫描/生成/汇总" 类任务 → 用 exec/一次性的方式
   （Codex exec 或 DSH 一次性任务）
```

## 7.2 反模式：新手最容易踩的坑

```
# ==========================================
# ❌ 反模式              ✅ 正确姿势
# ==========================================
# 1. 指令含糊             角色+任务+背景+格式四件套
# 2. 不问背景直接贴长文    先问"你了解这个项目吗" 或 给足路径
# 3. 让 AI 直接改文件后不审查  ⚠️ 涉及写操作一律 review diff
# 4. 敏感信息入 prompt     ⚠️ 永远不要把 API key/密码贴给 AI
#     （中转也不行！有些中转会记录对话）
# 5. 上下文爆了就硬聊      /clear 开新会话，把必要背景写进 AGENTS.md
# 6. 期待一次生成完美      ⚠️ 迭代是常态，分轮打磨
# 7. 让 AI 跑破坏性命令直接批准  ⚠️ rm -rf / 清库类操作先确认
# ==========================================
```

## 7.3 安全：沙箱与批准机制

```
# 📌 所有现代 agent 都有"危险操作要批准"机制

DSH/Claude Code/Codex 的行为：
  read 文件 → 直接做（安全）
  改文件/执行命令 → 需要你 approve（或沙箱范围控制）
  危险命令（删除、清空、网络请求） → 明确请示

⚠️ 原则：先看懂它要干嘛，再点批准。
   读操作随意放行，写操作看 diff，危险操作想清楚。

💡 沙箱级别（Codex 示例，各家类似）：
   read-only → workspace-write → danger-full-access
   平时用最窄的，需要时再临时升级
```

# ==========================================
# 八. Claude Code 现状：原文档哪里过时了
# ==========================================

📌 原文档不是错了，是**演进后有了更省事的方式**。对照更新：

```
# 📌 原文档内容 → 现在的状态

Node.js + Git 手动装       → 仍要装，但 npm 更成熟；桌面工具则免装
ccswitch 切供应商          → 各家工具进化：DSH Settings 内置切换，
                             桌面聚合工具（Workbuddy）内置多模型
CLAUDE.md                  → 升级为通用 AGENTS.md/PROJECT.md（多工具共识）
Memory 手动 /memory 管理    → 内置自动记忆 + memory 目录
本地 llama.cpp 配合        → 仍然是省钱路线，但现在更多用"中转+便宜模型"
                              或桌面工具内置的本地模型支持
/compact /model 等斜杠命令  → 各家都有等价物（/model、Settings）
```

```
# 📌 Claude Code 本身的新能力（2025）：
- Verified Commands：常用操作内置成命令
- Hooks：git 操作前后自动触发脚本
- Subagents：自带子任务
- IDE 集成（VS Code / JetBrains 插件）
👉 别把 Claude Code 当旧文档里"要手动配"的笨工具，它也在同步进化
```

# ==========================================
# 九. 总结与选型建议
# ==========================================

```
# 📌 一份文档，四个结论

① 原文档的配置步骤大多已被 harness 内置 → 装 App/一条命令即可
② 三个新工具：
   DSH        = DeepSeek 全家桶（CLI+桌面+Web），主力写笔记选它
   Workbuddy  = 多模型聚合桌面助手，想对比模型/零门槛选它
   Codex CLI  = OpenAI 终极端 Agent，批量脚本/CI 选它
③ 底层知识永远是核心：
   prompt 四件套 + CoT + Few-shot  → 任何工具都受益
   agent 原理（循环/工具/上下文）    → 理解界面上的每个动作
   skill/workflow                   → 把重复劳动固化成资产
④ 安全底线：敏感信息不进 prompt，危险操作先批准
```

```
# 🚀 新手 30 分钟上路路线图

0-10 分钟   装一个桌面工具（DSH 桌面端 或 Workbuddy）
10-20 分钟  在仓库根目录写一份 AGENTS.md（抄本文 1.4 节模板）
20-30 分钟  让它写第一篇笔记（给角色+任务+背景+格式）→ 落盘
之后       每次用完觉得"这流程可复用" → 沉淀成 skill
```

> 回到原文档：[[如何从0使用Claude Code辅助学习]] 讲的是 Claude Code 单点；
> 本文补充的是它的上位概念——harness、多工具、以及通用的 prompt/skill 方法论。
> 两篇配合读，就能从"会用 Claude Code"升级为"会用好 agent 生态"。

---

## 📚 相关阅读

- [[如何从0使用Claude Code辅助学习]] — 原文档：Claude Code 单点安装与深度集成
- [[如何在各种ide中使用ai agent进行ai coding]] — 各 IDE 里的 AI Agent 用法
- [[Obsidian Claude Code 插件使用指南]] — Obsidian 与 AI Coding 的插件联动
- [[NIM4CC的使用及复刻]] — NIM4CC（NotebookLM 的笔记版 Agent）使用与复刻