---
source_repo: cann-learning-hub
source_path: quick_start/first_llm_inference/01_qwen3_npu_inference_baseline.ipynb
source_commit: 1bf85454ed7c41e184a96fb51d109b6bb83b7c0d
note_kind: notebook_to_markdown
---

# 第一课：从零开始，让大模型在昇腾NPU上"说话"

> 📚 上游 Notebook：[quick_start/first_llm_inference/01_qwen3_npu_inference_baseline.ipynb](https://gitcode.com/cann/cann-learning-hub/blob/master/quick_start/first_llm_inference/01_qwen3_npu_inference_baseline.ipynb)
> 🧪 整理方式：保留 Markdown 与代码单元；省略 Jupyter 执行输出，避免把一次性环境结果误当成可复现结论。

## 🧭 学习目标

- 先跑通功能正确的 Baseline，再用 Profiling 定位瓶颈；
- 理解图模式、融合算子、量化和端到端收益验证。

# ==========================================
## 📖 课程内容

> 你也许用过 ChatGPT、豆包，但你知道它们背后是怎么工作的吗？今天，我们亲手让一个大模型在自己的昇腾NPU上跑起来！

> **学习提示**：本课会快速过一遍核心概念，不用纠结于单个名词的精确定义——先跟着跑通全流程，有了整体印象后再回头看细节，效果更好。

---
### 1. 什么是人工智能（AI）？

想象一个学生上学读书的过程：
- 他阅读 **大量的** 课本和试卷（这叫 **训练数据**）
- 他慢慢学会了知识，能理解和回答问题（这叫 **学习/训练**）
- 毕业后你问他一个问题，他能回答（这叫 **推理**）

**人工智能**就是让计算机模拟这个过程。我们用数学公式（**模型**）来代替"学生的大脑"，用海量数据来"教"它，教完之后它就能回答问题了。

| 概念 | 生活中的比喻 |
|------|-------------|
| 训练 | 上学读书，学习知识 |
| 推理 | 毕业后用学到的知识回答问题 |
| 模型 | 大脑中存储的知识和思维方式 |
| 数据 | 课本、试卷、阅读材料 |

---
### 2. 什么是大模型（LLM）？

**大模型**（Large Language Model，LLM）就是一种"读了特别多书"的AI模型。

打个比方：
- 普通AI模型 = 只读了小学课本的学生，能做简单问答
- **大模型** = 读了全人类几乎所有公开文字的学生，能写诗、写代码、翻译、聊天……

"大"在哪里？
- **参数量大**：模型的"脑容量"大，Qwen3-0.6B 有 **6亿** 个参数（0.6B = 0.6 Billion），相当于6亿个"旋钮"需要调节
- **训练数据大**：训练时读了TB级别的文本
- **计算量大**：训练一次可能需要成千上万张NPU跑几个月

我们今天用的 **Qwen3-0.6B** 是通义千问第3代中最小巧的版本，适合学习入门。虽然它只有6亿参数（最大的模型有数千亿参数），但已经能流畅对话了！

---
### 3. 大模型推理需要什么？

让大模型"说话"（推理），需要四个核心组件：

#### 3.1 分词器（Tokenizer）—— 翻译官

计算机不认识"你好"这样的文字，只认识数字。**分词器**就是一位翻译官：
- **编码**：把"你好"翻译成数字序列 `[108046, 3837]`（每个数字叫一个 **token**）
- **解码**：把模型输出的数字翻译回文字

> 比喻：就像摩斯密码，把文字变成"滴答滴"，传完再翻译回来。

#### 3.2 模型（Model）

模型是一个巨大的数学函数，里面存着几十亿个参数（数字）。输入一串 token，它输出下一个token的**概率分布**——告诉你在所有可能的token中，每个出现的可能性有多大。

举个例子：输入"从前有座"，模型可能输出这样的概率分布：
- "山"：0.85（最可能）
- "庙"：0.08
- "人"：0.04
- 其他所有token：0.03

注意，模型**只给概率，不做决定**——到底选哪个token，由后处理来定。

#### 3.3 后处理（Post-processing）

模型每次前向传播只给出一个概率分布，但这个概率分布还不能直接当结果用，需要**后处理**来决定最终输出：

| 后处理步骤 | 做什么 | 为什么需要 |
|-----------|--------|-----------|
| **选token** | 从概率分布中挑出一个token（贪心选最大概率，或按概率随机采样） | 模型只给概率，不替你做决定 |
| **检查结束** | 判断新token是否是结束标记（EOS） | 用于实现生成的“自然结束”；不检查EOS通常只能跑到最大token上限再被强制截断，输出可能不完整或冗余 |
| **拼接** | 把新token拼到已有序列末尾，作为下一轮的输入 | 模型每次只看已有内容预测下一个 |

接上面的例子，后处理的工作过程：
1. **选token**：贪心解码选概率最大的"山"
2. **检查结束**："山"不是EOS，继续
3. **拼接**：序列变成"从前有座山"，送回模型预测下一个token

如此循环，直到某一步选出了EOS，推理结束。

#### 3.4 计算设备 —— 工作台

几十亿参数的数学运算，CPU算得太慢。我们需要专门的加速芯片：
- **NPU**（神经网络处理器，如昇腾910B）：专为AI计算设计的芯片，擅长大规模矩阵运算

> 比喻：CPU是全能选手但速度一般，NPU是专门做矩阵运算的"速算专家"。

#### 推理流程一图看懂

```
用户输入: "你好，请介绍你自己"
      │
      ▼
  ┌────────────┐
  │ 分词器     │  "你好，请介绍你自己" → [108046, 3837, ...]
  │ (Tokenizer)│
  └────────────┘
      │
      ▼
  ┌────────────────────────────────────┐
  │     推理循环（重复以下步骤）       │
  │                                    │
  │  ① 模型前向传播 → 下一个token的概率 │
  │  ② 后处理：选token / 检查EOS / 拼接 │
  │  ③ 未结束 → 回到①继续生成           │
  └─────────────────────────────────────┘
      │
      ▼
  ┌────────────┐
  │ 分词器     │  token IDs → "我是AI助手，专注于帮助用户解决问题"
  │ (Tokenizer)│
  └────────────┘
      │
      ▼
输出结果: "我是AI助手，专注于帮助用户解决问题"
```

---
### 4. PyTorch：AI世界的“工具箱"

要让大模型跑起来，我们需要一个AI框架来编写和执行模型代码。目前最流行的AI框架就是 **PyTorch**。

#### 4.1 什么是 PyTorch？

**PyTorch** 是 当前最受欢迎的开源深度学习框架，你可以把它理解为AI开发的"标准工具箱"：
- 它提供了**张量（Tensor）**计算能力——张量就是多维数组，是AI计算的基本数据结构
- 它提供了**自动求导**——训练模型时自动计算梯度，不用手写微积分公式
- 它提供了**神经网络模块**——常用的层（全连接、卷积、注意力……）都帮你写好了

> 比喻：如果AI开发是盖房子，PyTorch就是你的工具箱——锤子、锯子、电钻都有，你只需要关注怎么设计房子，不用自己造工具。

#### 4.2 张量（Tensor）：AI计算的基本单位

在PyTorch中，所有数据都以**张量（Tensor）**的形式存在。张量就是多维数组，不同维度有不同叫法，但**它们都是张量**：
- 0维张量（标量）: `5` —— 一个数
- 1维张量（向量）: `[1, 2, 3]` —— 一排数
- 2维张量（矩阵）: `[[1,2], [3,4]]` —— 一个表格
- 3维及以上张量: 更高维的数组，大模型的参数就是高维张量

> 标量、向量、矩阵都是张量的特例，就像正方形是长方形的特例一样。

```python
import torch
x = torch.tensor([1.0, 2.0, 3.0])   # 创建一个张量
y = x * 2 + 1                        # 张量运算
print(y)  # tensor([3., 5., 7.])
```

> 比喻：张量就像Excel表格的超级升级版——Excel只有行和列（2维），张量可以有任意维度，而且能在NPU上高速计算。

---
### 5. 昇腾NPU：AI加速芯片

**昇腾（Ascend）** 是华为自研的AI芯片系列。

#### 从开源模型到昇腾NPU，只需一步！

开源大模型通常基于 PyTorch 开发。昇腾提供了 **torch_npu**，它是 PyTorch 的昇腾适配插件，让原本的模型代码几乎不用改就能跑在 NPU 上：

| 操作 | 代码 | 说明 |
|------|------|------|
| 导入适配层 | `import torch_npu` | 一行导入，自动注册 NPU 后端 |
| 数据搬到NPU | `.to('npu:0')` | 把张量/模型放到第0号NPU |
| 检查NPU可用 | `torch.npu.is_available()` | 返回 True 表示环境正常 |

> 比喻：torch_npu 就像一个**万能转接头**，你原来的代码插上转接头就能用昇腾的NPU了。

昇腾还提供 **CANN**（Compute Architecture for Neural Networks），它是昇腾的计算架构，相当于NPU的"操作系统+驱动"，提供算子库、图编译等底层能力。

---
### 6. 动手实践：环境检查

先确认我们的昇腾NPU和软件环境都正常。

```python
import torch
import torch_npu

print(f"PyTorch 版本: {torch.__version__}")
print(f"torch_npu 版本: {torch_npu.__version__}")
print(f"NPU 是否可用: {torch.npu.is_available()}")
print(f"NPU 设备数量: {torch.npu.device_count()}")
print(f"NPU 设备名称: {torch.npu.get_device_name(0)}")
print()
print("如果上面显示 NPU 是否可用: True，说明环境OK，继续往下走！")
```

---
### 7. 下载模型：从魔搭社区获取 Qwen3-0.6B

大模型的参数文件很大（Qwen3-0.6B 约1.4GB），我们需要先下载到本地。

[魔搭社区（ModelScope）](https://www.modelscope.cn) 是国内的模型开源平台，相当于国内的 HuggingFace，下载速度更快。

> 比喻：就像从应用商店下载APP，模型也是一种"应用"，需要先下载才能使用。

> tips：此步骤如果cannlab提示`Error rendering`直接等待代码块执行完成即可，只是由于Jupyter扩展版本下载的进度条无法显示，不影响实际下载。

```python
from modelscope import snapshot_download

model_dir = snapshot_download('Qwen/Qwen3-0.6B', cache_dir='/mnt/workspace/models')
print(f'模型已下载到: {model_dir}')
print('下载完成后，模型文件会保存在本地，下次不需要重新下载。')
```

---
### 8. 加载分词器和模型

现在我们把"翻译官"（分词器）和"大脑"（模型）请到我们的NPU上。

几个关键参数解释：
- `attn_implementation="eager"`：指定注意力机制使用 **Eager模式** 执行——即每个算子逐个立即执行，不做图编译或算子融合优化。这是最基础的执行方式，便于我们逐步理解推理流程，后续课程会在此基础上加速
- `.to('npu:0')`：把模型放到第0号NPU上
- `.half()`：用半精度浮点数（float16）存储参数，每个数字只占2字节（而不是4字节），节省一半显存，速度也更快
- `model.eval()`：告诉模型"现在是考试时间，不是学习时间"，关闭训练专用的功能（如Dropout）

```python
from transformers import AutoTokenizer, AutoModelForCausalLM

model_path = '/mnt/workspace/models/models/Qwen--Qwen3-0.6B/snapshots/master'

print('正在加载分词器...')
tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
print('分词器加载完成！')

print('正在加载模型到NPU（需要一点时间）...')
model = AutoModelForCausalLM.from_pretrained(
    model_path,
    trust_remote_code=True,
    attn_implementation='eager'
).to('npu:0').half()
model.eval()
print(f'模型加载完成！设备: {model.device}，精度: {model.dtype}')
```

---
### 9. 体验分词器：文字和数字的转换

在让模型推理之前，我们先看看分词器是怎么工作的。

```python
test_text = '你好，我是昇腾'

tokens = tokenizer.encode(test_text)
decoded = tokenizer.decode(tokens)

print(f'原文: {test_text}')
print(f'编码为token IDs: {tokens}')
print(f'解码回文字: {decoded}')
print()
print('分词器把文字切分成一个个"词片"(token)，每个词片对应一个数字ID。')
print('模型就是基于这些数字ID来进行计算的。')
```

---
### 10. 第一次推理：让大模型"说话"

现在，激动人心的时刻到了——让Qwen3回答我们的问题！


推理步骤：
1. 用分词器把问题翻译成数字（token IDs）
2. **推理循环**：把token送入模型，得到下一个token的概率分布
3. **后处理**：
   - **选token**：从概率分布中选出概率最大的token（贪心解码）
   - **检查结束**：如果生成了结束标记（EOS），就停止生成
   - **拼接**：把新token拼到已有序列后面，继续下一轮
4. 用分词器把生成的token IDs翻译回文字

```python
question = '你好，请介绍一下AI是什么'

messages = [{'role': 'user', 'content': question}]
text = tokenizer.apply_chat_template(
    messages, tokenize=False, add_generation_prompt=True, enable_thinking=False
)
input_ids = torch.tensor([tokenizer.encode(text)], dtype=torch.long).to('npu:0')

print(f'你的问题: {question}')
print(f'分词后输入模型的内容: {text[:80]}...')
print(f'输入token数量: {input_ids.shape[1]}')
print()

max_new_tokens = 128
generated_ids = input_ids.clone()

print('模型正在推理（逐token生成）...')
for step in range(max_new_tokens):
    with torch.no_grad():
        # 模型单次执行推理
        logits = model(generated_ids).logits

    # 后处理①：选token——取概率最大的（贪心解码）
    next_token_logits = logits[:, -1, :]
    next_token_id = torch.argmax(next_token_logits, dim=-1, keepdim=True)

    # 后处理②：检查结束——遇到EOS就停止
    if next_token_id.item() == tokenizer.eos_token_id:
        print(f'  在第{step}步遇到结束标记(EOS)，停止生成')
        break

    # 后处理③：拼接——把新token加到序列末尾
    generated_ids = torch.cat([generated_ids, next_token_id], dim=1)

response = tokenizer.decode(generated_ids[0][input_ids.shape[1]:], skip_special_tokens=True)
print(f'\n模型的回答: {response}')
print(f'生成了 {generated_ids.shape[1] - input_ids.shape[1]} 个token')
```

---
### 11. 测量推理速度

我们来看看自己写的推理循环一次需要多长时间。

> 注意：第一次推理通常较慢（"热身"），后续会稳定下来，所以我们要先跑一次热身，再正式计时。

```python
import time

max_new_tokens = 128

print('热身中...')
generated_ids_warmup = input_ids.clone()
for step in range(max_new_tokens):
    with torch.no_grad():
        logits = model(generated_ids_warmup).logits
    next_token_id = torch.argmax(logits[:, -1, :], dim=-1, keepdim=True)
    if next_token_id.item() == tokenizer.eos_token_id:
        break
    generated_ids_warmup = torch.cat([generated_ids_warmup, next_token_id], dim=1)
# 同步接口，为了准确统计推理耗时添加
torch.npu.synchronize()
print('热身完成，开始正式计时')

times = []
for i in range(3):
    generated_ids = input_ids.clone()
    t0 = time.time()

    for step in range(max_new_tokens):
        with torch.no_grad():
            logits = model(generated_ids).logits
        next_token_id = torch.argmax(logits[:, -1, :], dim=-1, keepdim=True)
        if next_token_id.item() == tokenizer.eos_token_id:
            break
        generated_ids = torch.cat([generated_ids, next_token_id], dim=1)

    torch.npu.synchronize()
    elapsed = time.time() - t0
    num_generated = generated_ids.shape[1] - input_ids.shape[1]
    times.append(elapsed)
    print(f'  第{i+1}次: {elapsed:.3f}s (生成{num_generated}个token)')

avg_time = sum(times) / len(times)
print(f'\n平均推理时间: {avg_time:.3f}s')
print(f'生成速度: {num_generated / avg_time:.1f} tokens/s')
print(f'\n这个速度就是 Baseline（基线），下一个 Notebook 我们会用图编译来加速它！')
```

---
### 12. 更多有趣的问题

让我们再问模型几个不同类型的问题，感受大模型的能力。

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
    for step in range(128):
        with torch.no_grad():
            logits = model(generated_ids).logits
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
### 课后练习：和大模型自由对话

现在轮到你了！修改下面代码中的 `my_question` 变量，向大模型提出你自己的问题，观察它的回答。

你可以尝试：
- 问一个知识类问题，比如"中国的首都是哪里？"
- 让它写一段代码，比如"用C++写一个Hello World"
- 让它创作，比如"写一个关于AI的科幻小故事"
- 问一个需要推理的问题，比如"如果今天是周一，3天后是周几？"
- 试试用英文提问，看看它能不能回答

你还可以调整 `max_new_tokens` 参数（比如改成256），让模型生成更长的回答。

> 提示：推理循环和后处理的代码已经写好，你只需要修改问题本身。如果想挑战自己，试试把贪心解码（`torch.argmax`）改成随机采样（`torch.multinomial`），看看回答会有什么不同！

```python
# ====== 课后练习：修改下面的内容，自由和大模型对话！======

my_question = '你好，请用一句话介绍你自己'   # <-- 修改这里！换成你想问的任何问题
max_new_tokens = 128                         # <-- 修改这里！控制模型最多生成多少个token

# ====== 下面不用改 ======

messages = [{'role': 'user', 'content': my_question}]
text = tokenizer.apply_chat_template(
    messages, tokenize=False, add_generation_prompt=True, enable_thinking=False
)
input_ids = torch.tensor([tokenizer.encode(text)], dtype=torch.long).to('npu:0')

print(f'你的问题: {my_question}')
print('模型正在思考...')

generated_ids = input_ids.clone()
for step in range(max_new_tokens):
    with torch.no_grad():
        logits = model(generated_ids).logits
    next_token_id = torch.argmax(logits[:, -1, :], dim=-1, keepdim=True)
    if next_token_id.item() == tokenizer.eos_token_id:
        break
    generated_ids = torch.cat([generated_ids, next_token_id], dim=1)

response = tokenizer.decode(generated_ids[0][input_ids.shape[1]:], skip_special_tokens=True)
print(f'模型的回答: {response}')
print(f'\n生成token数: {generated_ids.shape[1] - input_ids.shape[1]}')
```

---
### 小结

恭喜你完成了第一次大模型推理！我们来回顾一下今天学到的：

1. **AI** 是让计算机通过数据学习来完成任务的技术
2. **大模型** 是参数量巨大的语言模型，能理解和生成文本
3. 推理需要 **分词器**（文字↔数字翻译）、**模型**（计算大脑）、**计算设备**（NPU）
4. **PyTorch** 是AI开发的"标准工具箱"，提供张量计算、自动求导、神经网络模块
5. 昇腾NPU通过 **torch_npu** 适配层，让代码几乎不用改就能跑在NPU上
6. 推理本质上是一个**推理循环**：模型前向传播 → 后处理（选token / 检查EOS / 拼接）→ 重复，直到遇到结束标记
7. **后处理** 是推理中不可或缺的环节，负责从概率分布中选出token、判断是否停止、维护生成序列

下一个 Notebook，我们将学习如何用 **CANN npugraph_ex** 来加速推理！

# ==========================================
## 📝 练习与验证

> 📌 原 Notebook 中的练习、编译命令和校验代码已按原顺序保留在上文。需要 CANN 运行时、Ascend NPU 或 CANNLab 环境的单元，执行前请先核对版本和设备条件。
