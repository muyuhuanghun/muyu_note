**相关笔记**: [[UNet 训练代码]] | [[10.Basic CNN]] | [[unet-yolo-facenet study plan]] | [[UNet 学习白板.canvas]]

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
# 0.设备检测与加速
# ==========================================
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"当前核心设备：【{device}】")  
if torch.cuda.is_available():  
    torch.backends.cudnn.benchmark = True  
  
# ==========================================  
# 1. 超参数精调配置  
# ==========================================  
IMG_SIZE = (256, 256)  
BATCH_SIZE = 4  
NUM_EPOCHS = 60  
LR = 2e-4  
WEIGHT_DECAY = 1e-5  
DICE_WEIGHT = 0.5  
BCE_WEIGHT = 0.5  
VAL_SPLIT = 0.2  
  
# 根据你的系统路径自行对齐  
DATA_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "DRIVE")  
SAVE_DIR = os.path.join(os.path.dirname(DATA_ROOT), "checkpoints")  
os.makedirs(SAVE_DIR, exist_ok=True)  
  
  
# ==========================================  
# 2. 动态文件名捕获的数据集  
# ==========================================  
class DRIVEDataset(Dataset):  
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
  
        all_labels = os.listdir(self.label_dir)  
        label_fname = [f for f in all_labels if f.startswith(s['num']) and f.endswith('.gif')][0]  
        label = Image.open(os.path.join(self.label_dir, label_fname)).convert("L")  
  
        img = TF.resize(img, self.img_size, Image.BILINEAR)  
        label = TF.resize(label, self.img_size, Image.NEAREST)  
        mask = TF.resize(mask, self.img_size, Image.NEAREST)  
  
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
  
  
# ==========================================  
# 3. 模型与损失函数定义  
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
        self.enc1 = DoubleConv(in_c, base)  
        self.enc2 = DoubleConv(base, base * 2)  
        self.enc3 = DoubleConv(base * 2, base * 4)  
        self.enc4 = DoubleConv(base * 4, base * 8)  
        self.pool = nn.MaxPool2d(2, 2)  
  
        self.bottleneck = DoubleConv(base * 8, base * 16)  
  
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
        # 1. Encoder 路径  
        e1 = self.enc1(x)  
        e2 = self.enc2(self.pool(e1))  
        e3 = self.enc3(self.pool(e2))  
        e4 = self.enc4(self.pool(e3))  
  
        # 2. Bottleneck  
        b = self.bottleneck(self.pool(e4))  
  
        # 3. Decoder 路径（带动态尺寸填充补丁，防止奇数分辨率崩溃）  
        up_4 = self.up4(b)  
        if up_4.shape[2:] != e4.shape[2:]:  
            # 如果尺寸对不上，自动用 0 填充到和 e4 一样大  
            import torch.nn.functional as F  
            diff_h = e4.shape[2] - up_4.shape[2]  
            diff_w = e4.shape[3] - up_4.shape[3]  
            up_4 = F.pad(up_4, [diff_w // 2, diff_w - diff_w // 2,  
                                diff_h // 2, diff_h - diff_h // 2])  
        d4 = self.dec4(torch.cat([e4, up_4], dim=1))  
  
        up_3 = self.up3(d4)  
        if up_3.shape[2:] != e3.shape[2:]:  
            import torch.nn.functional as F  
            diff_h = e3.shape[2] - up_3.shape[2]  
            diff_w = e3.shape[3] - up_3.shape[3]  
            up_3 = F.pad(up_3, [diff_w // 2, diff_w - diff_w // 2,  
                                diff_h // 2, diff_h - diff_h // 2])  
        d3 = self.dec3(torch.cat([e3, up_3], dim=1))  
  
        up_2 = self.up2(d3)  
        if up_2.shape[2:] != e2.shape[2:]:  
            import torch.nn.functional as F  
            diff_h = e2.shape[2] - up_2.shape[2]  
            diff_w = e2.shape[3] - up_2.shape[3]  
            up_2 = F.pad(up_2, [diff_w // 2, diff_w - diff_w // 2,  
                                diff_h // 2, diff_h - diff_h // 2])  
        d2 = self.dec2(torch.cat([e2, up_2], dim=1))  
  
        up_1 = self.up1(d2)  
        if up_1.shape[2:] != e1.shape[2:]:  
            import torch.nn.functional as F  
            diff_h = e1.shape[2] - up_1.shape[2]  
            diff_w = e1.shape[3] - up_1.shape[3]  
            up_1 = F.pad(up_1, [diff_w // 2, diff_w - diff_w // 2,  
                                diff_h // 2, diff_h - diff_h // 2])  
        d1 = self.dec1(torch.cat([e1, up_1], dim=1))  
  
        return self.out_conv(d1)  
  
  
class SafeDiceLoss(nn.Module):  
    def __init__(self, smooth=1.0):  
        super().__init__()  
        self.smooth = smooth  
  
    def forward(self, pred, target):  
        pred = pred.view(-1)  
        target = target.view(-1)  
        intersection = (pred * target).sum()  
        dice = (2. * intersection + self.smooth) / (pred.sum() + target.sum() + self.smooth)  
        return 1.0 - dice  
  
  
def calc_dice(pred_logits, true_mask, threshold=0.5):  
    pred = torch.sigmoid(pred_logits)  
    pred_bin = (pred > threshold).float().view(-1)  
    true_mask = true_mask.view(-1)  
    intersection = (pred_bin * true_mask).sum()  
    return (2. * intersection + 1e-6) / (pred_bin.sum() + true_mask.sum() + 1e-6)  
  
  
# ==========================================  
# 4. 单张图像全兼容推理函数  
# ==========================================  
def time_synchronized():  
    torch.cuda.synchronize() if torch.cuda.is_available() else None  
    return time.time()  
  
  
def run_inference_and_save(best_model_path):  
    print("\n" + "=" * 50)  
    print("推理测试评估")  
    print("=" * 50)  
  
    # 1. 强行对齐 Wz 老师的推理脚本预处理参数  
    img_path = os.path.join(DATA_ROOT, "test", "images", "01_test.tif")  
    roi_mask_path = os.path.join(DATA_ROOT, "test", "mask", "01_test_mask.gif")  
    mean = (0.709, 0.381, 0.224)  
    std = (0.127, 0.079, 0.043)  
  
    # 2. 重新初始化一个干净的 eval 模型并载入刚刚训练的最佳权重  
    eval_model = UNet(in_c=3, out_c=1, base=64).to(device)  
    eval_model.load_state_dict(torch.load(best_model_path, map_location=device))  
    eval_model.eval()  
  
    # 3. 加载图像与掩码  
    roi_img = np.array(Image.open(roi_mask_path).convert('L'))  
    original_img = Image.open(img_path).convert('RGB')  
  
    data_transform = transforms.Compose([  
        transforms.ToTensor(),  
        transforms.Normalize(mean=mean, std=std)  
    ])  
    img = data_transform(original_img).unsqueeze(0).to(device)  
  
    # 4. 硬件同步计时推理  
    with torch.no_grad():  
        # 预热  
        _ = eval_model(torch.zeros_like(img))  
  
        t_start = time_synchronized()  
        output = eval_model(img)  
        t_end = time_synchronized()  
        print(f" 5070 纯净网络前向传播耗时: {t_end - t_start:.4f} 秒")  
  
        # 5. 1通道 Sigmoid 数据的提取与二值化  
        pred = torch.sigmoid(output).squeeze(0).squeeze(0).cpu().numpy()  
  
        prediction = np.zeros_like(pred, dtype=np.uint8)  
        prediction[pred > 0.5] = 255  # 提取血管  
        prediction[roi_img == 0] = 0  # 强行扣除眼球外部杂质  
  
        # 6. 保存最终大图  
        result_mask = Image.fromarray(prediction)  
        result_mask.save("test_result.png")  
        print("预测图输出至主目录下【test_result.png】！")  
  
  
# ==========================================  
# 5. 主运行流水线  
# ==========================================  
if __name__ == '__main__':  
    # 数据加载  
    full_train_set = DRIVEDataset(DATA_ROOT, train=True, img_size=IMG_SIZE)  
    n_val = int(len(full_train_set) * VAL_SPLIT)  
    n_train = len(full_train_set) - n_val  
    train_set, val_set = random_split(full_train_set, [n_train, n_val], generator=torch.Generator().manual_seed(42))  
  
    train_loader = DataLoader(train_set, batch_size=BATCH_SIZE, shuffle=True, num_workers=0, pin_memory=True)  
    val_loader = DataLoader(val_set, batch_size=1, shuffle=False, num_workers=0, pin_memory=True)  
  
    # 初始化组件  
    model = UNet(in_c=3, out_c=1, base=64).to(device)  
    criterion_bce = nn.BCEWithLogitsLoss()  
    criterion_dice = SafeDiceLoss()  
    optimizer = optim.Adam(model.parameters(), lr=LR, weight_decay=WEIGHT_DECAY)  
    scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=20, gamma=0.5)  
  
    best_val_dice = 0.0  
    best_weight_file = os.path.join(SAVE_DIR, "unet_drive_best.pth")  
  
    # 开启60 轮循环  
    for epoch in range(1, NUM_EPOCHS + 1):  
        model.train()  
        epoch_loss = 0.0  
        train_bar = tqdm(train_loader, desc=f"Epoch {epoch:2d}/{NUM_EPOCHS} [Train]")  
  
        for batch in train_bar:  
            imgs = batch["image"].to(device)  
            labels = batch["label"].to(device)  
  
            optimizer.zero_grad()  
            logits = model(imgs)  
            loss = 0.5 * criterion_bce(logits, labels) + 0.5 * criterion_dice(torch.sigmoid(logits), labels)  
  
            loss.backward()  
            optimizer.step()  
            epoch_loss += loss.item()  
  
        scheduler.step()  
  
        # 验证  
        model.eval()  
        val_dice_sum = 0.0  
        with torch.no_grad():  
            for batch in val_loader:  
                val_dice_sum += calc_dice(model(batch["image"].to(device)), batch["label"].to(device)).item()  
  
        avg_val_dice = val_dice_sum / len(val_loader)  
        if avg_val_dice > best_val_dice:  
            best_val_dice = avg_val_dice  
            torch.save(model.state_dict(), best_weight_file)  
  
    run_inference_and_save(best_weight_file)
```