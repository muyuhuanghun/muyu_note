# UNet 视网膜血管分割实战 (DRIVE 数据集)

- 论文：U-Net: Convolutional Networks for Biomedical Image Segmentation (2015)
- 数据集：DRIVE (Digital Retinal Images for Vessel Extraction)
- 结构特点：下采样抽语义 -> 上采样还空间 -> Skip Connection 补边缘

**相关笔记**: [[10.Basic CNN]] | [[11.引入RESNET的CNN网络]] | [[改进unet]] | [[unet-yolo-facenet study plan]] | [[02.Attention Is All You Need 论文学习报告]] | [[UNet 学习白板.canvas]]

---

# 一.依赖与环境

```
pip install torch torchvision pillow numpy matplotlib tqdm
```

---

# 二.UNet 网络架构

- 核心组件：DoubleConv 基础模块 + 对称编解码结构 + 动态尺寸填充

```
import torch
import torch.nn as nn
import torch.nn.functional as F

# ==========================================
# 基础模块：Double Conv（两层卷积 + BN + ReLU）
# ==========================================
class DoubleConv(nn.Module):
    """
    UNet 的最小积木块：Conv2d -> BN -> ReLU -> Conv2d -> BN -> ReLU
    每一级编/解码器都由这个模块构成，保持 3x3 卷积核不变
    """
    def __init__(self, in_channels, out_channels):
        super().__init__()
        self.double_conv = nn.Sequential(
            nn.Conv2d(in_channels, out_channels, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True),
            nn.Conv2d(out_channels, out_channels, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True),
        )

    def forward(self, x):
        return self.double_conv(x)


# ==========================================
# UNet 主体：对称编解码 + Skip Connection + 动态填充
# ==========================================
class UNet(nn.Module):
    """
    UNet 经典结构 (输入 3 通道 RGB，输出 1 通道二值分割)
    左半边 (Encoder): 逐级降采样，提取高层语义特征
    右半边 (Decoder): 逐级上采样，恢复空间分辨率
    Skip Connection: 将左侧特征图在通道维度拼接到右侧对应层级

    改进点：forward 中加入动态尺寸填充补丁
    当输入尺寸不是 16 的倍数时，ConvTranspose2d 上采样后尺寸可能与 Encoder 不匹配
    通过 F.pad 自动零填充对齐，避免 cat 时维度崩溃
    """
    def __init__(self, in_channels=3, out_channels=1, base_channels=64):
        super().__init__()
        # ========== Encoder（收缩路径 / 下采样）==========
        # 输入: [B, 3, H, W]
        self.enc1 = DoubleConv(in_channels, base_channels)        # -> [B, 64, H, W]
        self.pool1 = nn.MaxPool2d(2, 2)                            # -> [B, 64, H/2, W/2]

        self.enc2 = DoubleConv(base_channels, base_channels * 2)   # -> [B, 128, H/2, W/2]
        self.pool2 = nn.MaxPool2d(2, 2)                            # -> [B, 128, H/4, W/4]

        self.enc3 = DoubleConv(base_channels * 2, base_channels * 4)  # -> [B, 256, H/4, W/4]
        self.pool3 = nn.MaxPool2d(2, 2)                               # -> [B, 256, H/8, W/8]

        self.enc4 = DoubleConv(base_channels * 4, base_channels * 8)  # -> [B, 512, H/8, W/8]
        self.pool4 = nn.MaxPool2d(2, 2)                               # -> [B, 512, H/16, W/16]

        # ========== Bottleneck（U 型底部）==========
        self.bottleneck = DoubleConv(base_channels * 8, base_channels * 16)  # -> [B, 1024, H/16, W/16]

        # ========== Decoder（扩张路径 / 上采样）==========
        # 转置卷积 (ConvTranspose2d) 负责放大分辨率
        # 上采样后与 Encoder 对应层的特征图做 cat (dim=1 通道维拼接)
        self.upconv4 = nn.ConvTranspose2d(base_channels * 16, base_channels * 8, kernel_size=2, stride=2)
        self.dec4 = DoubleConv(base_channels * 16, base_channels * 8)        # cat 后通道翻倍

        self.upconv3 = nn.ConvTranspose2d(base_channels * 8, base_channels * 4, kernel_size=2, stride=2)
        self.dec3 = DoubleConv(base_channels * 8, base_channels * 4)

        self.upconv2 = nn.ConvTranspose2d(base_channels * 4, base_channels * 2, kernel_size=2, stride=2)
        self.dec2 = DoubleConv(base_channels * 4, base_channels * 2)

        self.upconv1 = nn.ConvTranspose2d(base_channels * 2, base_channels, kernel_size=2, stride=2)
        self.dec1 = DoubleConv(base_channels * 2, base_channels)

        # ========== 输出层 ==========
        self.out_conv = nn.Conv2d(base_channels, out_channels, kernel_size=1)

    def _pad_to_match(self, up_feat, enc_feat):
        """
        动态填充补丁：当上采样特征与 Encoder 特征尺寸不匹配时自动填充
        Args:
            up_feat:   上采样后的特征 [B, C, H', W']
            enc_feat:  Encoder 对应层特征 [B, C, H, W]
        Returns:
            填充后的特征 [B, C, H, W]
        """
        if up_feat.shape[2:] != enc_feat.shape[2:]:
            diff_h = enc_feat.shape[2] - up_feat.shape[2]
            diff_w = enc_feat.shape[3] - up_feat.shape[3]
            # F.pad 格式: (左, 右, 上, 下)，对称填充
            up_feat = F.pad(up_feat, [diff_w // 2, diff_w - diff_w // 2,
                                      diff_h // 2, diff_h - diff_h // 2])
        return up_feat

    def forward(self, x):
        # ======== Encoder ========
        enc1_out = self.enc1(x)         # [B, 64, H, W]
        x = self.pool1(enc1_out)        # [B, 64, H/2, W/2]

        enc2_out = self.enc2(x)         # [B, 128, H/2, W/2]
        x = self.pool2(enc2_out)        # [B, 128, H/4, W/4]

        enc3_out = self.enc3(x)         # [B, 256, H/4, W/4]
        x = self.pool3(enc3_out)        # [B, 256, H/8, W/8]

        enc4_out = self.enc4(x)         # [B, 512, H/8, W/8]
        x = self.pool4(enc4_out)        # [B, 512, H/16, W/16]

        # ======== Bottleneck ========
        x = self.bottleneck(x)          # [B, 1024, H/16, W/16]

        # ======== Decoder + Skip Connection（带动态填充）========
        # 关键操作 torch.cat：将 encoder 的"空间精确"特征与 decoder 的"语义丰富"特征在通道维度缝合
        # 改进：每次 cat 前检查尺寸，不匹配则自动填充
        x = self.upconv4(x)             # [B, 512, H/8, W/8]
        x = self._pad_to_match(x, enc4_out)  # 动态填充
        x = torch.cat([enc4_out, x], dim=1)  # [B, 1024, H/8, W/8]
        x = self.dec4(x)                # [B, 512, H/8, W/8]

        x = self.upconv3(x)             # [B, 256, H/4, W/4]
        x = self._pad_to_match(x, enc3_out)
        x = torch.cat([enc3_out, x], dim=1)  # [B, 512, H/4, W/4]
        x = self.dec3(x)                # [B, 256, H/4, W/4]

        x = self.upconv2(x)             # [B, 128, H/2, W/2]
        x = self._pad_to_match(x, enc2_out)
        x = torch.cat([enc2_out, x], dim=1)  # [B, 256, H/2, W/2]
        x = self.dec2(x)                # [B, 128, H/2, W/2]

        x = self.upconv1(x)             # [B, 64, H, W]
        x = self._pad_to_match(x, enc1_out)
        x = torch.cat([enc1_out, x], dim=1)  # [B, 128, H, W]
        x = self.dec1(x)                # [B, 64, H, W]

        x = self.out_conv(x)            # [B, 1, H, W]
        return x


# ==========================================
# 维度测试：打印每层输入输出形状（debug 必备）
# ==========================================
if __name__ == '__main__':
    model = UNet(in_channels=3, out_channels=1)
    # 测试非 16 倍数尺寸，验证动态填充是否生效
    dummy = torch.randn(1, 3, 257, 257)  # 奇数尺寸
    print(f"输入形状: {dummy.shape}\n")

    with torch.no_grad():
        output = model(dummy)
    print(f"输出形状: {output.shape}")
    print(f"参数量: {sum(p.numel() for p in model.parameters()) / 1e6:.2f}M")
```

