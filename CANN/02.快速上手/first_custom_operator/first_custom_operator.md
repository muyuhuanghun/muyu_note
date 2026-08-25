---
source_repo: cann-learning-hub
source_path: quick_start/first_custom_operator/first_custom_operator.ipynb
source_commit: 1bf85454ed7c41e184a96fb51d109b6bb83b7c0d
note_kind: notebook_to_markdown
---

# 快速入门-基于CANN快速跑通第一个自定义算子

> 📚 上游 Notebook：[quick_start/first_custom_operator/first_custom_operator.ipynb](https://gitcode.com/cann/cann-learning-hub/blob/master/quick_start/first_custom_operator/first_custom_operator.ipynb)
> 🧪 整理方式：保留 Markdown 与代码单元；省略 Jupyter 执行输出，避免把一次性环境结果误当成可复现结论。

## 🧭 学习目标

- 先读懂概念，再运行代码片段验证关键结论；
- 把本节内容接入后续 CANN / Ascend NPU 实践。

# ==========================================
## 📖 课程内容

本快速入门指南主要介绍Kernel直调工程下Ascend C算子开发的基础流程，核心内容及步骤如下：

1. 环境准备：配置程序运行所需的环境变量

2. 算子分析：梳理目标算子的原型定义

3. 核函数开发：实现算子核心功能代码

4. 算子调用：开发算子调用逻辑代码

5. 编译运行：编译算子与调用代码并执行，完成功能验证

Kernel 直调工程的核心优势为**算子实现与调用代码在同一源文件中**，可快速完成算子的开发与调用测试，是开发者高效开展算子原型开发、功能快速验证的实用利器。本次快速入门的所有开发工作，均基于Sources/add.asc文件开展。

---

### 1. 环境准备
正式开始快速入门之前，先要对jupyter环境进行初始化。以下代码完成了初始化并将环境中的变量导入jupyter环境，同时完成了代码目录的创建。保证能正常导入代码以及使用bisheng编译器，完成算子的开发及编译。

```bash
!mkdir -p Sources

import os, subprocess
env = subprocess.check_output("bash -l -c 'source $ASCEND_TOOLKIT_HOME/set_env.sh && env'", shell=True, text=True)
for line in env.splitlines():
    if "=" in line: os.environ.__setitem__(*line.split("=", 1))
print("\n🎉 Environment initialization process completed successfully!")
```

---

### 2. 算子分析
快速入门场景，基于Add算子为例进行自定义算子开发全流程介绍，为简化学习流程，该自定义算子存在以下特点。

- 输入shape固定为（8，2048）

- 输入类型仅支持float

- 固定使用8个核

基于上述条件，算子设计规格如下所示：

<table style="float: left; border-collapse: collapse; margin: 0 10px 10px 0; font-size: 14px;">
<tr style="background: #f0f0f0;">
    <td align="center">算子类型(OpType)</td>
    <td colspan="4" align="center">Add</td>
</tr>
<tr>
    <td rowspan="3" align="center">算子输入</td>
    <td align="center">name</td>
    <td align="center">shape</td>
    <td align="center">data type</td>
    <td align="center">format</td>
</tr>
<tr>
    <td align="center">x</td>
    <td align="center">(8, 2048)</td>
    <td align="center">float</td>
    <td align="center">ND</td>
</tr>
<tr>
    <td align="center">y</td>
    <td align="center">(8, 2048)</td>
    <td align="center">float</td>
    <td align="center">ND</td>
</tr>
<tr>
    <td rowspan="1" align="center">算子输出</td>
    <td align="center">z</td>
    <td align="center">(8, 2048)</td>
    <td align="center">float</td>
    <td align="center">ND</td>
</tr>
<tr>
    <td rowspan="1" align="center">核函数名</td>
    <td colspan="4" align="center">add</td>
</tr>
<tr>
    <td rowspan="1" align="center">使用核数</td>
    <td colspan="4" align="center">8</td>
</tr>
</table>

---

### 3. 核函数开发
本样例中使用固定8个核并行计算，即把数据进行分片，分配到多个核上进行处理。 Ascend C核函数是在一个核上的处理函数，所以只处理部分数据。  

分配方案是：数据整体长度为8 * 2048个元素，平均分配到8个核上运行，每个核上处理的数据大小为2048个元素。对于单核上的处理数据，也可以进行数据切块，实现对数据的流水并行处理。

#### 3.1 头文件引入
进行算子开发时，首先要在add.asc源文件中导入必要的头文件。这些头文件都是固定头文件，在进行其它自定义算子开发时可直接复用。

```bash
%%writefile Sources/add.asc

#include <cstdint>
#include <iostream>
#include <vector>
#include <algorithm>
#include <iterator>
#include "acl/acl.h"
#include "kernel_operator.h"
```

#### 3.2 定义BufferNum
由于AI Core上，矢量计算CopyIn、CopyOut过程使用MTE指令队列（MTE2、MTE3），Compute过程使用Vector指令队列（V），意味着CopyIn、CopyOut过程和Compute过程是可以并行的。

DoubleBuffer机制将待处理的数据一分为二，比如Tensor1、Tensor2。如下图所示，当Vector对Tensor1中数据进行Compute时，Tensor2可以执行CopyIn的过程；而当Vector切换到计算Tensor2时，Tensor1可以执行CopyOut的过程。由此，数据的进出搬运和Vector计算实现并行执行。 

<img src="../../../../CANN-assets-20260813/quick_start/first_custom_operator/images/double_buffer.png" alt="double_buffer"  width="300px" >

使用Double Buffer的简单代码示例如下：

```
pipe.InitBuffer(inQueueX, 2, 256);
```

而在实际代码中，一般会用宏进行替换，实际代码如下。

```bash
%%writefile -a Sources/add.asc

constexpr uint32_t BUFFER_NUM = 2; // tensor num for each queue
```

#### 3.3 tiling结构体创建
根据分配方案，需要定义一个结构体，用于保存并行数据切分相关的参数。结构体可由开发者自行定义，但需要注意以下两点：

1. 结构体命名需与算子配套，保证代码可读性

2. 结构体只定义必要参数，若存在大量冗余定义，会由于结构体下发速度慢从而导致算子性能下降。

本入门体验中，结构体命名为AddCustomTilingData，该结构体定义了如下两个参数：

- totalLength：指待处理的数据总大小，本入门体验中固定为（8 * 2048）个元素

- tileNum：指每个核需要计算的数据块个数。

```bash
%%writefile -a Sources/add.asc

struct AddCustomTilingData
{
    uint32_t totalLength;
    uint32_t tileNum;
};
```

#### 3.4 进行核函数的定义
核函数（Kernel Function）是Ascend C算子设备侧实现的入口。Ascend C允许用户使用C/C++函数的语法扩展来编写设备端的运行代码，用户在核函数中进行数据访问和计算操作，由此实现该算子的所有功能。区别于普通的C++函数调用时仅执行一次，当核函数被调用时，多个核都执行相同的核函数代码，具有相同的函数入参，并行执行。其定义要求如下：

- 使用__global__函数类型限定符来标识它是一个核函数。

- 使用__aicore__函数类型限定符来标识该核函数在设备端AI Core上执行。

- 指针入参变量需要增加变量类型限定符__gm__，表明该指针变量指向Global Memory上某处内存地址。

- 核函数必须具有void返回类型。

- 仅支持入参为指针或C/C++内置数据类型（Primitive data types），如：half* s0、float* s1、int32_t c。

- 为了统一表达，建议使用GM_ADDR宏来修饰入参，其为编译器中自带的宏，代表的含义为Global Memory中的地址，其定义如下:  
  ```
  #define GM_ADDR __gm__ uint8_t*
  ```

示例如下：
```
extern "C" __global__ __aicore__ void add_custom(GM_ADDR x, GM_ADDR y, GM_ADDR z, AddCustomTilingData tiling)
```

在本次体验中，由于涉及tiling结构体，所以核函数中增加了一个tiling结构体参数，并在核函数中调用算子类的Init和Process函数，算子类实现在后续步骤中介绍。

```bash
%%writefile Sources/add_bak.asc

__global__ __aicore__ void add_custom(GM_ADDR x, GM_ADDR y, GM_ADDR z, AddCustomTilingData tiling)
{
    KERNEL_TASK_TYPE_DEFAULT(KERNEL_TYPE_AIV_ONLY);    // 设置Kernel类型为Vector核（用于矢量计算）
    KernelAdd op;
    op.Init(x, y, z, tiling.totalLength, tiling.tileNum);
    op.Process();
}
```

#### 3.5 创建核函数类
矢量编程范式把算子的实现流程分为3个基本任务：CopyIn，Compute，CopyOut。

- **CopyIn**：将输入数据从Global Memory搬运到Local Memory，完成搬运后执行入队列操作；

- **Compute**：完成队列出队后，从Local Memory获取数据并计算，计算完成后执行入队操作；

- **CopyOut**：完成队列出队后，将计算结果从Local Memory搬运到Global Memory。

<img src="../../../../CANN-assets-20260813/quick_start/first_custom_operator/images/vector_programming_paradigm.png" alt="vector_programming_paradigm"  width="700px" >

根据矢量编程范式实现算子类，本样例中定义KernelAdd算子类，其具体成员如下：

```bash
%%writefile -a Sources/add.asc

class KernelAdd {
public:
    __aicore__ inline KernelAdd(){}
    // 初始化函数，完成内存初始化相关操作
    __aicore__ inline void Init(GM_ADDR x, GM_ADDR y, GM_ADDR z, uint32_t totalLength, uint32_t tileNum);
    // 核心处理函数，实现算子逻辑，调用私有成员函数CopyIn、Compute、CopyOut完成矢量算子的三级流水操作
    __aicore__ inline void Process();

private:
    // 搬入函数，从Global Memory搬运数据至Local Memory，被核心Process函数调用
    __aicore__ inline void CopyIn(int32_t progress);
    // 计算函数，完成两个输入参数相加，得到最终结果，被核心Process函数调用
    __aicore__ inline void Compute(int32_t progress);
    // 搬出函数，将最终结果从Local Memory搬运到Global Memory上，被核心Process函数调用
    __aicore__ inline void CopyOut(int32_t progress);

private:
    AscendC::TPipe pipe;  // TPipe内存管理对象
    AscendC::TQue<AscendC::TPosition::VECIN, BUFFER_NUM> inQueueX, inQueueY;  // 输入数据Queue队列管理对象，TPosition为VECIN
    AscendC::TQue<AscendC::TPosition::VECOUT, BUFFER_NUM> outQueueZ;  // 输出数据Queue队列管理对象，TPosition为VECOUT
    AscendC::GlobalTensor<float> xGm;  // 管理输入输出Global Memory内存地址的对象，其中xGm, yGm为输入，zGm为输出
    AscendC::GlobalTensor<float> yGm;
    AscendC::GlobalTensor<float> zGm;
    uint32_t blockLength; // 每个核的计算数据长度
    uint32_t tileNum; // 每个核需要计算的数据块个数
    uint32_t tileLength; // 每个核内每个数据块的长度
};
```

内部函数的调用关系如下所示：

<img src="../../../../CANN-assets-20260813/quick_start/first_custom_operator/images/calling_relationship.png" alt="calling_relationship"  width="700px" >
由此可见除了Init函数完成初始化外，Process中完成了对流水任务“搬入、计算、搬出”的调用，开发者可以重点关注三个流水任务的实现。

#### 3.6 init函数实现
初始化函数Init主要完成以下内容：

- 设置输入输出Global Tensor的Global Memory内存地址。

- 通过TPipe内存管理对象为输入输出Queue分配内存。  

本算子中，将数据切分成8块，平均分配到8个核上运行，每个核上处理的数据大小为2048个元素。通过在起始地址上增加GetBlockIdx() * blockLength（每个block处理的数据长度）的偏移，获取每个核对应的数据起始地址，从而实现多核并行计算的数据切分。

以输入x为例，x + blockLength * GetBlockIdx()即为单核处理程序中x在Global Memory上的内存偏移地址，获取偏移地址后，使用GlobalTensor类的SetGlobalBuffer接口设定该核上Global Memory的起始地址以及长度。具体示意图如下。

<img src="../../../../CANN-assets-20260813/quick_start/first_custom_operator/images/inter_kernel_partition.png" alt="inter_kernel_partition"  width="700px" >

对于单核上的处理数据，可以进行数据切块（Tiling），在本示例中，仅作为参考，将数据切分成8块（并不意味着8块就是性能最优）。切分后的每个数据块再次切分成2块，即可开启double buffer，实现流水线之间的并行。

这样单核上的数据（2048个数）被切分成16块，每块tileLength（128）个数据。TPipe为inQueueX分配了两块大小为tileLength * sizeof(float)个字节的内存块，每个内存块能容纳tileLength（128）个float类型数据。数据切分示意图如下。

<img src="../../../../CANN-assets-20260813/quick_start/first_custom_operator/images/intra_kernel_partition.png" alt="intra_kernel_partition"  width="700px" >

具体的初始化函数代码如下：

```bash
%%writefile -a Sources/add.asc

__aicore__ inline void KernelAdd::Init(GM_ADDR x, GM_ADDR y, GM_ADDR z, uint32_t totalLength, uint32_t tileNum)
{
    
     this->blockLength = totalLength / AscendC::GetBlockNum();     // length computed of each core
     this->tileNum = tileNum;                                      // split data into 8 tiles for each core
     this->tileLength = this->blockLength / tileNum / BUFFER_NUM;  // separate to 2 parts, due to double buffer
     // get start index for current core, core parallel
     xGm.SetGlobalBuffer((__gm__ float *)x + this->blockLength * AscendC::GetBlockIdx(), this->blockLength);
     yGm.SetGlobalBuffer((__gm__ float *)y + this->blockLength * AscendC::GetBlockIdx(), this->blockLength);
     zGm.SetGlobalBuffer((__gm__ float *)z + this->blockLength * AscendC::GetBlockIdx(), this->blockLength);
     // pipe alloc memory to queue, the unit is Bytes
     pipe.InitBuffer(inQueueX, BUFFER_NUM, this->tileLength * sizeof(float));
     pipe.InitBuffer(inQueueY, BUFFER_NUM, this->tileLength * sizeof(float));
     pipe.InitBuffer(outQueueZ, BUFFER_NUM, this->tileLength * sizeof(float));
}
```

#### 3.7 process函数实现
基于矢量编程范式，将核函数的实现分为3个基本任务：CopyIn，Compute，CopyOut。Process函数中通过如下方式调用这三个函数。

```bash
%%writefile -a Sources/add.asc

__aicore__ inline void KernelAdd::Process()
{
    // loop count need to be doubled, due to double buffer
    int32_t loopCount = this->tileNum * BUFFER_NUM;
    // tiling strategy, pipeline parallel
    for (int32_t i = 0; i < loopCount; i++) {
        CopyIn(i);
        Compute(i);
        CopyOut(i);
    }
}
```

#### 3.8 CopyIn函数实现
CopyIn函数的核心作用是将NPU端的数据拷贝至AICore，具体执行流程如下：

- 使用DataCopy接口将GlobalTensor数据拷贝到LocalTensor。

- 使用EnQue将LocalTensor放入VecIn的Queue中。

```bash
%%writefile -a Sources/add.asc

__aicore__ inline void KernelAdd::CopyIn( int32_t progress)
{
    // alloc tensor from queue memory
    AscendC::LocalTensor<float> xLocal = inQueueX.AllocTensor<float>();
    AscendC::LocalTensor<float> yLocal = inQueueY.AllocTensor<float>();
    // copy progress_th tile from global tensor to local tensor
    AscendC::DataCopy(xLocal, xGm[progress * this->tileLength], this->tileLength);
    AscendC::DataCopy(yLocal, yGm[progress * this->tileLength], this->tileLength);
    // enque input tensors to VECIN queue
    inQueueX.EnQue(xLocal);
    inQueueY.EnQue(yLocal);
}
```

#### 3.9 Compute函数实现
Compute为核心计算函数，通过调用Ascend C接口，对已搬入AICore的数据执行实际计算操作，具体流程如下：

- 使用DeQue从VecIn中取出LocalTensor。

- 使用Ascend C接口Add完成矢量计算。

- 使用EnQue将计算结果LocalTensor放入到VecOut的Queue中。

- 使用FreeTensor将释放不再使用的LocalTensor。

```bash
%%writefile -a Sources/add.asc

__aicore__ inline void KernelAdd::Compute(int32_t progress)
{
    // deque input tensors from VECIN queue
    AscendC::LocalTensor<float> xLocal = inQueueX.DeQue<float>();
    AscendC::LocalTensor<float> yLocal = inQueueY.DeQue<float>();
    AscendC::LocalTensor<float> zLocal = outQueueZ.AllocTensor<float>();
    // call Add instr for computation
    AscendC::Add(zLocal, xLocal, yLocal, this->tileLength);
    // enque the output tensor to VECOUT queue
    outQueueZ.EnQue<float>(zLocal);
    // free input tensors for reuse
    inQueueX.FreeTensor(xLocal);
    inQueueY.FreeTensor(yLocal);
}
```

#### 3.10 CopyOut函数实现。
CopyOut 函数用于将 AICore 中完成计算的结果数据搬出，具体流程如下：

- 使用DeQue接口从VecOut的Queue中取出LocalTensor。

- 使用DataCopy接口将LocalTensor拷贝到GlobalTensor上。

- 使用FreeTensor将不再使用的LocalTensor进行回收。

```bash
%%writefile -a Sources/add.asc

__aicore__ inline void KernelAdd::CopyOut(int32_t progress)
{
    // deque output tensor from VECOUT queue
    AscendC::LocalTensor<float> zLocal = outQueueZ.DeQue<float>();
    // copy progress_th tile from local tensor to global tensor
    AscendC::DataCopy(zGm[progress * this->tileLength], zLocal, this->tileLength);
    // free output tensor for reuse
    outQueueZ.FreeTensor(zLocal);
}
```

#### 3.11 重新写入核函数
由于核函数会调用实现类中的函数，所以需要将3.4中暂存于add_bak.asc中的核函数代码写入add.asc

```bash
!cat Sources/add_bak.asc >> Sources/add.asc
!rm Sources/add_bak.asc
```

---

### 4. 算子调用
完成Kernel侧核函数开发后，即可编写Host侧的核函数调用程序。实现从Host侧的APP程序调用算子，执行计算过程。本算子中主要分为以下三个部分。

1. 核函数调用：通过<<<...>>>内核调用符进行算子调用

2. 计算结果比对：比对golden数据和实际输出，验证算子精度

3. 算子验证主程序：生成输入及golden数据，用来进行算子验证

#### 4.1 核函数调用
常见的函数调用方式是如下的形式：

```
function_name(argument list);
```

核函数使用内核调用符<<<...>>>这种语法形式，来规定核函数的执行配置：

```
kernel_name<<<blockDim, l2ctrl, stream>>>(argument list);
```

执行配置由3个参数决定：

- **blockDim**: 规定了核函数将会在几个核上执行。每个执行该核函数的核会被分配一个逻辑ID，即block_idx，可以在核函数的实现中调用GetBlockIdx来获取block_idx；

- **l2ctrl**: 保留参数，暂时设置为固定值nullptr，开发者无需关注；

- **stream**: 类型为aclrtStream，stream用于维护一些异步操作的执行顺序，确保按照应用程序中的代码调用顺序在device上执行。

如下名为add_custom的核函数，实现两个矢量的相加，调用示例如下:

```
// blockDim设置为8表示在8个核上调用了add_custom核函数，每个核都会独立且并行地执行该核函数，该核函数的参数列表为x，y，z，tiling。
add_custom<<<8, nullptr, stream>>>(x, y, z, tiling);
```  
核函数的调用是异步的，核函数的调用结束后，控制权立刻返回给主机端，可以调用以下aclrtSynchronizeStream函数来强制主机端程序等待所有核函数执行完毕。

```
aclError aclrtSynchronizeStream(aclrtStream stream);
```

在整个调用过程中，需要申请Host和Device内存，在Host侧读入数据后，将数据拷贝到Device侧，进而调用<<<...>>>进行算子执行，其逻辑流程图如下所示：

<img src="../../../../CANN-assets-20260813/quick_start/first_custom_operator/images/kernel_function_call_code_logic_block_diagram.png" alt="kernel_function_call_code_logic_block_diagram"  width="200px" >

本样例实现如下：

```bash
%%writefile -a Sources/add.asc

std::vector<float> kernel_add(std::vector<float> &x, std::vector<float> &y)
{
    constexpr uint32_t blockDim = 8;
    uint32_t totalLength = x.size();
    size_t totalByteSize = totalLength * sizeof(float);
    int32_t deviceId = 0;
    aclrtStream stream = nullptr;
    AddCustomTilingData tiling = {/*totalLength:*/totalLength, /*tileNum:*/8};
    uint8_t *xHost = reinterpret_cast<uint8_t *>(x.data());
    uint8_t *yHost = reinterpret_cast<uint8_t *>(y.data());
    uint8_t *zHost = nullptr;
    uint8_t *xDevice = nullptr;
    uint8_t *yDevice = nullptr;
    uint8_t *zDevice = nullptr;

    // 初始化
    aclInit(nullptr);
    // 运行管理资源申请
    aclrtSetDevice(deviceId);
    aclrtCreateStream(&stream);
    // 分配Host内存
    aclrtMallocHost((void **)(&zHost), totalByteSize);
    // 分配Device内存
    aclrtMalloc((void **)&xDevice, totalByteSize, ACL_MEM_MALLOC_HUGE_FIRST);
    aclrtMalloc((void **)&yDevice, totalByteSize, ACL_MEM_MALLOC_HUGE_FIRST);
    aclrtMalloc((void **)&zDevice, totalByteSize, ACL_MEM_MALLOC_HUGE_FIRST);
    // 将Host上的输入数据拷贝到Device侧
    aclrtMemcpy(xDevice, totalByteSize, xHost, totalByteSize, ACL_MEMCPY_HOST_TO_DEVICE);
    aclrtMemcpy(yDevice, totalByteSize, yHost, totalByteSize, ACL_MEMCPY_HOST_TO_DEVICE);
    // 用内核调用符<<<...>>>调用核函数完成指定的运算
    add_custom<<<blockDim, nullptr, stream>>>(xDevice, yDevice, zDevice, tiling);
    aclrtSynchronizeStream(stream);
    // 将Device上的运算结果拷贝回Host
    aclrtMemcpy(zHost, totalByteSize, zDevice, totalByteSize, ACL_MEMCPY_DEVICE_TO_HOST);
    std::vector<float> z((float *)zHost, (float *)zHost + totalLength);
    // 释放申请的资源
    aclrtFree(xDevice);
    aclrtFree(yDevice);
    aclrtFree(zDevice);
    aclrtFreeHost(zHost);
    // 去初始化
    aclrtDestroyStream(stream);
    aclrtResetDevice(deviceId);
    aclFinalize();
    return z;
}
```

在实现其他算子时，这里大部分代码均可复用，需要修改的点如下：

1. 需要根据实际输入及输出个数，调整Host和Device的内存申请、拷贝、释放以及<<<...>>>中的参数。

2. 需要根据实际要使用的核数，定义blockDim。

3. 需要根据实际的分块策略定义tileNum。

#### 4.2 计算结果比对
传入实际输出与golden值，进行一一比对，若不相同，则证明存在精度问题。本样例中会同时将output和golden中前20个数打印出来进行查看。

```bash
%%writefile -a Sources/add.asc

uint32_t VerifyResult(std::vector<float> &output, std::vector<float> &golden)
{
    auto printTensor = [](std::vector<float> &tensor, const char *name) {
        constexpr size_t maxPrintSize = 20;
        std::cout << name << ": ";
        std::copy(tensor.begin(), tensor.begin() + std::min(tensor.size(), maxPrintSize),
            std::ostream_iterator<float>(std::cout, " "));
        if (tensor.size() > maxPrintSize) {
            std::cout << "...";
        }
        std::cout << std::endl;
    };
    printTensor(output, "Output");
    printTensor(golden, "Golden");
    if (output.size() == golden.size() && std::equal(output.begin(), output.end(), golden.begin())) {
        std::cout << "[Success] Case accuracy is verification passed." << std::endl;
        return 0;
    } else {
        std::cout << "[Failed] Case accuracy is verification failed!" << std::endl;
        return 1;
    }
    return 0;
}
```

#### 4.3 算子验证主程序
定义输入数据长度，并生成实际的golden数据。

```bash
%%writefile -a Sources/add.asc

int32_t main(int32_t argc, char *argv[])
{
    constexpr uint32_t totalLength = 8 * 2048;
    constexpr float valueX = 1.2f;
    constexpr float valueY = 2.3f;
    std::vector<float> x(totalLength, valueX);
    std::vector<float> y(totalLength, valueY);

    std::vector<float> output = kernel_add(x, y);

    std::vector<float> golden(totalLength, valueX + valueY);
    return VerifyResult(output, golden);
}
```

---

### 5. 编译运行
完成所有代码的开发工作后，即可进行编译运行。首先执行以下代码编译可执行文件：

```bash
!bisheng Sources/add.asc --npu-arch=dav-2201 -o add_custom
```

再执行以下代码，进行算子的实际运行。

```bash
!./add_custom
```

# ==========================================
## 📝 练习与验证

> 📌 原 Notebook 中的练习、编译命令和校验代码已按原顺序保留在上文。需要 CANN 运行时、Ascend NPU 或 CANNLab 环境的单元，执行前请先核对版本和设备条件。
