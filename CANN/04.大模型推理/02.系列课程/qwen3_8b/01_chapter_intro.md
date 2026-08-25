---
source_repo: cann-learning-hub
source_path: tutorials/llm_inference/qwen3_8b/01_chapter_intro.ipynb
source_commit: 1bf85454ed7c41e184a96fb51d109b6bb83b7c0d
note_kind: notebook_to_markdown
---

# 1 章节介绍

> 📚 上游 Notebook：[tutorials/llm_inference/qwen3_8b/01_chapter_intro.ipynb](https://gitcode.com/cann/cann-learning-hub/blob/master/tutorials/llm_inference/qwen3_8b/01_chapter_intro.ipynb)
> 🧪 整理方式：保留 Markdown 与代码单元；省略 Jupyter 执行输出，避免把一次性环境结果误当成可复现结论。

## 🧭 学习目标

- 先跑通功能正确的 Baseline，再用 Profiling 定位瓶颈；
- 理解图模式、融合算子、量化和端到端收益验证。

# ==========================================
## 📖 课程内容

本教程《Qwen3-8B 推理优化实践》以 `Qwen3-8B` 为例，展示如何在昇腾 NPU 上使用 cann-recipes-infer 推理框架完成模型离线推理跑通、Profiling 分析，并验证 Dense RMSNorm NPU 融合路径的性能收益。课程按 recipes 工作流展开：查看并修改 `models/qwen/config/` 下的 YAML 配置，通过 `executor/scripts/infer.sh` 拉起离线推理，再从日志和 Profiler 产物中分析优化点。

### 学习目标

- 了解 Qwen3-8B 在 NPU 上进行推理实践时的环境、权重和资源要求。
- 了解 Baseline、Profiling、优化版三类 recipes YAML 应该修改哪些字段，并通过 `executor/scripts/infer.sh` 跑通推理。
- 在 YAML 中打开 Profiling 开关，进入 recipes `prof/` 目录查看 kernel details、trace 和算子统计。
- 对比 QwenRMSNorm 小算子路径与 `torch_npu.npu_rms_norm` / `torch_npu.npu_add_rms_norm` 融合路径的端到端指标。
- 结合单算子精度、吐字检查和文本一致性给出优化建议。

### 章节安排

- [1 章节介绍](https://gitcode.com/cann/cann-learning-hub/blob/master/tutorials/llm_inference/qwen3_8b/01_chapter_intro.ipynb)
- [2 Baseline 跑通](https://gitcode.com/cann/cann-learning-hub/blob/master/tutorials/llm_inference/qwen3_8b/02_baseline_inference.ipynb)
- [3 Profiling 分析](https://gitcode.com/cann/cann-learning-hub/blob/master/tutorials/llm_inference/qwen3_8b/03_profiling_analysis.ipynb)
- [4 Dense RMSNorm NPU 融合路径优化验证](https://gitcode.com/cann/cann-learning-hub/blob/master/tutorials/llm_inference/qwen3_8b/04_npu_optimization.ipynb)
- [5 量化Qwen3-8B模型](https://gitcode.com/cann/cann-learning-hub/blob/master/tutorials/llm_inference/qwen3_8b/05_quantization_qwen3_8b.ipynb)
- [6 自定义量化 A8W8 matmul 算子开发并接入 Qwen3-8B](https://gitcode.com/cann/cann-learning-hub/blob/master/tutorials/llm_inference/qwen3_8b/06_custom_matmul_operator_development_and_integration_with_qwen3_8b.ipynb)

### 环境说明

- 在线体验请直接在 GitCode Notebook 环境中执行；Notebook 环境需包含 CANN、`torch`、`torch_npu`、`transformers`、`modelscope` 和 `datasets`。
- 本地运行前请先执行 `/usr/local/Ascend/ascend-toolkit/set_env.sh` 或等价 CANN 环境脚本。
- 运行 Qwen3-8B BF16 权重约需 16GB 权重空间，短上下文单卡验证建议使用 64GB HBM NPU，磁盘空间建议至少 40GB。
- 模型权重使用 `Qwen/Qwen3-8B`。首次运行 Baseline 推理时会通过 ModelScope 下载并缓存权重；如环境中已准备本地权重，可设置 `QWEN3_8B_MODEL_PATH=/path/to/Qwen3-8B`。
- 性能基准测试默认关闭 thinking 模式，并固定 prompt、batch、采样参数和输出长度。

### 指标口径

课程中的 `tokens_per_second` 和 `mean_per_token_latency_s` 来自 recipes 离线推理日志中的 prefill/decode 计时。Profiling 用于观察算子分布和定位优化点，第 4 章再结合 A/B 指标、单算子精度、吐字检查和文本一致性给出优化建议。

# ==========================================
## 📝 练习与验证

> 📌 原 Notebook 中的练习、编译命令和校验代码已按原顺序保留在上文。需要 CANN 运行时、Ascend NPU 或 CANNLab 环境的单元，执行前请先核对版本和设备条件。
