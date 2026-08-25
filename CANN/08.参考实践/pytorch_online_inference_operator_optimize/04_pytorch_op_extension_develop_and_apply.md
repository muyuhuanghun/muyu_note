---
source_repo: cann-learning-hub
source_path: reference_practice/pytorch_online_inference_operator_optimize/04_pytorch_op_extension_develop_and_apply.ipynb
source_commit: 1bf85454ed7c41e184a96fb51d109b6bb83b7c0d
note_kind: notebook_to_markdown
---

# 算子的Pytorch框架模型接入

> 📚 上游 Notebook：[reference_practice/pytorch_online_inference_operator_optimize/04_pytorch_op_extension_develop_and_apply.ipynb](https://gitcode.com/cann/cann-learning-hub/blob/master/reference_practice/pytorch_online_inference_operator_optimize/04_pytorch_op_extension_develop_and_apply.ipynb)
> 🧪 整理方式：保留 Markdown 与代码单元；省略 Jupyter 执行输出，避免把一次性环境结果误当成可复现结论。

## 🧭 学习目标

- 先读懂概念，再运行代码片段验证关键结论；
- 把本节内容接入后续 CANN / Ascend NPU 实践。

# ==========================================
## 📖 课程内容

本节将系统学习如何将开发的 Ascend C 自定义算子接入 PyTorch 框架进行在线推理，并在真实的 AI 模型中发挥作用。

本节大纲如下：
- Pytorch自定义算子插件实现
- Pytorch自定义算子调用
- Pytorch自定义算子接入模型
---

### 1. 环境准备

正式开始学习之前，先完成以下环境准备步骤：
#### 1.1 CANN环境变量加载

```bash
!mkdir -p Sources/04

import os, subprocess
env = subprocess.check_output("bash -l -c 'source $ASCEND_TOOLKIT_HOME/set_env.sh && env'", shell=True, text=True)
for line in env.splitlines():
    if "=" in line: os.environ.__setitem__(*line.split("=", 1))
print("\n🎉 Environment initialization process completed successfully!")
```

#### 1.2 安装Python依赖

接下来安装相应的 Python 依赖，用于模型下载、推理以及自定义算子测试。主要依赖包括：

- **modelscope**：用于从ModelScope平台下载预训练模型
- **transformers**：Hugging Face的transformers库，提供模型加载和推理功能
- **expecttest**：测试工具库，用于算子验证

以下命令将从清华源安装这些依赖包到Sources/04目录，并添加到Python路径中：

```bash
!pip3 install expecttest transformers==5.3.0 -i https://pypi.tuna.tsinghua.edu.cn/simple -t Sources/04
import os 
import sys
pkg_dir = os.path.abspath("Sources/04")
if pkg_dir not in sys.path:
    sys.path.insert(0, pkg_dir)
import importlib.util, subprocess
if importlib.util.find_spec("modelscope") is None:
    subprocess.run(["pip3", "install", "modelscope", "-i", "https://pypi.tuna.tsinghua.edu.cn/simple", "-t", pkg_dir], check=True)
```

#### 1.3 下载Qwen3.5模型

然后通过已安装的 modelscope 依赖下载本次自定义算子接入的模型 Qwen3.5-0.8B，完成所有环境准备事项。

Qwen3.5-0.8B 是通义千问系列的一个轻量级模型，参数量为 0.8B（8 亿参数），适合快速在 NPU 上部署验证。

以下命令将从ModelScope平台下载模型文件到本地Sources/04/Qwen目录：

```bash
!modelscope download --model Qwen/Qwen3.5-0.8B --local_dir Sources/04/Qwen
```

---
### 2. 自定义算子Add_Custom_Template部署

我们将上一节中开发的 Add_Custom_Template 算子示例进行编译部署，并加载自定义算子的环境变量，确保后续代码可以正常调用 Add_Custom_Template。

以下命令执行算子的编译和部署：

```bash
!cd src/add_custom_template/ && bash run_deploy.sh
import os, subprocess
env = subprocess.check_output("bash -l -c 'source $HOME/vendors/customize/bin/set_env.bash && env'", shell=True, text=True)
for line in env.splitlines():
    if "=" in line: os.environ.__setitem__(*line.split("=", 1))
```

---

### 3. Add_Custom_Template Pytorch插件实现

本节使用 C++ Extension 方式将 Add_Custom_Template 算子接入 PyTorch 框架。C++ Extension 提供了一套编程模板，要求开发者同时实现 C++ 侧代码和 Python 侧代码：C++ 代码实现具体的 Ascend C 算子调用功能，Python 代码提供兼容 PyTorch 框架的调用接口，二者通过 Pybind11 相互绑定，实现自定义 Python 接口调用 C++ 算子执行代码的逻辑。


#### 3.1 C++ Extension实现结构

C++ Extension项目的完整目录结构如下：

```
add_custom_template_pytorch_extension/
├── csrc/                              # C++源代码目录
│   ├── pytorch_npu_helper.hpp         # ❌ NPU辅助工具库（固定模板）
│   ├── function.h                     # ✅ 函数声明头文件（需修改）
│   ├── add_custom.cpp                 # ✅ 算子实现文件（需修改）
│   └── registration.cpp               # ✅ 算子注册文件（需修改）
├── custom_ops/                        # Python包目录
│   ├── __init__.py                    # ✅ 包初始化文件（需修改）
│   └── add_custom.py                  # ✅ Python接口文件（需修改）
├── setup.py                           # ❌ 构建脚本（固定模板）
```

**文件说明：**
- **❌ 标记的文件**：固定模板文件，提供了基础的框架支持，开发新算子时可直接复用，无需修改
- **✅ 标记的文件**：需要根据具体算子进行定制化开发，是实现算子功能的核心文件

#### 3.2 C++侧实现详解

##### 3.2.1 算子实现文件 (csrc/add_custom.cpp) ✅

该文件负责实现算子的前向和反向功能函数，并将函数接口注册到 PyTorch 框架中。当仅涉及推理场景时，无需实现和注册反向功能。

**开发流程(纯推理)：**

**1：实现算子的前向功能函数**

(1)函数定义:

- 函数名：无硬性要求，一般采用 `<op_name>_impl_npu` 的命名格式
- 输入参数：接收Pytorch张量（`at::Tensor`类型），对应算子的输入
- 返回值：返回计算结果张量或计算结果张量集合

对于Add算子，函数定义为：
```cpp
at::Tensor add_custom_impl_npu(const at::Tensor& self, const at::Tensor& other);
```


(2)创建输出张量

执行算子前需要申请输入输出的内存，而输入在调用前已经确定，因此只需创建输出张量来申请输出内存。
创建输出张量的关键在于确定其 shape 和数据类型。创建后张量中存储的具体数据无需关心，因为该数据会在算子调用后被实际输出覆盖。输出张量的 shape 和数据类型可以通过输入的 shape、数据类型结合算子的计算逻辑推导得出。对于 Add 算子，在不涉及广播的情况下，输出的 shape 和数据类型与任意输入相同，因此可以直接使用 `empty_like` 接口创建输出张量。

```cpp
at::Tensor result = at::empty_like(self);  // 创建输出张量
```

(3)调用Ascend C算子

使用`EXEC_NPU_CMD`宏调用Ascend C算子的aclnn接口：
```cpp
EXEC_NPU_CMD(aclnnAddCustomTemplate, self, other, result);
```

参数说明：
- 第一个参数：算子的aclnn接口名称（对应Host侧实现的算子）。
- 后续参数：算子的输入输出张量，顺序与算子aclnn接口里的一致。

该宏的工作原理：
1. 查找算子动态库，定位aclnn接口函数地址
2. 计算所需的workspace大小并分配内存
3. 调用aclnn二段接口执行算子计算
4. 释放临时资源

**2：注册算子实现**

通过`TORCH_LIBRARY_IMPL`宏将实现函数注册到Pytorch框架：
```cpp
TORCH_LIBRARY_IMPL(myops, PrivateUse1, m) {
    m.impl("add_custom", &add_custom_impl_npu);
}
```

不同的算子只需要调整`myops`, `add_custom`, `&add_custom_impl_npu`这三个参数:
- `myops`：算子命名空间（需在registration.cpp中定义）
- `add_custom`：注册的函数名称
- `&add_custom_impl_npu`：第一步中实现的前向函数

**完整代码示例：**
```cpp
#include <torch/library.h>
#include "pytorch_npu_helper.hpp"
#include "function.h"

at::Tensor add_custom_impl_npu(const at::Tensor& self, const at::Tensor& other) {
    at::Tensor result = at::empty_like(self);
    EXEC_NPU_CMD(aclnnAddCustomTemplate, self, other, result);
    return result;
}

TORCH_LIBRARY_IMPL(myops, PrivateUse1, m) {
    m.impl("add_custom", &add_custom_impl_npu);
}
```

##### 3.2.2 算子注册文件 (csrc/registration.cpp) ✅

该文件负责将自定义算子声明到 PyTorch 框架中，使其可被 Python 调用。

**开发步骤：**

**步骤1：定义算子Schema**

使用 `TORCH_LIBRARY` 宏定义算子的函数签名，提供类型检查、支持 TorchScript 编译、生成算子唯一标识等功能。
```cpp
TORCH_LIBRARY(myops, m) {
    m.def("add_custom(Tensor self, Tensor other) -> Tensor"); 
}
```

Schema定义说明：
- `myops`：算子命名空间,需和**注册算子实现**里的名称一致
- 函数签名遵循TorchScript语法：`输入参数类型 参数名 -> 返回值类型`
- 注册的函数名称需要和**注册算子实现**里的名称一致


**步骤2：绑定Python接口**

使用`PYBIND11_MODULE`宏将C++函数绑定Python自定义函数接口：
```cpp
PYBIND11_MODULE(TORCH_EXTENSION_NAME, m) {
    m.def("add_custom", &add_custom_impl_npu, "x + y");
}
```

绑定说明：
- 第一个参数：Python侧自定义函数接口名,需和**注册算子实现**里的函数名称一致
- 第二个参数：`add_custom.cpp`中实现的前向函数指针
- 第三个参数：函数文档字符串

**完整代码示例：**
```cpp
#include <torch/library.h>
#include <torch/extension.h>
#include "function.h"

TORCH_LIBRARY(myops, m) {
    m.def("add_custom(Tensor self, Tensor other) -> Tensor"); 
}

PYBIND11_MODULE(TORCH_EXTENSION_NAME, m) {
    m.def("add_custom", &add_custom_impl_npu, "x + y");
}
```
##### 3.2.3 算子注册文件 (csrc/function.h) ✅
声明前向函数接口即可，方便其他文件引用。实现如下：
```
#ifndef FUNCTION_H
#define FUNCTION_H

#include <ATen/ATen.h>

at::Tensor add_custom_impl_npu(const at::Tensor& self, const at::Tensor& other);

#endif //  FUNCTION_H
```
#### 3.3 Python侧实现详解

##### 3.3.1 Python接口文件 (custom_ops/add_custom.py) ✅

该文件的作用是为算子提供Python调用接口，将Python调用转发到底层C++实现。

**开发步骤：**

**步骤1：导入C++扩展模块**

C++ Extension编译后会生成一个Python模块（动态库），模块名由setup.py中的`NpuExtension(name="...")`指定：
```python
import custom_ops_lib  # 导入编译生成的C++扩展模块
```

**步骤2：定义Python接口函数**

创建一个Python函数，直接调用C++模块中的对应函数：
```python
def add_custom(self, other):
    return custom_ops_lib.add_custom(self, other)
```

说明：
- 函数名与C++侧保持一致，便于理解和使用
- 参数和返回值的类型转换由pybind11自动处理
- 可以在此层添加参数检查、文档字符串等Python特有的功能

**完整代码示例：**
```python
import torch
import custom_ops_lib

def add_custom(self, other):
    return custom_ops_lib.add_custom(self, other)
```
##### 3.3.2  初始化文件(custom_ops/__init__.py) ✅
修改引入的文件名称即可:
```
from .add_custom import *
```

#### 3.4 固定模板文件说明

以下文件为固定模板，开发新算子时无需修改：

**1. csrc/pytorch_npu_helper.hpp** ❌
- 提供EXEC_NPU_CMD宏定义，用于调用Ascend C算子的aclnn接口
- 包含ACL数据类型转换函数
- 提供内存管理和资源释放函数
- 该文件由torch_npu提供，无需任何修改

**2. setup.py** ❌
- 构建脚本，负责编译C++代码并打包
- 使用NpuExtension自动处理NPU相关配置
- 通常无需修改，除非需要调整编译选项或包名

#### 3.5 构建和安装自定义算子包

以下命令将编译C++ Extension并生成wheel包，然后安装到本地环境：

```bash
!cd src/add_custom_template_pytorch_extension/ && python3 setup.py build bdist_wheel && pip3 install dist/custom_ops-1.0-cp311-cp311-linux_aarch64.whl -t ../../Sources/04
```

#### 3.6 测试自定义算子

安装完成后，我们需要测试自定义算子是否能够正常工作。测试流程包括：

1. **导入必要的库**：torch、torch_npu和custom_ops(自定义算子包,3.5中安装)
2. **创建测试数据**：在CPU上生成随机张量，然后拷贝到NPU
3. **执行算子计算**：调用自定义算子和Pytorch原生算子
4. **验证结果**：比较两个算子的输出是否一致

以下代码演示了完整的测试流程：

```python
import copy
import torch
import torch_npu
import custom_ops

torch.npu.config.allow_internal_format = False
torch.npu.set_compile_mode(jit_compile=False)

x_cpu = torch.randn([8, 2048], dtype=torch.float16)
y_cpu = torch.randn([8, 2048], dtype=torch.float16)
x_npu = copy.deepcopy(x_cpu).npu()
y_npu = copy.deepcopy(y_cpu).npu()

output = custom_ops.add_custom(x_npu, y_npu).cpu()
cpuout = torch.add(x_cpu, y_cpu)

assert torch.allclose(output, cpuout, rtol=1e-3, atol=1e-3), "结果不一致"
print("\n测试通过")
```

如果测试通过，说明自定义算子已经成功接入Pytorch框架，可以正常调用。接下来我们将学习如何将自定义算子应用到实际的AI模型中。

---
### 4. 自定义算子接入模型

前面的步骤验证了自定义算子已成功接入 PyTorch 框架。接下来，我们将展示如何将自定义算子真正接入到模型中，替换模型原有的算子实现。

#### 4.1 修改Qwen3.5模型文件

首先在 modeling_qwen3_5.py 中导入 custom_ops 自定义算子库，供后续调用使用：
```
import custom_ops
```

在上一节最后，我们找到了 Add 算子的一处调用位置，现在将该处替换为自定义的 Add_Custom_Template 算子。

**修改位置：**

`modeling_qwen3_5.py`第437行：`last_recurrent_state = last_recurrent_state + k_t.unsqueeze(-1) * delta.unsqueeze(-2)`

**修改后代码：**
```python
last_recurrent_state = custom_ops.add_custom(last_recurrent_state, k_t.unsqueeze(-1) * delta.unsqueeze(-2))  # 自定义算子
```
替换 transformers 库内的模型文件完成修改：

```bash
!cp src/qwen3.5/modeling_qwen3_5.py Sources/04/transformers/models/qwen3_5/
```

#### 4.2 推理并采集性能数据

添加 Ascend PyTorch Profiler 接口采集替换后的性能数据，验证替换是否成功。

```bash
!cp src/qwen3.5/utils.py Sources/04/transformers/generation/utils.py
```

执行推理：

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import torch_npu
model_name = "Sources/04/Qwen/" # 本地模型路径
model = AutoModelForCausalLM.from_pretrained(
    model_name
).half().npu()
tokenizer = AutoTokenizer.from_pretrained(model_name)

prompt = "Hello!"
messages = [
    {"role": "user", "content": prompt}
]
text = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True,
    enable_thinking=False
)
model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

