# muyu_note

个人学习笔记仓库，使用 Obsidian 管理，内容以 AI、编程、深度学习和基础课程笔记为主。

近代史纲要笔记整理自[Xovee/uestc-course: 🎓电子科技大学 📔课程资料](https://github.com/Xovee/uestc-course/tree/main)

## 仓库概览

这个仓库主要用于：

- 记录课程学习过程中的知识点
- 整理 AI 工具、开发工具和本地模型相关资料
- 保存 Obsidian Canvas 图示、截图和辅助图片
- 持续沉淀可复用的实践笔记

## 目录结构

### AI 与工具

- `AI_CODING/`
  - AI agent、IDE 集成、AI coding 使用经验
- `Github/`
  - GitHub 基础、学生认证、Copilot、Git 基础操作等
- `LLAMA.CPP/`
  - 本地大模型运行全链路笔记（前期准备 → 量化格式转换 → 核心参数调优 → 性能优化 → Server API → LoRA 适配器 → 多模型管理 → 进阶玩法，共 9 章）
- `工具集/`
  - 分类整理的工具清单与使用笔记（文件管理、学习辅助、科研工具、编程辅助、服务器与环境等 13 类）
  - 含 UESTC MOOC 平台相关工具与分析

### 课程与技术学习

- `基于pytorch的深度学习/`
  - `Deep Learning Basic/` — 深度学习基础，共 14 章（概述、线性模型、梯度下降、反向传播、线性回归、逻辑回归、多维输入、Dataset & Dataloader、Softmax 分类器、基础/高级 CNN、RNN、RNN 分类器、Adam 优化器与权重衰减）
  - `Deep Learning advance/` — 深度学习进阶（UNet 图像分割、YOLO 目标检测、FaceNet 度量学习）
  - `Transformer/` — Transformer 架构相关笔记（Canvas 知识图谱，基于吴恩达课程框架）
  - `pythorch photos/` — 课程图示与截图
- `传统机器学习(结合西瓜书)/`
  - `all_md/` — 支持向量机、决策树、集成学习等理论笔记
  - `all_ipynb/` — 配套 Jupyter Notebook 代码
- `CANN/`
  - 华为昇腾 CANN 异构计算学习笔记，按板块组织：CANN 基础 → 快速上手 → AscendC 算子开发 → 大模型推理 → 专题算子 → HiXL 单边通信 → 社区实战 → 参考实践 → 技术博客等
  - 附官方资料库快照 `CANN-assets-20260813/`（技术博客、算子开发教程、快速上手文档）与学习路线 Canvas
- `PBLF/`
  - 算法练习题与练习记录
- `异构多核音频处理/`
  - 异构多核音频处理课程详解（MSP430 MCU → C674x DSP → DM8168 异构多核）
  - `VSCode嵌入式开发环境/` — VSCode 替代 Keil 搭建 STM32 开发环境指南

### 综合复习资料

- `other learning/`
  - `大一下期末复习/` — 近代史、离散数学、数据结构期末复习（含 PPT 转 Markdown 笔记）与英语词汇
  - `程序与算法设计/` — C 语言数据结构实现 + 成都地铁最短路径项目 + icoding 复习题与真题索引
  - `线性代数/`、`微积分/` — 数学基础笔记
  - `大学物理电磁学/` — 电磁学期末复习（静电场、稳恒磁场、变化的电磁场与电磁波，含公式推导、模型总结、易错习题）
  - `居然还有六级/` — CET-6 备考复习整理（写作框架、高分句式、话题语料、真题汇总、范文）
  - 智能体开发与教育应用实验报告

### 其他主题

- `量化交易入门(X)/`
  - 量化交易入门笔记（Hull《期权、期货及其他衍生品》章节笔记等）
- `灵感/`
  - 随手记录的想法与灵感片段
- `obsidian同步/`
  - Obsidian 多设备同步方案整理（自建 Azure + CouchDB + LiveSync 实时同步完整指南，含完整排错记录）
- `服务器与VPS/`
  - Linux 基础命令速查（文件操作、用户权限、网络、进程管理等）
- `科学上网/`
  - 网络访问与相关原理记录

### 敏感信息（不公开）

仓库中部分敏感内容（账号凭据、Token、研究项目草稿等）存放在 `secrets/` 目录下，该目录已通过 `.gitignore` 排除，不会推送到远程仓库，并在本地独立进行版本管理。

## 文件类型

仓库当前主要包含以下内容：

- `*.md`：Markdown 笔记
- `*.canvas`：Obsidian Canvas 可视化笔记
- `*.png`：课程图示、截图和辅助说明图片
- `.obsidian/`：Obsidian 配置与插件数据

## 推荐使用方式

建议直接使用 Obsidian 打开此仓库，以获得完整体验：

- 查看 Canvas 结构图
- 使用双向链接和搜索
- 保留原有笔记组织方式
- 访问 `.obsidian/` 中的本地配置

## 当前内容重点

现阶段内容主要集中在以下几个方向：

1. AI coding 工具与工作流（Claude Code 辅助学习、IDE 集成）
2. PyTorch 深度学习课程学习（14 章基础 + 进阶：UNet/YOLO/FaceNet + Transformer 论文精读）
3. 华为昇腾 CANN 异构计算（AscendC 算子开发、大模型推理优化、HiXL 单边通信）
4. 传统机器学习（西瓜书）理论与实践（SVM → 半监督学习，完整覆盖）
5. C 语言数据结构与程序设计（稀疏矩阵、二叉树、哈夫曼树、图、哈希表、排序，含成都地铁最短路径项目）
6. 本地大模型运行全链路（llama.cpp 9 章：量化、调优、API、LoRA、多模型管理）
7. 各科期末复习资料整合（近代史、离散数学、数据结构、大学物理电磁学，见 `other learning/`）
8. 量化交易入门（Hull《期权、期货及其他衍生品》章节笔记）
9. GitHub 与开发环境使用、Linux 基础命令与服务器管理
10. 异构多核音频处理课程笔记与 VSCode 嵌入式开发环境搭建
11. CET-6 / 英语备考复习（真题、句式分类、话题语料、范文）
12. Obsidian 多设备同步方案（自建 Azure + CouchDB + LiveSync 实时同步，含完整排错记录）

## 说明

- 仓库内容会持续更新
- 部分目录以资料整理为主，部分目录以课程笔记为主
- 图片和 Canvas 文件较多，适合配合 Obsidian 一起查看

## 协作规范

本仓库 `main` 分支已开启分支保护，禁止直接推送。所有改动必须通过 Pull Request 合并。

### 提交流程

1. **从 main 创建特性分支**
   ```bash
   git checkout main
   git pull origin main
   git checkout -b feature/你的分支名
   ```

2. **在特性分支上提交并推送**
   ```bash
   git add .
   git commit -m "简要描述改动内容"
   git push origin feature/你的分支名
   ```

3. **在 GitHub 上创建 Pull Request**
   - 目标分支选择 `main`
   - 标题简明扼要，描述清楚改动内容
   - 等待仓库管理员 Review 并合并

### 注意事项

- 不要直接向 `main` 分支推送代码
- 一个 PR 尽量只包含一个独立的改动主题
- commit message 使用中文，描述清楚做了什么
