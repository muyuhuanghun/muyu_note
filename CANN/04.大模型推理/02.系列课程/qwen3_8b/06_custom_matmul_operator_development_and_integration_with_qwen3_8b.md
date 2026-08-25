---
source_repo: cann-learning-hub
source_path: tutorials/llm_inference/qwen3_8b/06_custom_matmul_operator_development_and_integration_with_qwen3_8b.ipynb
source_commit: 1bf85454ed7c41e184a96fb51d109b6bb83b7c0d
note_kind: notebook_to_markdown
---

# 6 自定义量化 A8W8 matmul 算子开发并接入 Qwen3-8B

> 📚 上游 Notebook：[tutorials/llm_inference/qwen3_8b/06_custom_matmul_operator_development_and_integration_with_qwen3_8b.ipynb](https://gitcode.com/cann/cann-learning-hub/blob/master/tutorials/llm_inference/qwen3_8b/06_custom_matmul_operator_development_and_integration_with_qwen3_8b.ipynb)
> 🧪 整理方式：保留 Markdown 与代码单元；省略 Jupyter 执行输出，避免把一次性环境结果误当成可复现结论。

## 🧭 学习目标

- 先跑通功能正确的 Baseline，再用 Profiling 定位瓶颈；
- 理解图模式、融合算子、量化和端到端收益验证。

# ==========================================
## 📖 课程内容

本章是整个启航营的**核心实践环节**，将学习到的所有知识沉淀转化为一次完整的自定义算子开发实战。

实践的环境准备、提交方式可参考[启航营课程实践说明](https://gitcode.com/cann/cann-launch-camp/blob/master/2026/University/HIT/First-session/README.md)。

### 本章定位

本章将开发一个自定义的量化 matmul 算子 `QmmCustom`，通过 A8W8 量化（Activation INT8 + Weight INT8）减少计算量和内存占用，从而提升推理性能。这是本次启航营中综合性最强的一章——涵盖了从算子概念理解、Tiling 设计、Kernel 实现到算子编译、接入网络与功能性能测试的全链路。

### 通过实践达成的学习目标

- **理解量化推理原理**：掌握 A8W8 量化方案（INT8 激活 + INT8 权重）的数学原理与 Scale 反量化机制，理解 perChannelScale 与 perTokenScale 的作用。
- **设计 Tiling 数据结构与函数**：根据算子原型定义自行设计 TilingData 结构体，实现多核分块的 Tiling 函数，理解 Cube 计算单元的分块策略。
- **实现 Cube+Vector 双路径 Kernel**：完成 Cube-only（INT32 输出）和 Cube+Vector 协作（反量化 BF16 输出）两条 Kernel 路径的实现，理解昇腾 AI Core 的 Cube 与 Vector 协作编程模型。
- **完成算子编译与 Torch 接入**：编译自定义算子并通过 Torch 接口接入，打通“算子开发 → 框架调用”的链路。
- **测试算子功能与性能，尝试优化迭代**：验证自定义算子的精度正确性，测试单算子与网络性能，并根据测试结果对 Tiling 或 Kernel 进行优化迭代。

### 本章大纲

- 环境准备
- A8W8 量化 matmul 算子概念
- 自定义算子实现
    - **任务一：自行设计tilingdata结构体并实现tiling函数**
    - **任务二：实现A8W8输入，INT32输出的kernel**
    - **任务三：实现A8W8输入，经过perChannelScale和perTokenScale反量化输出BF16的kernel**
- 编译自定义算子
    - **任务四：成功编译自定义算子**
- 测试自定义算子功能性能
    - **任务五：根据提供的测试脚本，测试自定义算子功能与性能，尝试对自定义算子进行优化后重复整个流程**
- 自定义算子接入模型
- 模型性能测试
    - **任务六：测试模型性能，尝试对自定义算子进行优化后重复上述流程**
- 提交要求
---

### 1 环境准备

定位教程目录、准备运行目录，并把 CANN 环境变量导入当前 Notebook 进程：

```python
import json
import os
import subprocess
import sys
from pathlib import Path

print('[环境准备] 开始', flush=True)

def locate_repo_root():
    repo_roots = []
    try:
        cwd = Path.cwd()
        lineage = [cwd, *cwd.parents]
        repo_roots.extend(lineage)
        repo_roots.extend(base / 'cann-learning-hub' for base in lineage)
        for base in lineage:
            try:
                repo_roots.extend(base.glob('*/cann-learning-hub'))
            except OSError:
                pass
    except FileNotFoundError:
        pass
    repo_roots.append(Path('/opt/atomgit/cann-learning-hub'))

    seen = set()
    for repo_root in repo_roots:
        key = str(repo_root)
        if key in seen:
            continue
        seen.add(key)
        if (repo_root / 'tutorials/llm_inference/qwen3_8b/src').exists():
            return repo_root
    raise FileNotFoundError('Cannot locate cann-learning-hub repository root.')

REPO_ROOT = locate_repo_root()
os.chdir(REPO_ROOT)
TUTORIAL_DIR = REPO_ROOT / 'tutorials' / 'llm_inference' / 'qwen3_8b'
TUTORIAL_SRC_DIR = TUTORIAL_DIR / 'src'
if str(TUTORIAL_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(TUTORIAL_SRC_DIR))
SRC_DIR = TUTORIAL_DIR / 'src' / 'op_custom'

if not os.environ.get('ASCEND_TOOLKIT_HOME'):
    raise EnvironmentError('ASCEND_TOOLKIT_HOME is not set. Please activate the CANN environment.')
print('CANN包路径 =', os.environ.get('ASCEND_TOOLKIT_HOME'))
cann_script = Path(os.environ['ASCEND_TOOLKIT_HOME']) / 'set_env.sh'
env_cmd = f'source {cann_script} && env'
env = subprocess.check_output(f"bash -lc '{env_cmd}'", shell=True, text=True, cwd=REPO_ROOT)
for line in env.splitlines():
    if '=' in line:
        os.environ.__setitem__(*line.split('=', 1))

RECIPE_ROOT = TUTORIAL_DIR / 'src/inference_scripts/recipe_qwen3_8b'
QMM_CUSTOM_DIR = SRC_DIR / 'qmm_custom'

print('教程目录 =', TUTORIAL_DIR)
print('推理模型目录 =', RECIPE_ROOT)
print('算子相关文件目录 =', SRC_DIR)
print('算子实现目录 =', QMM_CUSTOM_DIR)
print('[环境准备] 完成', flush=True)
```

安装所需的依赖：

```bash
%pip install -r {SRC_DIR}/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn
```

---
### 2 A8W8 量化 matmul 算子概念

#### 2.1 什么是 A8W8 量化

A8W8 量化是 LLM 推理中常用的一种量化方案：
- **A（Activation）**：将输入激活值从 BF16/FP16 量化为 **INT8**
- **W（Weight）**：将权重从 BF16/FP16 量化为 **INT8**
- **反量化**：计算结果 `INT8 × INT8 → INT32` 后，通过 Scale 反量化回浮点精度

> **术语说明**：A8W8 与第 5 章使用的 W8A8 是同一种 INT8 激活 + INT8 权重量化方案的不同写法，本章沿用 A8W8 命名。仓库中 YAML 配置文件名（如 `qwen3_8b_a8w8_1tp.yaml`）和类名（`CompressedTensorsW8A8Int8LinearMethod`）也分别使用了这两种写法。

#### 2.2 算子规格

在上一章中，通过分析量化模型的profiling，归纳出了自定义算子的输入输出规格：

| 算子名称 | QmmCustom |
|------|-----|
| 输入 x1 (A) | INT8, ND 格式, shape [M, K] |
| 输入 x2 (B) | INT8, **FRACTAL_NZ** 格式, shape [K, N] |
| 输入 scale | FLOAT32, ND 格式, shape [N] |
| 输入 pertoken_scale | FLOAT32, ND 格式, shape [M]（可选） |
| 输出 y | 有 perTokenScale → BF16，无 → INT32；ND 格式, shape [M, N] |
| 架构 | ascend910b |

**注意**：x2 权重矩阵使用 **FRACTAL_NZ** 格式，这是昇腾 AI Core Cube 单元的高效存储格式，能提升 matmul 计算性能。

#### 2.3 Scale 模式

QmmCustom 算子支持两种 Scale：

| Scale 类型 | Shape | 作用 | 
|-----------|-------|------|
| **perChannelScale** | `[N]` | 对每个输出通道单独缩放 |
| **perTokenScale** | `[M]` | 对每行输入单独缩放 |

计算公式：
```
result_bf16 = (x1_int8 @ x2_int8) * perChannelScale * perTokenScale
```

### 3 自定义算子实现

与前面学习过的内容一致，本次实践采用 `<<<>>>` Kernel 直调方式开发上述原型的量化 matmul 算子。直调方式通过 `kernel<<<numBlocks, dynUBufSize, stream>>>(args)` 语法在 Host 侧直接启动 Kernel，适合快速验证算子功能与性能。

本节包含如下三个任务：

#### 任务一：自行设计 TilingData 结构体并实现 Tiling 函数

根据算子原型与 Kernel 的实现需求，自行设计 `QmmCustomTilingData` 结构体，并实现 `CalcQmmTiling` 函数。Tiling 函数需根据输入的 M、N、K 维度，结合平台硬件资源（L1/L0A/L0B/UB 内存限制、可用核数），计算多核分块参数。可借助 `platform_ascendc::PlatformAscendCManager` 获取硬件信息。

> **Tiling 设计提示**：
> 
> 设计 TilingData 时需要考虑以下要素：
> 1. **`TCubeTiling`**：CANN Matmul 库提供的标准 Tiling 结构体，包含 M/N/K 的分块大小（`baseM`、`baseN`、`baseK`）、使用的核数（`usedCoreNum`）等字段。可通过 `GetMatmulTiling` API 自动计算。
> 2. **`isPertoken`**：标记是否走反量化路径，用于 Kernel 内部分支选择。
> 3. **`workspaceSize`**：Path 2 中 Cube 写入 INT32 中间结果所需的 GM workspace 大小。
> 4. **多核分块策略**：将 M 维度或 N 维度分配到多个核上并行计算，每个核处理一个分块。分块大小需平衡 L1/L0A/L0B 缓存利用率与多核负载均衡。

#### 任务二：实现 A8W8 输入、INT32 输出的 Kernel

实现 `QmmCubeBasicKernel` 类，完成纯 Cube 路径的 INT8 矩阵乘法计算。

计算公式： ```result_int32 = x1_int8 @ x2_int8```

#### 任务三：实现 A8W8 输入、经 perChannelScale 和 perTokenScale 反量化输出 BF16 的 Kernel

实现 `QmmPertokenKernel` 类，在 Cube 计算的基础上增加 Vector 反量化路径。

计算公式： ```result_bf16 = (x1_int8 @ x2_int8) * perChannelScale * perTokenScale```

其中 `perChannelScale` 沿 N 维广播，`perTokenScale` 沿 M 维广播，两者均为 FLOAT32 类型。

---

#### 执行路径说明

在 Host 侧的 `qmm_custom` 函数中，根据是否传入 `pertoken_scale` 设置 `isPertoken` 标志，Kernel 启动时据此选择执行路径：

| 路径 | 条件 | 计算流程 | 输出类型 |
|------|------|----------|----------|
| **Path 1: Cube-only** | `isPertoken == 0` | INT8 matmul → INT32 | INT32 |
| **Path 2: Cube+Vector** | `isPertoken == 1` | INT8 matmul → INT32 → dequant(scale×pertoken) → BF16 | BF16 |

**Path 1（Cube-only）**：仅使用 AI Core 的 Cube 计算单元，完成 INT8×INT8 矩阵乘法后直接将 INT32 结果写入输出 GM，无 Vector 参与。对应 `QmmCubeBasicKernel` 的实现。

**Path 2（Cube+Vector）**：Cube 单元先完成 INT8 matmul 得到 INT32 中间结果并写入 GM workspace；随后 Vector 单元从 GM 读取 INT32 结果，依次完成 `Cast`（INT32→FLOAT32）、乘以 `perChannelScale` 和 `perTokenScale`、`Cast`（FLOAT32→BF16）等反量化操作，最终将 BF16 结果写入输出 GM。对应 `QmmPertokenKernel` 的实现。

Kernel 入口函数 `qmm_custom_kernel` 使用 `__mix__(1, 2)` 属性声明，表示为每个 Block 分配 1 个 Cube 核和 2 个 Vector 核，使 Cube 与 Vector 可在同一 Kernel 中协同工作。Kernel 内部通过 `tilingData.isPertoken` 判断走哪条路径，两条路径复用相同的 Tiling 结构和 Kernel 启动入口。

Tiling、Kernel、Torch 接口的实现均位于 `qmm_custom.asc` 文件中。文件已给出整体框架与函数签名，请自行完成下方代码中的 TODO 部分，以实现完整的自定义算子：

```bash
%%writefile {QMM_CUSTOM_DIR}/qmm_custom.asc
#include "acl/acl_base.h"
#include "acl/acl_prof.h"
#include "kernel_operator.h"
#include "lib/matmul_intf.h"
#include "tiling/platform/platform_ascendc.h"
#include "tiling/tiling_api.h"
#include "torch_npu/csrc/core/npu/NPUStream.h"
#include <torch/extension.h>

// TODO: 任务一: 自行设计tilingdata结构体并实现tiling函数

#pragma pack(push, 8)
struct alignas(8) QmmCustomTilingData {
  // TODO: 自行设计tilingData结构体
  TCubeTiling cubeTilingData;
  uint32_t isPertoken;
  uint32_t workspaceSize;
  //......
};
#pragma pack(pop)

// 计算QmmCustom tiling参数,返回tilingData结构体
static QmmCustomTilingData CalcQmmTiling(uint32_t isPertoken, uint32_t M,
                                         uint32_t N, uint32_t K) {
  QmmCustomTilingData tilingData;
  auto ascendcPlatform =
      platform_ascendc::PlatformAscendCManager::GetInstance();
  // TODO: 自行实现tiling函数, 返回tilingData结构体 
  //......
  return tilingData;
}

// TODO: 任务二: 实现A8W8输入INT32输出的kernel

class QmmCubeBasicKernel {
public:
    __aicore__ inline QmmCubeBasicKernel() {}

    __aicore__ inline void Init(GM_ADDR x1, GM_ADDR x2, GM_ADDR scale, GM_ADDR y,
                                GM_ADDR workSpace, const QmmCustomTilingData *__restrict tilingData, AscendC::TPipe *tPipe);

    __aicore__ inline void Process();
};

__aicore__ inline void QmmCubeBasicKernel::Init(
    GM_ADDR x1, GM_ADDR x2, GM_ADDR scale, GM_ADDR y,
    GM_ADDR workSpace, const QmmCustomTilingData *__restrict tilingData, AscendC::TPipe *tPipe)
{
    // TODO: 实现kernel初始化
}

__aicore__ inline void QmmCubeBasicKernel::Process()
{
    // TODO: 实现kernel执行
}

// TODO: 任务三: 实现A8W8输入, 经过perChannelScale和perTokenScale反量化输出BF16的kernel

class QmmPertokenKernel {
public:
    __aicore__ inline QmmPertokenKernel() {}

    __aicore__ inline void Init(GM_ADDR x1, GM_ADDR x2, GM_ADDR scale, GM_ADDR pertokenScale, GM_ADDR y,
                                GM_ADDR workSpace, const QmmCustomTilingData *__restrict tilingData,
                                AscendC::TPipe *tPipe);

    __aicore__ inline void Process();
};

__aicore__ inline void QmmPertokenKernel::Init(
    GM_ADDR x1, GM_ADDR x2, GM_ADDR scale, GM_ADDR pertokenScale, GM_ADDR y,
    GM_ADDR workSpace, const QmmCustomTilingData *__restrict tilingData,
    AscendC::TPipe *tPipe)
{
    // TODO: 实现kernel初始化
}

__aicore__ inline void QmmPertokenKernel::Process()
{
    // TODO: 实现kernel执行
}


__global__ __mix__(1, 2) __aicore__
    void qmm_custom_kernel(GM_ADDR x1, GM_ADDR x2, GM_ADDR scale,
                           GM_ADDR pertoken_scale, GM_ADDR y, GM_ADDR workspace,
                           QmmCustomTilingData tilingData) {
  if (workspace == nullptr) {
    return;
  }
  AscendC::TPipe pipe;

  if (tilingData.isPertoken == 0) {
    QmmCubeBasicKernel kernel;
    kernel.Init(x1, x2, scale, y, workspace, &tilingData, &pipe);
    kernel.Process();
    pipe.Destroy();
  } else {
    QmmPertokenKernel kernel;
    kernel.Init(x1, x2, scale, pertoken_scale, y, workspace, &tilingData,
                &pipe);
    kernel.Process();
    pipe.Destroy();
  }
}

#ifndef ACL_PROF_TENSOR_INFO_DEFINED
#define ACL_PROF_TENSOR_INFO_DEFINED
struct aclprofTensor {
  uint32_t type;     // Tensor类型: 0表示输入, 1表示输出。
  uint32_t format;   // Format类型, 对应aclFormat。
  uint32_t dataType; // 数据类型, 对应aclDataType。
  uint32_t shapeDim; // Shape维度数量, 最大支持8维。
  uint32_t shape[8]; // Shape信息。
};

struct aclprofTensorInfo {
  uint64_t opNameId; // 通过uint64_t aclprofStr2Id(const char *message)转化
  uint64_t opTypeId; // 通过uint64_t aclprofStr2Id(const char *message)转化
  uint32_t resv;
  uint32_t tensorNum;
  uint32_t kernelType;
  uint32_t blockNums;
  void *stream;
  aclprofTensor *tensors;
};

struct aclprofEventAttributes {
  uint16_t version;
  uint16_t size;
  uint32_t messageType;
  union message {
    aclprofTensorInfo *tensorInfo;
  } message;
};
#endif // ACL_PROF_TENSOR_INFO_DEFINED

#define INPUT(x)                                                               \
  aclprofTensor {                                                              \
    (uint32_t)0,                                                               \
        static_cast<uint32_t>(                                                 \
            ascendc_ops::GetFormat(static_cast<int64_t>(x.sizes().size()))),   \
        static_cast<uint32_t>(ascendc_ops::GetAclDataType(x.scalar_type())),   \
        static_cast<uint32_t>(x.sizes().size()), {                             \
      static_cast<uint32_t>(x.sizes().size() > 0 ? x.sizes().data()[0] : 0),   \
          static_cast<uint32_t>(x.sizes().size() > 1 ? x.sizes().data()[1]     \
                                                     : 0),                     \
          static_cast<uint32_t>(x.sizes().size() > 2 ? x.sizes().data()[2]     \
                                                     : 0),                     \
          static_cast<uint32_t>(x.sizes().size() > 3 ? x.sizes().data()[3]     \
                                                     : 0)                      \
    }                                                                          \
  }

#define OUTPUT(z)                                                              \
  aclprofTensor {                                                              \
    (uint32_t)1,                                                               \
        static_cast<uint32_t>(                                                 \
            ascendc_ops::GetFormat(static_cast<int64_t>(z.sizes().size()))),   \
        static_cast<uint32_t>(ascendc_ops::GetAclDataType(z.scalar_type())),   \
        static_cast<uint32_t>(z.sizes().size()), {                             \
      static_cast<uint32_t>(z.sizes().size() > 0 ? z.sizes().data()[0] : 0),   \
          static_cast<uint32_t>(z.sizes().size() > 1 ? z.sizes().data()[1]     \
                                                     : 0),                     \
          static_cast<uint32_t>(z.sizes().size() > 2 ? z.sizes().data()[2]     \
                                                     : 0),                     \
          static_cast<uint32_t>(z.sizes().size() > 3 ? z.sizes().data()[3]     \
                                                     : 0)                      \
    }                                                                          \
  }

#define INIT_ACL_PROF_TENSOR_INFO(opName, opType, blockdim, kernelType,        \
                                  tensorInfo, stream, ...)                     \
  uint64_t opNameId = aclprofStr2Id(opName);                                   \
  uint64_t opTypeId = aclprofStr2Id(opType);                                   \
  struct aclprofTensor tensors[] = {__VA_ARGS__};                              \
  tensorInfo = {                                                               \
      opNameId,   opTypeId, 0,      sizeof(tensors) / sizeof(aclprofTensor),   \
      kernelType, blockdim, stream, tensors}

namespace ascendc_ops {

aclDataType GetAclDataType(at::ScalarType scalarType) {
  switch (scalarType) {
  case at::ScalarType::Float:
    return ACL_FLOAT;
  case at::ScalarType::Int:
    return ACL_INT32;
  case at::ScalarType::BFloat16:
    return ACL_BF16;
  case at::ScalarType::Byte:
    return ACL_UINT8;
  case at::ScalarType::Char:
    return ACL_INT8;
  default:
    TORCH_CHECK(false,
                "Unsupported tensor dtype for profiling report: ", scalarType);
  }
}

aclFormat GetFormat(int64_t dimNum) {
  aclFormat format = ACL_FORMAT_ND;
  if (dimNum == 4) {
    format = ACL_FORMAT_FRACTAL_NZ;
  }
  return format;
}

at::Tensor qmm_custom(const at::Tensor &x1, const at::Tensor &x2,
                      const at::Tensor &scale,
                      const c10::optional<at::Tensor> &pertoken_scale) {
  auto aclStream = c10_npu::getCurrentNPUStream().stream(true);

  auto M = x1.size(0);
  auto K = x1.size(1);
  auto N = x2.size(1);

  uint32_t isPertoken =
      pertoken_scale.has_value() && pertoken_scale.value().defined() ? 1 : 0;
  at::ScalarType output_dtype =
      isPertoken ? at::ScalarType::BFloat16 : at::ScalarType::Int;
  at::Tensor y = at::empty({M, N}, x1.options().dtype(output_dtype));

  QmmCustomTilingData tilingData = CalcQmmTiling(isPertoken, M, N, K);
  uint32_t numBlocks = tilingData.cubeTilingData.usedCoreNum;

  at::Tensor workspaceTensor =
      at::empty({static_cast<int64_t>(tilingData.workspaceSize)},
                x1.options().dtype(at::ScalarType::Byte));

  aclprofTensorInfo tensorInfo;
  uint64_t opNameId = aclprofStr2Id("qmm_custom");
  uint64_t opTypeId = aclprofStr2Id("QmmCustom");
  uint8_t *pertokenPtr =
      isPertoken ? (uint8_t *)(pertoken_scale.value().mutable_data_ptr())
                 : nullptr;
  std::vector<aclprofTensor> tensors = {INPUT(x1), INPUT(x2), INPUT(scale)};
  if (isPertoken) {
    tensors.push_back(INPUT(pertoken_scale.value()));
  }
  tensors.push_back(OUTPUT(y));
  tensorInfo = {opNameId, opTypeId,  0,         (uint32_t)tensors.size(),
                0,        numBlocks, aclStream, tensors.data()};

  aclprofEventAttributes attrs = {1, sizeof(aclprofEventAttributes::message), 0,
                                  &tensorInfo};

  aclprofRangePushEx(&attrs);
  qmm_custom_kernel<<<numBlocks, 0, aclStream>>>(
      (uint8_t *)(x1.mutable_data_ptr()), (uint8_t *)(x2.mutable_data_ptr()),
      (uint8_t *)(scale.mutable_data_ptr()), pertokenPtr,
      (uint8_t *)(y.mutable_data_ptr()), workspaceTensor.data_ptr<uint8_t>(),
      tilingData);
  aclprofRangePop();
  return y;
}
} // namespace ascendc_ops

TORCH_LIBRARY(ascendc_ops, m) {
  m.def("qmm_custom(Tensor x1, Tensor x2, Tensor scale, Tensor? "
        "pertoken_scale=None) -> Tensor");
}

TORCH_LIBRARY_IMPL(ascendc_ops, PrivateUse1, m) {
  m.impl("qmm_custom", TORCH_FN(ascendc_ops::qmm_custom));
}
```

---
### 4 编译自定义算子

#### 任务四：成功编译自定义算子


在算子目录下执行编译命令：

```bash
!cd {QMM_CUSTOM_DIR} && mkdir -p build && cd build && cmake -DCMAKE_ASC_ARCHITECTURES=dav-2201 .. && make -j;
```

编译成功后会在build目录下生成ascendc_ops.so

---
### 5 测试自定义算子功能性能

#### 任务五：根据提供的测试脚本，测试自定义算子功能与性能，尝试对自定义算子进行优化后重复整个流程

使用测试脚本验证 QmmCustom 算子在不同规格输入下的精度和性能。测试脚本覆盖多组 (M, K, N) 规格，分别验证 INT32 输出（无 perTokenScale）和 BF16 输出（有 perTokenScale）两种路径。

核心接口调用如下：

```python
output_npu = torch.ops.ascendc_ops.qmm_custom(x1_npu, x2_npu, scale_npu, pertoken_scale_npu)
```

#### 5.1 测试算子功能

需要测试的 cases 的 shape 如下，对应的是 Qwen3-8B 模型中实际出现的调用，**全部通过**视为算子功能OK：
| M    | K     | N     |
| ---- | ----- | ----- |
| 1    | 4096  | 4096  |
| 1    | 4096  | 6144  |
| 1    | 4096  | 24576 |
| 1    | 12288 | 4096  |
| 50   | 4096  | 4096  |
| 50   | 4096  | 6144  |
| 50   | 4096  | 24576 |
| 50   | 12288 | 4096  |
| 4096 | 4096  | 4096  |
| 4096 | 4096  | 6144  |
| 4096 | 4096  | 24576 |
| 4096 | 12288 | 4096  |

```python
import torch
import torch_npu
torch.ops.load_library(str(QMM_CUSTOM_DIR / "build/libascendc_ops.so"))

torch.npu.config.allow_internal_format = True
torch.npu.config.allow_hf32 = False
torch.npu.set_compile_mode(jit_compile=False)

# ============================================================
# 测试配置: 多组 (M, K, N) 规格
# ============================================================
TEST_SHAPES = [
    (1, 4096, 4096),
    (1, 4096, 6144),
    (1, 4096, 24576),
    (1, 12288, 4096),
    (50, 4096, 4096),
    (50, 4096, 6144),
    (50, 4096, 24576),
    (50, 12288, 4096),
    (4096, 4096, 4096),
    (4096, 4096, 6144),
    (4096, 4096, 24576),
    (4096, 12288, 4096),
]


def check_close(output, ref, dtype):
    """统一的精度比对函数，根据输出 dtype 使用不同的 tolerance"""
    if dtype == torch.int32:
        # 整数运算应精确匹配，tolerance 为 0
        rtol, atol = 0, 0
    else:
        # BF16 允许浮点舍入误差
        rtol, atol = 0.01, 0.01

    output_f = output.to(torch.float32)
    ref_f = ref.to(torch.float32)
    passed = torch.allclose(output_f, ref_f, rtol=rtol, atol=atol)

    label = 'INT32' if dtype == torch.int32 else 'BF16'
    print(f"  {label} allclose验证: {'PASS' if passed else 'FAIL'}")

    if not passed:
        print(f"  output[0,0:5] = {output[0, 0:5].tolist()}")
        print(f"  ref[0,0:5]    = {ref[0, 0:5].tolist()}")

    return passed


def test_int32(M, K, N):
    """无 pertoken_scale, 纯INT8 matmul, INT32 输出"""
    x1_cpu = torch.randint(-128, 127, (M, K), dtype=torch.int8)
    x2_cpu = torch.randint(-128, 127, (K, N), dtype=torch.int8)
    scale_cpu = torch.randn([N], dtype=torch.float32)

    x1_npu = x1_cpu.npu()
    x2_npu = x2_cpu.npu()
    x2_npu = torch_npu.npu_format_cast(x2_npu, 29)  # 29: FORMAT_FRACTAL_NZ
    scale_npu = scale_cpu.npu()

    output_npu = torch.ops.ascendc_ops.qmm_custom(x1_npu, x2_npu, scale_npu, pertoken_scale=None)
    output_cpu = output_npu.cpu()

    # float64 matmul 走 BLAS 优化, 比 int32 朴素乘加快很多;
    # float64 精度足够精确表示 int32 范围内的整数结果
    ref_output = torch.matmul(x1_cpu.to(torch.float64), x2_cpu.to(torch.float64)).round().to(torch.int32)

    assert output_cpu.shape == ref_output.shape, f"shape不一致: {output_cpu.shape} vs {ref_output.shape}"
    assert output_cpu.dtype == torch.int32, f"输出dtype不正确: {output_cpu.dtype}"

    return check_close(output_cpu, ref_output, torch.int32)


def test_bf16(M, K, N):
    """有 pertoken_scale, INT8 matmul + dequant, BF16 输出"""
    x1_cpu = torch.randint(-128, 127, (M, K), dtype=torch.int8)
    x2_cpu = torch.randint(-128, 127, (K, N), dtype=torch.int8)
    scale_cpu = torch.randn([N], dtype=torch.float32)
    pertoken_scale_cpu = torch.randn([M], dtype=torch.float32)

    x1_npu = x1_cpu.npu()
    x2_npu = x2_cpu.npu()
    x2_npu = torch_npu.npu_format_cast(x2_npu, 29)  # 29: FORMAT_FRACTAL_NZ
    scale_npu = scale_cpu.npu()
    pertoken_scale_npu = pertoken_scale_cpu.npu()

    output_npu = torch.ops.ascendc_ops.qmm_custom(x1_npu, x2_npu, scale_npu,
                                                  pertoken_scale=pertoken_scale_npu)
    output_cpu = output_npu.cpu()

    int32_result = torch.matmul(x1_cpu.to(torch.float64), x2_cpu.to(torch.float64)).round().to(torch.int32)
    ref_bf16 = (int32_result.to(torch.float32) * scale_cpu.unsqueeze(0) * pertoken_scale_cpu.unsqueeze(1)).to(torch.bfloat16)

    assert output_cpu.shape == ref_bf16.shape, f"shape不一致: {output_cpu.shape} vs {ref_bf16.shape}"
    assert output_cpu.dtype == torch.bfloat16, f"输出dtype不正确: {output_cpu.dtype}"

    return check_close(output_cpu, ref_bf16, torch.bfloat16)


# ============================================================
# 主循环: 对每组 (M, K, N) 执行 INT32 和 BF16 测试
# ============================================================
int32_results = []
bf16_results = []

for i, (M, K, N) in enumerate(TEST_SHAPES, 1):
    print("=" * 60)
    print(f"规格{i}: M={M}, K={K}, N={N}")
    print("=" * 60)

    print("[INT32 测试]")
    int32_pass = test_int32(M, K, N)
    int32_results.append((M, K, N, int32_pass))

    print("[BF16 测试]")
    bf16_pass = test_bf16(M, K, N)
    bf16_results.append((M, K, N, bf16_pass))

# ============================================================
# 测试汇总
# ============================================================
print()
print("=" * 60)
print("测试汇总")
print("=" * 60)
print(f"{'规格':>24} | {'INT32':^8} | {'BF16':^8}")
print("-" * 46)
for (M, K, N, p1), (_, _, _, p2) in zip(int32_results, bf16_results):
    tag = f"M={M},K={K},N={N}"
    print(f"{tag:>24} | {'PASS' if p1 else 'FAIL':^8} | {'PASS' if p2 else 'FAIL':^8}")

int32_total = sum(p for _, _, _, p in int32_results)
bf16_total = sum(p for _, _, _, p in bf16_results)
total = len(TEST_SHAPES)
print(f"INT32: {int32_total}/{total} 通过, BF16: {bf16_total}/{total} 通过")
print("=" * 60)
```

#### 5.2 测试算子性能
基于torch_npu.profiler来测试算子性能，执行下面的code cell测试单算子性能数据：

```python
import os
import csv
from pathlib import Path

# ============================================================
# Profiler 配置
# ============================================================
PROF_OUTPUT_DIR = str(SRC_DIR / "prof_output")  # 采集数据的存放路径
WARMUP_ITERS = 0      # warmup 步数, 不采集数据

def parse_kernel_details(csv_path):
    """解析 kernel_details.csv, 提取 QmmCustom 每次执行的 Duration
    """
    rows = []
    with open(csv_path, newline="", encoding="utf-8", errors="replace") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row.get("Name", "")
            if "QmmCustom" not in name:
                continue

            # 解析 Input Shapes: 格式如 "1,4096;4096,4096;4096;"
            raw_shapes = row.get("Input Shapes", "").strip('"')
            parts = [p.strip() for p in raw_shapes.split(";")]
            x1_shape = parts[0].split(",")  # (M, K)
            x2_shape = parts[1].split(",")  # (K, N)
            M = int(x1_shape[0])
            K = int(x1_shape[1])
            N = int(x2_shape[1])

            # 从 Output Data Types 判断 dtype
            out_dtype_raw = row.get("Output Data Types", "").strip('"')
            dtype_tag = "INT32" if "INT32" in out_dtype_raw else "BF16"

            # Duration(us)
            duration_us = float(row.get("Duration(us)", "0") or "0")

            rows.append({
                "M": M, "K": K, "N": N,
                "dtype": dtype_tag,
                "duration_us": duration_us,
            })
    return rows


def find_kernel_details_csv(prof_dir):
    prof_path = Path(prof_dir)
    if not prof_path.exists():
        return None
    # 找出所有包含 ASCEND_PROFILER_OUTPUT/kernel_details.csv 的子目录
    candidates = []
    for subdir in sorted(prof_path.iterdir(), key=lambda d: d.name, reverse=True):
        csv_path = subdir / "ASCEND_PROFILER_OUTPUT" / "kernel_details.csv"
        if csv_path.exists():
            candidates.append(csv_path)
            break  # sorted reverse=True, 第一个就是最新的
    return str(candidates[0]) if candidates else None

# ============================================================
# 主流程: 先 warmup, 再开启 profiler 采集, 最后汇总
# ============================================================
int32_results = []
bf16_results = []

# warmup: 不采集数据, 让 NPU 稳定
if WARMUP_ITERS>0:
    print("=" * 60)
    print(f"Warmup: 运行 {WARMUP_ITERS} 轮不采集数据")
    print("=" * 60)
    for i, (M, K, N) in enumerate(TEST_SHAPES, 1):
        test_int32(M, K, N)
        test_bf16(M, K, N)

# 创建 profiler
os.makedirs(PROF_OUTPUT_DIR, exist_ok=True)
profiler = torch_npu.profiler.profile(
    activities=[
        torch_npu.profiler.ProfilerActivity.NPU,
        torch_npu.profiler.ProfilerActivity.CPU,
    ],
    experimental_config=torch_npu.profiler._ExperimentalConfig(
        profiler_level=torch_npu.profiler.ProfilerLevel.Level1,
        aic_metrics=torch_npu.profiler.AiCMetrics.PipeUtilization,
    ),
    on_trace_ready=torch_npu.profiler.tensorboard_trace_handler(PROF_OUTPUT_DIR),
)

# 开启 profiler 采集
profiler.start()

for i, (M, K, N) in enumerate(TEST_SHAPES, 1):
    print("=" * 60)
    print(f"规格{i}: M={M}, K={K}, N={N}")
    print("=" * 60)

    print("[INT32 测试]")
    int32_pass = test_int32(M, K, N)
    int32_results.append((M, K, N, int32_pass))
    profiler.step()

    print("[BF16 测试]")
    bf16_pass = test_bf16(M, K, N)
    bf16_results.append((M, K, N, bf16_pass))
    profiler.step()

# 停止 profiler
profiler.stop()

# ============================================================
# 测试汇总
# ============================================================
print()
print("=" * 60)
print("测试汇总")
print("=" * 60)
print(f"{'规格':>24} | {'INT32':^8} | {'BF16':^8}")
print("-" * 46)
for (M, K, N, p1), (_, _, _, p2) in zip(int32_results, bf16_results):
    tag = f"M={M},K={K},N={N}"
    print(f"{tag:>24} | {'PASS' if p1 else 'FAIL':^8} | {'PASS' if p2 else 'FAIL':^8}")

int32_total = sum(p for _, _, _, p in int32_results)
bf16_total = sum(p for _, _, _, p in bf16_results)
total = len(TEST_SHAPES)
print(f"INT32: {int32_total}/{total} 通过, BF16: {bf16_total}/{total} 通过")

# ============================================================
# Profiler 数据汇总: 每种规格每种 dtype 的 Duration(us)
# ============================================================
print()
print("=" * 70)
print("Profiler 数据汇总 (QmmCustom Duration)")
print("=" * 70)

csv_path = find_kernel_details_csv(PROF_OUTPUT_DIR)
print(f"原始数据路径：{csv_path}")
if csv_path:
    kernel_rows = parse_kernel_details(csv_path)
    if kernel_rows:
        # 按 (M, K, N) 分组, 每组内有 INT32 和 BF16
        shape_map = {}
        for kr in kernel_rows:
            key = (kr["M"], kr["K"], kr["N"])
            shape_map.setdefault(key, {})[kr["dtype"]] = kr["duration_us"]

        print(f"{'规格 (M,K,N)':>24} | {'INT32 Duration(us)':>18} | {'BF16 Duration(us)':>18}")
        print("-" * 70)
        for M, K, N in TEST_SHAPES:
            key = (M, K, N)
            int32_dur = shape_map.get(key, {}).get("INT32", "-")
            bf16_dur = shape_map.get(key, {}).get("BF16", "-")
            int32_str = f"{int32_dur:.3f}" if isinstance(int32_dur, float) else int32_dur
            bf16_str = f"{bf16_dur:.3f}" if isinstance(bf16_dur, float) else bf16_dur
            tag = f"M={M},K={K},N={N}"
            print(f"{tag:>24} | {int32_str:>18} | {bf16_str:>18}")
    else:
        print(f"在 {csv_path} 中未找到 QmmCustom 算子数据")
else:
    print(f"未在 {PROF_OUTPUT_DIR} 中找到 kernel_details.csv 文件")
    print("请检查 profiler 输出目录")

print("=" * 70)
```

---
### 6 自定义算子接入模型

#### 6.1 定位替换点

Qwen3-8B 推理框架中的 W8A8 量化 matmul 通过 `CompressedTensorsW8A8Int8LinearMethod` 类实现，其 `apply_weights` 方法中使用 `torch_npu.npu_quant_matmul` 执行 INT8 量化矩阵乘法。我们需要将这个调用替换为自定义的 `torch.ops.ascendc_ops.qmm_custom` 算子。

查看原始实现：

```bash
!grep -n 'npu_quant_matmul' {RECIPE_ROOT}/module/quantization/compressed_tensors/compressed_tensors_w8a8_int8.py
```

#### 6.2 替换实现

在 `CompressedTensorsW8A8Int8LinearMethod` 中，将 `torch_npu.npu_quant_matmul` 替换为 `torch.ops.ascendc_ops.qmm_custom`。

替换后的方法为：

```python
torch.ops.load_library(str(QMM_CUSTOM_DIR / "build/libascendc_ops.so"))

def apply_weights(self, layer: torch.nn.Module,
                x: torch.Tensor,
                bias: Optional[torch.Tensor],
                dynamic_scale: Optional = None,
                out_dtype: Optional = torch.bfloat16
                ) -> Union[torch.Tensor, Dict[str, Any]]:
    if dynamic_scale is not None:
        x_scale = dynamic_scale
    else:
        x, x_scale = torch_npu.npu_dynamic_quant(x, smooth_scales=layer.smooth_scales)
    out_shape_dim_0 = x.size()[:-1]
    x = x.view(-1, x.size(-1))
    x_scale = x_scale.view(-1)

    # --- 替换核心: npu_quant_matmul → qmm_custom ---
    x = torch.ops.ascendc_ops.qmm_custom(x, layer.weight, 
                                layer.weight_scale.view(-1),
                                pertoken_scale=None if out_dtype == torch.int32 else x_scale)
    # --- 替换结束 ---

    x = x.view(out_shape_dim_0 + (-1, ))
    if out_dtype == torch.int32:
        return x, x_scale
    else:
        return x
```

执行如下操作替换推理网络中调用的接口实现：

```python
# 6.2 替换实现: 将 torch_npu.npu_quant_matmul 替换为 torch.ops.ascendc_ops.qmm_custom

# 1: 导入libascendc_ops.so
W8A8_FILE = RECIPE_ROOT / 'module/quantization/compressed_tensors/compressed_tensors_w8a8_int8.py'
print('[替换] 目标文件:', W8A8_FILE)

# 备份原始内容，仅在首次执行时保存，避免重复执行时覆盖为已修改的代码
if 'W8A8_ORIGINAL_CODE' not in dir():
    W8A8_ORIGINAL_CODE = W8A8_FILE.read_text(encoding='utf-8')

ct_code = W8A8_FILE.read_text(encoding='utf-8')
_lib_path = str(QMM_CUSTOM_DIR / "build/libascendc_ops.so")
_load_lib_stmt = 'torch.ops.load_library(r"' + _lib_path + '")'
if _load_lib_stmt not in ct_code:
    # 在 'import torch' 行后插入 'torch.ops.load_library'
    ct_code = ct_code.replace('import torch\n', 'import torch\n' + _load_lib_stmt + '\n')
    W8A8_FILE.write_text(ct_code, encoding='utf-8')
    print('[插入] compressed_tensors.py: 已添加 torch.ops.load_library')
else:
    print('[插入] compressed_tensors.py: torch.ops.load_library 已存在，跳过')

# 2: 在 compressed_tensors_w8a8_int8.py 中替换 npu_quant_matmul → qmm_custom
code = W8A8_FILE.read_text(encoding='utf-8')

# 替换 npu_quant_matmul 调用为 qmm_custom 调用
old_call = (
    'x = torch_npu.npu_quant_matmul(x, layer.weight,\n'
    '                                    layer.weight_scale.view(-1),\n'
    '                                    pertoken_scale=None if out_dtype == torch.int32 else x_scale,\n'
    '                                    bias=layer.bias,\n'
    '                                    output_dtype=out_dtype)'
)
new_call = (
    '# --- 替换核心: npu_quant_matmul → qmm_custom ---\n'
    '        x = torch.ops.ascendc_ops.qmm_custom(x, layer.weight,\n'
    '                                    layer.weight_scale.view(-1),\n'
    '                                    pertoken_scale=None if out_dtype == torch.int32 else x_scale)\n'
    '        # --- 替换结束 ---'
)

if old_call in code:
    code = code.replace(old_call, new_call)
    W8A8_FILE.write_text(code, encoding='utf-8')
    print('[替换] 成功: npu_quant_matmul → qmm_custom')
else:
    print('[替换] 文件中未找到 npu_quant_matmul 调用，可能已替换')

# 验证替换结果
result = W8A8_FILE.read_text(encoding='utf-8')
if 'torch.ops.ascendc_ops.qmm_custom' in result:
    print('[验证] 替换已生效，当前使用 qmm_custom 算子')
else:
    print('[验证] 替换未生效，请检查文件内容')
```

#### 6.3 替换实现后执行量化推理

指定本地的量化模型权重路径，调用infer.sh执行量化推理，查看 W8A8 量化模型推理生成的文本，对比替换前的生成文本是否一致。

**注意：需要先完成第五章的量化模型推理过程，并将`W8A8_WEIGHT`指定为本地的量化模型权重的路径**

```python
import sys, subprocess, os
from inference_scripts.recipe_workflow import prepare_runtime_yaml

# 将W8A8_WEIGHT设置为量化模型权重实际所在路径
W8A8_WEIGHT = TUTORIAL_DIR / 'src/data/models/Qwen3-8B-W8A8'

YAML_A8W8_TEMPLATE =  RECIPE_ROOT / 'models/qwen/config/qwen3_8b_a8w8_1tp.yaml'
YAML_A8W8_CUSTOM  = RECIPE_ROOT / 'models/qwen/config/qwen3_8b_a8w8_custom.yaml'
prepare_runtime_yaml(YAML_A8W8_TEMPLATE, YAML_A8W8_CUSTOM, model_path=str(W8A8_WEIGHT))

env = os.environ.copy()
python_dir = os.path.dirname(sys.executable)
env["PATH"] = python_dir + ":" + env.get("PATH", "")
result = subprocess.run(
    ['bash', 'executor/scripts/infer.sh', '--model', 'qwen', '--yaml', YAML_A8W8_CUSTOM],
    cwd=str(RECIPE_ROOT),
    env=env,
    check=True,
)
```

---
### 7 模型性能测试

#### 任务六：测试模型性能，尝试对自定义算子进行优化后重复上述流程

将 QmmCustom 算子接入模型后，使用 Profiling 工具观测模型推理性能，对比自定义算子替换前后的 matmul 耗时变化。

#### 7.1 准备 Profiling YAML

沿用 recipes 的 YAML + `infer.sh` 工作流，在配置中打开 Profiler，运行一次推理并收集性能数据。

通过如下操作将 YAML 配置中的enable_profiler配置为 True ：

```python
from inference_scripts.recipe_workflow import prepare_profiling_yaml

YAML_A8W8_CUSTOM_PROFILER = RECIPE_ROOT / 'models/qwen/config/qwen3_8b_a8w8_custom_profiler.yaml'

prepare_profiling_yaml(YAML_A8W8_CUSTOM, YAML_A8W8_CUSTOM_PROFILER, enable_profiler=True)
```

#### 7.2 启动 Profiling 推理

使用 recipes 命令启动带 Profiler 的推理，推理结束后会在结果目录中生成 `prof/` 产物。

```python
result = subprocess.run(
    ['bash', 'executor/scripts/infer.sh', '--model', 'qwen', '--yaml', YAML_A8W8_CUSTOM_PROFILER],
    cwd=str(RECIPE_ROOT),
    env=env,
    check=True,
)
```

#### 7.3 查看 Profiling 结果

推理完成后，定位 `prof/` 目录，重点关注其中的 `op_statistic.csv` 和 `kernel_details.csv` 这两个文件。`op_statistic.csv`中展示了模型调用的所有算子的统计信息，可快速确认自定义算子 QmmCustom 的调用情况。`kernel_details.csv`中展示了详细的接口调用信息，可自行查看筛选自己关注的算子的性能。

通过如下操作统计 `kernel_details.csv` 中的 QmmCustom 算子耗时，可自行对比自定义算子替换前后的性能差异。

```python
import pandas as pd
from pathlib import Path

RES_DIR = RECIPE_ROOT / 'models/qwen/res'

# 取最新的 profiling 结果目录
result_dirs = sorted([d for d in RES_DIR.iterdir() if d.is_dir()], key=lambda d: d.name, reverse=True)
latest_result = result_dirs[0]
print(f'最新结果目录: {latest_result}')

def find_kernel_csv(phase_dir):
    matches = sorted(phase_dir.rglob('kernel_details.csv'), key=lambda p: p.parent.parent.name, reverse=True)
    return matches[0] if matches else None

prefill_csv = find_kernel_csv(latest_result / 'qwen3_8b_qwen3_8b_a8w8_custom_profiler/prof/prefill')
decode_csv = find_kernel_csv(latest_result / 'qwen3_8b_qwen3_8b_a8w8_custom_profiler/prof/decode')
assert prefill_csv and decode_csv, 'kernel_details.csv 未找到，请确认 profiling 已完成'
print(f'Prefill CSV: {prefill_csv}')
print(f'Decode CSV: {decode_csv}')

# 读取 CSV 并筛选 QmmCustom 算子
prefill_df = pd.read_csv(prefill_csv)
decode_df = pd.read_csv(decode_csv)

prefill_qmm = prefill_df[prefill_df['Type'].str.contains('QmmCustom')].copy()
decode_qmm = decode_df[decode_df['Type'].str.contains('QmmCustom')].copy()

# 按 Input Shapes 分组，统计每种 shape 下的平均 Duration
def qmm_duration_stats(df, phase):
    stats = df.groupby(['Input Shapes', 'Output Data Types'])['Duration(us)'].agg(['mean', 'count']).reset_index()
    stats.columns = ['Input Shapes', 'Output Dtype', 'Avg Duration(us)', 'Calls']
    stats = stats.sort_values('Avg Duration(us)', ascending=False).reset_index(drop=True)
    stats.insert(0, 'Phase', phase)
    return stats

prefill_stats = qmm_duration_stats(prefill_qmm, 'Prefill')
decode_stats = qmm_duration_stats(decode_qmm, 'Decode')

combined = pd.concat([prefill_stats, decode_stats], ignore_index=True)
display(combined.style.set_caption('QmmCustom 各 Shape 平均耗时 (us)'))
```

#### 7.4 恢复原始 W8A8 源码

自定义算子推理与 Profiling 已完成，下方单元格会从备份恢复 `compressed_tensors_w8a8_int8.py` 原始内容，避免修改后的源码污染 baseline 对比或产生 git 工作区变更。

```python
W8A8_FILE = RECIPE_ROOT / 'module/quantization/compressed_tensors/compressed_tensors_w8a8_int8.py'
W8A8_FILE.write_text(W8A8_ORIGINAL_CODE, encoding='utf-8')
print('[恢复] 已恢复原始 W8A8 源码，baseline 对比不受污染')
```

### 8 提交要求

> 完整的提交说明参考[启航营课程实践说明](https://gitcode.com/cann/cann-launch-camp/blob/master/2026/University/HIT/First-session/README.md)。

1. 提交完整的 Jupyter Notebook（.ipynb），**保留所有单元格输出**。
2. 提交前依次运行所有单元格，确保：
   - 自定义算子编译成功；
   - 算子功能测试通过；
   - 性能数据收集成功。
3. **文件命名**：`gitcode账号_result.ipynb`。
4. **允许并且鼓励**使用 AI 工具辅助，但须独立思考并在报告中简述（解决了什么疑惑、是否引入新 bug）。
5. **不得抄袭。**

---
#### 小结

本章完成了 QmmCustom 算子的开发、编译和单算子功能性能测试，并将该自定义算子接入了 Qwen3-8B 量化模型，验证功能并观测了其在模型中的性能。

#### 附录
实践相关参考材料链接：
- [Ascend C 高阶api文档](https://gitcode.com/cann/asc-devkit/blob/master/docs/api/SIMD-API/%E9%AB%98%E9%98%B6API/%E9%AB%98%E9%98%B6API.md)
- [昇腾社区文档](https://www.hiascend.com/zh/document)
- [Ascend C 算子开发系列教程](https://gitcode.com/cann/cann-learning-hub/tree/master/tutorials/ascendc_operator_development)
- [Ascend C 算子功能调试](https://gitcode.com/cann/cann-learning-hub/tree/master/tutorials/ascendc_operator_development/07_Troubleshooting)
- [Matmul最佳实践样例](https://gitcode.com/cann/asc-devkit/blob/master/examples/01_simd_cpp_api/05_best_practices/01_matrix_compute/matmul_high_performance/README.md)
- [CANN内置量化矩阵乘算子实现](https://gitcode.com/cann/ops-nn/tree/master/matmul/quant_batch_matmul_v3)

# ==========================================
## 📝 练习与验证

> 📌 原 Notebook 中的练习、编译命令和校验代码已按原顺序保留在上文。需要 CANN 运行时、Ascend NPU 或 CANNLab 环境的单元，执行前请先核对版本和设备条件。
