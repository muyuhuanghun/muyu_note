# uestc-mooc-helper 项目分析报告

> **⚠️ 使用警告**
>
> 本工具用于自动化完成成电慕课（mooc2.uestc.edu.cn）考试/测验的选择题。虽然工具声明"不自动提交"，但其实际效果等同于替用户完成答题。**在正式考试或有成绩评定性质的测验中使用本工具，可能构成学术不端行为。**
>
> 使用者应自行评估以下风险：
> - 违反学校学术诚信政策，可能面临纪律处分
> - 违反慕课平台服务条款，可能导致成绩作废或账号封禁
> - 本分析报告仅供技术研究和学习参考，不构成使用建议

---

> **📋 收录声明**
>
> 本报告仅作为笔记仓库中的技术参考资料，对 uestc-mooc-helper 项目进行收录和分析研究。报告内容不构成对该项目的推荐、背书或使用建议，亦不对使用者因参考本报告而产生的任何行为及其后果承担责任。
>
> 原项目仓库地址：https://github.com/Corundum-Ling/uestc-mooc-helper
>
> 本笔记仓库与原仓库作者无任何关联。如需了解项目详情或获取技术支持，请访问原仓库。

---

## 一、项目概述

**项目名称**：uestc-mooc-helper
**项目类型**：AI Agent Skill（技能文件）
**仓库来源**：GitHub - Corundum-Ling/uestc-mooc-helper
**许可证**：MIT (Copyright 2026 CorunLing)
**目标平台**：成电慕课 mooc2.uestc.edu.cn

**核心功能**：通过浏览器自动化（CDP 协议）自动完成成电慕课考试/测验的选择题，包括题目提取、答案分析、自动填写三个环节。

**关键限制**：
- 绝不自动提交，填写后由用户手动检查并提交
- 仅支持选择题（单选、判断、多选），不支持填空题
- 需要 AI Agent 平台支持浏览器自动化能力（CDP 连接）


## 二、技术架构

### 2.1 整体流程

```
启动浏览器 → 连接 CDP → 用户导航到题目页 → 提取题目文本
    → LLM 分析答案 → JS 操作 DOM 填入答案 → 验证无遗漏 → 用户手动提交
```

### 2.2 技术栈

- **浏览器控制**：Chrome DevTools Protocol (CDP)
- **DOM 操作**：原生 JavaScript（页面内执行）
- **答案分析**：LLM（由 Agent 平台提供）
- **前端框架适配**：Angular（慕课平台使用 AngularJS，通过 ng-model 管理状态）

### 2.3 文件结构

```
uestc-mooc-helper/
├── SKILL.md                    # 主技能文件（骨架，约 300 字）
├── references/
│   └── implementation.md       # 详细实现指引（DOM 结构分析、JS 代码、FAQ）
├── README.md                   # 项目说明
└── LICENSE                     # MIT 许可证
```


## 三、核心实现分析

### 3.1 浏览器启动与连接

**检测顺序**：Edge → Chrome

**启动参数**：`--remote-debugging-port=9222`

**关键步骤**：
- 检测浏览器安装路径（Edge: `C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe`，Chrome: `C:\Program Files\Google\Chrome\Application\chrome.exe`）
- 杀掉所有同名浏览器进程（否则新实例无法占用调试端口）
- 等待 2 秒确保进程完全退出
- 以可见窗口模式启动（非 headless）

**连接方式**：`http://127.0.0.1:9222`，获取页面对象后支持执行任意 JavaScript、读取 DOM、点击元素。

### 3.2 题目提取

**数据来源**：`document.body.innerText`（页面全部可见文本）

**解析规则**：

| 特征 | 含义 |
|------|------|
| 数字序号开头（`1.` `2.` ...） | 一道新题开始 |
| 字母开头（`A.` `B.` `C.` ...） | 选项 |
| `[方括号内容]` | 划线词，需选近义词 |
| "对 / 错"、"T / F" 两个选项 | 判断题 |
| 题干含"以下哪些"、"多选" | 多选题 |

