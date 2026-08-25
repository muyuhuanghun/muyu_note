---
source_repo: cann-learning-hub
source_path: quick_start/first_llm_inference/03_qwen3_npu_inference_fused_op.ipynb
source_commit: 1bf85454ed7c41e184a96fb51d109b6bb83b7c0d
note_kind: notebook_to_markdown
---

# 第三课：融合算子替换 —— 把"小车队"合并成"超级大巴"

> 📚 上游 Notebook：[quick_start/first_llm_inference/03_qwen3_npu_inference_fused_op.ipynb](https://gitcode.com/cann/cann-learning-hub/blob/master/quick_start/first_llm_inference/03_qwen3_npu_inference_fused_op.ipynb)
> 🧪 整理方式：保留 Markdown 与代码单元；省略 Jupyter 执行输出，避免把一次性环境结果误当成可复现结论。

## 🧭 学习目标

- 先跑通功能正确的 Baseline，再用 Profiling 定位瓶颈；
- 理解图模式、融合算子、量化和端到端收益验证。

# ==========================================
## 📖 课程内容

> 上一课我们用图编译消除了"路口红灯"，让 NPU 不再干等 CPU 调度。但路上跑的还是一辆辆"小轿车"——成百上千个小算子拆着跑，既多又慢。这节课我们就来把它们合并成"超级大巴"：**融合算子**。

---
### 1. 从上一课的两大优化方向说起

上一课开头我们打过一个比方——模型推理慢，就像一条拥堵的公路，原因有三：

| 瓶颈 | 优化方向 | 做什么 | 本课？ |
|------|---------|--------|:------:|
| 红灯多 | **图编译**（框架层） | 把所有算子编排成一张执行图，一次性交给NPU | 上一课 ✅ |
| 车多 + 车速慢 | **算子融合**（算子层） | 合并小算子为融合算子，并优化单个算子性能 | **本课** 👈 |

上一课解决了"红灯多"——CPU 不再逐个调度，NPU 不再空转。但图编译只是**编排**算子，并没有改变算子本身。如果路上跑的还是一堆小轿车：
- **车多**：一次归一化要拆成 `平方 → 求均值 → 加eps → 开方 → 倒数 → 乘权重` 六七个小算子，每个都要单独启动、读写一次内存
- **车速慢**：每个算子虽然功能一致，但不同实现方式算子的性能会有极大地差距。


本课我们就来动手做这件事：**用融合算子替换小算子拼接**。不过在动手之前，得先搞清楚两个基本问题——**算子到底是什么**？大模型又**由哪些算子组成**？

---
### 2. 算子是什么？

**算子（Operator，简称 Op）** 是模型计算的最小调度单元。拿最基础的矩阵乘 `matmul` 举例，它做的事是 $y = x \times W$。我们再加一个控制项：用一个属性 $a$ 决定输入 $x$ 是否先转置再乘，写出来就是：

$$y = \begin{cases} x \times W & a = 0 \\ x^T \times W & a = 1 \end{cases}$$

属性 $a$ 取 $0$ 或 $1$，决定走哪个公式。

算子里存在三类参数：


| 组成　　　　　　　　　| 公式里的符号 | 说明　　　　　　　　　　　　　　　　　　　　　　　 |
| -----------------------| :------------:| ----------------------------------------------------|
| **输入（Input）**　　 | $x$　　　　　| 上一道算子的输出流过来的数据张量，每次推理都不一样 |
| **权重（Weight）**　　| $W$　　　　　| 矩阵的值，训练时不断调整，训练完冻结　　　　　　　 |
| **属性（Attribute）** | $a$　　　　　| 选哪个公式，训练前就定好，训练中不调　　　　　　　 |

- **输入**是算子的原料——它不是这个算子自己产生的，而是上一道算子算完传过来的；每次推理用户喂的数据不同，输入就不同。
- **训练前就确定的是属性**：比如 $a=1$，它决定的是算子的**结构**（先转置 $x$ 还是不转），一旦定下来就不再变，训练过程不会去调它。
- **训练时不断调整的是权重**：比如 $W$ 的每个元素的值，训练就是在调这些值，让模型输出越来越逼近目标。训练完冻结，推理时不再变。

大模型里的算子结构一样，写成通用形式：

$$y = \text{Op}(x;\ w,\ a)$$


> 算子融合就是把多个算子串起来算的中间结果，合并成一个算子一次性算完——少读写几次中间数据、少启动几次计算。

---
### 3. 大模型由哪些算子单元组成？

要替换算子，得先知道大模型里有哪些算子。我们以本课程使用的 **Qwen3** 为例，从粗到细看它的结构。

#### 3.1 整体结构

```
                          ┌────────────────────┐
  token id ───────────▶  │   Embedding 查表    │  把 id 变成向量
                          └──────────┬─────────┘
                                     ▼
                          ┌──────────────────────┐
                          │  DecodeLayer 层 × N  │  ← 主体，重复堆叠 N 层
                          │  (Qwen3-0.6B: N=28)  │
                          └──────────┬───────────┘
                                     ▼
                          ┌─────────────────────┐
                          │    Qwen3RMSNorm     │
                          └──────────┬──────────┘
                                     ▼
                          ┌─────────────────────┐
                          │   LM Head (Linear)  │  映射回词表，得到 logits
                          └──────────┬──────────┘
                                     ▼
                                  下一个 token
```

主体是 **N 层重复堆叠的 DecodeLayer 层**，每一层的内部结构都一样。所以我们只要搞懂**一层**，就搞懂了整个模型。

#### 3.2 一层 DecodeLayer 内部结构介绍

每一层 DecodeLayer 内部，按数据流向可以拆成几个**粒度较大的单元**：

```
        hidden_states
            │
            ▼
      ┌─────────────┐
      │ Qwen3RMSNorm│  ◀── 输入归一化（Pre-Attention Norm）
      └────┬────────┘
           ▼
      ┌──────────────────────────┐
      │      Qwen3Attention      │  ◀── Q/K/V 投影 → QK-Norm → RoPE →
      │  (Q proj, K proj, V proj,│      打分 → softmax → 加权求和 → O proj
      │   RoPE, softmax, O proj) │
      └────────────┬─────────────┘
                   ▼  (+ 残差连接)
      ┌─────────────┐
      │ Qwen3RMSNorm│  ◀── 注意力后归一化（Post-Attention Norm）
      └────┬────────┘
           ▼
      ┌─────────────────────────┐
      │         MLP             │  ◀── 前馈网络：gate_proj → 激活 →
      │  (gate_proj, up_proj,   │      逐元素乘 → down_proj
      │   SiLU, down_proj)      │
      └────────────┬────────────┘
                   ▼  (+ 残差连接)
            下一层的输入
```

如果**不融合**，每个大方框内部都是一串小算子拼接；那通常我们会对以下单元进行融合：

| 单元（粗粒度） | 内部小算子（不融合时）　　　　　　　　　　　　　　　　　　 | 对应的融合算子　　　　　　　　　　　　　　 |
| ----------------| ------------------------------------------------------------| --------------------------------------------|
| **RMSNorm**　　| `pow → mean → add(eps) → rsqrt → mul → mul(weight)`　　　　| `npu_rms_norm`　　　　　　　　　　　　　　 |
| **Attention**　| `matmul → scaling → add(mask) → softmax → matmul → Linear` | `npu_fusion_attention` / FlashAttention 等 |
| **RoPE**　　　 | ` mul → mul → add`　　　　　　　　　　　　　　| `npu_rotary_mul`　　　　　　　　　　　　　 |

> 这张表是本课的核心地图：**左列是"要替换什么"，右列是"替换成什么"**。后面几节我们就挑其中一个——RMSNorm——亲手走一遍替换流程。

---
### 4. 以 RMSNorm 为例进行融合算子替换

RMSNorm（Root Mean Square Normalization）是 Qwen3 里最常出现的归一化单元——每一层 Transformer 里就出现两次，加上最后的 Final Norm，整个 Qwen3-0.6B（28 层）里一共 **57 个** RMSNorm。

#### 4.1 计算公式

给定三维输入 $x$（形状 $[B, S, H]$，即 `[batch, seq_len, hidden_size]`）、一维权重 $w$（形状 $[H]$，即 `[hidden_size]`）、标量属性 $\epsilon$（一个小常数）。RMSNorm **沿最后一维 $H$ 做归一化**：对每个 $(b, s)$ 位置，跨 $H$ 维求均方根，再逐元素缩放。计算为：

$$y_{b,s,i} = w_i \cdot \frac{x_{b,s,i}}{\sqrt{\frac{1}{H}\sum_{j=1}^{H} x_{b,s,j}^2 + \epsilon}}, \quad b=1..B,\ s=1..S,\ i=1..H$$

其中分母里的求和只对下标 $j$（即 `hidden_size` 那一维）进行，$b$、$s$ 固定——也就是说**每个 token 各自归一化**，彼此独立。拆成步骤看：
1. **平方**：$x_{b,s,j}^2$ —— 每个元素平方
2. **求均值**：沿最后一维 $H$ 求平均，得到方差 $\text{var}_{b,s} = \frac{1}{H}\sum_{j=1}^{H} x_{b,s,j}^2$，形状从 $[B,S,H]$ 降为 $[B,S,1]$
3. **加 epsilon**：$\text{var}_{b,s} + \epsilon$，防止除零
4. **开方求倒数**：$\text{rsqrt}_{b,s} = 1/\sqrt{\text{var}_{b,s} + \epsilon}$，形状仍为 $[B,S,1]$
5. **归一化**：$x_{b,s,i} \cdot \text{rsqrt}_{b,s}$，靠广播把 $[B,S,1]$ 拉回 $[B,S,H]$
6. **乘权重**：$w_i \cdot (\text{归一化结果})_{b,s,i}$，权重 $[H]$ 沿最后一维广播

光这一个公式，就涉及 **6个小算子**。

#### 4.2 RMSNorm 原小算子拼接实现方式介绍

我们看一下当前环境里 `transformers==4.51.0` 中 `Qwen3RMSNorm` 的原始实现。使用transformers库进行大模型推理时，大部分模型结构的定义都在transformers库中，位置位于`transformers/models/{模型文件夹}/modeling_{模型名称}.py`中，例如qwen3的模型结构文件就在`transformers/models/qwen3/modeling_qwen3.py` . 

通过如下命令可以定位transformers库位置：

```bash
!pip show transformers
```

`Location`显示的路径便是transformers库路径，从此路径下读取模型结构文件，这些算子的原始实现就在此文件中。

下面这段代码就是**不融合**时、用基础小算子拼接出来的版本（也正是昇腾替换前的原始写法）：

```python
class Qwen3RMSNorm(nn.Module):
    def __init__(self, hidden_size, eps=1e-6):
        super().__init__()
        self.weight = nn.Parameter(torch.ones(hidden_size))   # 权重 w
        self.variance_epsilon = eps                            # 属性 ε

    def forward(self, hidden_states):                          # 输入 x
        input_dtype = hidden_states.dtype
        hidden_states = hidden_states.to(torch.float32)        # （精度处理）转高精度
        variance = hidden_states.pow(2).mean(-1, keepdim=True) # ① 平方 + ② 求均值
        hidden_states = hidden_states * torch.rsqrt(variance + self.variance_epsilon)  # ③ 加ε + ④ 开方倒数 + ⑤ 归一化
        return self.weight * hidden_states.to(input_dtype)     # （精度处理）转回原精度 + ⑥ 乘权重
```

对应一下三类组成：
- **输入**：`hidden_states`（每次推理都变）
- **权重**：`self.weight`（训练学出来，推理时冻结）
- **属性**：`self.variance_epsilon`（即公式里的 $\epsilon$，构造时写死）

把公式里的步骤和代码里的**小算子**一一对应：

| 公式步骤 | 代码里的小算子 | 算子数 |
|---------|---------------|:------:|
| （精度处理） | `.to(float32)` | 1 |
| ① 平方 | `.pow(2)` | 1 |
| ② 求均值 | `.mean(-1)` | 1 |
| ③ 加 ε | `+ self.variance_epsilon` | 1 |
| ④ 开方求倒数 | `torch.rsqrt(...)` | 1 |
| ⑤ 归一化 | `hidden_states * ...` | 1 |
| （精度处理） | `.to(input_dtype)` | 1 |
| ⑥ 乘权重 | `self.weight * ...` | 1 |
| **合计** | | **8 个小算子** |

这 8 个小算子**串行执行**，每一步都要把中间结果写回内存、下一步再读出来——光 RMSNorm 一个单元就要 8 次算子启动、7 次中间显存读写。乘以全模型 57 个 RMSNorm，开销相当可观。

#### 4.3 融合算子接口：`torch_npu.npu_rms_norm`

昇腾 NPU 提供了 RMSNorm 的融合算子 `torch_npu.npu_rms_norm`，它把上面 8 个小算子在硬件内部**一次性算完**，中间结果不落盘、不回读。我们先看它的接口定义：

```python
torch_npu.npu_rms_norm(Tensor self, Tensor gamma, float epsilon=1e-6) -> (Tensor, Tensor)
```

三个参数正好对应 4.1 节公式里的三类组成，也和 `Qwen3RMSNorm` 里的成员一一对应：

| 接口参数 | 类型 | 含义 | 对应公式 | 对应 `Qwen3RMSNorm` 成员 |
|---------|------|------|---------|--------------------------|
| `self` | Tensor | 输入张量，支持 2~8 维，dtype 可为 float16/bfloat16/float32 | $x_{b,s,i}$，形状 $[B,S,H]$ | `forward` 的入参 `hidden_states` |
| `gamma` | Tensor | 权重张量，dtype 需与 `self` 一致，通常取 `self` 最后一维的大小 | $w_i$，形状 $[H]$ | `self.weight` |
| `epsilon` | float | 防除零小常数 | $\epsilon$ | `self.variance_epsilon` |

返回值是**两个** Tensor 的元组：
- 第 1 个：归一化结果 $y$，形状与输入 `self` 相同 $[B,S,H]$——这就是我们要的输出
- 第 2 个：反向传播用的中间结果（`reverse rms`），推理时用不到

所以调用时取 `[0]` 拿到最终输出即可。

> 注意 `gamma` 就是公式里的权重 $w$，只是接口里换了个名字——它和输入 `self` 的**最后一维大小必须一致**（$[H]$ 对 $[B,S,H]$ 的最后一维），靠广播沿 $H$ 维逐元素缩放。`epsilon` 是个 Python float（不是 Tensor），对应属性，推理时固定不变。

#### 4.4 融合算子替换：8 个小算子 → 1 个融合算子

用这个融合算子替换原来的小算子拼接，`Qwen3RMSNorm` 的实现变成：

```python
class Qwen3RMSNorm(nn.Module):
    def __init__(self, hidden_size, eps=1e-6):
        super().__init__()
        self.weight = nn.Parameter(torch.ones(hidden_size))   # 权重 w
        self.variance_epsilon = eps                            # 属性 ε

    def forward(self, hidden_states):                          # 输入 x
        return torch_npu.npu_rms_norm(
            hidden_states,                                     # 输入
            self.weight,                                       # 权重
            self.variance_epsilon                              # 属性
        )[0]
```

对比一下替换前后：

| 　　　　　　　　　| 替换前（小算子拼接） | 替换后（融合算子）　　 |
| -------------------| ----------------------| ------------------------|
| 算子数　　　　　　| 8 个　　　　　　　　 | **1 个**　　　　　　　 |
| 算子启动/调度次数 | 8 次　　　　　　　　 | 1 次　　　　　　　　　 |
| 中间显存读写　　　| 7 次　　　　　　　　 | 0次　　　　　　　　　　|
| 精度　　　　　　　| 转两次 dtype　　　　 | 算子内部统一精度处理 |
| 代码行数　　　　　| 5 行计算　　　　　　 | 1 行调用　　　　　　　 |


这就是算子融合的威力：**同样的数学计算，用更少的算子、更少的显存搬运、更针对硬件的实现来完成**。RMSNorm 只是一个例子，Attention、RoPE 等单元都可以用同样的思路替换成对应的融合算子，下一节我们将动手在模型上做替换并对比效果。

#### 4.5 算子替换执行

可以直接修改模型结构源文件进行算子替换，也可以在执行时对原融合算子模块进行重定义，如下进行替换：

```python
import torch
import torch_npu
import transformers.models.qwen3.modeling_qwen3 as qwen3_mod   # 拿到模块对象

# ---- 保存原始实现，方便随时切回 ----
orig_forward = qwen3_mod.Qwen3RMSNorm.forward

# ---- 定义"小算子拼接"版本（替换前）----
def small_ops_forward(self, hidden_states):
    input_dtype = hidden_states.dtype
    hidden_states = hidden_states.to(torch.float32)
    variance = hidden_states.pow(2).mean(-1, keepdim=True)
    hidden_states = hidden_states * torch.rsqrt(variance + self.variance_epsilon)
    return self.weight * hidden_states.to(input_dtype)

# ---- 定义"融合算子"版本（替换后）----
def fused_forward(self, hidden_states):
    return torch_npu.npu_rms_norm(hidden_states, self.weight, self.variance_epsilon)[0]

# ---- 打补丁：一行切换 ----
qwen3_mod.Qwen3RMSNorm.forward = small_ops_forward   # 切到小算子版
# qwen3_mod.Qwen3RMSNorm.forward = fused_forward     # 切到融合版
# qwen3_mod.Qwen3RMSNorm.forward = orig_forward      # 切回原始版
```

#### 4.6 替换完进行Eager模式推理

下面在 **Eager 模式**（不开图编译）下，分别用小算子版和融合算子版做推理，对比耗时。这样看到的是**纯算子层面**的差异，不混入图编译的效果。

```python
import time

# 加载模型
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

# 准备输入
messages = [{'role': 'user', 'content': '你好，请介绍一下AI是什么'}]
text = tokenizer.apply_chat_template(
    messages, tokenize=False, add_generation_prompt=True, enable_thinking=False
)
input_ids = torch.tensor([tokenizer.encode(text)], dtype=torch.long).to('npu:0')
max_new_tokens = 128

# 推理函数
def run_inference(model, input_ids, max_new_tokens):
    generated_ids = input_ids.clone()
    for step in range(max_new_tokens):
        with torch.no_grad():
            logits = model(generated_ids).logits
        next_token_id = torch.argmax(logits[:, -1, :], dim=-1, keepdim=True)
        if next_token_id.item() == tokenizer.eos_token_id:
            break
        generated_ids = torch.cat([generated_ids, next_token_id], dim=1)
    torch.npu.synchronize()
    return generated_ids

# ---- 1. 小算子版（不融合）----
qwen3_mod.Qwen3RMSNorm.forward = small_ops_forward
print('小算子版热身...')
run_inference(model, input_ids, max_new_tokens)

print('小算子版计时:')
times_small = []
for i in range(3):
    t0 = time.time()
    g = run_inference(model, input_ids, max_new_tokens)
    times_small.append(time.time() - t0)
    print(f'  第{i+1}次: {times_small[-1]:.3f}s')

# ---- 2. 融合算子版 ----
qwen3_mod.Qwen3RMSNorm.forward = fused_forward
print('\n融合算子版热身...')
run_inference(model, input_ids, max_new_tokens)

print('融合算子版计时:')
times_fused = []
for i in range(3):
    t0 = time.time()
    g = run_inference(model, input_ids, max_new_tokens)
    times_fused.append(time.time() - t0)
    print(f'  第{i+1}次: {times_fused[-1]:.3f}s')

# ---- 3. 对比 ----
avg_small = sum(times_small) / len(times_small)
avg_fused = sum(times_fused) / len(times_fused)
num_tokens = g.shape[1] - input_ids.shape[1]
print(f'\n=== 对比结果（Eager 模式，纯算子层面）===')
print(f'生成 token 数: {num_tokens}')
print(f'小算子版平均: {avg_small:.3f}s  ({num_tokens/avg_small:.1f} tokens/s)')
print(f'融合算子版平均: {avg_fused:.3f}s  ({num_tokens/avg_fused:.1f} tokens/s)')
print(f'加速比: {avg_small/avg_fused:.2f}x')
```

可以看到，**仅仅替换了 RMSNorm 一个单元**，推理速度就有明显提升。而模型里还有 Attention、MLP、RoPE 等单元同样可以用融合算子替换，如果把它们全部替换，加速效果会更加显著。

> 注意：这里对比的是 Eager 模式下的纯算子差异，没有开图编译。上一课的图编译优化和本课的算子融合优化是**正交**的——两者各管一层，可以叠加使用。

### 5.课后实践

1. 替换RMSNorm算子基础上使能图模式进行推理
2. 替换RoPE融合算子`npu_rotary_mul`进行Eager模式推理，原函数名称为apply_rotary_pos_emb，可以仿照上述替换代码，用qwen3_mod.apply_rotary_pos_emb获取原实现并替换，Qwen3中原旋转编码算子具体实现如下：
```
def apply_rotary_pos_emb(q, k, cos, sin, position_ids=None, unsqueeze_dim=1):
    cos = cos.unsqueeze(unsqueeze_dim)
    sin = sin.unsqueeze(unsqueeze_dim)
    q_embed = (q * cos) + (rotate_half(q) * sin)
    k_embed = (k * cos) + (rotate_half(k) * sin)
    return q_embed, k_embed
```

# ==========================================
## 📝 练习与验证

> 📌 原 Notebook 中的练习、编译命令和校验代码已按原顺序保留在上文。需要 CANN 运行时、Ascend NPU 或 CANNLab 环境的单元，执行前请先核对版本和设备条件。
