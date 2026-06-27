#!/usr/bin/env python3
"""
图片批量处理工具
📌 缩放、裁剪、格式转换、压缩、加水印
⚠️ 需要安装: pip install Pillow
"""

import argparse
import sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("❌ 需要安装 Pillow: pip install Pillow")
    sys.exit(1)


def resize_image(img: Image.Image, size_str: str) -> Image.Image:
    """
    缩放图片
    size_str 格式: "800x600" 或 "800x"（保持比例）或 "x600"（保持比例）
    """
    if "x" in size_str:
        parts = size_str.split("x")
        w = int(parts[0]) if parts[0] else None
        h = int(parts[1]) if parts[1] else None

        if w and h:
            return img.resize((w, h), Image.LANCZOS)
        elif w:
            ratio = w / img.width
            return img.resize((w, int(img.height * ratio)), Image.LANCZOS)
        elif h:
            ratio = h / img.height
            return img.resize((int(img.width * ratio), h), Image.LANCZOS)
    return img


def add_watermark(img: Image.Image, text: str, position: str = "bottom-right", opacity: int = 128) -> Image.Image:
    """添加文字水印"""
    # 确保是 RGBA 模式
    if img.mode != "RGBA":
        img = img.convert("RGBA")

    # 创建水印层
    watermark = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(watermark)

    # 尝试使用默认字体
    try:
        font = ImageFont.truetype("arial.ttf", max(16, img.width // 30))
    except Exception:
        font = ImageFont.load_default()

    # 计算文字大小
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]

    # 计算位置
    margin = 20
    if position == "bottom-right":
        x, y = img.width - tw - margin, img.height - th - margin
    elif position == "bottom-left":
        x, y = margin, img.height - th - margin
    elif position == "top-right":
        x, y = img.width - tw - margin, margin
    elif position == "top-left":
        x, y = margin, margin
    elif position == "center":
        x, y = (img.width - tw) // 2, (img.height - th) // 2
    else:
        x, y = img.width - tw - margin, img.height - th - margin

    draw.text((x, y), text, fill=(255, 255, 255, opacity), font=font)

    return Image.alpha_composite(img, watermark)


def process_images(
    directory: str,
    output: str = None,
    resize: str = None,
    fmt: str = None,
    quality: int = 85,
    compress: int = None,
    watermark: str = None,
    wm_position: str = "bottom-right",
    dry_run: bool = False,
):
    """批量处理图片"""
    dir_path = Path(directory)
    if not dir_path.is_dir():
        print(f"❌ 目录不存在: {directory}")
        sys.exit(1)

    out_path = Path(output) if output else dir_path / "processed"
    if not dry_run:
        out_path.mkdir(parents=True, exist_ok=True)

    # 收集图片
    exts = {".jpg", ".jpeg", ".png", ".bmp", ".gif", ".webp", ".tiff"}
    images = sorted(f for f in dir_path.iterdir() if f.suffix.lower() in exts and f.is_file())

    if not images:
        print("⚠️ 没有找到图片文件")
        return

    print(f"📂 目录: {dir_path}")
    print(f"🖼️ 图片: {len(images)} 个")
    if dry_run:
        print("🔍 预览模式")
    print("-" * 60)

    for img_path in images:
        try:
            img = Image.open(img_path)
        except Exception as e:
            print(f"  ❌ {img_path.name}: {e}")
            continue

        # 缩放
        if resize:
            img = resize_image(img, resize)

        # 压缩
        if compress:
            quality = compress

        # 水印
        if watermark:
            img = add_watermark(img, watermark, wm_position)

        # 确定输出格式和文件名
        out_fmt = fmt or img_path.suffix.lstrip(".")
        out_name = f"{img_path.stem}.{out_fmt}"
        out_file = out_path / out_name

        if dry_run:
            actions = []
            if resize: actions.append(f"缩放→{resize}")
            if fmt: actions.append(f"格式→{fmt}")
            if compress: actions.append(f"压缩→{compress}")
            if watermark: actions.append("加水印")
            print(f"  {img_path.name} → {out_name} ({', '.join(actions) if actions else '无操作'})")
        else:
            # 保存
            save_kwargs = {}
            if out_fmt.lower() in ("jpg", "jpeg"):
                if img.mode == "RGBA":
                    img = img.convert("RGB")
                save_kwargs["quality"] = quality
                save_kwargs["optimize"] = True
            elif out_fmt.lower() == "webp":
                save_kwargs["quality"] = quality
            elif out_fmt.lower() == "png":
                save_kwargs["optimize"] = True

            img.save(str(out_file), **save_kwargs)
            size_kb = out_file.stat().st_size / 1024
            print(f"  ✅ {img_path.name} → {out_name} ({size_kb:.1f} KB)")

    print("-" * 60)
    print(f"📊 处理完成")


def main():
    parser = argparse.ArgumentParser(
        description="图片批量处理工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python image_batch_process.py ./photos/ --resize 800x --output ./resized/
  python image_batch_process.py ./photos/ --format webp --quality 85
  python image_batch_process.py ./photos/ --watermark "© muyu" --position bottom-right
  python image_batch_process.py ./photos/ --compress 70 --dry-run
        """,
    )
    parser.add_argument("directory", help="图片目录")
    parser.add_argument("--output", "-o", help="输出目录")
    parser.add_argument("--resize", help="缩放尺寸（如 800x600, 800x, x600）")
    parser.add_argument("--format", dest="fmt", help="输出格式（jpg, png, webp）")
    parser.add_argument("--quality", type=int, default=85, help="输出质量（默认 85）")
    parser.add_argument("--compress", type=int, help="压缩质量（1-100）")
    parser.add_argument("--watermark", help="水印文字")
    parser.add_argument("--position", default="bottom-right",
                        choices=["top-left", "top-right", "bottom-left", "bottom-right", "center"],
                        help="水印位置")
    parser.add_argument("--dry-run", action="store_true", help="预览模式")

    args = parser.parse_args()
    process_images(
        directory=args.directory,
        output=args.output,
        resize=args.resize,
        fmt=args.fmt,
        quality=args.quality,
        compress=args.compress,
        watermark=args.watermark,
        wm_position=args.position,
        dry_run=args.dry_run,
    )


if __name__ == "__main__":
    main()
