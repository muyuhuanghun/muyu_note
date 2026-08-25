---
source_repo: cann-learning-hub
source_path: quick_start/first_llm_inference/02_qwen3_npu_inference_npugraph_ex.ipynb
source_commit: 1bf85454ed7c41e184a96fb51d109b6bb83b7c0d
note_kind: notebook_to_markdown
---

# 第二课：大模型推理加速 —— 从"堵车"到"高速通路"

> 📚 上游 Notebook：[quick_start/first_llm_inference/02_qwen3_npu_inference_npugraph_ex.ipynb](https://gitcode.com/cann/cann-learning-hub/blob/master/quick_start/first_llm_inference/02_qwen3_npu_inference_npugraph_ex.ipynb)
> 🧪 整理方式：保留 Markdown 与代码单元；省略 Jupyter 执行输出，避免把一次性环境结果误当成可复现结论。

## 🧭 学习目标

- 先跑通功能正确的 Baseline，再用 Profiling 定位瓶颈；
- 理解图模式、融合算子、量化和端到端收益验证。

# ==========================================
## 📖 课程内容

> 上一课我们让 Qwen3-0.6B 在昇腾NPU上跑了起来，但你有没有想过：模型推理还能更快吗？这节课我们就来揭开加速的秘密。

---
### 1. 大模型推理的两大优化方向

上一课我们让 Qwen3-0.6B 跑了起来，但推理速度还有提升空间。要加速，先得找**慢在哪**。

想象一条拥堵的公路，车流走走停停，慢的原因有三：
- **红灯多**：每个路口都要等红灯，车走一段停一段
- **车多**：很多私家小轿车挤在路上，如果都通过载客人数高的公交车出行就大幅降低了车的数量
- **车速慢**：每辆车本身的性能有限，跑不快

模型推理也是同样的道理——NPU 反复执行成百上千个**算子**（一次矩阵乘法、一次归一化……都算一个算子），慢的原因：
- 对应"红灯多"：一个算子跑完，CPU 才调度下一个，NPU 在间隙空转
- 对应"车多"：多个小算子本可以合并成一次大运算，却拆着跑
- 对应"车速慢"：单个算子自身也有优化空间

后两个原因归结为同一层面——算子本身效率低，于是两个优化方向：

| 瓶颈 | 优化方向 | 做什么 | 比喻 |
|------|---------|--------|------|
| 红灯多 | **图编译**（框架层） | 把所有算子编排成一张执行图，一次性交给NPU | 提前规划好所有车辆的行驶，消除路口红灯，一路畅行 |
| 车多 + 车速慢 | **算子融合**（算子层） | 合并小算子为融合算子，并优化单个算子性能 | 小车换大车，再换更强引擎 |

> 两者配合：路口不堵了，车也更快了，整条路就通畅了。

本课聚焦 框架层面的 **图编译**。

---
### 2. 不做图编译会怎样？——调度空泡与低并行

#### 2.1 Eager模式：一个算子一个算子地"排队"

默认的推理方式叫 **Eager模式**（急切模式），意思是：框架拿到一个算子就立刻发给NPU执行，算完再发下一个。

听起来很直接，但问题在于：
- 每发一个算子，CPU都要做一次**调度**（决定谁来执行、准备数据地址……），这需要时间
- NPU在执行算子A时，算子B还在CPU上排队等待调度——NPU"干等"了！
- 这种NPU空闲等待的时间，就叫 **调度空泡（Scheduling Bubble）**

> 比喻：就好像厨房中有学徒切菜备菜，掌勺厨师负责做饭，现在一道菜点了很多份。学徒备菜相当于CPU下发算子任务，厨师做饭相当于算子在NPU的实际执行。现在学徒每次只切一份菜，然后必须要厨师把这道菜做完才会去备下一道菜，这会造成厨师经常没事干，厨师没事干的时间就相当于调度空泡。

#### 2.2 低并行：算子串行执行，无法重叠

Eager模式的另一个问题是 **低并行**：算子只能一个接一个地执行，即使有些算子之间没有依赖关系，也无法同时跑。

> 比喻：仍然以厨房为例，现在是有两名厨师做不同的菜，互不依赖。低并行指的是其中一名厨师做菜的时候，虽然另一名厨师可以同时做菜，但他就是不做在那偷懒，非要等另一名厨师做完再去做他自己的菜。

![NPU_Schedule_Eager.png](../../../../CANN-assets-20260813/docs/images/first_llm_course/NPU_Schedule_Eager.png)

---
### 3. 图编译简介

#### 3.1 什么是图编译？

**图编译**的核心思想是：**提前把所有算子编排成一张完整的执行图**，一次性交给NPU，而不是一个一个地发。

> 比喻：图编译就相当于在厨房中学徒会提前将菜都备好，厨师做菜不需要在等学徒洗菜切菜，并且多个厨师同时做菜，效率极大提升。

#### 3.2 图编译的效果

1. **消除调度空泡**：NPU不再干等CPU调度，算子之间无缝衔接
2. **并行执行**：无依赖的算子可以同时跑
3. **内存优化**：提前规划好内存，减少临时变量的分配和释放

![NPU_Schedule_npugraphex.png](../../../../CANN-assets-20260813/docs/images/first_llm_course/NPU_Schedule_npugraphex.png)

---
### 4. npugraph_ex：昇腾的图编译加速利器

#### 4.1 什么是 npugraph_ex？

PyTorch 提供了一个统一的图编译接口 **`torch.compile`**，用法如下：
```python
opt_model = torch.compile(model, backend="???")
```

其中 `backend` 参数决定用哪种编译器——你可以把它理解为一个"万能插座"，`backend` 决定插什么"插头"：
- `backend="inductor"`（默认）：PyTorch 官方的 Inductor 编译器
- **`backend="npugraph_ex"`**：昇腾的图编译后端，专门为 NPU 优化

**npugraph_ex** 就是昇腾 CANN 提供的 `torch.compile` 后端实现。把 `backend` 设为 `"npugraph_ex"`，PyTorch 的图编译就会走昇腾的优化路径，NPU 就能全速运转。

#### 4.2 npugraph_ex 的使用方法

使用非常简单，只需加一行代码：

```python
opt_model = torch.compile(model, backend='npugraph_ex', fullgraph=True, dynamic=True, options={"capture_limit": 256})
```

参数解释：
- **`backend='npugraph_ex'`**：使用昇腾的图编译后端
- **`fullgraph=True`**：把整个模型捕获为一张完整的计算图，不允许图中断（部分算子没入图）
- **`dynamic=True`**：启用动态Shape追踪。大模型推理时，每生成一个token，输入序列就变长1个，Shape是动态变化的。开启此选项让图编译能适配这种变化
- **`options={"capture_limit": 256}`**：大于等于模型最大输出数量max_new_tokens即可，不设置可能会引起较长的编译时间

---
### 5. 动手实践：用 npugraph_ex 加速 Qwen3-0.6B
上一章我们初次体验了Qwen3-0.6B的简单推理，这次我们就在上一章代码的基础上，添加npugraph_ex的一行使能代码，体验图编译优化后的模型性能。

#### 5.1 加载模型

加载模型时指定 `attn_implementation="eager"`，与上一章保持一致，确保注意力机制使用 Eager 模式执行。

```python
import torch
import torch_npu
from transformers import AutoTokenizer, AutoModelForCausalLM

model_path = '/mnt/workspace/models/models/Qwen--Qwen3-0.6B/snapshots/master'

tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    model_path,
    trust_remote_code=True,
    attn_implementation='eager'
).to('npu:0').half()
model.eval()
print(f'Model loaded, device: {model.device}')
```

#### 5.2 使能 npugraph_ex 图编译

就一行代码！模型瞬间从"排队打饭模式"切换到"自助餐模式"。

```python
opt_model = torch.compile(model, backend='npugraph_ex', fullgraph=True, dynamic=True, options={"capture_limit": 256})

print('npugraph_ex 图编译已使能！')
print('现在用 opt_model 做推理时，会自动使用编译后的优化图。')
```

#### 5.3 第一次推理（含编译）

npugraph_ex的图编译是在第一次推理时执行的，耗时较长。编译完成后，后续推理会非常快。

```python
import time

messages = [{'role': 'user', 'content': '你好，请介绍一下AI是什么'}]
text = tokenizer.apply_chat_template(
    messages, tokenize=False, add_generation_prompt=True, enable_thinking=False
)
input_ids = torch.tensor([tokenizer.encode(text)], dtype=torch.long).to('npu:0')

print('第一次推理（包含图编译，会比较慢）...')
t0 = time.time()

max_new_tokens = 128
generated_ids = input_ids.clone()
for step in range(max_new_tokens):
    with torch.no_grad():
        logits = opt_model(generated_ids).logits
    next_token_id = torch.argmax(logits[:, -1, :], dim=-1, keepdim=True)
    if next_token_id.item() == tokenizer.eos_token_id:
        break
    generated_ids = torch.cat([generated_ids, next_token_id], dim=1)

compile_time = time.time() - t0

response = tokenizer.decode(generated_ids[0][input_ids.shape[1]:], skip_special_tokens=True)
print(f'首次推理耗时: {compile_time:.3f}s（包含编译时间）')
print(f'模型回答: {response}')
```

#### 5.4 后续推理
现在模型的编译热身的推理已经结束，可以体验编译完成后模型的推理速度究竟是什么样了。

```python
max_new_tokens = 128

print('后续推理（图已编译完成，纯执行）:')
times_accel = []
for i in range(3):
    generated_ids = input_ids.clone()
    t0 = time.time()

    for step in range(max_new_tokens):
        with torch.no_grad():
            logits = opt_model(generated_ids).logits
        next_token_id = torch.argmax(logits[:, -1, :], dim=-1, keepdim=True)
        if next_token_id.item() == tokenizer.eos_token_id:
            break
        generated_ids = torch.cat([generated_ids, next_token_id], dim=1)

    torch.npu.synchronize()
    num_generated = generated_ids.shape[1] - input_ids.shape[1]
    elapsed = time.time() - t0
    times_accel.append(elapsed)
    print(f'  第{i+1}次: {elapsed:.3f}s')

avg_accel = sum(times_accel) / len(times_accel)
print(f'npugraph_ex 平均推理时间: {avg_accel:.3f}s')
print(f'\n生成token数: {generated_ids.shape[1] - input_ids.shape[1]}')
print(f'npugraph_ex 吞吐量: {num_generated / avg_accel:.1f} tokens/s')
```

#### 5.5 对比 Baseline：加速效果一目了然

我们重新加载一个 Eager 模式的模型（不加图编译），做同样的推理，对比加速比。

```python
baseline_model = AutoModelForCausalLM.from_pretrained(
    model_path,
    trust_remote_code=True,
    attn_implementation='eager'
).to('npu:0').half()
baseline_model.eval()

print('Baseline 热身...')
generated_ids = input_ids.clone()
for step in range(max_new_tokens):
    with torch.no_grad():
        logits = baseline_model(generated_ids).logits
    next_token_id = torch.argmax(logits[:, -1, :], dim=-1, keepdim=True)
    if next_token_id.item() == tokenizer.eos_token_id:
        break
    generated_ids = torch.cat([generated_ids, next_token_id], dim=1)
torch.npu.synchronize()

print('Baseline 计时:')
times_baseline = []
for i in range(3):
    generated_ids = input_ids.clone()
    t0 = time.time()

    for step in range(max_new_tokens):
        with torch.no_grad():
            logits = baseline_model(generated_ids).logits
        next_token_id = torch.argmax(logits[:, -1, :], dim=-1, keepdim=True)
        if next_token_id.item() == tokenizer.eos_token_id:
            break
        generated_ids = torch.cat([generated_ids, next_token_id], dim=1)

    torch.npu.synchronize()
    elapsed = time.time() - t0
    times_baseline.append(elapsed)
    print(f'  第{i+1}次: {elapsed:.3f}s')

avg_baseline = sum(times_baseline) / len(times_baseline)
print(f'eager 平均推理时间: {avg_baseline:.3f}s')
print(f'\n生成token数: {generated_ids.shape[1] - input_ids.shape[1]}')
print(f'eager 吞吐量: {(generated_ids.shape[1] - input_ids.shape[1]) / avg_baseline:.1f} tokens/s')
print(f'npugraph_ex提升百分比：{(avg_baseline-avg_accel)/avg_accel*100:.3f} %')
```

---
### 课后实践
我们使用上一章一样的输入来体验下在图模式下Qwen3-0.6B的推理速度。

```python
test_prompts = [
    '请写一首关于春天的五言绝句',
    'What is the capital of France?',
    '用Python写一个快速排序算法',
]

for prompt in test_prompts:
    messages = [{'role': 'user', 'content': prompt}]
    text = tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True, enable_thinking=False
    )
    input_ids = torch.tensor([tokenizer.encode(text)], dtype=torch.long).to('npu:0')

    generated_ids = input_ids.clone()
    for step in range(max_new_tokens):
        with torch.no_grad():
            logits = opt_model(generated_ids).logits
        next_token_id = torch.argmax(logits[:, -1, :], dim=-1, keepdim=True)
        if next_token_id.item() == tokenizer.eos_token_id:
            break
        generated_ids = torch.cat([generated_ids, next_token_id], dim=1)

    response = tokenizer.decode(generated_ids[0][input_ids.shape[1]:], skip_special_tokens=True)
    print(f'Q: {prompt}')
    print(f'A: {response}')
    print('-' * 60)
```

---
### 小结

这节课我们学到了：

1. **两大优化方向**：图编译（框架调度）和算子优化（底层执行）
2. **Eager模式的问题**：调度空泡（NPU干等CPU）和低并行（算子串行执行）
3. **图编译的效果**：提前编排执行图，消除空泡、融合算子、并行执行
4. **npugraph_ex**：昇腾的 `torch.compile` 后端，一行代码即可使能

核心代码就一行：
```python
opt_model = torch.compile(model, backend='npugraph_ex', fullgraph=True, dynamic=True, options={'capture_limit': 256})
```

# ==========================================
## 📝 练习与验证

> 📌 原 Notebook 中的练习、编译命令和校验代码已按原顺序保留在上文。需要 CANN 运行时、Ascend NPU 或 CANNLab 环境的单元，执行前请先核对版本和设备条件。
