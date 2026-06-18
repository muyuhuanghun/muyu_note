# Role
你是一名精通编译原理、程序分析（Program Analysis）以及图深度学习（Graph Deep Learning）的交叉学科科学家。

# Context & Goal
在 LLM 驱动的 HLS 优化闭环中，最大的算力瓶颈在于商业 EDA 工具（如 Vitis HLS）进行电路综合太慢了，通常需要数分钟至数小时。我们计划开发一个超轻量、超快速的替代方案：利用开源编译器前端（如 Clang/LLVM 或 MLIR）将 C++ DSP 算法源码转化为控制数据流图（CDFG）或抽象语法树（AST），将 HLS Pragma 作为图节点的属性特征（Node Features），然后训练一个图神经网络（GNN，如 GCN/GAT/GGNN），在 0.01 秒内直接预测出该配置下的 Latency 和资源消耗（LUT/FF/DSP 分布），以此作为 LLM Agent 演进过程中的高性能虚拟判别器（Oracle）。

# Task 1: 从源代码到图结构：特征建模深度解密
1. 详细阐述如何将一段包含 `for` 循环和数组访问的 C++ 核心代码（如 FIR 滤波器）转换为适合 GNN 输入的图结构（Graph Topology）。定义什么是顶点（Nodes，如 Operation, Memory Access），什么是边（Edges，如 Data Dependency, Control Flow）。
2. 当 LLM 在代码的某个 Loop 插入了 `#pragma HLS UNROLL factor=4` 时，这个硬件意图在图神经网络中应该如何进行特征编码（Feature Encoding）？请设计一个特征向量（Feature Vector）的结构，向我展示 Pragma 参数是如何与节点/边特征进行拼接（Concatenation）或融合的。

# Task 2: 文献脉络与技术空白（Related Work & Gap）
深入挖掘学术界利用机器学习预测 HLS 性能的工作（重点解构近年的主流方案，如基于 GNN 监督微调的 LIFT 工作，以及更早期的 XPPE 等方案）。
请明确指出：
- 现有基于 GNN 的预测模型在面对“高度耦合的多种 Pragma 同时作用（例如 Pipeline 和 Array Partition 联合作用导致的时序悬崖效应）”时为什么预测准确率会暴跌？
- 我们引入大模型先验（LLM Semantics）作为 GNN 的 Initial Embedding，能带来什么本质上的增量（Novelty）？

# Task 3: 基于 PyTorch Geometric (PyG) 的全套预测模型架构设计
不要给出模糊的伪代码，请用严谨的 PyTorch / PyTorch Geometric (PyG) 风格编写出该 GNN 预测器的核心模型类实现：
1. 定义输入图数据的 `Data` 结构（包含节点特征变矩阵 `x`，边稀疏矩阵 `edge_index`，以及代表 Pragma 配置的全局特征 `global_attr`）。
2. 构建包含图卷积层（如 `GATConv` 或 `SAGEConv`）、全局池化层（Global Pooling）以及多任务输出全连接层（Multi-task Head，同时输出 Latency 连续值预测和资源占用的多维向量）的完整网络拓扑。

# Task 4: 实验指标与损失函数（Loss Function）设计
1. 硬件资源预测具有极强的非线性。如果大模型给出的参数导致了时序崩溃（Timing Fail），这在回归损失函数中应该如何体现？请设计一个融合了时序惩罚项（Timing Penalty Custom Loss）的自定义损失函数数学公式。
2. 规划如何收集训练 GNN 所需的数据集：如何用脚本随机/启发式抽样生成上万组“C++ Pragma $\rightarrow$ Vivado HLS 真实数字”的对齐样本？

# Constraints（硬性限制）
- 必须包含完整的、符合 PyG 规范的 Python 代码类定义，注释详尽，严禁大段省略。
- 技术报告需要体现深厚的图神经网络和体系结构功底。