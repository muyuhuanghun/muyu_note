---
source_repo: cann-learning-hub
source_path: reference_practice/pytorch_online_inference_operator_optimize/05_chapter_practice.ipynb
source_commit: 1bf85454ed7c41e184a96fb51d109b6bb83b7c0d
note_kind: notebook_to_markdown
---

# 章节实践

> 📚 上游 Notebook：[reference_practice/pytorch_online_inference_operator_optimize/05_chapter_practice.ipynb](https://gitcode.com/cann/cann-learning-hub/blob/master/reference_practice/pytorch_online_inference_operator_optimize/05_chapter_practice.ipynb)
> 🧪 整理方式：保留 Markdown 与代码单元；省略 Jupyter 执行输出，避免把一次性环境结果误当成可复现结论。

## 🧭 学习目标

- 先读懂概念，再运行代码片段验证关键结论；
- 把本节内容接入后续 CANN / Ascend NPU 实践。

# ==========================================
## 📖 课程内容

通过本章的系统学习，我们掌握了如何分析模型中需要优化的算子以及将优化后的算子应用到模型的全部流程。为了巩固所学知识，现提供以下实践练习：

基于Qwen2.5-0.5B-Instruct模型，优化其中至少一处Mul算子的调用

要求：

1.通过Ascend Pytorch Profiler工具找到一处Mul算子的调用位置以及对应的算子场景。  

2.开发自定义Mul算子MulCustom并完成部署  

3.开发MulCustom算子插件

4.替换原Mul算子并通过Ascend Pytorch Profiler工具确认MulCustom成功调用

5.模型输出精度正常

请开始你的实践，体验完整开发过程。

---

### **环境准备：**

```bash
!mkdir -p Sources/05

import os, subprocess
env = subprocess.check_output("bash -l -c 'source $ASCEND_TOOLKIT_HOME/set_env.sh && env'", shell=True, text=True)
for line in env.splitlines():
    if "=" in line: os.environ.__setitem__(*line.split("=", 1))
print("\n🎉 Environment initialization process completed successfully!")
```

安装相关依赖：

```bash
!pip3 install expecttest transformers==5.3.0 -i https://pypi.tuna.tsinghua.edu.cn/simple -t Sources/05
import os 
import sys
pkg_dir = os.path.abspath("Sources/05")
if pkg_dir not in sys.path:
    sys.path.insert(0, pkg_dir)
import importlib.util, subprocess
if importlib.util.find_spec("modelscope") is None:
    subprocess.run(["pip3", "install", "modelscope", "-i", "https://pypi.tuna.tsinghua.edu.cn/simple", "-t", pkg_dir], check=True)
```

下载模型：

```bash
!modelscope download --model Qwen/Qwen2.5-0.5B-Instruct  --local_dir Sources/05/Qwen
```

---
### **模型推理脚本：**
可以通过以下脚本推理模型进行验证

```python
import transformers
from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "Sources/05/Qwen/"

model = AutoModelForCausalLM.from_pretrained(
    model_name
).half().npu()
tokenizer = AutoTokenizer.from_pretrained(model_name)

prompt = "Give me a short introduction to large language model."
messages = [
    {"role": "system", "content": "You are Qwen, created by Alibaba Cloud. You are a helpful assistant."},
    {"role": "user", "content": prompt}
]
text = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True
)
model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

generated_ids = model.generate(
    **model_inputs,
    max_new_tokens=512
)
generated_ids = [
    output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
]

response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
```

# ==========================================
## 📝 练习与验证

> 📌 原 Notebook 中的练习、编译命令和校验代码已按原顺序保留在上文。需要 CANN 运行时、Ascend NPU 或 CANNLab 环境的单元，执行前请先核对版本和设备条件。
