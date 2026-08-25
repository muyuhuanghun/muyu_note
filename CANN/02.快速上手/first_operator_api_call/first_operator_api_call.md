---
source_repo: cann-learning-hub
source_path: quick_start/first_operator_api_call/first_operator_api_call.ipynb
source_commit: 1bf85454ed7c41e184a96fb51d109b6bb83b7c0d
note_kind: notebook_to_markdown
---

# 快速入门-基于CANN快速跑通第一个算子API调用

> 📚 上游 Notebook：[quick_start/first_operator_api_call/first_operator_api_call.ipynb](https://gitcode.com/cann/cann-learning-hub/blob/master/quick_start/first_operator_api_call/first_operator_api_call.ipynb)
> 🧪 整理方式：保留 Markdown 与代码单元；省略 Jupyter 执行输出，避免把一次性环境结果误当成可复现结论。

## 🧭 学习目标

- 先读懂概念，再运行代码片段验证关键结论；
- 把本节内容接入后续 CANN / Ascend NPU 实践。

# ==========================================
## 📖 课程内容

本快速入门指南主要介绍单算子API调用的基础流程，核心内容及步骤如下：

1. 环境准备：配置程序运行所需的环境变量

2. 单算子API介绍：了解单算子API的定义

3. 单算子API调用流程介绍：结合代码介绍单算子调用时各个流程的作用

4. 编译运行：基于开发的代码完成API调用的编译运行

本次快速入门聚焦**内置算子库中已有算子的API调用**实践，所有开发工作均基于Sources/test_abs.cpp文件开展。

---

### 1. 环境准备
正式开始快速入门之前，先要对jupyter环境进行初始化。以下代码完成了初始化并将环境中的变量导入jupyter环境，同时完成了代码目录的创建。确保后续能正常开展代码导入、算子调用程序的开发与编译工作。

```bash
!mkdir -p Sources

import os, subprocess
env = subprocess.check_output("bash -l -c 'source $ASCEND_TOOLKIT_HOME/set_env.sh && env'", shell=True, text=True)
for line in env.splitlines():
    if "=" in line: os.environ.__setitem__(*line.split("=", 1))
print("\n🎉 Environment initialization process completed successfully!")
```

---

### 2. 单算子API介绍
算子API调用是直接调用C语言实现的单算子API接口完成算子计算，这类接口统一设计为**两段式接口**，通用定义格式如下：

```
aclnnStatus aclxxXxxGetWorkspaceSize(const aclTensor *src, ..., aclTensor *out, ..., uint64_t *workspaceSize, aclOpExecutor **executor);
aclnnStatus aclxxXxx(void *workspace, uint64_t workspaceSize, aclOpExecutor *executor, aclrtStream stream);
```

调用时需遵循固定执行顺序：先调用第一段aclxxXxxGetWorkspaceSize接口，计算本次API执行所需的workspace内存大小；获取workspaceSize后，按需申请NPU侧内存，再调用第二段aclxxXxx接口执行实际计算。

其中，aclxx为算子接口通用前缀（如aclnn），Xxx为具体算子类型标识（如Add算子对应Add、Abs算子对应Abs）。

#### 2.1 适用场景
单算子 API 支持两种生成与使用场景，覆盖内置算子调用与自定义算子开发全需求：

- **CANN内置算子场景**：CANN ops算子包集成了CANN全量内置算子的API接口，完成算子包部署后，可直接参照官网单算子API文档进行调用；

- **自定义算子场景**：开发者开发的自定义算子完成编译后，会自动生成对应的单算子API接口，部署自定义算子后，即可按其专属API接口完成调用。

本次入门体验聚焦**CANN 内置算子场景**，讲解如何直接调用已有的算子API完成计算开发。

#### 2.2 Abs算子接口介绍
本文以CANN ops算子包中的Abs算子为例，详解单算子两段式API的具体定义与使用。

1. 功能说明

    - 接口功能：为输入张量的每一个元素取绝对值。

    - 计算公式：out = |self|

2. 函数原型及参数说明

    该算子分为两段式接口，必须先调用“aclnnAbsGetWorkspaceSize”接口获取计算所需workspace大小以及包含了算子计算流程的执行器，再调用“aclnnAbs”接口执行计算。

    **第一段接口原型与参数如下所示**：

    ```
    // 第一段接口
    aclnnStatus aclnnAbsGetWorkspaceSize(const aclTensor *self,  aclTensor *out,  uint64_t *workspaceSize,  aclOpExecutor  **executor)
    ```

    <table style="float: left; border-collapse: collapse; margin: 0 10px 10px 0; font-size: 14px;">
    <tr style="background-color:#f0f0f0">
    <td align="center"><strong>参数名</strong></td>
    <td align="center"><strong>输入/输出</strong></td>
    <td align="center"><strong>描述</strong></td>
    <td align="center"><strong>使用说明</strong></td>
    <td align="center"><strong>数据类型</strong></td>
    <td align="center"><strong>数据格式</strong></td>
    <td align="center"><strong>维度(shape)</strong></td>
    <td align="center"><strong>非连续Tensor</strong></td>
    </tr>
    <tr>
    <td align="center">self</td>
    <td align="center">输入</td>
    <td align="left">待进行abs计算的入参，公式中的self。</td>
    <td align="center">-</td>
    <td align="left">FLOAT、FLOAT16、DOUBLE、BFLOAT16、INT8、INT16、INT32、INT64、UINT8、BOOL、COMPLEX64</td>
    <td align="center">ND</td>
    <td align="center">0-8</td>
    <td align="center">√</td>
    </tr>
    <tr>
    <td align="center">out</td>
    <td align="center">输出</td>
    <td align="left">待进行abs计算的出参，公式中的out。</td>
    <td align="left">shape与self相同。</td>
    <td align="left">FLOAT、FLOAT16、DOUBLE、BFLOAT16、INT8、INT16、INT32、INT64、UINT8、BOOL</td>
    <td align="center">ND</td>
    <td align="center">0-8</td>
    <td align="center">√</td>
    </tr>
    <tr>
    <td align="center">workspaceSize</td>
    <td align="center">输出</td>
    <td align="left">返回需要在Device侧申请的workspace大小。</td>
    <td align="center">-</td>
    <td align="center">-</td>
    <td align="center">-</td>
    <td align="center">-</td>
    <td align="center">-</td>
    </tr>
    <tr>
    <td align="center">executor</td>
    <td align="center">输出</td>
    <td align="left">返回op执行器，包含了算子计算流程。</td>
    <td align="center">-</td>
    <td align="center">-</td>
    <td align="center">-</td>
    <td align="center">-</td>
    <td align="center">-</td>
    </tr>
    </table>

    **第二段接口原型与参数如下所示**：

    ```
    // 第二段接口
    aclnnStatus aclnnAbs( void *workspace, uint64_t workspaceSize, aclOpExecutor *executor, const aclrtStream stream)
    ```

    <table style="float: left; border-collapse: collapse; margin: 0 10px 10px 0; font-size: 14px;">
    <tr style="background-color:#f0f0f0">
    <td align="center"><strong>参数名</strong></td>
    <td align="center"><strong>输入/输出</strong></td>
    <td align="center"><strong>描述</strong></td>
    </tr>
    <tr>
    <td align="center">workspace</td>
    <td align="center">输入</td>
    <td align="left">在Device侧申请的workspace内存地址。</td>
    </tr>
    <tr>
    <td align="center">workspaceSize</td>
    <td align="center">输入</td>
    <td align="left">在Device侧申请的workspace大小，由第一段接口aclnnAbsGetWorkspaceSize获取。</td>
    </tr>
    <tr>
    <td align="center">executor</td>
    <td align="center">输入</td>
    <td align="left">op执行器，包含了算子计算流程。</td>
    </tr>
    <tr>
    <td align="center">stream</td>
    <td align="center">输入</td>
    <td align="left">指定执行任务的Stream。</td>
    </tr>
    </table>

---

### 3. 单算子API调用流程介绍
本样例以 CANN ops 算子包中的 Abs 算子为实操案例，讲解单算子 API 的完整调用流程,整体调用流程如下图所示。

<img src="../../../../CANN-assets-20260813/quick_start/first_operator_api_call/images/operator_apu_call_flow_chart.png" alt="operator_apu_call_flow_chart"  width="200px" >

本样例调用Abs的单算子API时，具体代码实现分段流程如下：

1. 头文件引入：引入必要的头文件和库文件。

2. ACL初始化：初始化ACL，固定写法；

3. 运行时资源创建设置：指定device，创建stream。

4. 申请内存：用aclrtMalloc申请device内存用于存储输入 / 输出数据。

5. 构造输入: 构造算子输入数据，通常为读取文件或从其他算子输出中获取；本样例通过直接填充vector内数据模拟读取数据。

6. 传输数据：通过aclrtMemcpy将host侧输入数据拷贝到device侧。

7. 构造输入输出Tensor：输入输出Tensor作为单算子API的入参。

8. 计算并申请 workspace：调用aclnnAbsGetWorkspaceSize获取内存大小，再用aclrtMalloc申请；

9. 执行算子：调用aclnnAbs传入 workspace、执行器句柄和流；

10. 同步等待：用aclrtSynchronizeStream等待流执行完成；

11. 处理输出：通过aclrtMemcpy将device侧输出数据拷贝到host侧，打印host输出数据；

12. 释放资源：调用aclrtFree释放内存、aclrtResetDevice重置设备；

13. 去初始化：调用aclFinalize释放 ACL 资源。

#### 3.1 头文件引入
开发单算子API调用代码时，需先在test_abs.cpp源文件中引入所需头文件，各类头文件的作用及使用说明如下：

- 基础功能头文件：iostream用于输入输出流操作、vector用于动态数组操作，可根据实际开发需求选择性引入；

- ACL 核心头文件：acl.h是ACL框架的汇总头文件，内部已通过#include引入所有核心子头文件，引入该文件即可调用ACL的全部核心功能，是单算子API调用的固定引入头文件；

- 算子专属头文件：aclnn_abs.h是CANN算子库中Abs算子的专属头文件，内含Abs算子两段式API的接口定义；开发不同算子的API调用时，需替换为对应算子的专属头文件。

```bash
%%writefile Sources/test_abs.cpp

#include <iostream>
#include <vector>
#include "acl/acl.h"
#include "aclnnop/aclnn_abs.h"
```

#### 3.2 ACL初始化
单算子API调用的ACL初始化为**通用固定写法**，开发其他算子的API调用时，可直接复用该初始化逻辑。

aclInit是 ACL 框架的核心初始化函数，**必须在所有 ACL 相关接口调用前执行**，单个进程内支持多次调用aclInit做重复初始化，但其去初始化需遵循对应时序：需以aclFinalize或aclFinalizeReference完成一次去初始化，才能再次执行下一轮aclInit。

标准调用时序为：aclInit--> 单算子 API 调用代码 -->aclFinalize-->aclInit--> 单算子 API 调用代码 -->aclFinalize。

```bash
%%writefile -a Sources/test_abs.cpp
#define CHECK_RET(cond, return_expr) \
  do {                               \
    if (!(cond)) {                   \
      return_expr;                   \
    }                                \
  } while (0)

#define LOG_PRINT(message, ...)     \
  do {                              \
    printf(message, ##__VA_ARGS__); \
  } while (0)

int InitACL() {
  auto ret = aclInit(nullptr);
  CHECK_RET(ret == ACL_SUCCESS, LOG_PRINT("aclInit failed. ERROR: %d\n", ret); return ret);
  return 0;
}
```

#### 3.3 运行时资源创建设置
单算子API调用的运行时资源创建与配置为**通用固定写法**，开发其他算子的API调用时，可直接复用该配置逻辑。

- aclrtSetDevice：用于指定当前线程的运算所用Device，不同进程或线程可指定相同或不同的Device；调用该接口指定Device 后，若后续无需使用该Device的资源，可调用aclrtResetDevice或aclrtResetDeviceForce接口，及时释放本进程占用的Device资源。

- aclrtCreateStream：用于创建最高优先级的执行流Stream；同一Stream内的异步任务，会严格按照应用程序中的调用顺序执行，可保障异步任务的执行时序性。

```bash
%%writefile -a Sources/test_abs.cpp

int32_t deviceId = 0;
aclrtStream stream;

int InitResource() {
  auto ret = aclrtSetDevice(deviceId);
  CHECK_RET(ret == ACL_SUCCESS, LOG_PRINT("aclrtSetDevice failed. ERROR: %d\n", ret); return ret);
  ret = aclrtCreateStream(&stream);
  CHECK_RET(ret == ACL_SUCCESS, LOG_PRINT("aclrtCreateStream failed. ERROR: %d\n", ret); return ret);
  return 0;
}
```

#### 3.4 申请内存
调用单算子API前，需提前在Device侧申请内存，用于存放算子的输入和输出数据，通常申请的内存指针数量与算子的输入输出张量数量保持一致。

内存申请通过aclrtMalloc接口实现，该接口会在Device侧分配指定大小的线性内存，返回已分配内存的指针，且内存首地址默认64字节对齐；需要注意的是，aclrtMalloc分配内存时会做额外的字节对齐处理，会将用户传入的申请大小size向上对齐为32字节的整数倍，再额外多分配32字节。

本快速入门，定义的输入为单个形状为 [32, 32] 的 float32 类型 Tensor，输出为同形状、同数据类型的 Tensor。

```bash
%%writefile -a Sources/test_abs.cpp

// 定义输入输出参数
constexpr uint32_t INPUT_DIM0 = 32;
constexpr uint32_t INPUT_DIM1 = 32;
constexpr float VALUE_X = 0.0f;
constexpr float VALUE_Y = 0.0f;

void* selfDevice = nullptr;
void* outDevice = nullptr;

uint32_t dataSize = INPUT_DIM0 * INPUT_DIM1 * sizeof(float);

int AllocateMemory() {
  
  auto ret = aclrtMalloc(&selfDevice, dataSize, ACL_MEM_MALLOC_HUGE_FIRST);
  CHECK_RET(ret == ACL_SUCCESS, LOG_PRINT("aclrtMalloc for x failed. ERROR: %d\n", ret));

  ret = aclrtMalloc(&outDevice, dataSize, ACL_MEM_MALLOC_HUGE_FIRST);
  CHECK_RET(ret == ACL_SUCCESS, LOG_PRINT("aclrtMalloc for z failed. ERROR: %d\n", ret));
  return 0;
}
```

#### 3.5 构造输入
在算子调用前，需要构造算子的输入数据，通常是通过读取文件或者从其他算子输出中获取，这里通过设置数据模拟读取文件数据操作。

算子本质上是一段封装好的计算逻辑，其核心作用就是对输入数据进行处理，经过一系列运算得到期望的输出结果，所以调用算子时通常会传入待计算的数据。

```bash
%%writefile -a Sources/test_abs.cpp

std::vector<float> inputData(INPUT_DIM0 * INPUT_DIM1, -1.0f);


void FillWithNegativeRandomSimple() {
     for (size_t i = 0; i < inputData.size(); ++i) {
        inputData[i] = -static_cast<float>(i + 1);
    }
}
```

#### 3.6 传输数据
由于算子需要在device侧执行运算，因此需要将host侧的输入数据拷贝到device侧。这里使用aclrtMemcpy接口将host侧的输入数据拷贝到device侧。

<img src="../../../../CANN-assets-20260813/quick_start/first_operator_api_call/images/input_memory_flow.png"  alt="input_memory_flow"  width="700px" >

```bash
%%writefile -a Sources/test_abs.cpp

int TransferData() {
  auto ret = aclrtMemcpy(selfDevice, dataSize, inputData.data(), dataSize, ACL_MEMCPY_HOST_TO_DEVICE);
  CHECK_RET(ret == ACL_SUCCESS, LOG_PRINT("aclrtMemcpy H2D for x failed. ERROR: %d\n", ret); return ret);
  
  return 0;
}
```

#### 3.7 构造输入输出Tensor
Tensor是算子计算数据的容器，包含了数据内容和Tensor属性信息。    

<table style="float: left; border-collapse: collapse; margin: 0 10px 10px 0; font-size: 14px;">
    <tr style="background: #f0f0f0;">
      <td align="center"><strong>属性</strong></td>
      <td align="center"><strong>定义</strong></td>
    </tr>
    <tr>
      <td><strong>形状</strong></td>
      <td>Tensor的形状，如形状(3,4)表示第一维有3个元素，第二维有4个元素，表示一个3行4列的矩阵数组...</td>
    </tr>
    <tr>
      <td><strong>数据类型</strong></td>
      <td>指定Tensor对象的数据类型。取值范围：float16, float32, int8, int16, int32, uint8, uint16, bfloat16, bool等。</td>
    </tr>
    <tr>
      <td><strong>数据排布格式</strong></td>
      <td>ND、NC1HWC0、NCHW、NHWC等。</td>
    </tr>
</table>
<div style="clear: both;"></div>

由于单算子API调用时输入输出都是Tensor，因此需要先构造输入输出Tensor。这里需要使用aclCreateTensor接口根据已有的Device内存和Tensor属性信息构造Tensor。

```bash
%%writefile -a Sources/test_abs.cpp
aclTensor *inputTensor = nullptr;

aclTensor *outputTensor = nullptr;

std::vector<int64_t> inputShape = {32, 32};

std::vector<int64_t> outputShape = {32, 32};
int ConstructingTensors() {
  inputTensor = aclCreateTensor(inputShape.data(), inputShape.size(), aclDataType::ACL_FLOAT, nullptr, 0, aclFormat::ACL_FORMAT_ND, inputShape.data(),
                              inputShape.size(), selfDevice);
  outputTensor = aclCreateTensor(outputShape.data(), outputShape.size(), aclDataType::ACL_FLOAT, nullptr, 0, aclFormat::ACL_FORMAT_ND, outputShape.data(),
                              outputShape.size(), outDevice);
  return 0;
}
```

#### 3.8 计算并申请workspace
单算子API执行方式调用算子API时必须先调用第一段接口aclxxXxxGetWorkspaceSize，用于计算本次API调用过程中需要多少workspace内存，获取到计算所需的workspaceSize后，按照workspaceSize申请NPU内存，然后调用第二段接口aclxxXxx执行计算。

```bash
%%writefile -a Sources/test_abs.cpp

void* workspace = nullptr;
uint64_t  workspaceSize = 0;
aclOpExecutor* executor;
int CalculateAndAllocateWorkspace() {
  auto ret = aclnnAbsGetWorkspaceSize(inputTensor, outputTensor, &workspaceSize, &executor);
  CHECK_RET(ret == ACL_SUCCESS, LOG_PRINT("aclnnAbsGetWorkspaceSize failed. ERROR: %d\n", ret); return ret);
  
  if (workspaceSize > 0) {
    ret = aclrtMalloc(&workspace, workspaceSize, ACL_MEM_MALLOC_HUGE_FIRST);
    CHECK_RET(ret == ACL_SUCCESS, LOG_PRINT("aclrtMalloc for workspace failed. ERROR: %d\n", ret); return ret);
  }
  
  return 0;
}
```

#### 3.9 执行算子
调用单算子API接口的第二段接口，执行算子。算子调用的第二段接口必须在第一段结果能成功获取workspace后才能正常调用。

```bash
%%writefile -a Sources/test_abs.cpp

int ExecuteOperator() {
  auto ret = aclnnAbs(workspace, workspaceSize, executor, stream);
  CHECK_RET(ret == ACL_SUCCESS, LOG_PRINT("aclnnAbs failed. ERROR: %d\n", ret); return ret);
  return 0;
}
```

#### 3.10 同步等待
使用aclrtSynchronizeStream等待流所有操作执行，确保算子计算完成。

```bash
%%writefile -a Sources/test_abs.cpp

int SynchronizeStream() {
  // 等待流执行完成
  auto ret = aclrtSynchronizeStream(stream);
  CHECK_RET(ret == ACL_SUCCESS, LOG_PRINT("aclrtSynchronizeStream failed. ERROR: %d\n", ret); return ret);
  
  return 0;
}
```

#### 3.11 处理输出
将device上的输出数据拷贝到host上，然后对host上的输出数据进行处理，样例以打印输出进行演示。Device侧的数据无法直接打印或者保存到文件，需要先将数据拷贝到host上。

<img src="../../../../CANN-assets-20260813/quick_start/first_operator_api_call/images/output_memory_flow.png"  alt="output_memory_flow"  width="700px" >

```bash
%%writefile -a Sources/test_abs.cpp

int ProcessOutput() {
  std::vector<float> outHost(INPUT_DIM0 * INPUT_DIM1);
  uint32_t dataSize = INPUT_DIM0 * INPUT_DIM1 * sizeof(float);
  
  auto ret = aclrtMemcpy(outHost.data(), dataSize, outDevice, dataSize, ACL_MEMCPY_DEVICE_TO_HOST);
  CHECK_RET(ret == ACL_SUCCESS, LOG_PRINT("aclrtMemcpy D2H for z failed. ERROR: %d\n", ret); return ret);
  
  for (size_t i = 0; i < outHost.size(); ++i) {
    printf("abs(%f) = %f\n", inputData[i], outHost[i]);
  }
  return 0;
}
```

#### 3.12 释放资源
单算子 API 调用执行完成后，需及时释放本次开发中申请的各类资源，包括 Tensor、Device 侧内存、Stream 及 Device 相关资源。本步骤的实现为**通用固定写法**，开发其他单算子 API 调用时可直接参考复用。

```bash
%%writefile -a Sources/test_abs.cpp

int ReleaseResource() {
  aclDestroyTensor(inputTensor);
  aclDestroyTensor(outputTensor);

  // 7. 释放device资源
  aclrtFree(selfDevice);
  aclrtFree(outDevice);
  if (workspaceSize > 0) {
    aclrtFree(workspace);
  }
  aclrtDestroyStream(stream);
  aclrtResetDevice(deviceId);
  
  return 0;
}
```

#### 3.13 去初始化
本步骤为**通用固定写法**，开发其他单算子API调用时可直接复用。

aclFinalize是ACL框架的专属去初始化函数，需与初始化函数aclInit配对使用；进程退出前必须调用该接口释放进程内所有aclnn相关资源，否则会导致系统内部出现异常。

```bash
%%writefile -a Sources/test_abs.cpp
int FinalizeACL(){
    aclFinalize();
    return 0;
}
```

---

### 4. 编译运行
将上述所有流程的代码按执行顺序整合至test_abs.cpp文件中，形成完整的 Abs 算子 API 调用程序；该程序的开发流程具备通用性，开发其他单算子 API 调用程序时，可依照此流程进行适配开发。

```bash
%%writefile -a Sources/test_abs.cpp
int main() {
    InitACL();
    InitResource();
    AllocateMemory();
    FillWithNegativeRandomSimple();
    TransferData();
    ConstructingTensors();
    CalculateAndAllocateWorkspace();
    ExecuteOperator();
    SynchronizeStream();
    ProcessOutput();
    ReleaseResource();
    FinalizeACL();
}
```

完成所有代码的开发工作后，即可进行编译运行。首先执行以下代码编译可执行文件：

```bash
!g++ -std=c++11 -fPIC -O0 -g -Wall  \
-I$ASCEND_TOOLKIT_HOME/include \
-I$ASCEND_TOOLKIT_HOME/include/aclnn \
Sources/test_abs.cpp -o Sources/opapi_test \
$ASCEND_TOOLKIT_HOME/lib64/libascendcl.so $ASCEND_TOOLKIT_HOME/lib64/libnnopbase.so $ASCEND_TOOLKIT_HOME/lib64/libopapi_math.so
```

再执行以下代码，进行应用的实际运行。

```bash
!./Sources/opapi_test
```

# ==========================================
## 📝 练习与验证

> 📌 原 Notebook 中的练习、编译命令和校验代码已按原顺序保留在上文。需要 CANN 运行时、Ascend NPU 或 CANNLab 环境的单元，执行前请先核对版本和设备条件。
