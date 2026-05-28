# muyu_note

个人学习笔记仓库，使用 Obsidian 管理，内容以 AI、编程、深度学习和基础课程笔记为主。

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
  - GitHub 基础、学生认证、Token、Copilot 等内容
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
  - 线性模型
  - 梯度下降
  - 反向传播
  - Logistic Regression
  - Dataset 与 Dataloader
  - Softmax Classifier
  - CNN 与 Advanced CNN
- `程序与算法设计/`
  - 算法与课程相关内容
- `微积分/`
  - 微积分基础笔记
- `线性代数/`
  - 线性代数基础笔记

### 其他主题

- `服务器与VPS/`
  - 服务器和 VPS 相关资料
- `科学上网/`
  - 网络访问与相关原理记录
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
2. PyTorch 深度学习课程学习
3. GitHub 与开发环境使用
4. 本地大模型运行与相关工具
5. 数学与课程基础笔记

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
