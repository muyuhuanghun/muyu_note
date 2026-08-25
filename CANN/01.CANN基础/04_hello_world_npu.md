---
source_repo: cann-learning-hub
source_path: quick_start/cann_basics/04_hello_world_npu.ipynb
source_commit: 1bf85454ed7c41e184a96fb51d109b6bb83b7c0d
note_kind: notebook_to_markdown
---

# Hello World：在 NPU 上跑通第一个加法

> 📚 上游 Notebook：[quick_start/cann_basics/04_hello_world_npu.ipynb](https://gitcode.com/cann/cann-learning-hub/blob/master/quick_start/cann_basics/04_hello_world_npu.ipynb)
> 🧪 整理方式：保留 Markdown 与代码单元；省略 Jupyter 执行输出，避免把一次性环境结果误当成可复现结论。

## 🧭 学习目标

- 先读懂概念，再运行代码片段验证关键结论；
- 把本节内容接入后续 CANN / Ascend NPU 实践。

# ==========================================
## 📖 课程内容

本教程带你从零开始，在昇腾 NPU 上完成第一个张量加法运算。

你将学到：
1. 如何检查 NPU 是否可用
2. 如何将数据从 CPU 搬运到 NPU
3. 如何在 NPU 上执行加法
4. 如何将结果搬回 CPU 验证
5. NPU 与 CPU 的性能对比

### Step 1：导入必要的库

- `torch`：PyTorch 深度学习框架
- `torch_npu`：昇腾 NPU 适配层，导入后 PyTorch 自动识别 `npu` 设备

```python
import torch
import torch_npu
```

### Step 2：检查 NPU 是否可用

就像用 `torch.cuda.is_available()` 检查 GPU 一样，我们用 `torch.npu.is_available()` 检查 NPU。

如果返回 `False`，说明 NPU 驱动未安装、CANN 环境未配置、或当前机器没有昇腾 NPU 硬件。

```python
print(f"NPU 是否可用: {torch.npu.is_available()}")
print(f"NPU 设备数量: {torch.npu.device_count()}")
if torch.npu.is_available():
    print(f"当前 NPU 设备名: {torch.npu.get_device_name(0)}")
```

### Step 3：在 CPU 上创建两个张量

先用 PyTorch 在 CPU 上创建两个简单的张量，作为加法的输入。

这里我们用全 1 和全 2 的张量，方便验证结果。

```python
a_cpu = torch.ones(3, 3)
b_cpu = torch.full((3, 3), 2.0)

print(f"a (CPU):\n{a_cpu}")
print(f"b (CPU):\n{b_cpu}")
print(f"a 的设备: {a_cpu.device}")
```

### Step 4：将张量搬运到 NPU

调用 `.npu()` 将张量从 CPU 搬运到 NPU 的 Device Memory。

这个过程在底层调用了 CANN 的 `acl.rt.memcpy`，将数据从 Host Memory 拷贝到 Device Memory（HBM）。

> 类比：就像把食材从仓库（CPU 内存）搬到厨房案板（NPU 内存），厨师（AI Core）才能开始做菜。

```python
a_npu = a_cpu.npu()
b_npu = b_cpu.npu()

print(f"a (NPU):\n{a_npu}")
print(f"b (NPU):\n{b_npu}")
print(f"a 的设备: {a_npu.device}")
```

### Step 5：在 NPU 上执行加法

直接用 `+` 运算符或 `torch.add()` 即可。

PyTorch 会自动调用 CANN 内置的 Add 算子，由 AI Core 的 **Vector 计算单元** 执行逐元素加法。

底层流程：
1. Host 侧 Tiling：计算数据切分策略
2. 任务下发：通过 ACL 将 Kernel 下发到 NPU
3. Device 侧执行：AI Core 的 Vector 单元执行 Add
4. 结果写入 Device Memory

```python
c_npu = a_npu + b_npu

print(f"c = a + b (NPU):\n{c_npu}")
print(f"c 的设备: {c_npu.device}")
```

### Step 6：将结果搬回 CPU 验证

调用 `.cpu()` 将结果从 NPU 搬回 CPU，然后与 CPU 上的计算结果对比，验证正确性。

这一步在实际训练/推理中通常不需要——后续计算会继续在 NPU 上进行。这里只是为了教学验证。

```python
c_cpu = c_npu.cpu()
c_expected = a_cpu + b_cpu

print(f"NPU 结果搬回 CPU:\n{c_cpu}")
print(f"CPU 参考结果:\n{c_expected}")
print(f"结果一致: {torch.allclose(c_cpu, c_expected)}")
```

### Step 7：用更大的张量体验 NPU 并行加速

3×3 的小张量无法体现 NPU 的优势——数据量太小，计算时间远小于数据搬运时间。

让我们用更大的张量（10000×10000，约 400MB）来感受 NPU 的并行计算能力。

```python
import time

N = 10000
a_large = torch.randn(N, N, dtype=torch.float32)
b_large = torch.randn(N, N, dtype=torch.float32)
print(f"张量大小: {N}x{N}，约 {a_large.numel() * 4 / 1024**2:.0f} MB")
```

#### CPU 执行计时

在 CPU 上执行加法，测量耗时。

```python
start = time.time()
c_cpu_large = a_large + b_large
cpu_time = time.time() - start
print(f"CPU 加法耗时: {cpu_time*1000:.2f} ms")
```

#### NPU 执行计时

在 NPU 上执行加法，测量耗时。

注意：NPU 执行是异步的，需要调用 `torch.npu.synchronize()` 等待计算完成才能准确计时。

> 这和 GPU 一样——`torch.cuda.synchronize()` 用于 GPU，`torch.npu.synchronize()` 用于 NPU。

```python
a_npu_large = a_large.npu()
b_npu_large = b_large.npu()

torch.npu.synchronize()
start = time.time()
c_npu_large = a_npu_large + b_npu_large
torch.npu.synchronize()
npu_time = time.time() - start
print(f"NPU 加法耗时: {npu_time*1000:.2f} ms")
```

#### 结果验证与性能对比

```python
c_npu_back = c_npu_large.cpu()
match = torch.allclose(c_npu_back, c_cpu_large, rtol=1e-5)
print(f"NPU 与 CPU 结果一致: {match}")
print(f"\n{'='*50}")
print(f"性能对比:")
print(f"  CPU: {cpu_time*1000:.2f} ms")
print(f"  NPU: {npu_time*1000:.2f} ms")
if npu_time > 0:
    print(f"  加速比: {cpu_time/npu_time:.1f}x")
```

### Step 8：NPU 加速的优势分析

#### 为什么 NPU 更快？

- **计算单元多**：CPU 只有少量通用 ALU，NPU 有数十~数百个 Vector + Cube 单元
- **并行度高**：CPU 串行或少量并行，NPU 大规模数据并行
- **低精度优化**：CPU 以 FP64 为主，NPU 针对 FP16/BF16 优化

#### 什么时候 NPU 有优势？

- **计算密集型任务**：矩阵乘法、卷积、大规模逐元素运算
- **批量并行**：同一操作对大量数据重复执行
- **低精度可接受**：FP16/BF16/FP8,甚至是Int8/FP4 可满足需求

#### 什么时候 CPU 更合适？

- **小数据量**：数据搬运开销 > 计算节省
- **复杂控制流**：大量条件分支、动态 shape
- **高精度需求**：必须 FP64

### Step 9：总结

恭喜！你已经完成了在 NPU 上的第一个加法运算！

回顾关键步骤：

```python
import torch
import torch_npu                    # 1. 导入 NPU 适配层

a = torch.ones(3, 3).npu()        # 2. 创建张量并搬到 NPU
b = torch.full((3,3), 2.0).npu()  # 3. 同上
c = a + b                          # 4. NPU 自动执行加法
print(c.cpu())                     # 5. 搬回 CPU 查看结果
```

**5 行代码，从 CPU 走到 NPU！**

接下来，你可以：
- 学习 [Ascend C 算子开发](https://gitcode.com/cann/cann-learning-hub/tree/master/tutorials/ascendc_operator_development) 开发自定义高性能算子
- 体验 [第一个自定义算子](https://gitcode.com/cann/cann-learning-hub/tree/master/quick_start/first_custom_operator) 了解算子开发全流程
- 体验 [第一个算子 API 调用](https://gitcode.com/cann/cann-learning-hub/tree/master/quick_start/first_operator_api_call) 调用 CANN 内置算子

# ==========================================
## 📝 练习与验证

> 📌 原 Notebook 中的练习、编译命令和校验代码已按原顺序保留在上文。需要 CANN 运行时、Ascend NPU 或 CANNLab 环境的单元，执行前请先核对版本和设备条件。
