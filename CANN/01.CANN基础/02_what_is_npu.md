---
source_repo: cann-learning-hub
source_path: quick_start/cann_basics/02_what_is_npu.ipynb
source_commit: 1bf85454ed7c41e184a96fb51d109b6bb83b7c0d
note_kind: notebook_to_markdown
---

# 什么是 NPU —— 昇腾 NPU 硬件架构

> 📚 上游 Notebook：[quick_start/cann_basics/02_what_is_npu.ipynb](https://gitcode.com/cann/cann-learning-hub/blob/master/quick_start/cann_basics/02_what_is_npu.ipynb)
> 🧪 整理方式：保留 Markdown 与代码单元；省略 Jupyter 执行输出，避免把一次性环境结果误当成可复现结论。

## 🧭 学习目标

- 先读懂概念，再运行代码片段验证关键结论；
- 把本节内容接入后续 CANN / Ascend NPU 实践。

# ==========================================
## 📖 课程内容

上一章我们讲到：**AI 模型 = 计算图 = 算子组合 → 需要硬件执行 → 昇腾 NPU 专为 AI 计算加速设计**。本章就来拆开 NPU，看看它到底长什么样、为什么能加速 AI 计算。

---

### 1. 为什么需要 NPU

AI 计算有三个特点，和传统程序很不一样：

<table style="text-align: left; margin-left: 0;">
<tr>
<th style="text-align: left;">特点</th>
<th style="text-align: left;">说明</th>
<th style="text-align: left;">类比</th>
</tr>
<tr>
<td style="text-align: left;">计算密集</td>
<td style="text-align: left;">单次推理/训练涉及数十亿次乘加运算</td>
<td style="text-align: left;">搬一万块砖，每块都要搬</td>
</tr>
<tr>
<td style="text-align: left;">数据并行</td>
<td style="text-align: left;">同一操作对海量数据重复执行</td>
<td style="text-align: left;">同一道工序处理一万个零件</td>
</tr>
<tr>
<td style="text-align: left;">低精度可接受</td>
<td style="text-align: left;">FP16/BF16 甚至 INT8 就够用</td>
<td style="text-align: left;">不需要精确到小数点后10位，差不多就行</td>
</tr>
</table>

CPU 是"全能型选手"，什么都能干但速度有限；NPU 是"专职选手"，矩阵和向量运算极快。

---

### 2. CPU vs NPU：算力差距有多大

以 AI 中最常见的**16×16 矩阵乘法**为例，看看不同计算方式的效率差距：

<img src="../../../CANN-assets-20260813/quick_start/cann_basics/images/matrix_multiplication_example.png"  alt="矩阵乘法示例" />

**CPU（标量计算）**——一个一个算，每次只能算一个乘加：

```c
for (int i=0; i<16; i++)
    for (int j=0; j<16; j++)
        for (int k=0; k<16; k++)
            c[i][j] += a[i][k] * b[k][j];
```

总周期：$16 \times 16 \times 16 \times 2 = \mathbf{8192}$

**Vector（向量计算）**——一次算一整行和一整列：

```c
for (int i=0; i<16; i++)
    for (int j=0; j<16; j++)
        c[i][j] = a[i][:] *+ b[:][j];  // 一行与一列同时乘加
```

总周期：$16 \times 16 = \mathbf{256}$

**Cube（矩阵计算）**——一次算完整矩阵：

```c
c[:][:] = a[:][:] × b[:][:];  // 两个矩阵一次性乘加
```

总周期：$\mathbf{1}$

<table style="text-align: left; margin-left: 0;">
<tr>
<th style="text-align: left;">计算方式</th>
<th style="text-align: left;">一句话理解</th>
<th style="text-align: left;">16×16 矩阵乘总周期</th>
</tr>
<tr>
<td style="text-align: left;">CPU</td>
<td style="text-align: left;">一个一个算</td>
<td style="text-align: left;">8192</td>
</tr>
<tr>
<td style="text-align: left;">Vector</td>
<td style="text-align: left;">一行一列一起算</td>
<td style="text-align: left;">256</td>
</tr>
<tr>
<td style="text-align: left;">Cube</td>
<td style="text-align: left;">整个矩阵一起算</td>
<td style="text-align: left;">1</td>
</tr>
</table>

这就是**异构计算**的思想：让 CPU 管逻辑和控制，让 NPU 管密集计算，**专人干专事**。

<img src="../../../CANN-assets-20260813/quick_start/cann_basics/images/heterogeneous_computing_architecture.png"  alt="异构计算架构" />

---

### 3. 昇腾 NPU 产品全览

<img src="../../../CANN-assets-20260813/quick_start/cann_basics/images/ascend.png"  alt="ascend" />

昇腾 NPU 处理器目前已推出多代产品，覆盖推理与训练全场景：

<table style="text-align: left; margin-left: 0;">
<tr>
<th style="text-align: left;">处理器</th>
<th style="text-align: left;">定位</th>
<th style="text-align: left;">典型场景</th>
</tr>
<tr>
<td style="text-align: left;">Ascend 310B</td>
<td style="text-align: left;">端侧/边缘推理</td>
<td style="text-align: left;">摄像头、边缘盒子等小功耗场景</td>
</tr>
<tr>
<td style="text-align: left;">Ascend 310P</td>
<td style="text-align: left;">数据中心推理</td>
<td style="text-align: left;">在线推理、视频分析等低功耗高吞吐场景</td>
</tr>
<tr>
<td style="text-align: left;">Ascend 910B</td>
<td style="text-align: left;">中大规模训练</td>
<td style="text-align: left;">大模型预训练、微调，单卡至千卡集群</td>
</tr>
<tr>
<td style="text-align: left;">Ascend 910C</td>
<td style="text-align: left;">大规模训练</td>
<td style="text-align: left;">千亿参数大模型训练，万卡集群</td>
</tr>
<tr>
<td style="text-align: left;">Ascend 950PR</td>
<td style="text-align: left;">训推一体</td>
<td style="text-align: left;">训练与推理兼顾，灵活部署</td>
</tr>
<tr>
<td style="text-align: left;">Ascend 950DT（即将上市）</td>
<td style="text-align: left;">下一代训推一体</td>
<td style="text-align: left;">更高算力、更优能效，面向未来大模型</td>
</tr>
</table>


---

### 4. NPU 怎么和 CPU 协作：Host 与 Device

把昇腾加速卡插入服务器后，CPU 和 NPU 各司其职：

<img src="../../../CANN-assets-20260813/quick_start/cann_basics/images/host_and_device.png"  alt="Host和Device" />

<table style="text-align: left; margin-left: 0;">
<tr>
<th style="text-align: left;"></th>
<th style="text-align: left;">Host（CPU 侧）</th>
<th style="text-align: left;">Device（NPU 侧）</th>
</tr>
<tr>
<td style="text-align: left;">角色</td>
<td style="text-align: left;">"老板"</td>
<td style="text-align: left;">"工人"</td>
</tr>
<tr>
<td style="text-align: left;">职责</td>
<td style="text-align: left;">发任务、传数据、收结果</td>
<td style="text-align: left;">拼命算、算完交差</td>
</tr>
</table>

#### 用代码感受 Host 与 Device

Host（CPU）负责发任务、传数据、收结果；Device（NPU）负责拼命算、算完交差。下面用代码逐步体验这个协作过程。

```python
import torch
import torch_npu

# 查看当前 NPU 是否可用
print(f"NPU 可用: {torch.npu.is_available()}")

# 查看当前 NPU 设备编号
print(f"当前 NPU 设备: {torch.npu.current_device()}")

# 查看 NPU 数量
print(f"NPU 卡数: {torch.npu.device_count()}")

# 查看 NPU 名称
print(f"NPU 名称: {torch.npu.get_device_name(0)}")
```

运行结果展示了 Host 侧查询到的 NPU 设备信息——这是 Host 在"认识"Device。

接下来，我们通过一个矩阵乘法示例，完整体验 Host 与 Device 的协作流程：

#### Host/Device 协作流程：矩阵乘法

数据可以直接在 NPU 上创建（推荐），也可以先在 CPU 创建再搬运到 NPU（适用于加载已有数据）。下面演示两种方式：

```python
import torch
import torch_npu  # 注册 NPU 后端，使 .npu() 和 torch.npu 可用

N = 1024

# ---- 方式一：数据直接在 NPU 上创建（推荐） ----
A_npu = torch.randn(N, N, device='npu:0')
B_npu = torch.randn(N, N, device='npu:0')
print(f'[Device] 直接在 NPU 上创建矩阵，A.device={A_npu.device}')

C_npu = torch.mm(A_npu, B_npu)
print(f'[Device] NPU 完成矩阵乘法，结果形状: {C_npu.shape}')

# ---- 方式二：数据先在 CPU 创建，再搬运到 NPU（适用于加载已有数据） ----
A_cpu = torch.randn(N, N)  # Host 创建
A_on_npu = A_cpu.npu()     # Host -> Device 搬运
print(f'[Host -> Device] 数据从 CPU 搬运到 NPU，A.device={A_on_npu.device}')

# ---- Device -> Host：结果搬回 CPU ----
C = C_npu.cpu()
print(f'[Device -> Host] 结果搬回 CPU，C.device={C.device}')
```

上面的示例展示了 Host/Device 协作的关键环节：

| 操作 | 代码 | 说明 |
|------|------|------|
| 数据直接在 NPU 创建 | `torch.randn(..., device='npu:0')` | 推荐方式，省去搬运开销 |
| Host -> Device | `.npu()` | 将 CPU 数据搬运到 Device 内存（适用于加载模型权重、数据集等已有数据） |
| Device 执行计算 | `torch.mm()` | NPU 完成矩阵乘法 |
| Device -> Host | `.cpu()` | 结果从 Device 内存搬回 CPU |

> **术语说明**：GPU 上叫"显存"，NPU 上对应的概念叫 **Device 内存**，CANN 文档统一使用此术语。

> 整个过程中，Host 负责"发任务、传数据、收结果"，Device 负责"拼命算、算完交差"——这就是异构计算的分工协作。

### 5. NPU 内部结构

打开 NPU 芯片，里面有 6 大组件：

<img src="../../../CANN-assets-20260813/quick_start/cann_basics/images/npu_processor.png"  alt="NPU处理器内部结构" />

<table style="text-align: left; margin-left: 0;">
<tr>
<th style="text-align: left;">组件</th>
<th style="text-align: left;">职责</th>
</tr>
<tr>
<td style="text-align: left;">AI Core</td>
<td style="text-align: left;">核心计算单元，矩阵/向量密集算子在此执行（如 MatMul、Conv、FlashAttention）</td>
</tr>
<tr>
<td style="text-align: left;">AI CPU</td>
<td style="text-align: left;">执行 AI Core 不擅长的 CPU 类算子，如控制流算子（If/While）、标量计算（Log/Exp）、复杂索引（Gather/Scatter）；也承担页表管理、性能监控等系统任务</td>
</tr>
<tr>
<td style="text-align: left;">控制 CPU</td>
<td style="text-align: left;">芯片内部管理控制：初始化、资源分配、故障处理、与 Host 侧驱动交互。不执行用户算子</td>
</tr>
<tr>
<td style="text-align: left;">TS（任务调度器）</td>
<td style="text-align: left;">硬件调度器（950 升级为 STARS 2.0），接收 Host 下沉的任务流，调度分发给 AI Core / AI CPU / DVPP 等执行单元，管理同步与依赖</td>
</tr>
<tr>
<td style="text-align: left;">DVPP</td>
<td style="text-align: left;">数字视觉预处理：图像解码（JPEG）、格式转换、缩放裁剪等，为 AI Core 准备输入数据</td>
</tr>
<tr>
<td style="text-align: left;">Device 内存</td>
<td style="text-align: left;">片上高速存储（HBM），存放模型权重、激活数据、KV Cache 等待计算数据和结果</td>
</tr>
</table>

> **协作关系**：Host CPU（外部）下发任务 → 控制CPU（接收管理）→ TS（调度分发）→ AI Core（密集计算）/ AI CPU（辅助算子）/ DVPP（图像预处理）→ 结果返回 Host。

> **互联总线**：芯片内/芯片间高速互联（如灵衢 UB），支撑多 Die 通信和多卡集群。

#### 查看 NPU 实时状态

`npu-smi info` 可以查看 NPU 的实时状态，就像给 NPU 做一次"体检"：

```bash
!npu-smi info
```

输出中各字段含义：

<table style="text-align: left; margin-left: 0;">
<tr>
<th style="text-align: left;">字段</th>
<th style="text-align: left;">含义</th>
</tr>
<tr>
<td style="text-align: left;">NPU Name</td>
<td style="text-align: left;">芯片型号（如 Ascend910B3）</td>
</tr>
<tr>
<td style="text-align: left;">Health</td>
<td style="text-align: left;">健康状态，`OK` 表示正常</td>
</tr>
<tr>
<td style="text-align: left;">Power(W)</td>
<td style="text-align: left;">当前功耗（瓦）</td>
</tr>
<tr>
<td style="text-align: left;">Temp(C)</td>
<td style="text-align: left;">当前温度（摄氏度）</td>
</tr>
<tr>
<td style="text-align: left;">AICore(%)</td>
<td style="text-align: left;">AI Core 利用率，0% 表示空闲，100% 表示满载</td>
</tr>
<tr>
<td style="text-align: left;">Memory-Usage(MB)</td>
<td style="text-align: left;">Device 内存使用量 / 总量</td>
</tr>
<tr>
<td style="text-align: left;">HBM-Usage(MB)</td>
<td style="text-align: left;">HBM 高带宽内存使用量 / 总量</td>
</tr>
</table>

> 如果 `Health: OK` 且温度和功耗在正常范围，说明 NPU 硬件和驱动都正常工作。

### 6. AI Core：NPU 的计算核心

AI Core 作为 NPU 的计算核心，绝大多数算子的加速执行均在此完成。其架构延续传统芯片"计算-存储-控制"的三大核心模块，通过专用化设计实现极致并行效能，下文逐一解析各模块功能。

<img src="../../../CANN-assets-20260813/quick_start/cann_basics/images/ai_core_architecture.png"  alt="ai_core_architecture" />

#### 6.1 计算单元
AI Core内置三类专用计算单元，分别适配矩阵、向量、标量不同维度的计算需求，实现分工协作与并行提速。

<img src="../../../CANN-assets-20260813/quick_start/cann_basics/images/computing_unit.png" alt="computing_unit"  width="700px" >

1. **矩阵计算单元（Cube Unit）**   
    核心负责矩阵乘加运算，搭配累加器实现高效数据累加。硬件层面支持高精度并行计算：FP16精度下，单时钟周期可完成16×16与16×16矩阵乘（4096次乘加运算）；INT8精度下，单时钟周期可完成16×32与32×16矩阵乘（8192次乘加运算）。累加器可将当前矩阵乘结果与历史中间结果叠加，天然适配卷积运算中偏置（bias）添加等场景。

2. **向量计算单元（Vector Unit）**  
    专注于向量级运算，支持FP16、FP32、Int32、Int8等多数据类型，覆盖基本算术运算与定制化向量操作。运算效能表现为：单时钟周期可完成两组128长度FP16向量的加/乘运算，或64个FP32/Int32向量的加/乘运算，适配激活函数、数据归一化等向量密集型任务。

3. **标量计算单元（Scalar Unit）**  
    承担标量运算与AI Core整体控制职责，相当于微型CPU。核心功能包括：循环控制、分支判断、地址计算与参数配置（为Cube/Vector单元提供数据地址及运算参数），同时支持基础算术运算，保障各计算单元的协同有序运行。

#### 6.2 存储系统
由片上存储单元与数据通路组成，通过分层存储设计减少外部总线访问频次，降低延迟、提升带宽，为高速计算提供数据支撑。

<img src="../../../CANN-assets-20260813/quick_start/cann_basics/images/storage_system.png" alt="storage_system"  width="700px" >

1. **存储转换引擎**  
    负责AI Core内部不同缓冲区的数据读写管理，同时支持多种数据格式转换操作，如Padding（填充）、Transpose（转置）、Img2Col（3D图像转2D矩阵）等预处理/后处理操作。此外，可通过总线接口直接访问AI Core外部的低层级缓存，拓展数据访问范围。

2. **缓冲区**  
    包含L1缓冲区、L0A/L0B缓冲区、L0C缓冲区、统一缓冲区及标量缓冲区，核心作用是缓存高频复用数据与中间结果：一方面，将频繁访问的数据暂存片上，避免反复从外部读取，减少总线拥堵与功耗消耗；另一方面，存储神经网络各层计算的中间结果，为下一层运算快速提供数据，相较总线访问大幅降低延迟、提升运算效率。

3. **寄存器**  
    主要为标量计算单元服务，用于暂存标量数据、运算指令及控制参数，保障标量运算的高速执行。

#### 6.3 控制单元
作为AI Core的“指挥中枢”，负责全流程指令控制与时序协调，确保各单元并行运算的有序性与数据一致性。核心组成及功能如下：

<img src="../../../CANN-assets-20260813/quick_start/cann_basics/images/control_unit.png" alt="control_unit"  width="700px" >

- **系统控制模块**：管控任务块（AI Core最小计算任务粒度）的执行进程，任务块完成后执行中断处理与状态上报；若运算过程中出现错误，及时向任务调度器反馈错误状态。

- **指令缓存**：提前预取后续待执行指令，一次性读取多条指令缓存，避免指令逐条读取的延迟，提升指令执行效率。

- **标量指令处理队列**：指令解码后导入该队列，完成地址解码与运算控制，覆盖矩阵、向量、存储转换等各类指令。

- **指令发射模块**：读取标量指令处理队列中的指令地址与参数，解码后按指令类型分发至对应执行队列，标量指令则留存于该队列中执行。

- **指令执行队列**：分为矩阵运算队列、向量运算队列、存储转换队列，不同类型指令按顺序在对应队列中执行，实现并行流水线运算。

- **事件同步模块**：实时监控各指令流水线的执行状态，分析不同流水线的依赖关系，解决数据依赖与时序同步问题（如矩阵乘完成后再执行向量加法），保障运算结果正确性。

---

### 7. 多核并行

一张 NPU 卡包含多个 AI Core（如 Atlas A2 有 8~30 个），算子计算时：

1. **Tiling**：Host 侧把总数据按核数切分
2. **多核并行**：每个 AI Core 独立处理自己分到的数据块
3. **隐式同步**：所有核完成后由 TS 统一回收

> Tiling 将数据切分后分给多个 AI Core 并行处理，可显著缩短计算时间。

### 8. 昇腾 NPU 与 GPU 的架构对比

<table style="text-align: left; margin-left: 0;">
<tr>
<th style="text-align: left;">维度</th>
<th style="text-align: left;">昇腾 910B</th>
<th style="text-align: left;">NVIDIA H100</th>
</tr>
<tr>
<td style="text-align: left;">核心架构</td>
<td style="text-align: left;">DaVinci（Cube + Vector + Scalar）</td>
<td style="text-align: left;">SM（Tensor Core + CUDA Core）</td>
</tr>
<tr>
<td style="text-align: left;">矩阵计算单元</td>
<td style="text-align: left;">Cube Unit</td>
<td style="text-align: left;">Tensor Core</td>
</tr>
<tr>
<td style="text-align: left;">向量/标量单元</td>
<td style="text-align: left;">Vector Unit（向量级，128 FP16 元素/周期）</td>
<td style="text-align: left;">CUDA Core</td>
</tr>
<tr>
<td style="text-align: left;">编程范式</td>
<td style="text-align: left;">Ascend C，SIMD 为主，950开始增加了SIMT</td>
<td style="text-align: left;">CUDA，SIMT 为主</td>
</tr>
<tr>
<td style="text-align: left;">软件栈</td>
<td style="text-align: left;">CANN</td>
<td style="text-align: left;">CUDA Toolkit</td>
</tr>
</table>

### FAQ

**Q：AI CPU 和 AI Core 中的标量计算单元有什么区别？**

两者都能做标量/控制类运算，但本质不同：

| 维度 | AI Core 标量计算单元 | AI CPU |
|------|---------------------|--------|
| 本质 | AI Core 流水线内的一级硬件，和 Cube/Vector 紧耦合 | 芯片内独立的 ARM CPU 核 |
| 能力 | 简单标量运算：循环计数、地址计算、分支判断 | 完整 CPU，可运行任意代码 |
| 用途 | 服务算子内部执行：为 Cube/Vector 计算地址、控制循环 | 执行算子本身：跑 AI Core 不擅长的整类算子 |
| 举例 | 计算下一次 Cube 读取的 L1 Buffer 地址 | 执行 If/While 控制流算子、Gather/Scatter 动态索引 |
| 性能 | 极低延迟（ns 级），流水线内同步执行 | 较慢（通用 CPU），但灵活 |
| 独立性 | 不能独立运行，依附 AI Core 流水线 | 独立运行，有自己的 L1/L2/L3 Cache |

> 一句话：标量计算单元是 AI Core 的"内置计算器"，帮 Cube/Vector 算地址、控循环；AI CPU 是芯片内的"独立小电脑"，跑那些塞不进 AI Core 流水线的复杂算子。

---

---

### 小结

<table style="text-align: left; margin-left: 0;">
<tr>
<th style="text-align: left;">概念</th>
<th style="text-align: left;">说明</th>
</tr>
<tr>
<td style="text-align: left;">NPU</td>
<td style="text-align: left;">专为 AI 计算设计的处理器，矩阵与向量运算性能优异</td>
</tr>
<tr>
<td style="text-align: left;">异构计算</td>
<td style="text-align: left;">CPU 负责逻辑控制，NPU 负责密集计算</td>
</tr>
<tr>
<td style="text-align: left;">Host / Device</td>
<td style="text-align: left;">CPU 负责任务调度，NPU 负责计算执行</td>
</tr>
<tr>
<td style="text-align: left;">AI Core</td>
<td style="text-align: left;">NPU 的核心计算单元，算子主要在此执行</td>
</tr>
<tr>
<td style="text-align: left;">Cube / Vector / Scalar</td>
<td style="text-align: left;">三类计算单元分工协作</td>
</tr>
<tr>
<td style="text-align: left;">多核并行</td>
<td style="text-align: left;">多个 AI Core 并行执行，数据切分后各核独立处理</td>
</tr>
</table>

---

### 课后练习

请根据本节课程学习内容完成以下题目进行自测，在每题下方的代码框中输入选项字母后运行。

**第1题**（单选题）AI计算的三个特点中，"低精度可接受"指的是什么？

- A. 只能用INT8计算
- B. FP16/BF16甚至INT8就够用
- C. 不需要任何精度
- D. 必须使用FP64

```python
q1 = ''  # 填入你的选项，如 'B'，修改后务必运行本单元格（Shift+Enter）
print(f'第{1}题答案已记录：{q1}' if q1 else '⚠️ 请填入答案并运行本单元格')
```

**第2题**（单选题）以16×16矩阵乘法为例，CPU（标量计算）的总周期是多少？

- A. 256
- B. 1024
- C. 4096
- D. 8192

```python
q2 = ''  # 填入你的选项，如 'B'，修改后务必运行本单元格（Shift+Enter）
print(f'第{2}题答案已记录：{q2}' if q2 else '⚠️ 请填入答案并运行本单元格')
```

**第3题**（单选题）以16×16矩阵乘法为例，Cube（矩阵计算）的总周期是多少？

- A. 1
- B. 16
- C. 256
- D. 4096

```python
q3 = ''  # 填入你的选项，如 'B'，修改后务必运行本单元格（Shift+Enter）
print(f'第{3}题答案已记录：{q3}' if q3 else '⚠️ 请填入答案并运行本单元格')
```

**第4题**（单选题）昇腾产品线中，"加速卡"形态的代表产品是？

- A. Ascend 910B
- B. Atlas 300I A2
- C. Atlas 800T A2
- D. Atlas 900 A3 SuperPoD

```python
q4 = ''  # 填入你的选项，如 'B'，修改后务必运行本单元格（Shift+Enter）
print(f'第{4}题答案已记录：{q4}' if q4 else '⚠️ 请填入答案并运行本单元格')
```

**第5题**（单选题）在Host与Device的分工中，Host（CPU侧）的职责是？

- A. 拼命算、算完交差
- B. 发任务、传数据、收结果
- C. 管理NPU内部存储
- D. 执行矩阵乘法

```python
q5 = ''  # 填入你的选项，如 'B'，修改后务必运行本单元格（Shift+Enter）
print(f'第{5}题答案已记录：{q5}' if q5 else '⚠️ 请填入答案并运行本单元格')
```

**第6题**（单选题）NPU内部的6大组件中，哪个是核心计算单元？

- A. AI CPU
- B. 控制CPU
- C. AI Core
- D. 任务调度器

```python
q6 = ''  # 填入你的选项，如 'B'，修改后务必运行本单元格（Shift+Enter）
print(f'第{6}题答案已记录：{q6}' if q6 else '⚠️ 请填入答案并运行本单元格')
```

**第7题**（单选题）AI Core中，矩阵计算单元（Cube Unit）在FP16精度下单时钟周期可完成多大规模的矩阵乘？

- A. 8×8
- B. 16×16
- C. 32×32
- D. 64×64

```python
q7 = ''  # 填入你的选项，如 'B'，修改后务必运行本单元格（Shift+Enter）
print(f'第{7}题答案已记录：{q7}' if q7 else '⚠️ 请填入答案并运行本单元格')
```

**第8题**（单选题）AI Core中，标量计算单元（Scalar Unit）的核心功能不包括？

- A. 循环控制
- B. 分支判断
- C. 地址计算
- D. 大规模矩阵乘法

```python
q8 = ''  # 填入你的选项，如 'B'，修改后务必运行本单元格（Shift+Enter）
print(f'第{8}题答案已记录：{q8}' if q8 else '⚠️ 请填入答案并运行本单元格')
```

**第9题**（单选题）多核并行中，Host侧把总数据按核数切分的过程叫什么？

- A. Tiling
- B. Fusion
- C. Quantization
- D. Parallelization

```python
q9 = ''  # 填入你的选项，如 'B'，修改后务必运行本单元格（Shift+Enter）
print(f'第{9}题答案已记录：{q9}' if q9 else '⚠️ 请填入答案并运行本单元格')
```

**第10题**（单选题）昇腾NPU与GPU的架构对比中，昇腾NPU的核心架构名称是？

- A. SM
- B. DaVinci
- C. Tensor Core
- D. CUDA Core

```python
q10 = ''  # 填入你的选项，如 'B'，修改后务必运行本单元格（Shift+Enter）
print(f'第{10}题答案已记录：{q10}' if q10 else '⚠️ 请填入答案并运行本单元格')
```

**全部作答完成后，运行下方代码查看批改结果：**

```python
import sys
from pathlib import Path

for candidate in (
    Path.cwd() / 'answer',
    Path.cwd() / 'quick_start' / 'cann_basics' / 'answer',
    Path.cwd() / 'cann-learning-hub' / 'quick_start' / 'cann_basics' / 'answer',
):
    if candidate.exists():
        sys.path.insert(0, str(candidate.resolve()))
        break
else:
    raise FileNotFoundError('Cannot find quick_start/cann_basics/answer')
from grade_02 import grade
grade(globals())
```

### 参考资料

- [Ascend C 算子开发教程 - CANN 架构与昇腾 NPU 原理](https://gitcode.com/cann/cann-learning-hub/blob/master/tutorials/ascendc_operator_development/01_basic_overview/01.03_cann_arch_ascend_npu_principle.ipynb)
- [昇腾社区 - CANN 文档](https://hiascend.com/document)

# ==========================================
## 📝 练习与验证

> 📌 原 Notebook 中的练习、编译命令和校验代码已按原顺序保留在上文。需要 CANN 运行时、Ascend NPU 或 CANNLab 环境的单元，执行前请先核对版本和设备条件。
