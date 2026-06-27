# 10.图片处理

📌 图片批量处理工具，解决日常图片管理需求。
⚠️ 部分脚本需要安装 Pillow：`pip install Pillow`

# ==========================================
# 📁 脚本列表
# ==========================================

| 脚本 | 功能 | 适用场景 |
|------|------|----------|
| `image_batch_process.py` | 图片批量缩放/裁剪/格式转换/加水印 | 笔记插图规范化、论文图片处理 |
| `image_rename_exif.py` | 根据拍摄时间重命名照片 | 照片整理、旅行照片归档 |
| `image_metadata.py` | 查看/清除图片元数据（EXIF） | 隐私保护、图片信息查看 |

# ==========================================
# 🚀 使用示例
# ==========================================

## image_batch_process.py — 批量处理

```bash
# 批量缩放到 800px 宽（保持比例）
python image_batch_process.py ./photos/ --resize 800x --output ./resized/

# 批量转换为 WebP 格式（减小体积）
python image_batch_process.py ./photos/ --format webp --quality 85

# 批量添加水印
python image_batch_process.py ./photos/ --watermark "© muyu_note" --position bottom-right

# 批量压缩（调整质量）
python image_batch_process.py ./photos/ --compress 70 --output ./compressed/

# 预览模式
python image_batch_process.py ./photos/ --resize 640x --dry-run
```

## image_rename_exif.py — 按拍摄时间重命名

```bash
# 按拍摄时间重命名（YYYYMMDD_HHMMSS_序号.jpg）
python image_rename_exif.py ./photos/

# 自定义格式
python image_rename_exif.py ./photos/ --format "{date}_{camera}_{n:03d}"

# 预览
python image_rename_exif.py ./photos/ --dry-run
```

## image_metadata.py — 元数据管理

```bash
# 查看图片 EXIF 信息
python image_metadata.py photo.jpg

# 清除所有 EXIF（隐私保护）
python image_metadata.py photo.jpg --strip -o clean.jpg

# 批量清除
python image_metadata.py ./photos/ --strip --output ./clean/
```

# ==========================================
# ⚠️ 注意事项
# ==========================================

- 需要安装 Pillow：`pip install Pillow`
- 图片处理不修改原文件，输出到指定目录
- EXIF 清除后不可恢复，建议保留原文件备份
