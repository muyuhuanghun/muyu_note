---
source_repo: cann-learning-hub
source_path: quick_start/cann_basics/03_what_is_cann.ipynb
source_commit: 1bf85454ed7c41e184a96fb51d109b6bb83b7c0d
note_kind: notebook_to_markdown
---

# 什么是 CANN —— 昇腾 NPU 的软件大脑

> 📚 上游 Notebook：[quick_start/cann_basics/03_what_is_cann.ipynb](https://gitcode.com/cann/cann-learning-hub/blob/master/quick_start/cann_basics/03_what_is_cann.ipynb)
> 🧪 整理方式：保留 Markdown 与代码单元；省略 Jupyter 执行输出，避免把一次性环境结果误当成可复现结论。

## 🧭 学习目标

- 先读懂概念，再运行代码片段验证关键结论；
- 把本节内容接入后续 CANN / Ascend NPU 实践。

# ==========================================
## 📖 课程内容

上一章我们拆开了 NPU 硬件，看到它有几十上百个 AI Core，算力惊人。但问题来了—— **你写的 PyTorch 代码，NPU 看不懂，也跑不了。** NPU 只认识它自己的指令，而你的代码是 Python 或者其他高级语言写的。这就像买了一台挖掘机，但没有驾驶员，挖掘机再强也只能原地吃灰。

CANN，就是那个让 NPU"活起来"的软件大脑。

---

### 1. 从 NPU 到 CANN：硬件需要软件才能跑

#### 1.1 NPU 能算，但不会"听"你说话

回顾一下上一章的结论：

- NPU 有大量 AI Core，每个 AI Core 有 Cube（矩阵）、Vector（向量）计算单元
- NPU 擅长大规模并行计算，算力远超 CPU
- 但 NPU**只认识底层硬件指令**，不理解 Python、不理解 PyTorch、不理解你定义的模型


#### 1.2 CANN = 翻译官 + 调度员 + 工具箱

**CANN**（Compute Architecture for Neural Networks，神经网络计算架构）就是华为为昇腾 NPU 打造的完整软件栈，它解决的核心问题就是：

<table style="text-align: left; margin-left: 0;">
<tr>
<th style="text-align: left;">角色</th>
<th style="text-align: left;">解决什么问题</th>
</tr>
<tr>
<td style="text-align: left;">翻译官</td>
<td style="text-align: left;">把 PyTorch/MindSpore 的算子调用翻译成 NPU 能执行的指令</td>
</tr>
<tr>
<td style="text-align: left;">调度员</td>
<td style="text-align: left;">优化计算顺序、融合算子、分配内存、调度多核并行</td>
</tr>
<tr>
<td style="text-align: left;">工具箱</td>
<td style="text-align: left;">提供大量预置算子、通信库、调试工具</td>
</tr>
</table>

没有 CANN，NPU 就是废铁；有了 CANN，NPU 才能跑你的 AI 模型。

> 一句话总结：**CANN 是连接上层 AI 框架与底层 NPU 硬件的桥梁，让开发者写的代码能在昇腾 NPU 上高效运行。**

---
#### 1.3 昇腾软硬件平台全栈一览

在深入 CANN 之前，先从全局视角看昇腾软硬件平台的全栈全场景布局：

<img src="../../../CANN-assets-20260813/quick_start/cann_basics/images/ascend_all.png"  alt="昇腾软硬件平台全栈全场景" />

从上到下：

- **应用层**：大模型、推荐搜索、计算机视觉等 AI 应用
- **框架层**：PyTorch、MindSpore 等主流 AI 框架
- **CANN**：位于框架与硬件之间，是昇腾 AI 处理器的核心软件栈，提供算子库、图优化、编译器、运行时等能力
- **硬件层**：昇腾 910B（训练）、310P（推理）等 AI 处理器

可以看到，**CANN 是昇腾全栈中承上启下的关键枢纽**——对上适配 AI 框架，对下驱动 NPU 硬件，内部提供完整的计算优化与执行能力。

---

### 2. CANN 是什么：一张架构图看全貌

CANN 采用**分层解耦**的设计，从上到下分为多个层次，每一层各司其职：

<img src="../../../CANN-assets-20260813/quick_start/cann_basics/images/cann_software_architecture.png"  alt="CANN软件架构" />

从上往下看，各层的职责一目了然：

<table style="text-align: left; margin-left: 0;">
<tr>
<th style="text-align: left;">层次</th>
<th style="text-align: left;">组件</th>
<th style="text-align: left;">一句话职责</th>
</tr>
<tr>
<td style="text-align: left;">框架适配层</td>
<td style="text-align: left;">torch_npu 等</td>
<td style="text-align: left;">让 PyTorch 代码一行改动就能跑在 NPU 上</td>
</tr>
<tr>
<td style="text-align: left;">算子库</td>
<td style="text-align: left;">ops-math / ops-nn / ops-cv / ops-transformer 等</td>
<td style="text-align: left;">提供海量预置算子，覆盖主流 AI 场景</td>
</tr>
<tr>
<td style="text-align: left;">通信库</td>
<td style="text-align: left;">HCCL / HIXL</td>
<td style="text-align: left;">多卡分布式训练/推理的通信保障</td>
</tr>
<tr>
<td style="text-align: left;">图引擎</td>
<td style="text-align: left;">GE</td>
<td style="text-align: left;">整网图优化（融合、内存、流水），最大化性能</td>
</tr>
<tr>
<td style="text-align: left;">领域加速库</td>
<td style="text-align: left;">FFT / BLAS 等</td>
<td style="text-align: left;">特定领域的算子+算法组合，提供极致加速</td>
</tr>
<tr>
<td style="text-align: left;">编程语言</td>
<td style="text-align: left;">Ascend C / PyPTO 等</td>
<td style="text-align: left;">算子编程语言，开发算子</td>
</tr>
<tr>
<td style="text-align: left;">编译器</td>
<td style="text-align: left;">毕昇 Bisheng</td>
<td style="text-align: left;">把算子源码编译成 NPU 可执行指令</td>
</tr>
<tr>
<td style="text-align: left;">运行时</td>
<td style="text-align: left;">Runtime</td>
<td style="text-align: left;">管理 NPU 设备、内存、任务调度</td>
</tr>
<tr>
<td style="text-align: left;">驱动</td>
<td style="text-align: left;">Driver</td>
<td style="text-align: left;">与 NPU 硬件直接交互的最底层软件</td>
</tr>
</table>

接下来，我们逐层拆解，看看每个组件具体干什么。

---

### 3. CANN 各组件一览

#### 3.1 框架适配层 —— 让框架代码跑在 NPU 上

你用 PyTorch 写的代码默认跑在 CPU 或 GPU 上。框架适配层的作用就是：**让这些代码几乎不用改就能跑在昇腾 NPU 上。**

<table style="text-align: left; margin-left: 0;">
<tr>
<th style="text-align: left;">框架</th>
<th style="text-align: left;">适配组件</th>
<th style="text-align: left;">怎么用</th>
</tr>
<tr>
<td style="text-align: left;">PyTorch</td>
<td style="text-align: left;">torch_npu</td>
<td style="text-align: left;">`import torch_npu`，然后把 `.cuda()` 改成 `.npu()`</td>
</tr>
<tr>
<td style="text-align: left;">MindSpore</td>
<td style="text-align: left;">MindSpore 昇腾版</td>
<td style="text-align: left;">原生支持，无需额外适配</td>
</tr>
</table>

> 类比：框架适配层就像一个**万能转接头**——你的电器是国标插头，墙上的插座是昇腾接口，转接头一插，就能用了。

核心原理：torch_npu 注册 `npu` 为 PyTorch 后端设备，将 PyTorch 的 `aten` 算子调用映射到 CANN 内置算子，内存和流管理通过 ACL 实现。

##### 体验框架适配：一行代码切换 NPU

下面我们亲手体验 torch_npu 的"一行代码切换"：

```python
import torch
import torch_npu

# 创建一个 CPU 上的张量
x_cpu = torch.tensor([1.0, 2.0, 3.0])
print(f"设备: {x_cpu.device}")

# 一行代码搬到 NPU
x_npu = x_cpu.npu()
print(f"设备: {x_npu.device}")

# 在 NPU 上执行运算，结果自动留在 NPU
y_npu = x_npu * 2 + 1
print(f"结果: {y_npu.cpu().tolist()}")
```

`.npu()` 一调用，数据就从 Host 内存搬到了 Device 内存，后续运算自动在 NPU 上执行——这就是框架适配层的威力。

#### 3.2 算子库 —— AI 计算的"标准件仓库"

算子库是 CANN 预置的高性能算子集合，分为四个子库，覆盖从基础数学到前沿 Transformer 的全场景：

<img src="../../../CANN-assets-20260813/quick_start/cann_basics/images/ops_math.jpg"  alt="数学库ops-math" />

**数学库 ops-math**：提供基础数学运算与张量操作能力，如 Add、Mul、MatMul、ReduceSum 等。它是所有上层算子的"地基"，专为昇腾 NPU 优化适配，能为人工智能及通用数值计算场景提供高效、稳定的硬件加速计算支持。

<img src="../../../CANN-assets-20260813/quick_start/cann_basics/images/ops_nn.jpg"  alt="神经网络库ops-nn" />

**神经网络库 ops-nn**：提供卷积、池化、激活、归一化等神经网络计算常用算子，如 Conv2D、MaxPool、ReLU、BatchNorm、Softmax、LayerNorm 等。专为昇腾 NPU 优化适配，能为深度学习模型训练、推理等神经网络应用场景提供高效、稳定的硬件加速计算支持。


<img src="../../../CANN-assets-20260813/quick_start/cann_basics/images/ops_cv.jpg"  alt="计算机视觉库ops-cv" />

**计算机视觉库 ops-cv**：提供深度学习计算机视觉任务的核心操作能力，如 NMS、ROIAlign、Resize 等。专为昇腾 NPU 优化适配，能为智能驾驶、视频安防、医学影像分割等计算机视觉场景提供高效、稳定的硬件加速计算支持。

<img src="../../../CANN-assets-20260813/quick_start/cann_basics/images/ops_transformer.jpg"  alt="Transformer库ops-transformer" />

**Transformer库 ops-transformer**：提供 Transformer 相关常用算子，如 FlashAttention、KVCache 等。专为昇腾 NPU 优化适配，能为自然语言处理、多模态学习等 Transformer 相关场景提供高效、稳定的硬件加速计算支持。

> 详见：[昇腾社区 - CANN 算子库](https://www.hiascend.com/cann/aol)

此外，当内置算子不够用时，开发者还可以用 **[Ascend C](https://www.hiascend.com/cann/ascend-c)** 开发自定义算子，就像自己定制特殊构件。

#### 3.3 通信库 —— 多卡协同

当模型太大一张卡放不下，或者训练数据量太大需要多卡并行时，多张 NPU 之间就需要频繁交换数据。通信库就是干这个的。

**集合通信库 HCCL**（Huawei Collective Communication Library）类似 NVIDIA 的 NCCL，为计算集群提供高性能、高可靠的集合通信方案：

<img src="../../../CANN-assets-20260813/quick_start/cann_basics/images/hccl.png"  alt="集合通信库HCCL" />

<table style="text-align: left; margin-left: 0;">
<tr>
<th style="text-align: left;">操作</th>
<th style="text-align: left;">说明</th>
<th style="text-align: left;">类比</th>
</tr>
<tr>
<td style="text-align: left;">AllReduce</td>
<td style="text-align: left;">所有卡求和后广播给每张卡</td>
<td style="text-align: left;">4个人各算一部分，汇总后每人拿一份总结果</td>
</tr>
<tr>
<td style="text-align: left;">AllGather</td>
<td style="text-align: left;">所有卡数据拼接在一起</td>
<td style="text-align: left;">4个人各拿一块拼图，拼好后每人拿一份完整图</td>
</tr>
<tr>
<td style="text-align: left;">Broadcast</td>
<td style="text-align: left;">一卡数据广播到所有卡</td>
<td style="text-align: left;">老板发通知，所有员工都收到</td>
</tr>
<tr>
<td style="text-align: left;">ReduceScatter</td>
<td style="text-align: left;">求和后按卡分发不同部分</td>
<td style="text-align: left;">4个人汇总后，每人只拿自己负责的那部分</td>
</tr>
</table>

**单边通信库 HIXL**（Huawei Xfer Library）提供灵活、高效的点对点数据传输能力。它的杀手锏是**单边零拷贝**——传输数据时不需要远端参与，就像你往别人信箱里塞信，不需要对方在家等着接收。这为构建"通信与计算重叠"的调度机制提供了核心技术能力。

> 类比：HCCL 像开**全员会议**（所有人同时参与），HIXL 像发**微信消息**（点对点，对方不用在线也能收到）。

> 详见：[昇腾社区 - HCCL 通信库](https://www.hiascend.com/cann/hccl)

#### 3.4 图引擎 GE —— 全局优化的大脑

<img src="../../../CANN-assets-20260813/quick_start/cann_basics/images/ge_graph_engine.jpg"  alt="GE图引擎" />

图引擎（Graph Engine）是 CANN 生态中面向昇腾系列芯片的高性能图模式实现，支撑模型的开箱即用以及性能加速。它包含三大部分：

**图编译**：提供统一的图开发接口，聚焦于图编译优化技术，核心能力包括：

<table style="text-align: left; margin-left: 0;">
<tr>
<th style="text-align: left;">优化技术</th>
<th style="text-align: left;">说明</th>
<th style="text-align: left;">类比</th>
</tr>
<tr>
<td style="text-align: left;">图融合 / 算子融合</td>
<td style="text-align: left;">将多个小算子合并为一个大算子，减少访存开销</td>
<td style="text-align: left;">把"搬砖→砌墙→刷漆"三个工序合并为一步完成</td>
</tr>
<tr>
<td style="text-align: left;">自动融合</td>
<td style="text-align: left;">自动识别可融合的算子组合</td>
<td style="text-align: left;">智能发现哪些工序可以合并</td>
</tr>
<tr>
<td style="text-align: left;">极致内存</td>
<td style="text-align: left;">复用中间 tensor 内存，降低峰值显存</td>
<td style="text-align: left;">工位共享，一个工位干完活立刻让给下一个工序</td>
</tr>
<tr>
<td style="text-align: left;">自动流水</td>
<td style="text-align: left;">自动安排算子执行流水线</td>
<td style="text-align: left;">生产线自动排班，让每个工位都不闲着</td>
</tr>
</table>

**图执行**：聚焦于图的调度执行性能优化，提供**计算图执行下沉**技术——把整个计算图一次性"下沉"到 NPU 侧执行，而不是逐个算子下发，减少 Host 与 Device 之间的交互开销，提升计算性能。

> 类比：不下沉 = 每道工序都要打电话请示老板才能开始；下沉 = 老板一次性把整条生产线的指令都交给车间主任，车间自己按顺序执行，效率大幅提升。

**metadef 元数据**：作为 CANN 图和算子的基础数据结构，支撑 CANN 分包解耦、分层开放的基础能力。它定义了算子的输入输出描述、属性等信息，是图编译和图执行的"通用语言"。

> 详见：[昇腾社区 - GE 图引擎](https://www.hiascend.com/cann/graph-engine)

#### 3.5 领域加速库 —— 特定场景的"专业施工队"

领域加速库是针对特定领域或场景的**算子和算法的结合**。根据场景需要，每个加速库可提供不同形式的功能：包括但不限于本领域内的补充算子、特定算法或机制、特定辅助类工具等。

<img src="../../../CANN-assets-20260813/quick_start/cann_basics/images/domain_fft.jpg"  alt="FFT加速库" />

**FFT 加速库**：面向开发者开放接口以实现 FFT（快速傅里叶变换）时域到频域的转换，为信号处理、频谱分析等场景提供高效加速。

<img src="../../../CANN-assets-20260813/quick_start/cann_basics/images/domain_blas.jpg"  alt="Blas库" />

**BLAS 库**：依照 BLAS（Basic Linear Algebra Subprograms，基本线性代数子系统库）标准定义，为开发者提供三个层级的接口：

<table style="text-align: left; margin-left: 0;">
<tr>
<th style="text-align: left;">层级</th>
<th style="text-align: left;">运算类型</th>
<th style="text-align: left;">示例</th>
</tr>
<tr>
<td style="text-align: left;">Level 1</td>
<td style="text-align: left;">向量与向量运算</td>
<td style="text-align: left;">向量内积、向量加法</td>
</tr>
<tr>
<td style="text-align: left;">Level 2</td>
<td style="text-align: left;">向量与矩阵运算</td>
<td style="text-align: left;">矩阵-向量乘法</td>
</tr>
<tr>
<td style="text-align: left;">Level 3</td>
<td style="text-align: left;">矩阵与矩阵运算</td>
<td style="text-align: left;">矩阵乘法（GEMM）</td>
</tr>
</table>

> 类比：领域加速库就像**专业施工队**——算子库提供的是通用"砖头水泥"，而领域加速库是自带专用设备和工艺的专业队伍。你需要做傅里叶变换（FFT库）或矩阵运算（BLAS库）时，直接请专业施工队来做，比自己用通用算子拼凑又快又好。

#### 3.6 编程语言 Ascend C —— 自定义算子的开发利器

<img src="../../../CANN-assets-20260813/quick_start/cann_basics/images/ascend_c.png"  alt="Ascend C" />

当 CANN 内置算子不满足需求时（比如遇到了不支持的算子，或者想自己写一个更快的版本），就需要用 **Ascend C**开发自定义算子。

Ascend C 是 CANN 针对算子开发场景推出的编程语言，核心特点：

<table style="text-align: left; margin-left: 0;">
<tr>
<th style="text-align: left;">特点</th>
<th style="text-align: left;">说明</th>
<th style="text-align: left;">类比</th>
</tr>
<tr>
<td style="text-align: left;">C/C++ 标准规范</td>
<td style="text-align: left;">语法和 C/C++ 一致，学习成本低</td>
<td style="text-align: left;">用你熟悉的语言写，不用学新语法</td>
</tr>
<tr>
<td style="text-align: left;">多层接口抽象</td>
<td style="text-align: left;">从底层指令级到高层算法级，灵活选择</td>
<td style="text-align: left;">既可以用扳手（基础API），也可以用电动工具（高阶API）</td>
</tr>
<tr>
<td style="text-align: left;">自动并行计算</td>
<td style="text-align: left;">自动安排多核并行，开发者不用手动调度</td>
<td style="text-align: left;">你只管写"做什么"，编译器帮你安排"谁来做"</td>
</tr>
<tr>
<td style="text-align: left;">孪生调试</td>
<td style="text-align: left;">CPU 侧模拟调试 + NPU 侧真实执行，双管齐下</td>
<td style="text-align: left;">先在沙盘上推演，再上真战场</td>
</tr>
</table>

Ascend C 提供多层级 API 体系：

- **基础 API**：基于 Tensor 进行编程的 C++ 类库 API，实现单指令级抽象，为底层算子开发提供灵活控制能力
- **高阶 API**：封装单核公共算法，涵盖常见计算算法（如卷积、矩阵运算等），显著降低复杂算法开发门槛
- **算子模板库**：基于模板提供算子完整实现参考，简化 Tiling（切分算法）开发

> 详见：[昇腾社区 - Ascend C](https://www.hiascend.com/cann/ascend-c)

#### 3.7 毕昇编译器 —— 从源码到 NPU 指令的"翻译机"

<img src="../../../CANN-assets-20260813/quick_start/cann_basics/images/bisheng_compiler.png"  alt="毕昇编译器" />

毕昇编译器（Bisheng）是连接 AI 开发者与昇腾硬件的关键纽带，负责把 Ascend C 算子源码编译成 NPU 可执行的指令。核心能力：

<table style="text-align: left; margin-left: 0;">
<tr>
<th style="text-align: left;">能力</th>
<th style="text-align: left;">说明</th>
</tr>
<tr>
<td style="text-align: left;">Host-Device 异构编程编译</td>
<td style="text-align: left;">同时编译 Host 侧代码（Tiling 函数、算子原型注册）和 Kernel 侧代码（NPU 执行指令）</td>
</tr>
<tr>
<td style="text-align: left;">微架构精准编译优化</td>
<td style="text-align: left;">针对昇腾芯片的微架构特性做精准优化，释放芯片极致性能</td>
</tr>
<tr>
<td style="text-align: left;">完备二进制调试信息</td>
<td style="text-align: left;">提供调试信息和工具链，支撑开发者自主调试调优</td>
</tr>
</table>

> 类比：毕昇编译器就像一个**高级翻译官**——不仅翻译语言，还会根据对方的文化习惯（微架构特性）调整表达方式，让翻译效果（执行性能）最佳。

> 详见：[昇腾社区 - 毕昇编译器](https://www.hiascend.com/cann/bisheng)

#### 3.8 运行时 Runtime —— NPU 的"管家"

<img src="../../../CANN-assets-20260813/quick_start/cann_basics/images/acl_runtime.jpg"  alt="Runtime" />

运行时（Runtime）是 CANN 软件栈中负责驱动硬件执行与管理 AI 计算任务的核心组件，是连接应用与 NPU 硬件的桥梁。它提供统一的运行环境与 API，使得上层应用和框架能够高效利用 Ascend NPU 计算资源。

核心管理能力：

<table style="text-align: left; margin-left: 0;">
<tr>
<th style="text-align: left;">管理对象</th>
<th style="text-align: left;">说明</th>
<th style="text-align: left;">类比</th>
</tr>
<tr>
<td style="text-align: left;">Device 管理</td>
<td style="text-align: left;">计算设备的设置、重置、查询和配置</td>
<td style="text-align: left;">选择哪台机器干活</td>
</tr>
<tr>
<td style="text-align: left;">Memory 管理</td>
<td style="text-align: left;">设备内存和 Host 内存的申请、释放、拷贝</td>
<td style="text-align: left;">给数据分配工作台和仓库</td>
</tr>
<tr>
<td style="text-align: left;">Context 管理</td>
<td style="text-align: left;">计算设备的执行上下文环境</td>
<td style="text-align: left;">给每个任务准备一个工作环境</td>
</tr>
<tr>
<td style="text-align: left;">Stream 管理</td>
<td style="text-align: left;">Device 提供的逻辑任务执行队列</td>
<td style="text-align: left;">排队系统，任务按队列顺序执行</td>
</tr>
<tr>
<td style="text-align: left;">Kernel 管理</td>
<td style="text-align: left;">AI Core、AI CPU 等算子注册管理和 KernelLaunch</td>
<td style="text-align: left;">登记有哪些工人可以干活，并派活给他们</td>
</tr>
<tr>
<td style="text-align: left;">Event 管理</td>
<td style="text-align: left;">设备内 Stream 间任务同步的事件</td>
<td style="text-align: left;">一个工序完成后发信号，通知下一个工序可以开始</td>
</tr>
<tr>
<td style="text-align: left;">Notify 管理</td>
<td style="text-align: left;">跨设备间任务同步的通知</td>
<td style="text-align: left;">跨车间的协调信号</td>
</tr>
<tr>
<td style="text-align: left;">ACL Graph</td>
<td style="text-align: left;">任务捕获或编排方式构建"运行时图"，整体下发节省 Host 调度耗时</td>
<td style="text-align: left;">把一整套工序打包成一个"工艺包"一次性下发</td>
</tr>
</table>


> 详见：[昇腾社区 - CANN Runtime](https://www.hiascend.com/cann/runtime)

#### 3.9 驱动 Driver —— 与硬件对话的"底层接口"

<img src="../../../CANN-assets-20260813/quick_start/cann_basics/images/driver.jpg"  alt="驱动" />

驱动是 CANN 软件栈与 NPU 硬件交互的基础设施，位于整个软件栈最底层。三大核心能力：

<table style="text-align: left; margin-left: 0;">
<tr>
<th style="text-align: left;">能力</th>
<th style="text-align: left;">说明</th>
</tr>
<tr>
<td style="text-align: left;">统一内存管理</td>
<td style="text-align: left;">纳管 HBM、DDR 等多元内存资源，为 Host/Device、多 Device 间提供统一内存管理接口，屏蔽异构内存差异，简化编程</td>
</tr>
<tr>
<td style="text-align: left;">HDC/P2P 通信</td>
<td style="text-align: left;">提供 Host↔Device、Device↔Device 低延迟通信通路与高带宽共享访问，抽象统一接口屏蔽硬件通路差异，减少冗余拷贝，支撑多卡训练与分布式推理</td>
</tr>
<tr>
<td style="text-align: left;">硬件调度使能</td>
<td style="text-align: left;">深度使能硬件调度器（TS/STARS），精准下发任务、动态分配资源、快速回传结果</td>
</tr>
<tr>
<td style="text-align: left;">设备全生命周期管理</td>
<td style="text-align: left;">初始化配置→运行监控→参数调优→故障检测上报，形成完整管控闭环；内置 npu-smi、hccn-tool 等轻量工具；提供 DCMI 北向接口支持二次开发</td>
</tr>
</table>

> 详见：[昇腾社区 - CANN Driver](https://www.hiascend.com/cann/driver)

### 4. 一行代码的完整旅程

理解了各组件的职责，现在用一个具体例子把它们串起来。当你写下这行代码时：

```python
output = torch.matmul(tensor_a.npu(), tensor_b.npu())
```

数据经历了以下完整旅程：

<table style="text-align: left; margin-left: 0;">
<tr>
<th style="text-align: left;">步骤</th>
<th style="text-align: left;">组件</th>
<th style="text-align: left;">做了什么</th>
<th style="text-align: left;">类比</th>
</tr>
<tr>
<td style="text-align: left;">1</td>
<td style="text-align: left;">torch_npu</td>
<td style="text-align: left;">.npu() 把数据从 Host 内存搬到 Device 内存</td>
<td style="text-align: left;">客户在 App 上下单</td>
</tr>
<tr>
<td style="text-align: left;">2</td>
<td style="text-align: left;">torch_npu</td>
<td style="text-align: left;">把 torch.matmul 映射到 CANN 的 MatMul 算子</td>
<td style="text-align: left;">前台把订单转成内部工单</td>
</tr>
<tr>
<td style="text-align: left;">3</td>
<td style="text-align: left;">GE 图引擎</td>
<td style="text-align: left;">将 MatMul 算子加入计算图，做融合/内存/流水优化</td>
<td style="text-align: left;">调度中心优化排班：合并工序、复用内存</td>
</tr>
<tr>
<td style="text-align: left;">4</td>
<td style="text-align: left;">毕昇编译器</td>
<td style="text-align: left;">将优化后的算子编译成 NPU 可执行的 Kernel 指令</td>
<td style="text-align: left;">厨房把菜谱翻译成具体操作步骤</td>
</tr>
<tr>
<td style="text-align: left;">5</td>
<td style="text-align: left;">Runtime</td>
<td style="text-align: left;">分配 Device 内存、创建 Stream、下发 Kernel</td>
<td style="text-align: left;">管家分配灶台、安排厨师排队</td>
</tr>
<tr>
<td style="text-align: left;">6</td>
<td style="text-align: left;">Driver</td>
<td style="text-align: left;">通过驱动把指令下发到 NPU 硬件</td>
<td style="text-align: left;">灶台通电点火</td>
</tr>
<tr>
<td style="text-align: left;">7</td>
<td style="text-align: left;">AI Core</td>
<td style="text-align: left;">Cube 单元执行矩阵乘法，结果写回 Device 内存</td>
<td style="text-align: left;">厨师炒菜，菜放在出餐口</td>
</tr>
<tr>
<td style="text-align: left;">8</td>
<td style="text-align: left;">--</td>
<td style="text-align: left;">output 在 Device 内存中，后续操作继续在 NPU 上执行</td>
<td style="text-align: left;">菜做好等骑手取，下一单继续</td>
</tr>
</table>

整个过程从你写下 `tensor.npu()` 到结果出来，CANN 各组件各司其职、无缝衔接，你只需要写一行代码，剩下的全由 CANN 搞定。

#### 亲手走一遍这个旅程

下面我们用代码实际走一遍"一行代码的完整旅程"：

```python
import torch
import torch_npu

# ① 数据在 Host（CPU）上
tensor_a = torch.randn(2, 3)
tensor_b = torch.randn(3, 4)
print(f"① 数据在 Host: {tensor_a.device}, {tensor_b.device}")

# ② .npu() 把数据搬到 Device（NPU）
a_npu = tensor_a.npu()
b_npu = tensor_b.npu()
print(f"② 数据搬到 Device: {a_npu.device}, {b_npu.device}")

# ③~⑦ CANN 在幕后完成：算子映射 → GE优化 → 编译 → Runtime调度 → Driver下发 → AI Core执行
output = torch.matmul(a_npu, b_npu)

# ⑧ 结果在 Device 上
print(f"⑧ 结果在 Device: {output.device}, shape: {output.shape}")
print(f"   结果值:\n{output.cpu()}")
```

---

### 5. CANN 与 CUDA 的对照

如果你之前用过 NVIDIA GPU + CUDA，下表帮你快速建立对应关系：

<table style="text-align: left; margin-left: 0;">
<tr>
<th style="text-align: left;">维度</th>
<th style="text-align: left;">CANN（昇腾）</th>
<th style="text-align: left;">CUDA（NVIDIA）</th>
<th style="text-align: left;">说明</th>
</tr>
<tr>
<td style="text-align: left;">框架适配</td>
<td style="text-align: left;">torch_npu</td>
<td style="text-align: left;">torch.cuda</td>
<td style="text-align: left;">把框架调用适配到自家硬件</td>
</tr>
<tr>
<td style="text-align: left;">算子库</td>
<td style="text-align: left;">ops-math / ops-nn / ops-cv / ops-transformer</td>
<td style="text-align: left;">cuDNN / cuSPARSE</td>
<td style="text-align: left;">预置高性能算子</td>
</tr>
<tr>
<td style="text-align: left;">通信库</td>
<td style="text-align: left;">HCCL + HIXL</td>
<td style="text-align: left;">NCCL</td>
<td style="text-align: left;">多卡分布式通信</td>
</tr>
<tr>
<td style="text-align: left;">图引擎</td>
<td style="text-align: left;">GE</td>
<td style="text-align: left;">TensorRT</td>
<td style="text-align: left;">整网图优化与编译</td>
</tr>
<tr>
<td style="text-align: left;">领域加速库</td>
<td style="text-align: left;">FFT / BLAS 等</td>
<td style="text-align: left;">cuFFT / cuBLAS</td>
<td style="text-align: left;">特定领域极致加速</td>
</tr>
<tr>
<td style="text-align: left;">编程语言</td>
<td style="text-align: left;">Ascend C</td>
<td style="text-align: left;">CUDA C++</td>
<td style="text-align: left;">自定义算子开发语言</td>
</tr>
<tr>
<td style="text-align: left;">编译器</td>
<td style="text-align: left;">毕昇 Bisheng</td>
<td style="text-align: left;">NVCC</td>
<td style="text-align: left;">源码编译为硬件指令</td>
</tr>
<tr>
<td style="text-align: left;">运行时</td>
<td style="text-align: left;">Runtime</td>
<td style="text-align: left;">CUDA Runtime</td>
<td style="text-align: left;">设备/内存/任务管理</td>
</tr>
<tr>
<td style="text-align: left;">驱动</td>
<td style="text-align: left;">Driver</td>
<td style="text-align: left;">NVIDIA Driver</td>
<td style="text-align: left;">最底层硬件交互</td>
</tr>
<tr>
<td style="text-align: left;">Profiling</td>
<td style="text-align: left;">msprof / MindStudio</td>
<td style="text-align: left;">Nsight</td>
<td style="text-align: left;">性能分析工具</td>
</tr>
</table>

> 可以看到，CANN 和 CUDA 的软件栈结构几乎一一对应——**概念是相通的，只是名字不同**。如果你熟悉 CUDA，学 CANN 会非常快。

---

### 6. CANN 环境验证

CANN 环境部署完成后，可以通过工具或接口验证环境是否正常。

#### 6.1 查看 CANN 版本信息

```bash
!cat $ASCEND_HOME_PATH/aarch64-linux/ascend_toolkit_install.info
```

#### 6.2 验证 CANN 运行时（ACL）

```python
import acl

# 获取芯片型号
soc_name = acl.get_soc_name()
print(f"芯片型号: {soc_name}")

# 获取 Device 数量
device_count, ret = acl.rt.get_device_count()
if ret != 0:
    raise RuntimeError(f"获取Device数量失败，错误码：{ret}")

print(f"Device 数量: {device_count}")
```

#### 6.3 验证 torch_npu 框架适配层

```python
import torch
import torch_npu

print(f"torch_npu 版本: {torch_npu.__version__}")
print(f"PyTorch 版本: {torch.__version__}")
print(f"NPU 可用: {torch.npu.is_available()}")
print(f"NPU 名称: {torch.npu.get_device_name(0)}")
```

---

### 小结

<table style="text-align: left; margin-left: 0;">
<tr>
<th style="text-align: left;">概念</th>
<th style="text-align: left;">一句话</th>
</tr>
<tr>
<td style="text-align: left;">CANN</td>
<td style="text-align: left;">昇腾 NPU 的完整软件栈，连接上层框架与底层硬件</td>
</tr>
<tr>
<td style="text-align: left;">框架适配层</td>
<td style="text-align: left;">让 PyTorch 代码一行改动就能跑在 NPU 上</td>
</tr>
<tr>
<td style="text-align: left;">算子库</td>
<td style="text-align: left;">多个算子库（math/nn/cv/transformer等）提供海量预置算子</td>
</tr>
<tr>
<td style="text-align: left;">通信库</td>
<td style="text-align: left;">HCCL 集合通信 + HIXL 单边通信，支撑多卡协同</td>
</tr>
<tr>
<td style="text-align: left;">图引擎 GE</td>
<td style="text-align: left;">图编译（融合/内存/流水）+ 图执行（计算下沉）+ metadef</td>
</tr>
<tr>
<td style="text-align: left;">领域加速库</td>
<td style="text-align: left;">FFT/BLAS 等，特定领域的算子+算法组合</td>
</tr>
<tr>
<td style="text-align: left;">Ascend C</td>
<td style="text-align: left;">C/C++ 标准规范的自定义算子开发语言</td>
</tr>
<tr>
<td style="text-align: left;">毕昇编译器</td>
<td style="text-align: left;">Host-Device 异构编译，微架构精准优化</td>
</tr>
<tr>
<td style="text-align: left;">Runtime</td>
<td style="text-align: left;">设备/内存/流/事件管理，NPU 的"管家"</td>
</tr>
<tr>
<td style="text-align: left;">Driver</td>
<td style="text-align: left;">与 NPU 硬件交互的最底层软件</td>
</tr>
</table>


---

### 课后练习

请根据本节课程学习内容完成以下题目进行自测，在每题下方的代码框中输入选项字母后运行。

**第1题**（单选题）CANN的全称是什么？

- A. Compute Architecture for Neural Networks
- B. Cloud Architecture for Neural Networks
- C. Compute Application for Neural Networks
- D. Core Architecture for Natural Networks

```python
q1 = ''  # 填入你的选项，如 'B'，修改后务必运行本单元格（Shift+Enter）
print(f'第{1}题答案已记录：{q1}' if q1 else '⚠️ 请填入答案并运行本单元格')
```

**第2题**（单选题）CANN在昇腾全栈中的定位是？

- A. 最上层应用
- B. 最底层硬件
- C. 承上启下的关键枢纽，连接框架与硬件
- D. 独立的第三方库

```python
q2 = ''  # 填入你的选项，如 'B'，修改后务必运行本单元格（Shift+Enter）
print(f'第{2}题答案已记录：{q2}' if q2 else '⚠️ 请填入答案并运行本单元格')
```

**第3题**（单选题）框架适配层中，让PyTorch代码跑在NPU上的组件是？

- A. torch.cuda
- B. torch_npu
- C. MindSpore
- D. TF Adapter

```python
q3 = ''  # 填入你的选项，如 'B'，修改后务必运行本单元格（Shift+Enter）
print(f'第{3}题答案已记录：{q3}' if q3 else '⚠️ 请填入答案并运行本单元格')
```

**第4题**（单选题）CANN算子库中，提供卷积、池化、激活等神经网络算子的子库是？

- A. ops-math
- B. ops-nn
- C. ops-cv
- D. ops-transformer

```python
q4 = ''  # 填入你的选项，如 'B'，修改后务必运行本单元格（Shift+Enter）
print(f'第{4}题答案已记录：{q4}' if q4 else '⚠️ 请填入答案并运行本单元格')
```

**第5题**（单选题）CANN算子库中，提供FlashAttention、KVCache等算子的子库是？

- A. ops-math
- B. ops-nn
- C. ops-cv
- D. ops-transformer

```python
q5 = ''  # 填入你的选项，如 'B'，修改后务必运行本单元格（Shift+Enter）
print(f'第{5}题答案已记录：{q5}' if q5 else '⚠️ 请填入答案并运行本单元格')
```

**第6题**（单选题）集合通信库HCCL中，AllReduce操作的含义是？

- A. 一卡数据广播到所有卡
- B. 所有卡数据拼接在一起
- C. 所有卡求和后广播给每张卡
- D. 求和后按卡分发不同部分

```python
q6 = ''  # 填入你的选项，如 'B'，修改后务必运行本单元格（Shift+Enter）
print(f'第{6}题答案已记录：{q6}' if q6 else '⚠️ 请填入答案并运行本单元格')
```

**第7题**（单选题）图引擎GE中，"计算图执行下沉"技术的核心思想是？

- A. 逐个算子下发执行
- B. 把整个计算图一次性下沉到NPU侧执行
- C. 只在Host侧执行
- D. 将算子拆分为更小的单元

```python
q7 = ''  # 填入你的选项，如 'B'，修改后务必运行本单元格（Shift+Enter）
print(f'第{7}题答案已记录：{q7}' if q7 else '⚠️ 请填入答案并运行本单元格')
```

**第8题**（单选题）Ascend C编程语言的核心特点不包括？

- A. C/C++标准规范
- B. 多层接口抽象
- C. 自动并行计算
- D. 仅支持Python语法

```python
q8 = ''  # 填入你的选项，如 'B'，修改后务必运行本单元格（Shift+Enter）
print(f'第{8}题答案已记录：{q8}' if q8 else '⚠️ 请填入答案并运行本单元格')
```

**第9题**（单选题）在"一行代码的完整旅程"中，毕昇编译器负责的步骤是？

- A. 把数据从Host搬到Device
- B. 将优化后的算子编译成NPU可执行的Kernel指令
- C. 分配Device内存
- D. 通过驱动把指令下发到NPU

```python
q9 = ''  # 填入你的选项，如 'B'，修改后务必运行本单元格（Shift+Enter）
print(f'第{9}题答案已记录：{q9}' if q9 else '⚠️ 请填入答案并运行本单元格')
```

**第10题**（单选题）CANN与CUDA的对照中，CANN的图引擎GE对应CUDA中的哪个组件？

- A. NCCL
- B. cuDNN
- C. TensorRT
- D. NVCC

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
from grade_03 import grade
grade(globals())
```

### 参考资料

- [昇腾社区 - CANN 主页](https://www.hiascend.com/cann)
- [昇腾社区 - CANN 算子库（AOL）](https://www.hiascend.com/cann/aol)
- [昇腾社区 - Ascend C](https://www.hiascend.com/cann/ascend-c)
- [昇腾社区 - 毕昇编译器](https://www.hiascend.com/cann/bisheng)
- [昇腾社区 - CANN Runtime](https://www.hiascend.com/cann/runtime)
- [昇腾社区 - CANN Driver](https://www.hiascend.com/cann/driver)
- [昇腾社区 - HCCL 通信库](https://www.hiascend.com/cann/hccl)
- [昇腾社区 - GE 图引擎](https://www.hiascend.com/cann/ge)
- [昇腾社区 - PyTorch 框架适配](https://www.hiascend.com/cn/developer/software/ai-frameworks/pytorch)
- [Ascend C 算子开发教程 - CANN 架构与昇腾 NPU 原理](https://gitcode.com/cann/cann-learning-hub/blob/master/tutorials/ascendc_operator_development/01_basic_overview/01.03_cann_arch_ascend_npu_principle.ipynb)

# ==========================================
## 📝 练习与验证

> 📌 原 Notebook 中的练习、编译命令和校验代码已按原顺序保留在上文。需要 CANN 运行时、Ascend NPU 或 CANNLab 环境的单元，执行前请先核对版本和设备条件。
