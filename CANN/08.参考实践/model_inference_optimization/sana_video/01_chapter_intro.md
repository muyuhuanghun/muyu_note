---
source_repo: cann-learning-hub
source_path: reference_practice/model_inference_optimization/sana_video/01_chapter_intro.ipynb
source_commit: 1bf85454ed7c41e184a96fb51d109b6bb83b7c0d
note_kind: notebook_to_markdown
---

# 1 章节介绍

> 📚 上游 Notebook：[reference_practice/model_inference_optimization/sana_video/01_chapter_intro.ipynb](https://gitcode.com/cann/cann-learning-hub/blob/master/reference_practice/model_inference_optimization/sana_video/01_chapter_intro.ipynb)
> 🧪 整理方式：保留 Markdown 与代码单元；省略 Jupyter 执行输出，避免把一次性环境结果误当成可复现结论。

## 🧭 学习目标

- 先读懂概念，再运行代码片段验证关键结论；
- 把本节内容接入后续 CANN / Ascend NPU 实践。

# ==========================================
## 📖 课程内容

本教程《Sana-Video 推理优化实践》以 `Sana-Video` 为例，展示如何在昇腾 NPU 上完成模型跑通、Profiling 分析，并在整网中接入 `RMSNorm` 融合算子验证性能收益。

---

### 学习目标
- 完成 `Sana-Video` Baseline 跑通。
- 使用 `torch_npu.profiler` 采集 Baseline 性能数据。
- 在 `Sana-Video` 中接入 `torch_npu.npu_rms_norm` 并验证整网收益。
- 对比优化前后的整网时延变化。

### 章节安排
- [1 章节介绍](https://gitcode.com/cann/cann-learning-hub/blob/master/reference_practice/model_inference_optimization/sana_video/01_chapter_intro.ipynb)
- [2 Baseline 跑通](https://gitcode.com/cann/cann-learning-hub/blob/master/reference_practice/model_inference_optimization/sana_video/02_baseline_run.ipynb)
- [3 Profiling 分析](https://gitcode.com/cann/cann-learning-hub/blob/master/reference_practice/model_inference_optimization/sana_video/03_profiling_analysis.ipynb)
- [4 RMSNorm 融合接入与收益验证](https://gitcode.com/cann/cann-learning-hub/blob/master/reference_practice/model_inference_optimization/sana_video/04_rmsnorm_fusion_optimization.ipynb)

### 环境说明
- 本教程依赖上游 `Sana` 仓库代码，并在运行目录中拉取固定 commit。
- 在线体验请直接在 GitCode Notebook 环境中执行；Notebook 默认复用环境中已预装的 `torch`、`torch_npu`、`torchvision` 与 `torchaudio`。本地运行前请先准备兼容版本的上述依赖，并配置 CANN 与 `torch_npu`。
- 运行本教程时，主机内存需至少 16GB。Notebook 计算类型建议选择 NPU 910B、CPU 32GB，容器镜像建议选择 ubuntu22-cann8.5-py3.11-jupyter-notebook。

# ==========================================
## 📝 练习与验证

> 📌 原 Notebook 中的练习、编译命令和校验代码已按原顺序保留在上文。需要 CANN 运行时、Ascend NPU 或 CANNLab 环境的单元，执行前请先核对版本和设备条件。