generated_ids = model.generate(
    **model_inputs,
    max_new_tokens=512,
    top_k=20,
    top_p=1.00, 
    temperature= 1.0, 
    do_sample= True, 
    repetition_penalty= 1.0
)
generated_ids = [
    output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
]

response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
print(response)
```

#### 4.3 查看性能数据
使用 MindStudio Insight 工具导入生成的性能数据，在 `Operator` 页签可以看到 AddCustomTemplate 自定义算子已被调用：
<img src="../../../../CANN-assets-20260813/reference_practice/pytorch_online_inference_operator_optimize/images/mindstudio_add_custom.png" width="90%">

---
### 课后实践

请根据本节课程学习内容完成以下题目进行自测。

1. （单选题）Ascend Pytorch 算子插件的作用是什么（）  
   A. 用于替换 PyTorch 的数据加载模块  
   B. 将自定义算子注册到 PyTorch，并在昇腾 NPU 上执行计算  
   C. 用于管理模型训练过程中的学习率  
   D. 用于将模型导出为 ONNX 格式  

2. （单选题）C++ Extension方式实现Ascend Pytorch插件中，以下哪个文件不需要修改（）  
   A. pytorch_npu_helper.hpp  
   B. function.h  
   C. add_custom.cpp  
   D. registration.cpp  

3. （单选题） C++ Extension方式实现Ascend Pytorch插件中，调用的底层算子接口是哪种类型（）   
   A. kernel直调接口  
   B. aclop接口    
   C. aclnn接口    
   D. acldvpp接口    

4. （单选题）验证算子插件是否开发正确的测试代码流程中，不包含以下哪个步骤（）   
   A. 构建输入数据    
   B. 执行自定义算子和标杆算子   
   C. 比对自定义算子结果和标杆结果   
   D. 构建输出数据  

5. （单选题）通过什么库调用自定义算子（）  
    A. torch  
    B. torch_npu  
    C. 自定义算子包  
    D. transformers  


执行以下代码查看答案：

```bash
!cat ./answers/04_answer.txt
```

# ==========================================
## 📝 练习与验证

> 📌 原 Notebook 中的练习、编译命令和校验代码已按原顺序保留在上文。需要 CANN 运行时、Ascend NPU 或 CANNLab 环境的单元，执行前请先核对版本和设备条件。