---

# 三.DRIVE 数据集加载

- 改进点1：动态标签文件匹配（支持 1st_manual / 2nd_manual 等不同命名格式）
- 改进点2：训练时随机数据增强（水平翻转 + 垂直翻转，三者同步）

```
import os
import random
from PIL import Image
import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader
import torchvision.transforms.functional as TF
from torchvision import transforms

# ==========================================
# DRIVE 眼底血管数据集（改进版）
# ==========================================
class DRIVEDataset(Dataset):
    """
    加载 DRIVE 数据集，返回 (图像, 标签, 掩码)
    - 图像: .tif 格式，RGB 眼底彩照
    - 标签: .gif 格式，手动标注的血管二值图（0=背景 255=血管）
    - 掩码: .gif 格式，FOV 视野范围掩码（只在有效区域计算 Loss）
    """

    def __init__(self, root_dir, train=True, img_size=(256, 256)):
        """
        Args:
            root_dir: DRIVE 数据集根目录（包含 test/ 和 training/ 子文件夹）
            train: True 使用 training 集，False 使用 test 集
            img_size: 统一放缩到的尺寸
        """
        self.img_size = img_size
        self.train = train
        sub_dir = "training" if train else "test"

        self.img_dir = os.path.join(root_dir, sub_dir, "images")
        # 改进：测试集优先用 2nd_manual，找不到再 fallback 到 1st_manual
        self.label_dir = os.path.join(root_dir, sub_dir, "1st_manual" if train else "2nd_manual")
        if not os.path.exists(self.label_dir):
            self.label_dir = os.path.join(root_dir, sub_dir, "1st_manual")

        self.mask_dir = os.path.join(root_dir, sub_dir, "mask")

        # DRIVE 文件命名规律：
        #   training: 21_training.tif / 21_manual1.gif / 21_training_mask.gif
        #   test:     01_test.tif     / 01_manual1.gif / 01_test_mask.gif
        #   因此只提取数字前缀（如 "21" 或 "01"），再拼接各类型的后缀
        self.samples = []  # 每个元素: {"num": "21", "sub": "training"}
        for f in sorted(os.listdir(self.img_dir)):
            if f.endswith(".tif"):
                basename = f.replace(".tif", "")
                parts = basename.split("_")
                self.samples.append({"num": parts[0], "sub": parts[1]})

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        s = self.samples[idx]

        # 加载图像
        img = Image.open(os.path.join(self.img_dir, f"{s['num']}_{s['sub']}.tif")).convert("RGB")
        mask = Image.open(os.path.join(self.mask_dir, f"{s['num']}_{s['sub']}_mask.gif")).convert("L")

        # 改进：动态查找标签文件（支持不同命名格式）
        all_labels = os.listdir(self.label_dir)
        label_fname = [f for f in all_labels if f.startswith(s['num']) and f.endswith('.gif')][0]
        label = Image.open(os.path.join(self.label_dir, label_fname)).convert("L")

        # 统一尺寸
        img = TF.resize(img, self.img_size, Image.BILINEAR)
        label = TF.resize(label, self.img_size, Image.NEAREST)  # 标签必须用 NEAREST，避免插值产生中间灰度
        mask = TF.resize(mask, self.img_size, Image.NEAREST)

        # 改进：训练时随机数据增强（同时翻转三者保持一致性）
        if self.train:
            if random.random() > 0.5:
                img = TF.hflip(img)
                label = TF.hflip(label)
                mask = TF.hflip(mask)
            if random.random() > 0.5:
                img = TF.vflip(img)
                label = TF.vflip(label)
                mask = TF.vflip(mask)

        # 转 Tensor
        img_tensor = TF.to_tensor(img)  # [3, H, W], float [0, 1]

        # GIF 是调色板模式(P)，必须先 convert('L') 转灰度再取数组
        label_np = (np.array(label, dtype=np.float32) > 127).astype(np.float32)
        label_tensor = torch.from_numpy(label_np).unsqueeze(0).float()  # [1, H, W]

        mask_np = (np.array(mask, dtype=np.float32) > 127).astype(np.float32)
        mask_tensor = torch.from_numpy(mask_np).unsqueeze(0).float()   # [1, H, W]

        # Mask 盖在 label 上，无效区域血管置 0
        label_tensor = label_tensor * mask_tensor

        return {"image": img_tensor, "label": label_tensor, "mask": mask_tensor}


# ==========================================
# 快速测试：加载一张图看看维度
# ==========================================
if __name__ == '__main__':
    # 改进：动态获取脚本所在目录，不再硬编码绝对路径
    data_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "DRIVE")
    train_set = DRIVEDataset(data_root, train=True, img_size=(256, 256))
    test_set = DRIVEDataset(data_root, train=False, img_size=(256, 256))

    print(f"训练集样本数: {len(train_set)}")
    print(f"测试集样本数: {len(test_set)}")

    sample = train_set[0]
    print(f"\n图像维度:     {sample['image'].shape}  (C, H, W)")
    print(f"标签维度:     {sample['label'].shape}  (1, H, W)")
    print(f"掩码维度:     {sample['mask'].shape}  (1, H, W)")
    print(f"血管像素占比: {sample['label'].mean().item():.2%}")
    print(f"FOV 范围占比: {sample['mask'].mean().item():.2%}")
```

