# Role
你是一名精通软硬件协同设计（Hardware-Software Co-Design）与高效率神经网络加速器（Neural Network Accelerators）设计的杰出研究员。

# Context & Goal
传统的 FPGA 加速（如基于 HLS 的 CNN/Transformer 算子加速）往往将算法和硬件隔裂优化：要么固定算法去调 pragma，要么固定硬件去剪枝。我们计划提出一个双 Agent 协同框架：算法 Agent 负责在软件层进行模型剪枝与量化（位宽调整），硬件 Agent 负责同步调整 HLS 的流水线、阵列并行度（Array Partition），两边同时演进，共同寻找 PPA（性能、功耗、面积）与模型精度（Accuracy）的最优帕累托前沿。

现需要你完成该课题的立项报告与可行性论证。

# Task 1: 软硬件解耦优化的“局部最优解陷阱”论证
1. 请用严谨的数学形式化（Formalization）语言，将软硬件协同设计空间探索定义为一个多目标优化问题。使用 LaTeX 公式推导其目标函数 $F(W, H)$，其中 $W$ 为软件权重/架构参数空间，$H$ 为硬件高级综合配置空间。
2. 举例论述：为什么固定神经网络结构（如固定为一个普通 $3\times3$ 卷积）去单方面寻找 HLS 的最优 `unroll` 和 `pipeline` 参数，会导致设计陷入局部最优？如果允许软件层将卷积改为深度可分离卷积（Depthwise Separable），硬件空间会发生怎样颠覆性的改变？

# Task 2: 前沿多模态/多Agent协同文献调研（Survey）
调研近几年（2024-2026年）在 ASPLOS, MICRO, ISCA 甚至 NeurIPS 上关于“Machine Learning for Hardware-Software Co-Design”或“Multi-Agent in EDA”的前沿文章（如 MPM-LLM4DSE 或同类软硬件双向搜索工作）。
重点梳理：
- 他们是如何解决“软件空间（指数级） $\times$ 硬件空间（指数级）”带来的超大规模搜索空间爆炸（Search Space Explosion）问题的？
- 他们采用了什么代理模型（Surrogate Model）来加速评估？

# Task 3: 双 Agent 对唱协议与状态机设计
请设计“软件裁剪 Agent”与“硬件综合 Agent”之间的通信机制：
1. 用 Markdown 绘制一个清晰的状态转换图或时序流向，展示两个 Agent 如何交替迭代（例如：软件 Agent 降低位宽 $\rightarrow$ 触发硬件 Agent 释放 BRAM 资源并加大并行 $\rightarrow$ 反馈时延变化 $\rightarrow$ 触发软件 Agent 进一步微调）。
2. 提供一个高可用的 JSON 协议规范，定义两个 Agent 在握手交互时传递的核心元数据（Metadata，需包含：比特位宽、模型准确率估值、预计 LUT 占用、时钟周期估算）。

# Task 4: 实验评估设计方案（Evaluation Setup）
1. 为这个宏大的课题规划你的基准测试集（Benchmarks）。除了传统的图像算子，如何引入轻量化大模型（Mini-LLM）的 Attention 算子作为核心测试？
2. 详细描述你在论文中准备用来击败对手的 Baseline（对照组）应该怎么设计，如何向审稿人证明你们的双 Agent 框架找出的 Pareto 前沿面比单向 HLS 优化（如 AutoDSE）更贴近极限？

# Constraints（硬性限制）
- 严禁空泛的概念堆砌，所有技术路径必须落地到具体的算子位宽、HLS 指令和编译行为。
- LaTeX 公式必须书写规范，逻辑链条必须闭环。