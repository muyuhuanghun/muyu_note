# 🗺️ 深度学习实战进阶大通关：UNet、YOLO 与 FaceNet 自研路线图

**相关笔记**: [[UNet 训练代码]] | [[改进unet]] | [[10.Basic CNN]] | [[11.引入RESNET的CNN网络]] | [[02.Attention Is All You Need 论文学习报告]] | [[UNet 学习白板]]

## 🏷️ 文档元数据
* **当前状态**：进行中 (In Progress)
* **安全策略**：`.gitignore` 严格阻断 Key 泄露风险；AI 注入“推送前风险审查”及“强制 PR”底层记忆

---

## 🏗️ 承前启后：为什么在这个节点选择这三个算法？
包含：反向传播、Softmax 分类器、Basic/Advanced CNN、ResNet 残差、双向 GRU 变长序列打包及 Adam 优化器

不盲目在旧技术里做边际效应递减的拓展，而是通过 **UNet (图像分割)**、**YOLOv1 (目标检测)**、**FaceNet (度量学习)** 三大下游任务神作，彻底打通“将基础零件（卷积、残差、池化）组装成工业级高达”的算法审美，并为后续跨越到 **Transformer 体系 (Attention, ViT)** 奠定最坚实的实战内功。

---

## 🟢 第一阶段：UNet 与医疗影像分割 (像素级抠图)
* **核心思想**：完美的对称美学。利用下采样（Encoder）提取高维语义特征，利用上采样（Decoder）还原空间分辨率，并通过**跨层级特征拼接（Skip Connection）**挽救丢失的边缘细节。



### 🛠️ 个人手搓实战步骤
1. **网络拓扑构建**：
   * 使用 `torch.nn.Conv2d` 和 `torch.nn.MaxPool2d` 构建左半边的收缩路径。
   * 学习并使用 `torch.nn.ConvTranspose2d`（转置卷积）构建右半边的扩张路径。
   * **核心攻坚**：在前向传播 `forward` 中，利用 `torch.cat(..., dim=1)` 将左侧未缩小的特征图与右侧放大上来的特征图在**通道维度**强行拼接。
2. **损失函数升级**：
   * 放弃常规的交叉熵，手写一个 `Dice Loss`（专门用于计算预测轮廓与真实轮廓重合度的函数），解决医疗影像中背景大、病灶小的类别不均衡问题。

### 📚 顶级学习资源
* **📺 最佳源码视频**：B 站搜索 **[霹雳吧啦Wz] 的 UNet 源码解析与实战**。全网公认最干净的纯手写 PyTorch 视觉教程，无任何冗余工程封装。
* **📄 经典原始论文**：《U-Net: Convolutional Networks for Biomedical Image Segmentation》(2015)
* **🔗 GitHub 优质参考**：[milesial/Pytorch-UNet](https://github.com/milesial/Pytorch-UNet) —— 结构极度清晰，适合在手写时用来对齐矩阵维度。

---

## 🟡 第二阶段：YOLOv1 与目标检测 (高维张量的回归暴政)
* **核心思想**：You Only Look Once。彻底放弃传统多阶段画候选框的繁琐逻辑，直接将整张图划分为 $S \times S$ 的网格，用全卷积网络直接回归出一个包含“位置 + 置信度 + 类别”的超高维矩阵张量。



### 🛠️ 个人手搓实战步骤
1. **骨干网络剥离**：
   * 不要去啃最新 YOLOv8/v10 几万行的工程化源码。
   * 直接死磕初代 **YOLOv1**。骨干网络可以直接借用 `torchvision.models.resnet50` 提取特征，在末端接上自己的全连接层，强行输出一个形状为 `[Batch, 7, 7, 30]` 的大张量。
2. **张量通道解包**：
   * 搞懂输出的 `30` 个通道的数学含义：前 10 个代表 2 个预测边界框的 $(x, y, w, h, confidence)$，后 20 个通道代表 20 个类别的条件概率。
3. **多任务损失函数手写**：
   * YOLO 的精髓全在 Loss。对照公式手写一个包含：位置中心点误差、宽高根号误差、负责物体置信度误差、不负责物体置信度误差以及分类误差的巨型复合型损失函数。

### 📚 顶级学习资源
* **📺 最佳源码视频 (硬核首选)**：YouTube 搜索 **[Aladdin Persson] YOLOv1 PyTorch from scratch**。全程面对空白文件一行行敲出网络架构和那段复杂的 YOLO Loss，极其适合极客式学习。
* **📺 理论通俗讲解**：B 站搜索 **[吴恩达深度学习] 目标检测章节**（第四门课第三周）。讲透网格划分、交并比 (IoU) 和非极大值抑制 (NMS) 的底层逻辑。
* **📄 经典原始论文**：《You Only Look Once: Unified, Real-Time Object Detection》(2015)

---

## 🔴 第三阶段：FaceNet 与度量学习 (万物皆可 Embedding)
* **核心思想**：打破常规分类器的思维禁锢。不再让网络输出某一类别的概率（因为无法应对全世界几十亿张人脸），而是利用网络将人脸图片压缩成一个 128 维的空间几何坐标（Embedding），通过拉近同类、拉远异类来做连连看。



### 🛠️ 个人手搓实战步骤
1. **特征截断与归一化**：
   * 采用任意标准 CNN（如 Inception）作为基础，砍掉最后的 Softmax 分类头，强行接一个 `Linear(..., 128)` 映射层。
   * 紧跟一步 `torch.nn.functional.normalize(..., p=2, dim=1)` 做 L2 归一化，将所有特征锁定在单位球面上。
2. **核心三元组损失 (Triplet Loss) 手写**：
   * 构建数据流水线，一次读入三张图：原告（Anchor）、正例（Positive）、反例（Negative）。
   * 手写损失公式：$L = \max(d(A, P) - d(A, N) + \alpha, 0)$，通过反向传播拼向外踢开不同人脸的坐标。

### 📚 顶级学习资源
* **📺 理论通俗讲解**：B 站搜索 **[吴恩达深度学习] 人脸识别章节**（第四门课第四周）。吴恩达教授对三元组挑选（聚类、难样本挖掘）的直观解释极其透彻。
* **📄 经典原始论文**：《FaceNet: A Unified Embedding for Face Recognition and Clustering》(2015)
* **🔗 GitHub 优质参考**：[timesler/facenet-pytorch](https://github.com/timesler/facenet-pytorch) —— 重点参考其模型定义部分，学习人脸对齐和编码的技巧。

---

## 🛠️ 下一步开发指令 (Claude Code 联动专用)
当准备好对某一章节发起进攻时，可直接在终端对 `Claude Code` 下达指令：
> *"Claude, 参照本地知识库的 `.md` 规划，首先在当前目录下创建 `models/unet.py`。请基于 PyTorch 纯手写一个标准的 UNet 结构，要求包含 ConvTranspose2d 以及 forward 中的特征图 Concat 拼接，不要引入任何第三方工程库，写完后打印出每层矩阵维度的变化过程。"*