---

# 四.SafeDiceLoss

- 分割任务的灵魂损失函数
- 为什么不用纯交叉熵：DRIVE 中血管像素只占约 10%，背景占 90%，模型偷懒全预测成背景也能拿 90% 低 Loss
- Dice Loss 直接在"重叠度"层面监督，不受类别不均衡影响
- 改进点：smooth 参数从 1e-6 调大到 1.0，提供更强的数值稳定性

```
import torch.nn as nn

# ==========================================
# SafeDiceLoss：计算预测与真实标签的重叠度（数值稳定版）
# ==========================================
class SafeDiceLoss(nn.Module):
    """
    Dice = 2 * |X ∩ Y| / (|X| + |Y|)
    用于衡量两个二值图像的重叠程度，Dice=1 表示完全重合
    Loss = 1 - Dice，越小越好
    """

    def __init__(self, smooth=1.0):
        super().__init__()
        self.smooth = smooth  # 改进：smooth=1.0 比 1e-6 更稳定

    def forward(self, pred, target):
        """
        Args:
            pred:   [B, 1, H, W] 模型预测，经过 sigmoid 后属于 [0, 1]
            target: [B, 1, H, W] 真实标签，属于 {0, 1}
        """
        pred = pred.view(-1)
        target = target.view(-1)

        intersection = (pred * target).sum()          # |X ∩ Y|
        union = pred.sum() + target.sum()              # |X| + |Y|

        dice = (2. * intersection + self.smooth) / (union + self.smooth)
        return 1 - dice


# ==========================================
# Dice 逻辑验证
# ==========================================
if __name__ == '__main__':
    dice_loss = SafeDiceLoss(smooth=1.0)
    # 完美预测 -> loss 近似 0
    a = torch.ones(1, 1, 10, 10)
    print(f"完美预测 Dice Loss: {dice_loss(torch.sigmoid(a), a):.6f}")

    # 完全错误 -> loss 近似 1
    b = torch.ones(1, 1, 10, 10)
    c = torch.zeros(1, 1, 10, 10)
    print(f"完全错误 Dice Loss: {dice_loss(torch.sigmoid(b), c):.6f}")
```

