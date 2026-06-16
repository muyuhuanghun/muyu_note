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
- `ANTHROPIC/`
  - Claude 相关笔记
- `OPENAI_GPT_CODEX/`
  - Codex 相关记录
- `Github/`
  - GitHub 基础、学生认证、Token、Copilot、Git 基础操作等
- `LLAMA.CPP/`
  - 本地运行大模型的准备与使用笔记
- `GOOGLE INFO/`
  - Google 相关信息整理
- `TENCENT INFO/`
  - 腾讯相关记录
- `UESTC INFO/`
  - 学校相关信息

### 课程与技术学习

- `基于pytorch的深度学习/`
  - `Deep Learning Basic/` — 深度学习基础，共 14 章（概述、线性模型、梯度下降、反向传播、线性回归、逻辑回归、多维输入、Dataset & Dataloader、Softmax 分类器、基础/高级 CNN、RNN、RNN 分类器、Adam 优化器与权重衰减）
  - `Deep Learning advance/` — 深度学习进阶（UNet 图像分割、YOLO 目标检测、FaceNet 度量学习）
  - `Transformer/` — Transformer 架构相关笔记（Canvas 知识图谱，基于吴恩达课程框架）
  - `pythorch photos/` — 课程图示与截图
- `传统机器学习(结合西瓜书)/`
  - `all_md/` — 支持向量机、决策树、集成学习等理论笔记
  - `all_ipynb/` — 配套 Jupyter Notebook 代码
- `PBLF/`
  - 算法练习题与练习记录
- `程序与算法设计/`
  - C 语言数据结构实现（稀疏矩阵、二叉树、哈夫曼树、图、哈希表、排序算法）+ 成都地铁最短路径项目
- `微积分/`
  - 微积分基础笔记
- `线性代数/`
  - 线性代数基础笔记

### 期末复习

- `期末复习/`
  - `近代史/` — 中国近代史纲要完整复习资料（含 Canvas 白板）
  - `离散数学/` — 离散数学完整复习资料（含 Canvas 白板）
- `大学物理电磁学/`
  - 大学物理电磁学期末复习（静电场、稳恒磁场、变化的电磁场与电磁波，含公式推导、模型总结、易错习题）

### 其他主题

- `服务器与VPS/`
  - Linux 基础命令速查（文件操作、用户权限、网络、进程管理等）
- `科学上网/`
  - 网络访问与相关原理记录
- `other learning/`
  - CET-6 备考复习整理（写作框架、高分句式、话题语料、近三年真题汇总、翻译核心词汇、范文）
  - 智能体开发与教育应用实验报告
- `Excalidraw/`
  - 绘图资源目录

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

1. AI coding 工具与工作流
2. PyTorch 深度学习课程学习（26 章基础 + 进阶：UNet/YOLO/FaceNet + Transformer 论文精读）
3. 传统机器学习（西瓜书）理论与实践（SVM → 半监督学习，完整覆盖）
4. C 语言数据结构实现（稀疏矩阵、二叉树、哈夫曼树、图、哈希表、排序，含成都地铁最短路径项目）
5. GitHub 与开发环境使用、Git 基础操作
6. Linux 基础命令与服务器管理
7. 本地大模型运行与相关工具
8. 数学与课程基础笔记（离散数学、微积分、线性代数）
9. Transformer 架构与 Attention 机制
10. LLM 驱动的 DSP-HLS 自适应调优研究（前期调研阶段）
11. CET-6 写作与翻译备考复习（2023-2025真题、句式分类、话题语料、范文）
12. 大学物理电磁学期末复习（静电场、稳恒磁场、电磁波，含公式推导与易错习题）
13. 语言模仿残卷 - 聊天对话数据集（用于语言模型训练）
14. PBLF 爬虫项目 - Sanic + SQLite 全栈应用（含一键执行、SSE 实时事件流、SnowNLP 情感分析、词云图）

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
