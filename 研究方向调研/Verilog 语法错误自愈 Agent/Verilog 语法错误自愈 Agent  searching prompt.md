# Role
你是一名资深的计算机体系结构科学家，专门从事 AI4EDA（人工智能辅助电子设计自动化）中的硬件描述语言（HDL）自动生成与验证。

# Context & Goal
大语言模型直接生成的 Verilog 代码常常因为轻微的语法偏差、端口未对齐或多驱动（Multi-driven）问题导致编译失败。我们计划搭建一个基于 Python 的闭环 Agent，通过自动捕获开源仿真器（Icarus Verilog / Verilator）的 Error Log，回传给 LLM 进行自适应修复（Self-Healing），直至功能正确（Pass Testbench）。

现需要你连夜完成该课题的前期深度调研与立项可行性报告。

# Task 1: 前沿文献挖掘与学术空白（Gap Analysis）
请系统性检索并分析近3年（2023-2026年）发表在 DAC, ICCAD, TCAD 上关于 "Verilog Code Generation" 和 "RTL Auto-Debugging" 的核心工作（必须包含 NVIDIA 的 VerilogEval、RTLCoder 和 ScaleRTL 等工作的演进脉络）。
请用 Markdown 表格对比它们，表格必须包含以下硬核维度：
- 论文名称/作者/发表年份与会议
- 底层大模型选择与微调策略（如 DAPT, SFT, RLCF）
- 验证与反馈机制（是纯功能验证，还是包含时序/面积评估？）
- 核心学术局限性（Limitation，必须一针见血，作为我们项目的立论依据）

# Task 2: 编译器报错特征与大模型自愈的“长尾效应”
1. 请从学术角度论述：为什么 Verilog 的硬件并发语义（如 always 块、non-blocking assignment `<=`）导致的编译报错，比 C++/Python 等串行软件语言的 Bug 更难让普通大模型通过单次 Prompt 修复？
2. 详细列举 5 种最容易导致大模型崩溃的经典 Verilog 语法/时序隐患（如 Latch 隐性生成、Async Reset 冲突、比特位宽不匹配导致的隐含截断），并给出对应的“Error Log 文本示例”以及“指导大模型自愈的 Prompt 纠错模板”。

# Task 3: 自动化工具链与系统架构设计（Architecture Design）
请设计这个自适应修复 Agent 的系统架构。不要给出抽象的概念，必须提供具体的工程实现蓝图：
1. 给出基于 Python `subprocess` 模块异步调用 `iverilog` 和 `vvp` 进行自动化编译与 Testbench 仿真测试的伪代码流。
2. 详细定义 Agent 的核心数据交互流（Data Schema），使用标准的 JSON 格式展示：如何将【原始含Bug代码 + 编译行号 + 仿真器标准错误输出（stderr） + 历史迭代轮数】打包并优雅地投喂回大模型。

# Task 4: 学术论文引言（Introduction）前置撰写
请按照 IEEE 双栏学术会议论文的标准高度与修辞，用英文（或极其严谨的中文学术语）撰写本项目的 Introduction 前三段：
- 第一段：从全球算力需求爆棚、芯片设计人才断层出发，引出自动化 RTL 生成（RTL Generation）的极端重要性。
- 第二段：指出目前直接用大模型生成代码的死穴（幻觉、语法高错率、无法通过编译），引出“报错反馈自愈”这一流派的发展瓶颈。
- 第三段：正式推出本项目的核心贡献（Our Contributions），列举 3 点创新（例如：提出了结构感知的错误解析器、设计了针对长尾硬件 Bug 的惩罚奖励函数等）。

# Constraints（硬性限制）
- 拒绝任何编造的、不合逻辑的论文。
- 涉及代码设计和 JSON 数据流的地方，必须保证完全符合生产环境的标准，严禁使用 `... (省略此处)`。
- 输出总字数预期不少于 2000 字，请展现深度思考。