---

# 五.完整训练脚本

- 超参数配置：
  - IMG_SIZE = (256, 256)
  - BATCH_SIZE = 4（DRIVE 训练集只有 20 张，batch 不宜太大）
  - NUM_EPOCHS = 60
  - LR = 2e-4（从 1e-4 提高，加速收敛）
  - WEIGHT_DECAY = 1e-5（从 1e-8 提高，更强正则化）
- 损失函数：BCE_WEIGHT * BCEWithLogitsLoss + DICE_WEIGHT * SafeDiceLoss（各 0.5 权重）
- 优化器：Adam + StepLR（每 20 轮衰减 0.5）

```
import os
import time
import random
import numpy as np
from PIL import Image
from tqdm import tqdm

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader, random_split
import torchvision.transforms.functional as TF
from torchvision import transforms

# ==========================================
# 0. 设备检测与加速
# ==========================================
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"当前核心设备：【{device}】")
if torch.cuda.is_available():
    torch.backends.cudnn.benchmark = True  # cuDNN 自动寻找最优卷积算法

# ==========================================
# 1. 超参数精调配置
# ==========================================
IMG_SIZE = (256, 256)
BATCH_SIZE = 4
NUM_EPOCHS = 60
LR = 2e-4                    # 改进：从 1e-4 提高到 2e-4，加速收敛
WEIGHT_DECAY = 1e-5          # 改进：从 1e-8 提高到 1e-5，更强正则化
DICE_WEIGHT = 0.5
BCE_WEIGHT = 0.5
VAL_SPLIT = 0.2

# 改进：动态获取脚本所在目录，不再硬编码绝对路径
DATA_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "DRIVE")
SAVE_DIR = os.path.join(os.path.dirname(DATA_ROOT), "checkpoints")
os.makedirs(SAVE_DIR, exist_ok=True)

# ==========================================
# 2. 数据集加载（带数据增强）
# ==========================================
class DRIVEDataset(Dataset):
    """DRIVE 眼底血管数据集（改进版，支持动态标签匹配 + 数据增强）"""
    def __init__(self, root_dir, train=True, img_size=(256, 256)):
        self.img_size = img_size
        self.train = train
        sub_dir = "training" if train else "test"

        self.img_dir = os.path.join(root_dir, sub_dir, "images")
        self.label_dir = os.path.join(root_dir, sub_dir, "1st_manual" if train else "2nd_manual")
        if not os.path.exists(self.label_dir):
            self.label_dir = os.path.join(root_dir, sub_dir, "1st_manual")
        self.mask_dir = os.path.join(root_dir, sub_dir, "mask")

        self.samples = []
        for f in sorted(os.listdir(self.img_dir)):
            if f.endswith(".tif"):
                basename = f.replace(".tif", "")
                parts = basename.split("_")
                self.samples.append({"num": parts[0], "sub": parts[1]})

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        s = self.samples[idx]

        img = Image.open(os.path.join(self.img_dir, f"{s['num']}_{s['sub']}.tif")).convert("RGB")
        mask = Image.open(os.path.join(self.mask_dir, f"{s['num']}_{s['sub']}_mask.gif")).convert("L")

        # 动态查找标签文件
        all_labels = os.listdir(self.label_dir)
        label_fname = [f for f in all_labels if f.startswith(s['num']) and f.endswith('.gif')][0]
        label = Image.open(os.path.join(self.label_dir, label_fname)).convert("L")

        img = TF.resize(img, self.img_size, Image.BILINEAR)
        label = TF.resize(label, self.img_size, Image.NEAREST)
        mask = TF.resize(mask, self.img_size, Image.NEAREST)

        # 训练时随机翻转增强
        if self.train:
            if random.random() > 0.5:
                img = TF.hflip(img)
                label = TF.hflip(label)
                mask = TF.hflip(mask)
            if random.random() > 0.5:
                img = TF.vflip(img)
                label = TF.vflip(label)
                mask = TF.vflip(mask)

        img_tensor = TF.to_tensor(img)
        label_np = (np.array(label, dtype=np.float32) > 127).astype(np.float32)
        label_tensor = torch.from_numpy(label_np).unsqueeze(0).float()
        mask_np = (np.array(mask, dtype=np.float32) > 127).astype(np.float32)
        mask_tensor = torch.from_numpy(mask_np).unsqueeze(0).float()
        label_tensor = label_tensor * mask_tensor

        return {"image": img_tensor, "label": label_tensor, "mask": mask_tensor}


# 加载完整 training 集并划分 train/val
full_train_set = DRIVEDataset(DATA_ROOT, train=True, img_size=IMG_SIZE)
n_val = int(len(full_train_set) * VAL_SPLIT)   # 20 * 0.2 = 4
n_train = len(full_train_set) - n_val          # 16
train_set, val_set = random_split(full_train_set, [n_train, n_val],
                                   generator=torch.Generator().manual_seed(42))

train_loader = DataLoader(train_set, batch_size=BATCH_SIZE, shuffle=True, num_workers=0, pin_memory=True)
val_loader = DataLoader(val_set, batch_size=1, shuffle=False, num_workers=0, pin_memory=True)

print(f"训练集: {n_train} 张 | 验证集: {n_val} 张\n")

# ==========================================
# 3. 模型、损失、优化器
# ==========================================
class DoubleConv(nn.Module):
    def __init__(self, in_c, out_c):
        super().__init__()
        self.double_conv = nn.Sequential(
            nn.Conv2d(in_c, out_c, 3, padding=1, bias=False),
            nn.BatchNorm2d(out_c),
            nn.ReLU(inplace=True),
            nn.Conv2d(out_c, out_c, 3, padding=1, bias=False),
            nn.BatchNorm2d(out_c),
            nn.ReLU(inplace=True),
        )
    def forward(self, x):
        return self.double_conv(x)

class UNet(nn.Module):
    def __init__(self, in_c=3, out_c=1, base=64):
        super().__init__()
        # Encoder
        self.enc1 = DoubleConv(in_c, base)
        self.enc2 = DoubleConv(base, base * 2)
        self.enc3 = DoubleConv(base * 2, base * 4)
        self.enc4 = DoubleConv(base * 4, base * 8)
        self.pool = nn.MaxPool2d(2, 2)
        # Bottleneck
        self.bottleneck = DoubleConv(base * 8, base * 16)
        # Decoder
        self.up4 = nn.ConvTranspose2d(base * 16, base * 8, 2, 2)
        self.dec4 = DoubleConv(base * 16, base * 8)
        self.up3 = nn.ConvTranspose2d(base * 8, base * 4, 2, 2)
        self.dec3 = DoubleConv(base * 8, base * 4)
        self.up2 = nn.ConvTranspose2d(base * 4, base * 2, 2, 2)
        self.dec2 = DoubleConv(base * 4, base * 2)
        self.up1 = nn.ConvTranspose2d(base * 2, base, 2, 2)
        self.dec1 = DoubleConv(base * 2, base)
        self.out_conv = nn.Conv2d(base, out_c, 1)

    def forward(self, x):
        # Encoder
        e1 = self.enc1(x)
        e2 = self.enc2(self.pool(e1))
        e3 = self.enc3(self.pool(e2))
        e4 = self.enc4(self.pool(e3))
        # Bottleneck
        b = self.bottleneck(self.pool(e4))

        # Decoder（带动态尺寸填充补丁）
        up_4 = self.up4(b)
        if up_4.shape[2:] != e4.shape[2:]:
            diff_h = e4.shape[2] - up_4.shape[2]
            diff_w = e4.shape[3] - up_4.shape[3]
            up_4 = F.pad(up_4, [diff_w // 2, diff_w - diff_w // 2,
                                diff_h // 2, diff_h - diff_h // 2])
        d4 = self.dec4(torch.cat([e4, up_4], dim=1))

        up_3 = self.up3(d4)
        if up_3.shape[2:] != e3.shape[2:]:
            diff_h = e3.shape[2] - up_3.shape[2]
            diff_w = e3.shape[3] - up_3.shape[3]
            up_3 = F.pad(up_3, [diff_w // 2, diff_w - diff_w // 2,
                                diff_h // 2, diff_h - diff_h // 2])
        d3 = self.dec3(torch.cat([e3, up_3], dim=1))

        up_2 = self.up2(d3)
        if up_2.shape[2:] != e2.shape[2:]:
            diff_h = e2.shape[2] - up_2.shape[2]
            diff_w = e2.shape[3] - up_2.shape[3]
            up_2 = F.pad(up_2, [diff_w // 2, diff_w - diff_w // 2,
                                diff_h // 2, diff_h - diff_h // 2])
        d2 = self.dec2(torch.cat([e2, up_2], dim=1))

        up_1 = self.up1(d2)
        if up_1.shape[2:] != e1.shape[2:]:
            diff_h = e1.shape[2] - up_1.shape[2]
            diff_w = e1.shape[3] - up_1.shape[3]
            up_1 = F.pad(up_1, [diff_w // 2, diff_w - diff_w // 2,
                                diff_h // 2, diff_h - diff_h // 2])
        d1 = self.dec1(torch.cat([e1, up_1], dim=1))

        return self.out_conv(d1)


class SafeDiceLoss(nn.Module):
    """改进：smooth=1.0 提供更强数值稳定性"""
    def __init__(self, smooth=1.0):
        super().__init__()
        self.smooth = smooth
    def forward(self, pred, target):
        pred = pred.view(-1)
        target = target.view(-1)
        intersection = (pred * target).sum()
        dice = (2. * intersection + self.smooth) / (pred.sum() + target.sum() + self.smooth)
        return 1 - dice


def calc_dice(pred_logits, true_mask, threshold=0.5):
    """从 logits 计算 Dice 系数"""
    pred = torch.sigmoid(pred_logits)
    pred_bin = (pred > threshold).float().view(-1)
    true_mask = true_mask.view(-1)
    intersection = (pred_bin * true_mask).sum()
    return (2. * intersection + 1e-6) / (pred_bin.sum() + true_mask.sum() + 1e-6)


model = UNet(in_c=3, out_c=1, base=64).to(device)
print(f"模型参数量: {sum(p.numel() for p in model.parameters()) / 1e6:.2f}M\n")

criterion_bce = nn.BCEWithLogitsLoss()   # 自带 Sigmoid + BCE，比手动写更稳
criterion_dice = SafeDiceLoss(smooth=1.0)
optimizer = optim.Adam(model.parameters(), lr=LR, weight_decay=WEIGHT_DECAY)

# 学习率调度：每 20 轮衰减为原来的 0.5
scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=20, gamma=0.5)

# ==========================================
# 4. 训练 & 验证
# ==========================================
best_val_dice = 0.0
best_weight_file = os.path.join(SAVE_DIR, "unet_drive_best.pth")

for epoch in range(1, NUM_EPOCHS + 1):
    # ========== Train ==========
    model.train()
    epoch_loss = 0.0
    train_bar = tqdm(train_loader, desc=f"Epoch {epoch:2d}/{NUM_EPOCHS} [Train]")
    for batch in train_bar:
        imgs = batch["image"].to(device)
        labels = batch["label"].to(device)

        optimizer.zero_grad()
        logits = model(imgs)
        # 组合损失: BCE(像素级对齐) + Dice(区域级重叠)
        loss_bce = criterion_bce(logits, labels)
        loss_dice = criterion_dice(torch.sigmoid(logits), labels)
        loss = BCE_WEIGHT * loss_bce + DICE_WEIGHT * loss_dice

        loss.backward()
        optimizer.step()

        epoch_loss += loss.item()
        train_bar.set_postfix(loss=f"{loss.item():.4f}")

    avg_loss = epoch_loss / len(train_loader)
    scheduler.step()

    # ========== Validate ==========
    model.eval()
    val_dice_sum = 0.0
    with torch.no_grad():
        for batch in val_loader:
            imgs = batch["image"].to(device)
            labels = batch["label"].to(device)
            val_dice_sum += calc_dice(model(imgs), labels).item()

    avg_val_dice = val_dice_sum / len(val_loader)

    print(f"  Epoch {epoch:2d} | Train Loss: {avg_loss:.4f} | "
          f"Val Dice: {avg_val_dice:.4f} | LR: {scheduler.get_last_lr()[0]:.2e}")

    # 保存最佳模型
    if avg_val_dice > best_val_dice:
        best_val_dice = avg_val_dice
        torch.save(model.state_dict(), best_weight_file)
        print(f"  保存最佳模型 (Dice={best_val_dice:.4f})")

print(f"\n训练完成！最佳验证 Dice: {best_val_dice:.4f}")
```