**注意事项**：
- 选项数量不固定（2-5 个），根据实际出现的字母数量判断
- 选项内容可能含 LaTeX 数学公式（MathJax 渲染），提取出的文本中可能包含 `\(...\)` 或 `$$...$$` 格式
- 选项字母格式宽松匹配 `A.` 或 `A .`（点前后可能有空格）

### 3.3 DOM 结构分析

**题目容器层级**：

```
ol.subjects-jit-display          ← 所有题目列表
  li.subject.single_selection    ← 一道题（类名 = 题型）
    div.subject-body
      ol.subject-options         ← 该题的所有选项
        li.option                ← 单个选项
          label
            span.left
              input[type="radio"]    ← 单选/判断用 radio
              span.option-index      ← 选项字母（如 "A"）
            div.option-content
              span[mathjax]          ← 选项文本（可能含 LaTeX）
```

**关键特征**：

| 特征 | 说明 |
|------|------|
| 题型类名 | `subject` 元素上的 CSS 类：`single_selection` / `multiple_selection` / `true_or_false` |
| 单选 input | `input[type="radio"][ng-model="subject.answeredOption"]` |
| 多选 input | `input[type="checkbox"][ng-model="option.checked"]` |
| 选项字母 | `<span class="option-index">` 由 `ui.intToChar($index)` 生成 |
| 选项顺序 | DOM 中 `<li class="option">` 的排列顺序就是 A → B → C → D... |
| **无 `name` 属性** | radio 没有 `name` 属性，Angular 通过 `ng-model` 分组 |
| 选中标记 | 被选中的 label 有类 `answered-option` |
| 自动保存 | radio/checkbox 会触发 `ng-change="onChangeSubmission(subject)"` |

### 3.4 答案填写

**核心逻辑**：按 DOM 顺序取 `<ol class="subject-options">`，每个 `<ol>` 对应一道题，其内的 radio 按 DOM 顺序对应 A/B/C/D...

**单选题填写代码**：

```javascript
const answers = ['D','C','A',...];  // 每道题的答案字母
const optionLists = document.querySelectorAll('ol.subject-options');
let clicked = 0;

optionLists.forEach((ol, qIdx) => {
  const inputs = ol.querySelectorAll('li.option input[type="radio"]');
  if (!inputs.length) return;

  const letter = answers[qIdx];
  if (!letter) return;

  const idx = letter.charCodeAt(0) - 65;  // A→0, B→1, C→2, ...
  if (inputs[idx]) {
    inputs[idx].click();
    clicked++;
  }
});
```

**多选题处理**：检测 `<input type="checkbox">`，答案用逗号分隔（如 `"A,C"`），每个正确选项单独点击。

**click 不生效的兜底**：Angular 可能依赖 change 事件，click 后手动派发 `change` 和 `input` 事件。

### 3.5 答案验证

**验证方式**：检测页面左侧答题卡区域的 `.subject-item.unanswered` 元素数量

```javascript
const unanswered = document.querySelectorAll('.subject-item.unanswered');
// unanswered.length === 0 → 全部已填
// unanswered.length > 0  → 报告剩余数量
```

### 3.6 LLM 分析答案

**提示词模板**：

> 你是成电慕课答题助手。以下是一道来自 mooc2.uestc.edu.cn 的题目，请分析并给出正确选项的字母。注意：题干中的 `[划线词]` 表示需要选择同义词/近义词。选项内容可能包含 LaTeX 数学公式。只需回复选项字母（单选一个字母，多选用逗号分隔），不要解释。

**各题型作答策略**：

| 题型 | 判断依据 | 作答策略 |
|------|----------|----------|
| 词汇同义词 | 题干含 `[xx]` + 选项为四个词 | 排除法，选词义最接近的 |
| 填空选择 | 题干含下划线/空位 + 选项为词组 | 据语境、搭配、词义选 |
| 介词搭配 | 题干短 + 选项为介词 | 动介/形介固定搭配 |
| 概念理解 | 题干为定义/概念 + 选项为术语 | 学科知识直接判断 |
| 判断题 | 仅两个选项（T/F 或 对/错） | 据事实判断 |

