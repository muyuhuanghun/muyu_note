---
source_repo: cann-learning-hub
source_path: reference_practice/pytorch_online_inference_operator_optimize/03_operator_develop.ipynb
source_commit: 1bf85454ed7c41e184a96fb51d109b6bb83b7c0d
note_kind: notebook_to_markdown
---

# AddCustomTemplate 算子开发

> 📚 上游 Notebook：[reference_practice/pytorch_online_inference_operator_optimize/03_operator_develop.ipynb](https://gitcode.com/cann/cann-learning-hub/blob/master/reference_practice/pytorch_online_inference_operator_optimize/03_operator_develop.ipynb)
> 🧪 整理方式：保留 Markdown 与代码单元；省略 Jupyter 执行输出，避免把一次性环境结果误当成可复现结论。

## 🧭 学习目标

- 先读懂概念，再运行代码片段验证关键结论；
- 把本节内容接入后续 CANN / Ascend NPU 实践。

# ==========================================
## 📖 课程内容

上一节我们通过Profiling找到了需要开发的算子Add以及它在框架中的调用位置，这一节来介绍如何开发一个自定义Add算子AddCustomTemplate。
我们将按照以下结构，介绍AddCustomTemplate的开发内容：
- 环境准备
- Tiling介绍
- Tiling设计思路介绍
- 泛化Tiling设计示例
- 课后实践 
---

### **1. 环境准备**
本文所有内容均存放于Sources文件夹。
在开始创建算子工程前，先要对jupyter环境进行初始化。以下代码完成了初始化并将环境中的变量导入jupyter环境，并完成代码目录的创建。保证能正常导入代码以及代码能编译运行。

```bash
!mkdir -p Sources/03

import os, subprocess
env = subprocess.check_output("bash -l -c 'source $ASCEND_TOOLKIT_HOME/set_env.sh && env'", shell=True, text=True)
for line in env.splitlines():
    if "=" in line: os.environ.__setitem__(*line.split("=", 1))
print("\n🎉 Environment initialization process completed successfully!")
```

--- 
### **2. Tiling介绍**
大多数情况下，Local Memory的存储，无法完全容纳算子的输入与输出的所有数据，需要每次搬运一部分输入数据进行计算然后搬出，再搬运下一部分输入数据进行计算，直到得到完整的最终结果，这个数据切分、分块计算的过程称之为**Tiling**。

➤ 每次搬运的那一部分数据块，叫做**Tiling块**  
➤ 根据算子中不同输入形状确定搬入基本块大小的相关算法，叫做**Tiling算法**（或Tiling策略）  
➤ 算子中实现Tiling算法的函数（一般定义在host侧的tiling头文件中），叫做**Tiling函数**（或Tiling Function）  
  

<img src="../../../../CANN-assets-20260813/reference_practice/pytorch_online_inference_operator_optimize/images/tiling.png" alt="tiling" width="700px">

---
### **3. Tiling设计思路**
受硬件架构约束，在对输入数据进行切分与调度时，通常需要遵循以下设计原则，以保障算子性能与执行正确性：

 ### **3.1 内存对齐原则**  
AI Core 的Unified Buffer存在物理层面的存储约束，要求其上的数据空间必须保持32字节对齐。
- 若输入数据长度不满足32字节对齐，需将其长度向**上对齐至32字节**，并以此作为总长度参与后续计算。
- 所有Tiling相关的计算逻辑，均应以**32**字节为最小粒度单位进行。 

 ### **3.2 访存优化原则**  
AI Core 与外部存储（Global Memory）间的数据交互会引入显著的性能开销，频繁的数据搬运极易成为性能瓶颈。
- 核心目标：充分利用 Unified Buffer 空间，通过增大单次搬运的数据块大小，最大限度减少数据搬运的总次数。 
 
 ### **3.3 多核均衡原则**  
昇腾 AI 处理器集成了多个 AI Core，为充分释放硬件算力，需进行合理的任务调度。
- 核心目标：均衡利用多核计算能力，将整体计算任务均匀地分配至各个 AI Core 上，避免出现算力闲置或负载不均的情况。

<img src="../../../../CANN-assets-20260813/reference_practice/pytorch_online_inference_operator_optimize/images/tiling_partition_schematic.png"  alt="tiling_partition_schematic" />

数据切分示意如上图所示，将长度为TOTAL_LENGTH的算子输入分配到多个核上进行计算，每个核上计算的数据长度为BLOCK_LENGTH。对于每个核的计算数据，基于Local Memory的大小进一步切分，切分数据块的个数为TILE_NUM，得到的每个数据块的长度为TILE_LENGTH。

根据每个核计算的数据量是否相同、核内每个数据块的数据量是否相同，切分策略可能会存在以下几种场景：
- 核间均分，核内均分：每个核处理的数据量相同，核内每个数据块的数据量相同。在此场景中，通过多核Tiling将数据均匀分配到各个核上执行，每个核上每次计算的数据长度相同。  

- 核间均分，核内不均分：每个核处理的数据量相同，核内各数据块的数据量不完全相同。此场景基于多核Tiling，核内数据不能切分为多个数据量相同且32字节对齐的数据块，需要通过尾块Tiling处理尾块数据的计算。  

- 核间不均分，核内均分：每个核处理的数据量不同，核内每个数据块的数据量相同。在此场景中，通过尾核Tiling的处理解决数据无法在各核间均匀分配的问题。  

- 核间不均分，核内不均分：每个核处理的数据量不同，核内各数据块的数据量不完全相同。该场景下需要同时考虑尾核&尾块，处理多核间及核内数据的合理切分。

#### **3.4 Tiling设计示例**

以形状为(1,660)的half类型算子输入数据，要分配到4个aicore上完成Add计算为例，我们来逐步完成Tiling设计。

##### **3.4.1 32字节对齐**
Add算子输入为`shape=(1,660)`、`dtype=half`的张量（`half`单元素占2B）。因硬件要求数据对齐到32B，`660×2=1320B`无法被32整除，需将输入从660向上补齐至32B对齐，计算逻辑如下：
```text
(660 × 2 + 32 - 1) // 32 × 32 = 672 × 2 = 1344B
```

<img src="../../../../CANN-assets-20260813/reference_practice/pytorch_online_inference_operator_optimize/images/align_32.png" alt="align_32" width="700">

##### **3.4.2 核间数据拆分**
将补齐后的 **42 个 32B 数据块** 分配到 4 个 AI Core 上并行计算：

- 基础分配：`42 // 4 = 10` 个块/核
- 剩余块：`42 % 4 = 2` 个，由前 2 个核各多处理 1 块

最终分配：
- 前 2 个核（大核）：11 块 → `11×32B = 352B`
- 后 2 个核（小核）：10 块 → `10×32B = 320B`

<img src="../../../../CANN-assets-20260813/reference_practice/pytorch_online_inference_operator_optimize/images/core_data_split.png" alt="tiling_32" width="700">

##### **3.4.3 核内数据切分**
假设UB（Unified Buffer）容量限制为768B，单核单次处理数据量受此约束，需按UB大小对核内数据进行批次拆分。  

Add算子包含2个输入（x/y）和1个输出（z），且三者数据大小一致，因此UB空间均分后：  
- 单路数据最大可用UB空间：`768 // 3 = 256B`  
- 对应32B数据块数量：`256 ÷ 32 = 8` 块（即单核单次最多处理8个32B数据块）  

基于单批次上限，各核数据拆分如下：  
- 前2个核（共11个32B块）：第1批处理8块，第2批处理3块  
- 后2个核（共10个32B块）：第1批处理8块，第2批处理2块  

<img src="../../../../CANN-assets-20260813/reference_practice/pytorch_online_inference_operator_optimize/images/kernel_data_split.png" alt="tiling_32" width="700">

##### **3.4.4 Tiling 结构体定义**
为存储 Tiling 相关参数，我们基于前述的核间拆分、UB 批次拆分逻辑，我们需要以下字段：

<div style="text-align: left; float: left;">
<table style="border-collapse: collapse; width: 100%; max-width: 800px; border: 1px solid #ddd;">
  <!-- 表头行 -->
  <tr>
    <td style="padding: 8px; border-bottom: 1px solid #ddd; font-weight: bold; background-color: #f5f5f5;">结构体字段</td>
    <td style="padding: 8px; border-bottom: 1px solid #ddd; font-weight: bold; background-color: #f5f5f5;">对应数值</td>
    <td style="padding: 8px; border-bottom: 1px solid #ddd; font-weight: bold; background-color: #f5f5f5;">计算逻辑/业务含义</td>
  </tr>
  <!-- 行1 -->
  <tr>
    <td style="padding: 8px; border-bottom: 1px solid #ddd;"><code>smallCoreDataNum</code></td>
    <td style="padding: 8px; border-bottom: 1px solid #ddd;">160（个元素）</td>
    <td style="padding: 8px; border-bottom: 1px solid #ddd;">小核（后2个核）总数据量：10个32B块 × 32B/块 = 320B；half单元素占2B，因此320B / 2B = 160个元素</td>
  </tr>
  <!-- 行2 -->
  <tr>
    <td style="padding: 8px; border-bottom: 1px solid #ddd;"><code>bigCoreDataNum</code></td>
    <td style="padding: 8px; border-bottom: 1px solid #ddd;">176（个元素）</td>
    <td style="padding: 8px; border-bottom: 1px solid #ddd;">大核（前2个核）总数据量：11个32B块 × 32B/块 = 352B；half单元素占2B，因此352B / 2B = 176个元素</td>
  </tr>
  <!-- 行3 -->
  <tr>
    <td style="padding: 8px; border-bottom: 1px solid #ddd;"><code>finalBigTileNum</code></td>
    <td style="padding: 8px; border-bottom: 1px solid #ddd;">2</td>
    <td style="padding: 8px; border-bottom: 1px solid #ddd;">大核批次次数：单批次最多8块（256B），11块需分2批（8块+3块）</td>
  </tr>
  <!-- 行4 -->
  <tr>
    <td style="padding: 8px; border-bottom: 1px solid #ddd;"><code>finalSmallTileNum</code></td>
    <td style="padding: 8px; border-bottom: 1px solid #ddd;">2</td>
    <td style="padding: 8px; border-bottom: 1px solid #ddd;">小核批次次数：单批次最多8块（256B），10块需分2批（8块+2块）</td>
  </tr>
  <!-- 行5 -->
  <tr>
    <td style="padding: 8px; border-bottom: 1px solid #ddd;"><code>tileDataNum</code></td>
    <td style="padding: 8px; border-bottom: 1px solid #ddd;">128（个元素）</td>
    <td style="padding: 8px; border-bottom: 1px solid #ddd;">单核单次最大搬运量：UB 768B ÷ 3（2输入+1输出）= 256B（8个32B块）；half单元素占2B，因此256B / 2B = 128个元素</td>
  </tr>
  <!-- 行6 -->
  <tr>
    <td style="padding: 8px; border-bottom: 1px solid #ddd;"><code>smallTailDataNum</code></td>
    <td style="padding: 8px; border-bottom: 1px solid #ddd;">32（个元素）</td>
    <td style="padding: 8px; border-bottom: 1px solid #ddd;">小核最后一批数据量：2个32B块 × 32B/块 = 64B；half单元素占2B，因此64B / 2B = 32个元素</td>
  </tr>
  <!-- 行7 -->
  <tr>
    <td style="padding: 8px; border-bottom: 1px solid #ddd;"><code>bigTailDataNum</code></td>
    <td style="padding: 8px; border-bottom: 1px solid #ddd;">48（个元素）</td>
    <td style="padding: 8px; border-bottom: 1px solid #ddd;">大核最后一批数据量：3个32B块 × 32B/块 = 96B；half单元素占2B，因此96B / 2B = 48个元素</td>
  </tr>
  <!-- 行8 -->
  <tr>
    <td style="padding: 8px;"><code>tailBlockNum</code></td>
    <td style="padding: 8px;">2</td>
    <td style="padding: 8px;">大核个数：42个32B块 ÷ 4核，余数为2，前2个核为大核</td>
  </tr>
</table>
</div>
<div style="clear: both;"></div>

<br>

基于上述字段定义 Tiling 结构体：
```cpp
struct TilingDataTemplate {
    uint32_t smallCoreDataNum;  // 小核处理的总数据量（字节数）
    uint32_t bigCoreDataNum;    // 大核处理的总数据量（字节数）
    uint32_t finalBigTileNum;   // 大核数据搬运总批次次数
    uint32_t finalSmallTileNum; // 小核数据搬运总批次次数
    uint32_t tileDataNum;       // 单核单次可搬运数据量（字节数）
    uint32_t smallTailDataNum;  // 小核最后一批处理数据量（字节数）
    uint32_t bigTailDataNum;    // 大核最后一批处理数据量（字节数）
    uint32_t tailBlockNum;      // 大核个数（余数分配的核数量）
};

```

---
### **4. 泛化算子实现**
接下来我们将基于上述tiling设计思路，完成AddCustomTemplate算子的泛化开发。首先使用AddCustomTemplate算子原型json文件创建算子工程。  

点击查看算子原型json文件内容：

```bash
!cat src/add_custom.json
```

```python
# 清除已有的custom_op目录
!rm -rf Sources/03/custom_op
# 使用已有的算子原型json文件创建算子工程
!cp src/add_custom.json Sources/03/add_custom.json
# 生成算子工程
!msopgen gen -i Sources/03/add_custom.json -c ai_core-ascend910b1 -lan cpp -out Sources/03/custom_op
```

命令执行完后，会创建算子工程，目录结构如下所示：
```
custom_op
|--- framework
|--- op_host
|   |--- add_custom_template.cpp          // 包含算子原型注册、tiling实现 shape与Dtype推导内容
|   |--- CMakeLists.txt                   // host侧CMakeLists文件，一般不需要修改
|--- op_kernel
|   |--- add_custom_template_tiling.h     // 算子tiling定义文件   
|   |--- add_custom_template.cpp          // 算子代码实现文件 
|   |--- CMakeLists.txt                   // kernel侧CMakeLists文件，一般不需要修改
|--- CMakeLists.txt                       // 根目录CMakeLists文件，一般不需要修改
|--- CMakePresets.json                    // CMake编译配置文件
|--- build.sh                             // 编译脚本
```  
工程目录中的op_kernel和op_host包含了算子的核心实现文件。op_kernel下存放kernel侧算子实现。op_host下存放host侧代码实现，包括算子原型定义、host侧tiling实现。
* custom_op: msopgen工具创建算子工程时指定的算子工程名，可自定义
* **op_host/add_custom_template.cpp**: 文件名会根据add_custom.json内定义的算子名生成，包含算子原型注册、tiling实现 Shape与Dtype推导内容。
* **op_kernel/add_custom_template_tiling.h**: 文件名会根据add_custom.json内定义的算子名生成，包含算子tiling结构体定义。
* **op_kernel/add_custom_template.cpp**: 文件名会根据add_custom.json内定义的算子名生成，包含算子代码实现。
* **CMakePresets.json**: CMake编译配置文件，一般只需要修改ASCEND_CANN_PACKAGE_PATH为实际CANN安装路径。

执行以下命令查看刚刚生成的算子工程目录结构：

```bash
!cd Sources/03/custom_op;find . -maxdepth 2 -print | sed -e 's;[^/]*/;|____;g;s;____|;    |;g'
```

#### **4.1 Host侧实现**
首先需要完成Host侧的Tiling实现，该部分逻辑决定了每个核处理的数据量，以及核内数据的切分方式。
##### **4.1.1 头文件引用**
由于泛化Tiling实现时需要获取AiCore的UB大小，以及可能需要获取的数据类型的字节数，所以需要引用相关头文件。
- op_def_registry.h：算子注册头文件，固定引用
- add_custom_template_tiling.h： 自定义的Tiling结构体定义文件
- type_utils.h：数据类型相关的工具类
- platform_utils.h：平台信息相关的工具类

```bash
%%writefile Sources/03/custom_op/op_host/add_custom_template.cpp

#include "register/op_def_registry.h"
#include "../op_kernel/add_custom_template_tiling.h"
#include "graph/utils/type_utils.h"
#include "tiling/platform/platform_ascendc.h"
```

##### **4.1.2 获取输入大小及核数**
根据Tiling设计多核均衡原则，每个核处理的数据量应尽可能相等。所以我们需要先获取输入数据大小以及可以使用的核数。
- GetCoreNum：获取当前环境的核数
- GetShapeSize：获取输入的元素数量
- GetDataTypeLength： 获取输入数据类型所占内存大小

```bash
%%writefile -a Sources/03/custom_op/op_host/add_custom_template.cpp
namespace optiling {
static ge::graphStatus TilingFunc(gert::TilingContext *context)
{
    
    auto ascendcPlatform = platform_ascendc::PlatformAscendC(context->GetPlatformInfo());
    auto coreNum = ascendcPlatform.GetCoreNum();
    
    uint32_t inputNum = context->GetInputShape(0)->GetStorageShape().GetShapeSize();
    uint32_t typeLength = 0;
    ge::TypeUtils::GetDataTypeLength(context->GetInputDesc(0)->GetDataType(), typeLength);
    uint32_t inputLength = inputNum * typeLength;
```

##### **4.1.3 计算每个核处理的数据量**
结合Tiling设计的内存对齐原则，输入数据需向上对齐至32B的整数倍，且所有数据块均以32B为最小处理单位。基于此，核数分配与核内数据块的切分规则设计如下：
1. 先将输入数据的总大小向上对齐至32B整数倍，得到对齐后的总32B数据块数；  

2. 以每个核至少分配1个32B数据块为基准，判断是否启用全部核数：若对齐后的数据块总量过小，核数不足时则至少启用1个核完成计算；  

3. 确定实际使用的核数后，计算核均基础处理的32B数据块数，对无法均分的剩余数据块，采用前N核补块的方式分配：让前tailBlockNum个核各多处理1个32B数据块，其余核按基础数处理；  

4. 按补块规则划分核类型：多处理1个32B 数据块的核称为大核，按基础数处理的核称为小核。  

**参数说明如下：**

- everyCoreInputBlockNum： 每个核处理的32B数据块个数

- tailBlockNum： 前tailBlockNum个核每个核多计算一个32B数据块

<img src="../../../../CANN-assets-20260813/reference_practice/pytorch_online_inference_operator_optimize/images/input_alignment.png"  alt="input_alignment" />

```bash
%%writefile -a Sources/03/custom_op/op_host/add_custom_template.cpp
    const uint32_t BLOCK_SIZE = 32;
    uint32_t inputLengthAlign32 = (((inputLength + BLOCK_SIZE - 1) / BLOCK_SIZE) * BLOCK_SIZE);
    coreNum = std::min(coreNum, inputLengthAlign32 / BLOCK_SIZE);
    coreNum = std::max(coreNum, static_cast<uint32_t>(1));
    uint32_t everyCoreInputBlockNum = inputLengthAlign32 / BLOCK_SIZE / coreNum;
    uint32_t tailBlockNum = (inputLengthAlign32 / BLOCK_SIZE) % coreNum;
    context->SetBlockDim(coreNum);
```

##### **4.1.4 核内数据切分**
结合访存优化原则，设计核心为尽可能占满单个核的 UB 内存，以此最大化访存效率。具体计算逻辑如下：  

1. 先获取单个核的可用UB内存总大小；  

2. 针对AddCustomTemplate算子，其包含两个输入、一个输出，因此核上会同时存在输入x、输入y、输出z共3个Buffer块；  

3. 基于核可用UB总大小与3个Buffer块的数量，即可计算出单个Buffer最多可容纳的32B数据块个数，以及对应的元素个数。

**参数说明如下：**
- GetCoreMemSize： 获取硬件平台存储空间的内存大小

```bash
%%writefile -a Sources/03/custom_op/op_host/add_custom_template.cpp
	uint64_t ubSize;
    ascendcPlatform.GetCoreMemSize(platform_ascendc::CoreMemType::UB, ubSize);
    uint32_t ubDataNumber = 3;
    uint32_t tileBlockNum = (ubSize / BLOCK_SIZE ) / ubDataNumber;
    uint32_t tileDataNum = (tileBlockNum * BLOCK_SIZE) / typeLength;
```

针对小核的运算调度，需结合其分配到的总数据量、核内单次可运算的数据量，计算核内的循环运算次数；若总数据量无法被单次运算量整除，需额外执行一次循环处理剩余数据。

**参数说明如下：**
- smallTileNum： 每个核分到数据不能一次运算完成时需要循环计算的次数

- smallTailDataNum： 最后一次循环需要处理的数据量

<img src="../../../../CANN-assets-20260813/reference_practice/pytorch_online_inference_operator_optimize/images/intra_kernel_partition.png"  alt="intra_kernel_partition" />

```bash
%%writefile -a Sources/03/custom_op/op_host/add_custom_template.cpp
    uint32_t smallCoreDataNum = everyCoreInputBlockNum * BLOCK_SIZE / typeLength;
    uint32_t smallTileNum = everyCoreInputBlockNum / tileBlockNum;
    uint32_t finalSmallTileNum = (everyCoreInputBlockNum % tileBlockNum) == 0 ? smallTileNum : smallTileNum + 1;
    uint32_t smallTailDataNum = smallCoreDataNum - (tileDataNum * smallTileNum);
    smallTailDataNum = smallTailDataNum == 0 ? tileDataNum : smallTailDataNum;
```

对于大核，因需多处理1个32B数据块，其实际处理的32B数据块总数为everyCoreInputBlockNum + 1

**参数说明如下：**
- bigTileNum：每个核分到数据不能一次运算完成时需要循环计算的次数

- bigTailDataNum：大核最后一次循环需要处理的数据量

```bash
%%writefile -a Sources/03/custom_op/op_host/add_custom_template.cpp
    everyCoreInputBlockNum += 1;
    uint32_t bigCoreDataNum = everyCoreInputBlockNum * BLOCK_SIZE / typeLength;
    uint32_t bigTileNum = everyCoreInputBlockNum / tileBlockNum;
    uint32_t finalBigTileNum = (everyCoreInputBlockNum % tileBlockNum) == 0 ? bigTileNum : bigTileNum + 1;
    uint32_t bigTailDataNum = bigCoreDataNum - tileDataNum * bigTileNum;
    bigTailDataNum = bigTailDataNum == 0 ? tileDataNum : bigTailDataNum;
```

需将上文Tiling阶段计算得到的各类核心参数，统一封装至TilingDataTemplate结构体进行持久化存储，为后续算子的实际计算逻辑提供数据支撑。为此，需先行在TilingDataTemplate结构体中扩展添加上述所有相关字段。

```bash
%%writefile  Sources/03/custom_op/op_kernel/add_custom_template_tiling.h

#ifndef ADD_CUSTOM_TEMPLATE_TILING_H
#define ADD_CUSTOM_TEMPLATE_TILING_H
#include <cstdint>

struct TilingDataTemplate {
    uint32_t smallCoreDataNum;
    uint32_t bigCoreDataNum;
    uint32_t finalBigTileNum;
    uint32_t finalSmallTileNum;
    uint32_t tileDataNum;
    uint32_t smallTailDataNum;
    uint32_t bigTailDataNum;
    uint32_t tailBlockNum;
};
#endif // ADD_CUSTOM_TEMPLATE_TILING_H
```

回到Tiling实现函数中，我们将上述所有计算得到的参数值，逐一赋值至TilingDataTemplate结构体进行存储。至此，便完成了整套Tiling方案的设计与实现，该方案可全面覆盖4种不同的Tiling场景，具备良好的泛化性。

```bash

%%writefile -a Sources/03/custom_op/op_host/add_custom_template.cpp    
    TilingDataTemplate *tiling = context->GetTilingData<TilingDataTemplate>();
    tiling->smallCoreDataNum = smallCoreDataNum;
    tiling->bigCoreDataNum = bigCoreDataNum;
    tiling->tileDataNum = tileDataNum;
    tiling->smallTailDataNum = smallTailDataNum;
    tiling->bigTailDataNum = bigTailDataNum;
    tiling->finalSmallTileNum = finalSmallTileNum;
    tiling->finalBigTileNum = finalBigTileNum;
    tiling->tailBlockNum = tailBlockNum;
    
    return ge::GRAPH_SUCCESS;
}
}  // namespace optiling
```

##### **4.1.5 算子原型注册以及shape推导**
最后补充算子原型注册、Shape推导等核心配套代码，即可完整完成Host侧的全部开发实现。

```bash
%%writefile -a Sources/03/custom_op/op_host/add_custom_template.cpp
namespace ge {
static graphStatus InferShape(gert::InferShapeContext *context)
{
    const gert::Shape *intputShape = context->GetInputShape(0);
    gert::Shape *outputShape = context->GetOutputShape(0);
    *outputShape = *intputShape;
    return GRAPH_SUCCESS;
}

static graphStatus InferDataType(gert::InferDataTypeContext *context)
{
    context->SetOutputDataType(0, context->GetInputDataType(0));
    return ge::GRAPH_SUCCESS;
}
}  // namespace ge

namespace ops {
class AddCustomTemplate : public OpDef {
public:
    explicit AddCustomTemplate(const char *name) : OpDef(name)
    {
        this->Input("x")
            .ParamType(REQUIRED)
            .DataType({ge::DT_FLOAT16, ge::DT_FLOAT})
            .Format({ge::FORMAT_ND, ge::FORMAT_ND});
        this->Input("y")
            .ParamType(REQUIRED)
            .DataType({ge::DT_FLOAT16, ge::DT_FLOAT})
            .Format({ge::FORMAT_ND, ge::FORMAT_ND});
        this->Output("z")
            .ParamType(REQUIRED)
            .DataType({ge::DT_FLOAT16, ge::DT_FLOAT})
            .Format({ge::FORMAT_ND, ge::FORMAT_ND});

        this->SetInferShape(ge::InferShape).SetInferDataType(ge::InferDataType);
        this->AICore()
            .SetTiling(optiling::TilingFunc)
            .AddConfig("ascend910b");
    }
};
OP_ADD(AddCustomTemplate);
}  // namespace ops
```

#### **4.2 Kernel实现**
完成Host侧的开发后，接下来开展 Kernel 侧算子类的实现工作。
##### **4.2.1 头文件引用**
实现Kernel侧算子类时，需引用相关固定头文件，包含算子类的定义文件、Tiling数据结构体的头文件；同时因Tiling设计阶段未考虑开启Double Buffer模式，此处需将BUFFER_NUM定义为1。

```bash
%%writefile Sources/03/custom_op/op_kernel/add_custom_template.cpp 
#include "kernel_operator.h"
#include "add_custom_template_tiling.h"
#include "kernel_operator_dump_tensor_intf_impl.h"
constexpr int32_t BUFFER_NUM = 1;
```

##### **4.2.2 定义算子类**
定义算子类，通过模板接收输入和输出的数据类型。

```bash
%%writefile -a Sources/03/custom_op/op_kernel/add_custom_template.cpp 

template<typename TYPE_X, typename TYPE_Y, typename TYPE_Z> class KernelAdd {
public:
    __aicore__ inline KernelAdd() {}
```

声明Init函数完成算子计算参数的初始化，函数入参包含输入输出张量、Tiling切分数据。
1. 先基于大核处理元素数，计算当前核的GlobalMemory地址偏移。

2. 通过当前核索引与tailBlockNum的对比结果判断核类型
    - 若为大核，直接配置算子类的大核规格参数（元素数、切分次数、尾块元素数）；
    
    - 若为小核，则配置小核规格参数，同时重新计算GlobalMemory地址偏移（因初始偏移量基于大核计算）。

3. 最后根据已配置的核规格参数，完成GlobalTensor的初始化与LocalMemory的内存分配。

```bash
%%writefile -a Sources/03/custom_op/op_kernel/add_custom_template.cpp 
    __aicore__ inline void Init(GM_ADDR x, GM_ADDR y, GM_ADDR z, uint32_t smallCoreDataNum,
                                uint32_t bigCoreDataNum, uint32_t finalBigTileNum, 
                                uint32_t finalSmallTileNum, uint32_t tileDataNum, 
                                uint32_t smallTailDataNum, uint32_t bigTailDataNum, 
                                uint32_t tailBlockNum) 
    {
        uint32_t coreNum = AscendC::GetBlockIdx();
        uint32_t globalBufferIndex = bigCoreDataNum * AscendC::GetBlockIdx();
        this->tileDataNum = tileDataNum;
        if (coreNum < tailBlockNum) { 
          this->coreDataNum = bigCoreDataNum;
          this->tileNum = finalBigTileNum;
          this->tailDataNum = bigTailDataNum;
        }
        else { 
          this->coreDataNum = smallCoreDataNum;
          this->tileNum = finalSmallTileNum;
          this->tailDataNum = smallTailDataNum;
          globalBufferIndex -= (bigCoreDataNum - smallCoreDataNum) * (AscendC::GetBlockIdx() - tailBlockNum);
        }
        xGm.SetGlobalBuffer((__gm__ TYPE_X*)x + globalBufferIndex, this->coreDataNum);
        yGm.SetGlobalBuffer((__gm__ TYPE_Y*)y + globalBufferIndex, this->coreDataNum);
        zGm.SetGlobalBuffer((__gm__ TYPE_Z*)z + globalBufferIndex, this->coreDataNum);
        pipe.InitBuffer(inQueueX, BUFFER_NUM, this->tileDataNum * sizeof(TYPE_X));
        pipe.InitBuffer(inQueueY, BUFFER_NUM, this->tileDataNum * sizeof(TYPE_Y));
        pipe.InitBuffer(outQueueZ, BUFFER_NUM, this->tileDataNum * sizeof(TYPE_Z));
    }
```

声明Process函数，按Tiling切分次数循环执行CopyIn→Compute→CopyOut计算流程：常规次循环处理Tiling单次最大数据量，最后一次循环适配尾块数据量完成处理。

```bash
%%writefile -a Sources/03/custom_op/op_kernel/add_custom_template.cpp  
   __aicore__ inline void Process()
    {
        int32_t loopCount = this->tileNum;
        this->processDataNum = this->tileDataNum;
        for (int32_t i = 0; i < loopCount; i++) {
            if (i == this->tileNum - 1) {
              this->processDataNum = this->tailDataNum;
            }
            CopyIn(i);
            Compute(i);
            CopyOut(i);
        }
    }
```

CopyIn函数依据Tiling实现计算得到的单次处理数据量，完成数据的搬入操作。

```bash
%%writefile -a Sources/03/custom_op/op_kernel/add_custom_template.cpp 
private:
    __aicore__ inline void CopyIn(int32_t progress)
    {
      AscendC::LocalTensor<TYPE_X> xLocal = inQueueX.AllocTensor<TYPE_X>();
      AscendC::LocalTensor<TYPE_Y> yLocal = inQueueY.AllocTensor<TYPE_Y>();
      AscendC::DataCopy(xLocal, xGm[progress * this->tileDataNum], this->processDataNum);
      AscendC::DataCopy(yLocal, yGm[progress * this->tileDataNum], this->processDataNum);
      inQueueX.EnQue(xLocal);
      inQueueY.EnQue(yLocal);
    }
```

Compute函数函数依据Tiling实现计算得到的单次处理数据量，完成数据的计算操作。

```bash
%%writefile -a Sources/03/custom_op/op_kernel/add_custom_template.cpp 
    __aicore__ inline void Compute(int32_t progress)
    {
      AscendC::LocalTensor<TYPE_X> xLocal = inQueueX.DeQue<TYPE_X>();
      AscendC::LocalTensor<TYPE_Y> yLocal = inQueueY.DeQue<TYPE_Y>();
      AscendC::LocalTensor<TYPE_Z> zLocal = outQueueZ.AllocTensor<TYPE_Z>();
      AscendC::Add(zLocal, xLocal, yLocal, this->processDataNum);
      outQueueZ.EnQue<TYPE_Z>(zLocal);
      inQueueX.FreeTensor(xLocal);
      inQueueY.FreeTensor(yLocal);
    }
```

CopyOut函数函数依据Tiling实现计算得到的单次处理数据量，完成计算结果的搬出操作。

```bash
%%writefile -a Sources/03/custom_op/op_kernel/add_custom_template.cpp 
    __aicore__ inline void CopyOut(int32_t progress)
    {
      AscendC::LocalTensor<TYPE_Z> zLocal = outQueueZ.DeQue<TYPE_Z>();  
      AscendC::DataCopy(zGm[progress * this->tileDataNum], zLocal, this->processDataNum);
      outQueueZ.FreeTensor(zLocal);
    }
```

定义上文使用的变量

```bash
%%writefile -a Sources/03/custom_op/op_kernel/add_custom_template.cpp 
private:
    AscendC::TPipe pipe;
    AscendC::TQue<AscendC::QuePosition::VECIN, BUFFER_NUM> inQueueX, inQueueY;
    AscendC::TQue<AscendC::QuePosition::VECOUT, BUFFER_NUM> outQueueZ;
    AscendC::GlobalTensor<TYPE_X> xGm;
    AscendC::GlobalTensor<TYPE_Y> yGm;
    AscendC::GlobalTensor<TYPE_Z> zGm;
    uint32_t coreDataNum;
    uint32_t tileNum;
    uint32_t tileDataNum;
    uint32_t tailDataNum;
    uint32_t processDataNum;
};
```

##### **4.2.3 算子类调用**
算子类实现完成后，在核函数内固定通过REGISTER_TILING_DEFAULT搭配GET_TILING_DATA_WITH_STRUCT的方式获取 Tiling 切分信息；解析得到有效 Tiling 数据后，将其传入算子类对象的Init函数完成算子计算参数的初始化，后续调用Process函数执行算子完整的计算流程。

- REGISTER_TILING_DEFAULT：注册TilingData结构体用于告知框架侧用户使用标准C++语法来定义TilingData，同时告知框架TilingData结构体类型，用于框架做tiling数据解析。

- GET_TILING_DATA_WITH_STRUCT：获取指定的tiling信息，并填入对应的Tiling结构体中，第一个参数为TilingData的结构体类型，第二个参数为指定Tiling结构体变量，第三个参数为核函数处传入的tiling参数。

```bash
%%writefile -a Sources/03/custom_op/op_kernel/add_custom_template.cpp 
 __global__ __aicore__ void add_custom_template(GM_ADDR x, GM_ADDR y, GM_ADDR z, GM_ADDR workspace, GM_ADDR tiling)
{
    REGISTER_TILING_DEFAULT(TilingDataTemplate);
    GET_TILING_DATA_WITH_STRUCT(TilingDataTemplate, tiling_data, tiling);
    KernelAdd<DTYPE_X, DTYPE_Y, DTYPE_Z> op;
    op.Init(x, y, z, tiling_data.smallCoreDataNum, 
            tiling_data.bigCoreDataNum, tiling_data.finalBigTileNum, 
            tiling_data.finalSmallTileNum, tiling_data.tileDataNum, 
            tiling_data.smallTailDataNum, tiling_data.bigTailDataNum, 
            tiling_data.tailBlockNum);
    op.Process();
}
```

使用输入为Shape[33, 31]的half类型数据测试一下上文实现的算子吧。

```python
# 编译部署算子
!cd Sources/03/custom_op;bash build.sh;./build_out/custom_opp*.run --install-path=${HOME}/
# 复制测试代码
!cp -r ./src/add_custom_template/test Sources/03/test
# 编译测试代码
!g++ -I$ASCEND_TOOLKIT_HOME/include -I${HOME}/vendors/customize/op_api/include -L$ASCEND_TOOLKIT_HOME/lib64 -L${HOME}/vendors/customize/op_api/lib Sources/03/test/main.cpp -lcust_opapi -lnnopbase -lacl_rt -o Sources/03/execute_add_op;
# 设置自定义算子so路径并执行调用代码
!source ${HOME}/vendors/customize/bin/set_env.bash;./Sources/03/execute_add_op
```

### 课后实践
请根据本节课程学习内容完成以下题目进行自测。

1. （单选题）以下关于Tiling介绍不正确的是（）    
    A. 每次搬运的数据块，叫做Tiling块    
    B. 根据算子中不同输入形状确定搬入基本块大小的相关算法，叫做Tiling算法    
    C. Tiling只影响算子功能实现，不影响算子性能  
    D. 算子中实现Tiling算法的函数，叫做Tiling函数 

2. （单选题） 为保障算子性能与执行正确性，要遵循以下哪些原则（）   
    A. 内存对齐原则  
    B. 访存优化原则   
    C. 多核均衡原则     
    D. 以上都是   

3. （单选题）昇腾硬件要求算子数据对齐到多少（）    
    A. 16B    
    B. 32B    
    C. 64B    
    D. 128B    

4. （单选题）根据访存优化原则，单次搬运的数据块在满足硬件约束的前提下应该遵循以下哪个规律（）  
    A. 越小越好  
    B. 越大越好  
    C. UB的1/2    
    D. 不同算子场景规律不同      

5. （单选题）对于以下概念解释不正确的是（）  
    A. BLOCK_LENGTH指每个核上计算的数据长度  
    B. TILE_NUM指切分数据块的个数  
    C. TILE_LENGTH指每个数据块的长度    
    D. TOTAL_LENGTH指每个数据块的长度  

执行以下代码查看答案：

```bash
!cat ./answers/03_answer.txt
```

# ==========================================
## 📝 练习与验证

> 📌 原 Notebook 中的练习、编译命令和校验代码已按原顺序保留在上文。需要 CANN 运行时、Ascend NPU 或 CANNLab 环境的单元，执行前请先核对版本和设备条件。