---

# 六.独立推理函数

- 改进点：
  - 重新初始化干净的 eval 模型加载最佳权重（避免训练状态污染）
  - 加入 Normalize 预处理（mean/std 对齐 Wz 老师的推理脚本）
  - 推理时用 ROI 掩码扣除眼球外部杂质
  - 硬件同步计时，准确测量前向传播耗时

```
import time
import numpy as np
from PIL import Image
import torch
import torch.nn as nn
from torchvision import transforms

# ==========================================
# 硬件同步计时工具
# ==========================================
def time_synchronized():
    """
    CUDA 同步计时
    GPU 操作是异步的，不同步的话 time.time() 拿到的是 kernel 提交时间，不是执行完成时间
    """
    if torch.cuda.is_available():
        torch.cuda.synchronize()
    return time.time()


# ==========================================
# 独立推理函数（改进版）
# ==========================================
def run_inference_and_save(best_model_path, data_root, save_dir):
    """
    改进点：
    1. 重新初始化干净的 eval 模型加载最佳权重
    2. 加入 Normalize 预处理（mean/std 对齐 Wz 老师的推理脚本）
    3. 推理时用 ROI 掩码扣除眼球外部杂质
    4. 硬件同步计时，准确测量前向传播耗时
    """
    print("\n" + "=" * 50)
    print("推理测试评估")
    print("=" * 50)

    # 1. 预处理参数（对齐 Wz 老师的推理脚本）
    img_path = os.path.join(data_root, "test", "images", "01_test.tif")
    roi_mask_path = os.path.join(data_root, "test", "mask", "01_test_mask.gif")
    mean = (0.709, 0.381, 0.224)  # DRIVE 数据集的统计均值
    std = (0.127, 0.079, 0.043)   # DRIVE 数据集的统计标准差

    # 2. 重新初始化干净模型并载入最佳权重
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    eval_model = UNet(in_c=3, out_c=1, base=64).to(device)
    eval_model.load_state_dict(torch.load(best_model_path, map_location=device))
    eval_model.eval()

    # 3. 加载图像与 ROI 掩码
    roi_img = np.array(Image.open(roi_mask_path).convert('L'))
    original_img = Image.open(img_path).convert('RGB')

    # 改进：加入 Normalize 预处理
    data_transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(mean=mean, std=std)
    ])
    img = data_transform(original_img).unsqueeze(0).to(device)

    # 4. 硬件同步计时推理
    with torch.no_grad():
        # 预热（第一次推理会触发 CUDA kernel 编译，不算在计时内）
        _ = eval_model(torch.zeros_like(img))

        t_start = time_synchronized()
        output = eval_model(img)
        t_end = time_synchronized()
        print(f"  前向传播耗时: {t_end - t_start:.4f} 秒")

        # 5. Sigmoid + 二值化 + ROI 掩码过滤
        pred = torch.sigmoid(output).squeeze(0).squeeze(0).cpu().numpy()

        prediction = np.zeros_like(pred, dtype=np.uint8)
        prediction[pred > 0.5] = 255       # 提取血管
        prediction[roi_img == 0] = 0        # 强行扣除眼球外部杂质

        # 6. 保存结果
        result_path = os.path.join(save_dir, "test_result.png")
        result_mask = Image.fromarray(prediction)
        result_mask.save(result_path)
        print(f"  预测图已保存至: {result_path}")


# ==========================================
# 主运行流水线
# ==========================================
if __name__ == '__main__':
    # ... 训练代码同上 ...

    # 训练完成后执行推理
    run_inference_and_save(best_weight_file, DATA_ROOT, SAVE_DIR)
```