**输出格式**：`["D","C","A","B","对"]`（每道题一个字母或"对"/"错"）


## 四、平台兼容性

| 平台 | 支持情况 | 说明 |
|------|----------|------|
| OMP Agent | ✅ 推荐 | 内置 browser 工具，原生支持 CDP |
| Claude Code | ✅ 支持 | 通过 Playwright MCP 实现 |
| 其他支持 CDP 的 Agent | ✅ 可适配 | 按 implementation.md 映射到对应工具 API |

**必要能力**：
- 执行 PowerShell/bash 命令启动浏览器
- 连接 CDP 获取页面对象
- 在页面中执行 JavaScript
- 读取 DOM 结构和文本
- 点击元素


## 五、使用方法

### 5.1 环境要求

**硬件与系统**：
- Windows 系统（PowerShell 可用）
- 已安装 Edge 或 Chrome 浏览器

**软件与平台**：
- 支持浏览器自动化的 AI Agent 平台（OMP Agent 或 Claude Code + Playwright MCP）
- 项目文件已放置在 Agent 的 skills 目录下

### 5.2 安装

将项目克隆或下载到 Agent 的 skills 目录：

```bash
cd path/to/your/skills
git clone https://github.com/Corundum-Ling/uestc-mooc-helper.git
```

或直接下载 ZIP 解压到 skills 目录。

### 5.3 完整使用流程

整个流程分为 7 个步骤，其中步骤 3 需要用户手动操作并确认，其余步骤由 Agent 自动执行。

**步骤 1：启动浏览器**

Agent 执行 PowerShell 命令，检测 Edge/Chrome 安装路径，杀掉已有进程后以 `--remote-debugging-port=9222` 参数重新启动浏览器。浏览器以可见窗口模式打开（非 headless），用户可以看到整个操作过程。

**步骤 2：连接 CDP**

Agent 通过 `http://127.0.0.1:9222` 连接已启动的浏览器，获取页面控制权。连接成功后可执行 JavaScript、读取 DOM、点击元素。

**步骤 3：用户导航到题目页（需手动操作）**

Agent 停止执行，提示用户在浏览器中手动进入考试/测验页面。用户打开目标题目页面后，回复 Agent 确认，流程才会继续。

**步骤 4：提取题目**

Agent 在页面中执行 `document.body.innerText` 获取全部可见文本，按数字序号识别题目边界，按字母序号识别选项，解析出每道题的题干和所有选项。

**步骤 5：分析答案**

Agent 将提取的逐题文本交给 LLM 分析，LLM 根据题型（同义词/填空/介词/概念/判断）给出正确选项字母。输出格式为答案数组，如 `["D","C","A","B","对"]`。

**步骤 6：自动填写**

Agent 在页面中执行 JavaScript，按 DOM 顺序定位每道题的选项容器 `ol.subject-options`，根据答案字母计算索引（A→0, B→1, C→2, ...），点击对应的 radio 或 checkbox。Angular 框架会自动触发 `ng-change` 事件保存答案。

**步骤 7：验证**

Agent 检测页面答题卡区域中 `.subject-item.unanswered` 的数量。若为 0 则全部已填，告知用户手动检查并提交；若大于 0 则报告剩余数量。

### 5.4 触发方式

在 Agent 对话中输入以下类型的指令即可触发：

- 「帮我完成成电慕课的考试题」
- 「成电慕课自动答题」
- 「慕课做题」

Agent 会自动识别 SKILL.md 中定义的触发词并启动流程。

### 5.5 支持的题型

| 题型 | 支持情况 | 说明 |
|------|----------|------|
| 单选题 | ✅ 完全支持 | `input[type="radio"]`，按答案字母索引点击 |
| 判断题 | ✅ 完全支持 | 视为两个选项的单选题（T/F 或 对/错） |
| 多选题 | ⚠️ 基础支持 | `input[type="checkbox"]`，答案用逗号分隔（如 `"A,C"`），需验证稳定性 |
| 填空题 | ❌ 不支持 | 需要输入文本，当前脚本仅处理选择类题型 |

### 5.6 注意事项

