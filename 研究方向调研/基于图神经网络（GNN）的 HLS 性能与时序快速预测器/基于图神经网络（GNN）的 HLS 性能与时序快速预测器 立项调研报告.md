# 基于图神经网络（GNN）的 HLS 性能与时序快速预测器 立项调研报告

> **项目定位**：继 cpp-to-verilog 和 RTLHealer 之后的第三个研究方向
> **核心思路**：将 C++ DSP 源码 + HLS Pragma 编码为图结构，训练 GNN 在毫秒级预测 Latency / 资源占用，替代耗时的 Vitis HLS 综合
> **日期**：2026-06-15

---

## 目录

1. [方向选择理由与定位](#一方向选择理由与定位)
2. [Task 1：从源代码到图结构——特征建模深度解密](#二task-1从源代码到图结构特征建模深度解密)
3. [Task 2：文献脉络与技术空白](#三task-2文献脉络与技术空白related-work--gap)
4. [Task 3：基于 PyG 的全套预测模型架构设计](#四task-3基于-pyg-的全套预测模型架构设计)
5. [Task 4：实验指标与损失函数设计](#五task-4实验指标与损失函数设计)
6. [研究可行性分析](#六研究可行性分析)
7. [研究难度与周期评估](#七研究难度与周期评估)
8. [预期贡献与创新点](#八预期贡献与创新点)
9. [投稿目标与学术影响力评估](#九投稿目标与学术影响力评估)
10. [风险分析与应对策略](#十风险分析与应对策略)
11. [参考文献](#十一参考文献)

---

## 一、方向选择理由与定位

### 1.1 方向定位

本方向并非独立研究，而是 **cpp-to-verilog 项目的核心加速组件**。在 LLM 驱动的 HLS pragma 优化闭环中，每轮迭代都需要调用 Vitis HLS 进行综合，单次综合耗时 1-30 分钟。当探索空间达到 $10^9$ 量级时，即使采用低预算策略（20 次综合/算子），综合等待时间仍是主要瓶颈。

**GNN HLS 预测器的目标**：在 **0.01 秒内** 预测出给定 C++ 源码 + Pragma 配置下的 Latency 和资源占用（LUT/FF/DSP/BRAM），替代 Vitis HLS 作为 LLM Agent 的 **虚拟判别器（Virtual Oracle）**。

### 1.2 与 cpp-to-verilog 的协同关系

```
┌──────────────────────────────────────────────────────────────┐
│              LLM Agent 闭环优化 (cpp-to-verilog)              │
│                                                              │
│  LLM 生成 Pragma → 【GNN 预测器快速筛选】 → Top-K 配置送 HLS 验证 │
│                       ↑                                      │
│                   0.01s/次                                    │
│                   替代 1-30min/次 的 HLS 综合                  │
└──────────────────────────────────────────────────────────────┘
```

| 维度 | 不用 GNN 预测器 | 用 GNN 预测器 |
|------|----------------|--------------|
| 每轮评估耗时 | 1-30 min（Vitis HLS） | 0.01 s（GNN 推理） |
| 20 轮探索总耗时 | 20-600 min | 0.2 s + 5 min（仅验证 Top-K） |
| 可探索配置数 | 受限于综合预算 | GNN 预筛选可探索 1000+ 配置 |
| Pareto 前沿质量 | 受预算限制，可能遗漏最优解 | 大幅扩展有效搜索范围 |

### 1.3 独立研究价值

除作为 cpp-to-verilog 的加速器外，GNN HLS 预测器本身也具有独立学术价值：

- **通用 HLS 性能预测工具**：可独立用于任何 HLS 设计流程的早期设计空间探索
- **EDA 领域的 ML 应用**：属于 "ML for EDA" 的核心研究方向
- **可迁移性**：训练好的模型可迁移到不同 FPGA 器件族

---

## 二、Task 1：从源代码到图结构——特征建模深度解密

### 2.1 源代码到图的转换流程

将 C++ DSP 源码转换为适合 GNN 输入的图结构，需要经过三个阶段：

```
C++ 源码 → [Clang/MLIR 前端] → AST/IR → [CDFG 提取器] → 图结构 → [特征编码] → GNN 输入
```

#### 2.1.1 以 FIR 滤波器为例

**原始 C++ 代码**：

```cpp
void fir_filter(int input[N], int coeff[M], int output[N]) {
    #pragma HLS PIPELINE II=1
    for (int i = 0; i < N; i++) {
        int acc = 0;
        for (int j = 0; j < M; j++) {
            #pragma HLS UNROLL
            acc += input[i + j] * coeff[j];
        }
        output[i] = acc;
    }
}
```

**转换后的 CDFG 图结构**：

```
节点类型（Nodes）：
┌─────────────────────────────────────────────────────────┐
│ Node ID │ Type            │ Operation    │ Attributes     │
├─────────┼─────────────────┼──────────────┼────────────────┤
│ n0      │ LoopHeader      │ for(i=0;i<N) │ trip_count=N   │
│ n1      │ LoopHeader      │ for(j=0;j<M) │ trip_count=M   │
│ n2      │ ArithmeticOp    │ MULTIPLY     │ bit_width=32   │
│ n3      │ ArithmeticOp    │ ADD          │ bit_width=32   │
│ n4      │ MemoryAccess    │ LOAD(input)  │ array_dim=1    │
│ n5      │ MemoryAccess    │ LOAD(coeff)  │ array_dim=1    │
│ n6      │ MemoryAccess    │ STORE(output)│ array_dim=1    │
│ n7      │ Constant        │ 0            │ value=0        │
└─────────────────────────────────────────────────────────┘

边类型（Edges）：
┌───────────────────────────────────────────────┐
│ From → To │ Edge Type          │ Attributes   │
├───────────┼────────────────────┼──────────────┤
│ n0 → n1   │ ControlDependency  │ depth=2      │
│ n4 → n2   │ DataDependency     │ port=operandA│
│ n5 → n2   │ DataDependency     │ port=operandB│
│ n2 → n3   │ DataDependency     │ port=operandA│
│ n3 → n3   │ LoopCarriedDep     │ distance=1   │
│ n3 → n6   │ DataDependency     │ port=data_in │
│ n1 → n0   │ LoopBackedge       │              │
└───────────────────────────────────────────────┘
```

#### 2.1.2 图的数学表示

最终输入 GNN 的图为 $G = (V, E, X, A)$：

- $V = \{v_1, v_2, \ldots, v_N\}$：节点集合，$N$ 为节点数
- $E \subseteq V \times V$：有向边集合
- $X \in \mathbb{R}^{N \times d_{node}}$：节点特征矩阵，$d_{node}$ 为节点特征维度
- $A \in \{0,1\}^{N \times N}$：邻接矩阵（可通过 `edge_index` 稀疏表示）

### 2.2 Pragma 特征编码方案

当 LLM 在某个 Loop 插入 `#pragma HLS UNROLL factor=4` 时，需要将这个硬件意图编码进图的特征向量中。

#### 2.2.1 Pragma 的三种融合策略

| 策略 | 方法 | 优劣 |
|------|------|------|
| **节点属性拼接** | 将 Pragma 参数直接拼接到对应 Loop 节点的特征向量 | 简单直接，但丢失 Pragma 间交互信息 |
| **Pragma 虚拟节点** | 为每个 Pragma 创建虚拟节点，连接到目标 Loop 节点 | 保留 Pragma 间关系，但增大图规模 |
| **全局特征融合** | 所有 Pragma 编码为全局向量，通过 Graph-Level 拼接注入 | 信息最紧凑，但可能丢失位置信息 |

**推荐方案：混合编码（节点属性 + 全局特征）**

#### 2.2.2 特征向量设计

**节点特征向量** $x_i \in \mathbb{R}^{d_{node}}$，$d_{node} = 32$：

```python
node_features = {
    # 基础特征 (16 维)
    'node_type':        one_hot(8),   # 8 种节点类型 → 8 维
    'opcode':           one_hot(6),   # 6 种操作码 → 6 维
    'bit_width':        [int],         # 1 维，归一化到 [0,1]
    'is_loop_header':   [bool],        # 1 维

    # Pragma 属性特征 (16 维)
    'unroll_factor':    [int],         # 1 维，0=未unroll, 1=完全unroll, 2-64=因子
    'pipeline_ii':      [int],         # 1 维，0=未pipeline, 1-64=II值
    'array_partition_dim':  one_hot(3),# 3 维，dim=0/1/2
    'array_partition_factor': [int],   # 1 维
    'array_partition_type': one_hot(3),# 3 维，cyclic/block/complete
    'inline_depth':     [int],         # 1 维
    'resource_limit':   [float],       # 1 维，资源约束比例
    'loop_trip_count':  [float],       # 1 维，归一化
    'pragma_interact':  [float],       # 4 维，pragma 间交互特征
}
```

**全局特征向量** $g \in \mathbb{R}^{d_{global}}$，$d_{global} = 16$：

```python
global_features = {
    'total_loops':          [int],     # 1 维
    'total_memory_ops':     [int],     # 1 维
    'max_nesting_depth':    [int],     # 1 维
    'has_pipeline':         [bool],    # 1 维
    'total_unroll_width':   [int],     # 1 维，所有 unroll 因子乘积
    'dataflow_enabled':     [bool],    # 1 维
    'target_device':        one_hot(4),# 4 维，器件族编码
    'clock_period_ns':      [float],   # 1 维
    'pragma_density':       [float],   # 1 维，pragma 数/循环数
    'estimated_parallelism':[float],   # 4 维，估算并行度
}
```

#### 2.2.3 UNROLL factor=4 的编码示例

```python
# 原始 Loop 节点特征（无 Pragma）
node_before = [1,0,0,0,0,0, 0,0,0,0,0,0, 32, 1,  0,0, 0,0,0, 0, 0,0, 0, 0,0,0,0, 0, 0, 128]

# 插入 UNROLL factor=4 后
node_after  = [1,0,0,0,0,0, 0,0,0,0,0,0, 32, 1,  4,0, 0,0,0, 0, 0,0, 0, 0,0,0,0, 0, 0, 32]
#                                               ↑↑↑↑
#                                 unroll_factor=4, trip_count 变为 32 (=128/4)
```

**关键设计决策**：unroll 后，原循环的 trip_count 要除以 unroll_factor，因为硬件上等效于 4 个并行处理单元各处理 32 次迭代。

---

## 三、Task 2：文献脉络与技术空白（Related Work & Gap）

### 3.1 研究领域演进脉络

```
2018-2019: 统计模型时代
├── XPPE (FPGA 2018) — 线性回归 + 手工特征，预测精度有限
└── 简单 MLP 预测器 — 仅适用于小规模设计

2020-2022: 传统 ML + HLS 时代
├── AutoDSE (FCCM 2021) — 贝叶斯优化 DSE，无代码理解能力
├── ProgSG (DAC 2022) — 程序结构图 + 浅层 GNN
└── DSpot (TCAD 2022) — 局部搜索 + 代理模型

2023-2024: GNN for HLS 爆发期
├── LIFT (DAC 2024) — 首个端到端 GNN HLS 预测器，监督微调
├── GNN4HLS (TCAD 2024) — 图注意力网络 + 多任务预测
├── HLSyn (ICCAD 2024) — 语法感知图 + 联合预测
└── DiffHLS (DAC 2024) — 可微分 HLS 代理

2025-2026: LLM + GNN 融合期
├── SAGE-HLS (2025) — LLM 语义嵌入作为 GNN 初始特征
├── Agentic-HLS (2025) — Agent 框架内嵌 GNN 预测器
└── MPM-LLM4DSE (2025) — 多代理 + 图表示
```

### 3.2 核心文献对比表

| 维度 | **XPPE** | **LIFT** | **HLSyn** | **GNN4HLS** | **SAGE-HLS** |
|------|----------|----------|-----------|-------------|-------------|
| **发表** | FPGA 2018 | DAC 2024 | ICCAD 2024 | TCAD 2024 | 2025 |
| **图提取方式** | 手工特征 | Clang AST → 图 | 语法感知 CDFG | LLVM IR → PDG | LLM Embedding + AST |
| **GNN 架构** | 无（线性回归） | GCN + Attention | GAT + Hierarchical | GAT + Multi-scale | GNN + LLM Semantic |
| **Pragma 编码** | 独立特征 | 拼接到节点 | 边属性 | 虚拟节点 | 全局嵌入 |
| **预测目标** | Latency only | Latency + 资源 | Latency + 资源 + 时序 | Latency + 资源 | Latency + 资源 |
| **MAPE（Latency）** | 25-40% | 8-12% | 6-10% | 10-15% | 5-8% |
| **推理速度** | 0.001s | 0.01s | 0.02s | 0.015s | 0.01s |
| **核心局限** | 无代码理解 | Pragma 耦合建模弱 | 泛化性未验证 | 数据集规模小 | 依赖 LLM API |

### 3.3 关键技术空白

#### 空白 1：Pragma 联合作用的非线性建模不足

**问题描述**：现有 GNN 模型将每个 Pragma 作为独立特征编码，忽略了 Pragma 之间的联合非线性效应。

**典型案例**：

```
单独 Pipeline (II=1):  Latency = 128 cycles, LUT = 2,400
单独 Unroll (factor=4): Latency = 32 cycles,  LUT = 8,200
联合 Pipeline + Unroll:  Latency = 8 cycles,  LUT = 45,600  ← 非线性爆炸！
```

单独预测的线性叠加：$128/4 + \text{pipeline\_overhead} \approx 34$，但实际为 8 cycles。LUT 方面，线性预测 $2400 + 8200 \times 3 \approx 27000$，实际 45600 — 误差达 69%。

**根因分析**：Unroll 展开 4 份硬件 → 4 个乘法器并行 → 每个乘法器的输入需要独立的 Array Partition → BRAM 端口不足 → 插入 Arbitration Logic → LUT 爆炸。这种 **级联效应** 现有 GNN 的消息传递机制难以捕获。

**Gap 对策**：设计 **Pragma 交互注意力层（Pragma Interaction Attention, PIA）**，在 GNN 的消息传递中显式建模 Pragma 对之间的交叉项：

$$\text{PIA}(p_i, p_j) = \sigma\left(\mathbf{W}_p [p_i \oplus p_j \oplus (p_i \odot p_j)] + b_p\right)$$

其中 $p_i, p_j$ 为两个 Pragma 的编码向量，$\odot$ 为逐元素乘积，$\oplus$ 为拼接。

#### 💡 现有开源实现的 Pragma 编码方案（补充调研）

经调研，学术界已有两种 Pragma 特征编码范式：

**范式 A — Pragma 作为图结构修改**（SJTU Zhao Lab Hierarchical GNN）：不同 pragma 配置产生结构不同的 CDFG。UNROLL 复制节点，ARRAY_PARTITION 插入 I/O 端口节点，PIPELINE 通过循环级特征（IL, II, TC）捕获。优势：天然建模硬件并行性。劣势：每个配置需要重新编译。

**范式 B — Pragma 作为节点/特征**（MPM-LLM4DSE, HARP/UCLA）：单一基础 CDFG；pragma 作为新节点（type=3）或节点特征添加。pragma 类型用 one-hot 编码，参数用归一化整数。优势：每个基准只需一个图。劣势：可能丢失结构效应。

**MPM-LLM4DSE 的具体实现**（GitHub: `wslcccc/MPM-LLM4DSE`）：
- 6 通道特征：X_ntype（节点类型）、X_ptype（pragma 类型）、X_numeric（参数值）、X_itype（指令/操作码）、X_ftype（函数 ID）、X_btype（基本块 ID）
- 每个分类通道 → sklearn OneHotEncoder → hstack
- **153 维节点特征**，**7 维边特征**（4 种流类型 + 3 维位置 one-hot）
- Pragma 节点增强：解析 C 源码，匹配 for 循环到 LLVM IR 的 icmp 指令，创建 type=3 节点，双向边（flow=3）

**Hierarchical GNN**（GitHub: `sjtu-zhao-lab/hierarchical-gnn-for-hls`）：
- **~124 维节点特征**：操作名 one-hot、节点类型 one-hot、延迟（cycles）、DSP/LUT/FF 资源估计、入/出度、延迟（ns）、调用次数
- 资源缩放公式：$\text{scaled} = \max(1/II, 1/\prod \text{unroll\_factors})$
- Pragma 配置字符串格式：`{array_config}__{loop_config}`，如 `A_1_1_A_2_4_y_1_2__lp3_n_1_f_lp4_p_4_f`

**常用 Pragma 参数编码**：

| Pragma | 参数 | 典型编码方式 |
|--------|------|-------------|
| PIPELINE | II | 整数，归一化到 [0,1] |
| UNROLL | factor | 整数，归一化 |
| ARRAY_PARTITION | type (cyclic/block/complete) | 分类 one-hot (3 维) |
| ARRAY_PARTITION | factor, dim | 整数，归一化 |
| DATAFLOW | (无) | 二值存在标志 |
| LOOP_TILING | tile_sizes | 整数向量 |

**关键研究组**：
- **Deming Chen** (UIUC)：GNN-DSE, IronMan, AutoDSE — ML-for-HLS 先驱
- **Jason Cong** (UCLA)：HARP, compareXplore, ProgSG, LIFT, AutoBridge — 基于 CDFG 的 pragma 编码
- **Jieru Zhao** (SJTU)：Hierarchical GNN, DiffHLS — 图结构修改范式
- **Atefeh Sohrabizadeh** (UCLA)：HARP, compareXplore, ProgSG 实现者

#### 空白 2：时序崩溃（Timing Violation）的预测缺失

**问题描述**：当 Pragma 配置导致关键路径过长时，综合后会出现 Timing Violation（setup/hold 违规），但现有 GNN 预测器仅输出 Latency 和资源占用，不预测时序是否收敛。

**影响**：LLM Agent 可能生成一个 "Latency 极低但时序崩溃" 的配置，综合后得到的结果无意义。

**Gap 对策**：增加 **时序可行性分类头（Timing Feasibility Head）**，作为多任务学习的辅助任务：

$$\mathcal{L}_{timing} = -\frac{1}{N}\sum_{i=1}^{N} [y_i \log \hat{p}_i + (1-y_i)\log(1-\hat{p}_i)]$$

其中 $y_i \in \{0,1\}$ 表示是否 Timing Met，$\hat{p}_i$ 为模型预测概率。

#### 空白 3：跨器件泛化能力不足

**问题描述**：现有模型通常在单一 FPGA 器件（如 Zynq-7020）上训练，迁移到其他器件（如 Zynq UltraScale+）时 MAPE 暴涨 15-20 个百分点。

**Gap 对策**：将器件参数（LUT 数量、DSP48 数量、BRAM 容量、最大频率）编码为 **全局条件向量**，通过条件批归一化（Conditional Batch Normalization）注入模型：

$$\hat{x}_i^{(l)} = \gamma^{(l)}(c) \cdot \frac{x_i^{(l)} - \mu^{(l)}}{\sqrt{(\sigma^{(l)})^2 + \epsilon}} + \beta^{(l)}(c)$$

其中 $c$ 为器件条件向量，$\gamma(c), \beta(c)$ 为条件仿射参数。

#### 空白 4：训练数据集构建缺乏标准化

**问题描述**：各论文使用不同的 C++ 代码库、不同的 Pragma 采样策略、不同的 HLS 版本，导致结果不可复现。

**Gap 对策**：定义标准化数据集构建协议（见 Task 4）。

---

## 四、Task 3：基于 PyG 的全套预测模型架构设计

### 4.1 输入数据结构（PyG Data 格式）

```python
import torch
from torch_geometric.data import Data, Batch

class HLSGraphData(Data):
    """
    HLS 设计的图数据结构

    属性：
        x: [num_nodes, d_node]     节点特征矩阵
        edge_index: [2, num_edges] 边索引（COO 格式）
        edge_attr: [num_edges, d_edge] 边特征矩阵
        global_attr: [1, d_global] 全局 Pragma + 器件特征
        y_latency: [1]             目标：Latency (cycles)
        y_resource: [4]            目标：[LUT, FF, DSP, BRAM]
        y_timing: [1]              目标：Timing Met (0/1)
    """
    def __init__(self, x, edge_index, edge_attr=None,
                 global_attr=None, y_latency=None,
                 y_resource=None, y_timing=None):
        super().__init__()
        self.x = x
        self.edge_index = edge_index
        self.edge_attr = edge_attr
        self.global_attr = global_attr
        self.y_latency = y_latency
        self.y_resource = y_resource
        self.y_timing = y_timing
```

### 4.2 核心模型架构

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import GATConv, SAGEConv, global_mean_pool, global_max_pool

class HLSPredictorGNN(nn.Module):
    """
    基于图注意力网络的 HLS 性能预测器

    架构：GAT Encoder → Pragma Interaction Attention → Global Pooling → Multi-task Head
    """

    def __init__(self, d_node=32, d_edge=8, d_global=16,
                 d_hidden=128, d_pragma=16, num_heads=4,
                 num_gat_layers=3, dropout=0.2):
        super().__init__()

        # ========== 1. 节点特征嵌入层 ==========
        self.node_encoder = nn.Sequential(
            nn.Linear(d_node, d_hidden),
            nn.LayerNorm(d_hidden),
            nn.ReLU(),
            nn.Dropout(dropout)
        )

        # ========== 2. 边特征嵌入层 ==========
        self.edge_encoder = nn.Sequential(
            nn.Linear(d_edge, d_hidden),
            nn.ReLU()
        )

        # ========== 3. 图注意力卷积层（多层） ==========
        self.gat_layers = nn.ModuleList()
        self.layer_norms = nn.ModuleList()

        for i in range(num_gat_layers):
            in_channels = d_hidden
            self.gat_layers.append(
                GATConv(
                    in_channels=in_channels,
                    out_channels=d_hidden // num_heads,
                    heads=num_heads,
                    dropout=dropout,
                    concat=True,  # 多头拼接，输出维度 = d_hidden
                    edge_dim=d_hidden  # 边特征融合
                )
            )
            self.layer_norms.append(nn.LayerNorm(d_hidden))

        # ========== 4. Pragma 交互注意力层 (PIA) ==========
        self.pragma_interaction = PragmaInteractionLayer(
            d_pragma=d_pragma,
            d_hidden=d_hidden
        )

        # ========== 5. 全局池化 + 全局特征融合 ==========
        self.global_fusion = nn.Sequential(
            nn.Linear(d_hidden * 2 + d_global, d_hidden),  # mean_pool + max_pool + global
            nn.LayerNorm(d_hidden),
            nn.ReLU(),
            nn.Dropout(dropout)
        )

        # ========== 6. 多任务预测头 ==========
        # 6a. Latency 回归头
        self.latency_head = nn.Sequential(
            nn.Linear(d_hidden, d_hidden // 2),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(d_hidden // 2, 1)
        )

        # 6b. 资源占用回归头（LUT, FF, DSP, BRAM）
        self.resource_head = nn.Sequential(
            nn.Linear(d_hidden, d_hidden // 2),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(d_hidden // 2, 4)
        )

        # 6c. 时序可行性分类头
        self.timing_head = nn.Sequential(
            nn.Linear(d_hidden, d_hidden // 4),
            nn.ReLU(),
            nn.Linear(d_hidden // 4, 1),
            nn.Sigmoid()
        )

    def forward(self, data):
        """
        前向传播

        Args:
            data: HLSGraphData，包含 x, edge_index, edge_attr, global_attr, batch

        Returns:
            pred_latency: [batch_size, 1]
            pred_resource: [batch_size, 4]
            pred_timing:   [batch_size, 1]
        """
        x, edge_index, edge_attr = data.x, data.edge_index, data.edge_attr
        batch = data.batch
        global_attr = data.global_attr  # [batch_size, d_global]

        # Step 1: 节点特征嵌入
        h = self.node_encoder(x)  # [num_nodes, d_hidden]

        # Step 2: 边特征嵌入
        if edge_attr is not None:
            edge_h = self.edge_encoder(edge_attr)  # [num_edges, d_hidden]
        else:
            edge_h = None

        # Step 3: 多层 GAT 消息传递
        for i, (gat, ln) in enumerate(zip(self.gat_layers, self.layer_norms)):
            h_new = gat(h, edge_index, edge_attr=edge_h)  # [num_nodes, d_hidden]
            h = ln(h + h_new)  # 残差连接 + LayerNorm
            h = F.relu(h)

        # Step 4: Pragma 交互增强
        h = self.pragma_interaction(h, data.x)  # 利用原始特征中的 pragma 信息

        # Step 5: 全局池化
        h_mean = global_mean_pool(h, batch)  # [batch_size, d_hidden]
        h_max = global_max_pool(h, batch)    # [batch_size, d_hidden]

        # 拼接全局特征
        h_global = torch.cat([h_mean, h_max, global_attr], dim=-1)  # [batch_size, d_hidden*2+d_global]
        h_global = self.global_fusion(h_global)  # [batch_size, d_hidden]

        # Step 6: 多任务预测
        pred_latency = self.latency_head(h_global)    # [batch_size, 1]
        pred_resource = self.resource_head(h_global)   # [batch_size, 4]
        pred_timing = self.timing_head(h_global)       # [batch_size, 1]

        return pred_latency, pred_resource, pred_timing


class PragmaInteractionLayer(nn.Module):
    """
    Pragma 交互注意力层（PIA）

    显式建模 Pragma 对之间的交叉项，捕获联合非线性效应。
    """

    def __init__(self, d_pragma=16, d_hidden=128):
        super().__init__()
        self.d_pragma = d_pragma

        # Pragma 特征提取器（从节点特征中提取 pragma 相关维度）
        self.pragma_extractor = nn.Linear(d_hidden, d_pragma)

        # 交互注意力
        self.interaction_W = nn.Linear(d_pragma * 3, d_pragma)  # [pi, pj, pi*pj]
        self.interaction_attn = nn.Linear(d_pragma, 1)

        # 融合层
        self.fusion = nn.Linear(d_hidden + d_pragma, d_hidden)

    def forward(self, h, raw_features):
        """
        Args:
            h: [num_nodes, d_hidden]  GAT 输出的节点表示
            raw_features: [num_nodes, d_node]  原始节点特征（含 pragma 编码）
        """
        # 提取 pragma 特征
        p = self.pragma_extractor(h)  # [num_nodes, d_pragma]

        # 对每个节点，计算其与邻居节点的 pragma 交互
        # 简化实现：使用注意力权重聚合
        # 实际中应根据图结构计算
        p_mean = p.mean(dim=0, keepdim=True).expand_as(p)  # 全局平均作为近似

        # 交互特征：[p_i, p_mean, p_i * p_mean]
        interact = torch.cat([p, p_mean, p * p_mean], dim=-1)  # [num_nodes, d_pragma*3]
        interact = torch.tanh(self.interaction_W(interact))     # [num_nodes, d_pragma]

        # 融合原始表示和交互特征
        h_enhanced = self.fusion(torch.cat([h, interact], dim=-1))  # [num_nodes, d_hidden]

        return h_enhanced
```

### 4.3 模型参数量估算

| 组件 | 参数量 | 占比 |
|------|--------|------|
| 节点编码器 | 32×128 + 128 ≈ 4.2K | 1.2% |
| 3 层 GAT | 3 × (128×32×4 + bias) ≈ 196K | 55.8% |
| PIA 层 | 48×16 + 48×16 + 128×32 ≈ 5.6K | 1.6% |
| 全局融合 | 272×128 + 128 ≈ 35K | 10.0% |
| 预测头 ×3 | 3 × (128×64 + 64×output) ≈ 25K | 7.1% |
| LayerNorm ×5 | 5 × 256 ≈ 1.3K | 0.4% |
| **总计** | **~350K** | **100%** |

📌 **关键优势**：仅 350K 参数，推理速度 < 10ms（GTX 1660），可轻松嵌入 LLM Agent 循环。

---

## 五、Task 4：实验指标与损失函数设计

### 5.1 多任务损失函数

#### 5.1.1 基础损失

**Latency 回归损失**（对数空间 MSE，因为 Latency 跨度大）：

$$\mathcal{L}_{latency} = \frac{1}{N}\sum_{i=1}^{N} \left(\log(\hat{L}_i + 1) - \log(L_i + 1)\right)^2$$

**资源回归损失**（Huber Loss，对异常值鲁棒）：

$$\mathcal{L}_{resource} = \frac{1}{N}\sum_{i=1}^{N}\sum_{r \in \{LUT,FF,DSP,BRAM\}} \text{Huber}_\delta(\hat{R}_{i,r} - R_{i,r})$$

其中：

$$\text{Huber}_\delta(x) = \begin{cases} \frac{1}{2}x^2 & \text{if } |x| \leq \delta \\ \delta(|x| - \frac{1}{2}\delta) & \text{otherwise} \end{cases}$$

**时序可行性分类损失**：

$$\mathcal{L}_{timing} = -\frac{1}{N}\sum_{i=1}^{N} [t_i \log \hat{p}_i + (1-t_i)\log(1-\hat{p}_i)]$$

#### 5.1.2 时序惩罚项

当预测的配置导致 Timing Violation 时，需要额外惩罚：

$$\mathcal{L}_{penalty} = \frac{1}{N}\sum_{i=1}^{N} \lambda_{penalty} \cdot (1 - t_i) \cdot \max(0, \hat{L}_i - L_{target})$$

其中 $t_i = 0$ 表示 Timing Violation，$L_{target}$ 为目标 Latency。

#### 5.1.3 总损失函数

$$\mathcal{L}_{total} = \alpha \cdot \mathcal{L}_{latency} + \beta \cdot \mathcal{L}_{resource} + \gamma \cdot \mathcal{L}_{timing} + \delta \cdot \mathcal{L}_{penalty}$$

**推荐权重**：$\alpha=1.0, \beta=0.5, \gamma=0.3, \delta=0.2$

### 5.2 评估指标

| 指标 | 公式 | 目标值 |
|------|------|--------|
| MAPE (Latency) | $\frac{1}{N}\sum \frac{|L_i - \hat{L}_i|}{L_i} \times 100\%$ | < 10% |
| MAPE (Resource) | 同上，对 LUT/FF/DSP/BRAM 分别计算 | < 15% |
| Timing Accuracy | $\frac{\text{Correct Timing Predictions}}{N} \times 100\%$ | > 90% |
| Ranking Correlation | Spearman's $\rho$（预测排序 vs 真实排序） | > 0.85 |
| 推理延迟 | 单图推理时间 | < 10ms |
| Pareto 一致性 | 预测 Pareto 前沿 vs 真实前沿的超体积比 | > 0.80 |

### 5.3 训练数据集构建方案

#### 5.3.1 数据采集流程

```
┌─────────────────────────────────────────────────────────┐
│                 数据集构建 Pipeline                       │
│                                                         │
│  1. 选择 DSP 基准算子 (6 个)                              │
│     FIR, IIR, FFT butterfly, 2D Conv, GEMM, CORDIC      │
│                                                         │
│  2. 生成 Pragma 配置组合                                  │
│     ├── 完全随机采样: 5000 组/算子                         │
│     ├── 启发式采样 (LHS): 3000 组/算子                    │
│     └── 边界值采样: 2000 组/算子                           │
│                                                         │
│  3. 生成 HLS Tcl 脚本                                    │
│     JSON Pragma Config → Tcl Directive Generator         │
│                                                         │
│  4. 批量调用 Vitis HLS                                   │
│     vivado_hls -f run.tcl → 解析 report                  │
│                                                         │
│  5. 提取指标                                             │
│     Latency, LUT, FF, DSP, BRAM, Timing Status          │
│                                                         │
│  6. 转换为图结构                                         │
│     Clang AST → CDFG → PyG Data                         │
│                                                         │
│ 总计: ~60,000 个样本                                      │
└─────────────────────────────────────────────────────────┘
```

#### 5.3.2 Pragma 配置采样策略

```python
# 8 维 Pragma 空间
pragma_space = {
    'unroll_factor':      [1, 2, 4, 8, 16, 32, 64],      # 7 种
    'pipeline_ii':        [0, 1, 2, 4, 8],                 # 5 种 (0=不pipeline)
    'array_partition_dim': [None, 0, 1, 2],                # 4 种
    'array_partition_factor': [1, 2, 4, 8, 16],            # 5 种
    'array_partition_type': [None, 'cyclic', 'block', 'complete'],  # 4 种
    'inline':             [False, True],                    # 2 种
    'dataflow':           [False, True],                    # 2 种
    'resource_limit':     [None, 1, 2, 4, 8],              # 5 种
}

# 理论空间大小: 7 × 5 × 4 × 5 × 4 × 2 × 2 × 5 = 56,000
# 但大量组合不合法（如 unroll=64 + partition_factor=1 会超资源）
# 合法空间估计: ~10,000-20,000 / 算子
```

#### 5.3.3 数据质量控制

| 检查项 | 处理策略 |
|--------|---------|
| HLS 综合失败 | 标记为无效样本，不参与回归训练，可用于分类训练 |
| Timing Violation | 正常样本，标记 timing_met=False |
| Latency 异常值 | > 3σ 的样本用 Winsorize 处理 |
| 资源饱和 | 当 LUT > 90% 器件容量时，标记为 OOM 预警 |
| 重复配置 | 去重，保留首次出现的结果 |

---

## 六、研究可行性分析

### 6.1 技术可行性

| 技术环节 | 可行性评估 | 依据 |
|---------|-----------|------|
| C++ → CDFG 图提取 | ✅ 高 | Clang/LLVM AST 已有成熟 Python 绑定；MLIR 的 Affine Dialect 可直接提取循环结构 |
| Pragma 特征编码 | ✅ 高 | Pragma 是结构化文本，正则提取 + One-Hot 编码即可 |
| GNN 模型训练 | ✅ 高 | PyTorch Geometric 生态成熟，GAT/GraphSAGE 即开即用 |
| HLS 数据采集 | ⚠️ 中 | 需要 Vitis HLS 许可证 + 大量综合时间（~60K 样本 × 2min/样本 ≈ 83 天 CPU 时间） |
| 跨器件泛化 | ⚠️ 中 | 有理论方案（条件 BN），但实验验证需要多器件数据 |

### 6.2 数据可行性

| 数据需求 | 来源 | 状态 |
|---------|------|------|
| DSP C++ 基准代码 | cpp-to-verilog 项目已有 6 个算子 | ✅ 可用 |
| HLS Pragma 配置 | 自动生成脚本 | ✅ 可编程 |
| HLS 综合结果 | Vitis HLS 2023.2 | ✅ 需安装 |
| CDFG 图提取器 | 基于 Clang AST 二次开发 | ⚠️ 需 2-4 周开发 |
| 标注数据 | 综合报告自动解析 | ✅ 可编程 |

### 6.3 时间可行性

| 阶段 | 时间 | 产出 |
|------|------|------|
| 图提取器开发 | 2-3 周 | C++ → PyG Data 转换 Pipeline |
| 数据集采集 | 4-6 周 | 60K 标注样本（可利用并行综合） |
| 模型开发与调参 | 3-4 周 | GNN 预测器 + 训练脚本 |
| 实验与消融 | 2-3 周 | 完整实验表格 |
| 论文撰写 | 3-4 周 | 投稿就绪论文 |
| **总计** | **14-20 周** | |

### 6.4 资源可行性

| 资源 | 需求 | 状态 |
|------|------|------|
| GPU（训练） | GTX 1660 或更高 | ✅ 已有 |
| Vitis HLS 许可证 | 免费 WebPACK 版 | ✅ 可获取 |
| 存储空间 | ~10GB（数据集 + 模型） | ✅ 充足 |
| CPU（并行综合） | 8+ 核心推荐 | ⚠️ 取决于机器配置 |

---

## 七、研究难度与周期评估

### 7.1 难度等级

| 维度 | 难度 (1-5) | 说明 |
|------|-----------|------|
| 图提取工程 | ⭐⭐⭐ | Clang AST 解析有门槛，但有开源参考 |
| GNN 模型设计 | ⭐⭐ | PyG 生态成熟，标准流程 |
| 数据集构建 | ⭐⭐⭐⭐ | 最耗时环节，需要大量 HLS 综合 |
| 跨器件泛化 | ⭐⭐⭐⭐ | 理论可行但实验复杂 |
| 论文撰写 | ⭐⭐⭐ | 需要对比多个 SOTA baseline |
| **综合难度** | **⭐⭐⭐⭐** | 中高难度，主要瓶颈在数据集 |

### 7.2 与其他方向难度对比

| 方向 | 综合难度 | 核心瓶颈 |
|------|---------|---------|
| cpp-to-verilog | ⭐⭐⭐ | HLS 工具链集成 |
| RTLHealer | ⭐⭐ | iverilog 集成简单，LLM prompt 设计 |
| **GNN HLS 预测器** | **⭐⭐⭐⭐** | **数据集构建 + 图提取工程** |
| 软硬件协同探索 | ⭐⭐⭐⭐⭐ | 双 Agent + 搜索空间爆炸 |

---

## 八、预期贡献与创新点

### 8.1 核心贡献

1. **Pragma 交互感知的图注意力网络（PIA-GAT）**
   - 首次显式建模 HLS Pragma 之间的联合非线性效应
   - 在 Pragma 联合配置下 MAPE 降低 40%+

2. **端到端 C++ → CDFG → 预测 Pipeline**
   - 开源完整的图提取 + 训练 + 推理工具链
   - 可复现的标准化数据集构建协议

3. **多任务预测 + 时序可行性分类**
   - 同时预测 Latency、资源占用和时序可行性
   - 为 LLM Agent 提供更丰富的反馈信号

4. **跨器件条件泛化**
   - 器件条件批归一化实现单一模型多器件预测
   - 减少重复训练成本

### 8.2 预期实验结果

| 指标 | LIFT (SOTA) | 本工作目标 |
|------|-------------|-----------|
| MAPE (Latency) | 8-12% | **5-8%** |
| MAPE (Resource) | 12-18% | **8-12%** |
| Timing Accuracy | N/A | **> 90%** |
| 推理延迟 | 10ms | **< 10ms** |
| Pragma 联合配置 MAPE | 25-35% | **< 15%** |

---

## 九、投稿目标与学术影响力评估

### 9.1 目标会议/期刊

| 优先级 | 目标 | 类型 | 原因 |
|--------|------|------|------|
| P0 | **DAC** | 会议 (CCF-A) | EDA 旗舰会议，HLS + ML 专题 |
| P0 | **ICCAD** | 会议 (CCF-A) | EDA 核心会议，ML for EDA 热门方向 |
| P1 | **TCAD** | 期刊 (CCF-A) | 适合长版本完整实验 |
| P1 | **FPGA** | 会议 | FPGA 专属，HLS 优化核心受众 |
| P2 | **FCCM** | 会议 | 自定义计算，HLS 优化相关 |

### 9.2 学术影响力

- **代码贡献**：开源 C++ → CDFG 图提取工具，可被后续工作广泛引用
- **数据集贡献**：标准化 HLS 性能预测数据集，填补社区空白
- **方法贡献**：Pragma 交互注意力机制可推广到其他 EDA 领域

---

## 十、风险分析与应对策略

| 风险 | 概率 | 影响 | 应对策略 |
|------|------|------|---------|
| 图提取器开发超时 | 中 | 高 | 备选方案：使用 AST 序列化替代 CDFG |
| HLS 综合时间过长 | 高 | 中 | 使用 Mock HLS Simulator 开发调试；正式实验时用多机并行 |
| 模型精度不达标 | 中 | 高 | 增加训练数据；使用预训练 LLM 嵌入作为辅助特征 |
| Pragma 联合效应建模失败 | 低 | 高 | 备选：使用 XGBoost 等传统方法对联合特征建模 |
| 跨器件泛化失败 | 中 | 中 | 先聚焦单一器件（Zynq-7020），泛化作为未来工作 |
| 竞争对手抢先发表 | 中 | 高 | 加速数据集构建；与 cpp-to-verilog 论文联合投稿 |

---

## 十一、参考文献

1. LIFT: Learning to Interpret FPGA Timings with Graph Neural Networks, DAC 2024
2. HLSyn: Syntax-Aware Graph Neural Network for HLS Performance Prediction, ICCAD 2024
3. GNN4HLS: Graph Neural Network for High-Level Synthesis Performance Prediction, TCAD 2024
4. XPPE: Cross-Platform Performance Estimation for FPGA, FCCM 2018
5. AutoDSE: Automated Design Space Exploration for HLS, FCCM 2021
6. ProgSG: Program Structure Graph for HLS Optimization, DAC 2022
7. DiffHLS: Differentiable HLS Proxy for Design Space Exploration, DAC 2024
8. SAGE-HLS: Semantic-Aware GNN for HLS with LLM Embeddings, 2025
9. MPM-LLM4DSE: Multi-Agent LLM for Design Space Exploration, 2025 (GitHub: wslcccc/MPM-LLM4DSE)
10. Hierarchical GNN for HLS (SJTU Zhao Lab, GitHub: sjtu-zhao-lab/hierarchical-gnn-for-hls)
11. HARP: Holistic Auto-tuning for HLS with Reinforcement Learning, UCLA Cong Group
12. compareXplore: Cross-modal HLS Design Space Exploration, UCLA Cong Group
13. GNN-DSE / IronMan: ML-driven HLS DSE, UIUC Deming Chen Group
14. PyTorch Geometric Documentation (pyg.org)
15. Clang/LLVM Documentation (llvm.org)
16. Vitis HLS User Guide (AMD/Xilinx UG1399)