---

# 七.学习要点总结

| 模块 | 核心考点 |
|------|---------|
| **Encoder** | 4 次 Conv2d + MaxPool2d 逐级提取高层语义，通道翻倍(64->128->256->512) |
| **Decoder** | ConvTranspose2d 上采样，通道折半，逐步恢复空间分辨率 |
| **Skip Connection** | torch.cat([encoder_feat, decoder_feat], dim=1) 在通道维缝合，挽救下采样丢失的边缘细节 |
| **Dynamic Padding** | 上采样后自动检测尺寸，F.pad 零填充对齐，兼容任意输入分辨率 |
| **SafeDiceLoss** | smooth=1.0 提供更强数值稳定性，解决血管占比过低导致的类别不均衡 |
| **Data Augmentation** | 训练时随机水平/垂直翻转，三者(image/label/mask)同步翻转保持一致性 |
| **FOV Mask** | 只在眼底视野范围内算 Loss 和 Dice，避免模型被黑背景误导 |
| **Inference Pipeline** | 独立 eval 模型 + Normalize 预处理 + ROI 掩码后处理 + CUDA 同步计时 |

---

# 八.改进版 vs 经典版对比

| 维度 | 经典版 | 改进版 |
|------|--------|--------|
| 数据增强 | 无 | 随机水平/垂直翻转 |
| 尺寸兼容 | 假设被 16 整除 | 动态 F.pad 补丁 |
| 标签匹配 | 硬编码文件名 | 动态列表查找 |
| Dice smooth | 1e-6 | 1.0 (更稳定) |
| 学习率 | 1e-4 | 2e-4 (更快收敛) |
| 推理 | 简单可视化 | 独立推理+计时+Normalize+ROI掩码 |
| 路径处理 | 硬编码绝对路径 | __file__ 动态获取 |