- **分页处理**：当前仅支持单页题目。如果题目分多页显示，需用户手动翻页后重新触发提取和填写流程
- **浏览器冲突**：启动时会杀掉所有 Edge/Chrome 进程，如有未保存的浏览内容请提前保存
- **提交方式**：填写完成后 Agent 不会自动提交，用户需自行检查答案后手动点击提交按钮
- **平台改版**：如果慕课平台前端 DOM 结构发生变化，脚本可能失效，需更新 implementation.md 中的 DOM 分析

### 5.7 常见问题

**Q: 浏览器启动失败？**
确认 Edge 或 Chrome 已安装。如果浏览器正在运行，脚本会自动关闭后重启。

**Q: CDP 连接失败？**
杀掉所有浏览器进程，重新带 `--remote-debugging-port=9222` 启动。

**Q: 题目提取不全？**
如果题目分页显示，需手动翻页后重新执行。检查页面是否完全加载后再触发提取。

**Q: 点击选项后页面没反应？**
Angular 可能依赖 `change` 事件。脚本有兜底处理（click 后手动派发 `change` 和 `input` 事件），如仍无效可能是平台版本变化。

**Q: 多选题答案不正确？**
多选题支持处于基础阶段，答案格式为逗号分隔的字母（如 `"A,C"`）。如果 DOM 结构中 checkbox 的排列与预期不符，可能需要手动调整。

**Q: 当前 Agent 平台不支持浏览器操作？**
如果平台没有 CDP 连接能力，无法使用此 skill。建议切换到支持浏览器自动化的平台（OMP Agent 或 Claude Code + Playwright MCP）。


## 六、优缺点分析

### 5.1 优点

- **模块化设计**：SKILL.md 为骨架，implementation.md 为详细指引，便于维护和适配不同平台
- **DOM 结构分析详尽**：对慕课平台的 Angular 前端框架做了深入分析，包括 ng-model 分组机制、事件派发兜底等
- **安全机制**：明确禁止自动提交，要求用户手动检查
- **代码简洁**：核心填写逻辑仅 10 余行 JavaScript，易于理解和调试
- **容错处理**：考虑了 click 不生效时的事件派发兜底、选项数量不固定等情况

### 5.2 缺点与局限

- **单页限制**：当前只能处理单页题目，分页需用户手动翻页后重新执行
- **多选题支持有限**：README 标注为"基础支持，需验证"
- **填空题不支持**：仅支持选择题
- **平台依赖**：需要 Agent 平台支持浏览器自动化，普通对话式 AI 无法使用
- **DOM 结构耦合**：如果慕课平台改版，脚本可能失效
- **题目提取依赖 innerText**：可能丢失部分格式信息或遇到特殊字符解析问题


## 七、潜在风险

### 6.1 学术诚信风险

该工具本质上是**自动化答题辅助工具**，虽然声明了"仅用于学习辅助"且"不自动提交"，但实际使用场景与学术诚信政策存在冲突。使用该工具完成考试/测验可能构成学术不端行为。

### 6.2 法律与合规风险

- 项目使用 MIT 许可证，代码本身开源合法
- 但用于自动化答题可能违反学校/平台的服务条款
- 公开仓库中包含此类工具可能引发争议

### 6.3 技术风险

- CDP 协议依赖本地浏览器，远程/受限环境无法使用
- 浏览器版本更新可能导致 CDP 协议变化
- 慕课平台可能增加反自动化检测机制


## 八、总结

uestc-mooc-helper 是一个技术实现较为完善的 AI Agent Skill 项目，对目标平台的 DOM 结构做了深入分析，核心逻辑简洁清晰。但其本质是自动化答题辅助工具，存在明确的学术诚信风险。建议仅将其作为学习浏览器自动化技术的参考，而非实际用于考试答题。

**适用场景**：
- 学习 CDP 协议和浏览器自动化技术
- 研究 Angular 前端框架的 DOM 操作方式
- 了解 AI Agent Skill 的设计模式

**不推荐场景**：
- 实际用于考试/测验答题
- 任何形式的学术不端行为
