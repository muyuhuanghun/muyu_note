#!/usr/bin/env python3
"""
图片元数据（EXIF）管理工具
📌 查看、清除图片的 EXIF 元数据，保护隐私
⚠️ 需要安装: pip install Pillow
"""

import argparse
import sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

try:
    from PIL import Image
    from PIL.ExifTags import TAGS
except ImportError:
    print("❌ 需要安装 Pillow: pip install Pillow")
    sys.exit(1)


def get_exif(img: Image.Image) -> dict:
    """提取 EXIF 信息"""
    exif_data = {}
    try:
        raw = img._getexif()
        if raw:
            for tag_id, value in raw.items():
                tag = TAGS.get(tag_id, tag_id)
                # 过滤过长的值
                if isinstance(value, bytes) and len(value) > 100:
                    value = f"<{len(value)} bytes>"
                exif_data[tag] = value
    except Exception:
        pass
    return exif_data


def show_metadata(filepath: str, fmt: str = "text"):
    """显示图片元数据"""
    path = Path(filepath)
    if not path.is_file():
        print(f"❌ 文件不存在: {filepath}")
        return

    img = Image.open(path)
    exif = get_exif(img)

    # 基本信息
    info = {
        "文件名": path.name,
        "格式": img.format,
        "尺寸": f"{img.width} × {img.height}",
        "色彩模式": img.mode,
        "文件大小": f"{path.stat().st_size / 1024:.1f} KB",
    }

    if fmt == "md":
        print(f"## {path.name}\n")
        print(f"| 项目 | 值 |")
        print(f"|------|-----|")
        for k, v in info.items():
            print(f"| {k} | {v} |")
        if exif:
            print(f"\n### EXIF 信息\n")
            print(f"| 标签 | 值 |")
            print(f"|------|-----|")
            for k, v in exif.items():
                print(f"| {k} | {v} |")
    else:
        print(f"📸 {path.name}")
        print(f"{'='*40}")
        for k, v in info.items():
            print(f"  {k}: {v}")

        if exif:
            print(f"\n  EXIF 信息:")
            for k, v in exif.items():
                print(f"    {k}: {v}")
        else:
            print(f"\n  无 EXIF 信息")

    img.close()


def strip_metadata(filepath: str, output: str = None, dry_run: bool = False) -> bool:
    """清除图片元数据"""
    path = Path(filepath)
    if not path.is_file():
        return False

    img = Image.open(path)
    exif = get_exif(img)

    if not exif:
        return False

    out_path = Path(output) if output else path

    if dry_run:
        print(f"  {path.name}: 将清除 {len(exif)} 个 EXIF 标签")
        img.close()
        return True

    # 创建无 EXIF 的副本
    data = list(img.getdata())
    clean = Image.new(img.mode, img.size)
    clean.putdata(data)

    save_kwargs = {}
    if img.format in ("JPEG", "JPG"):
        save_kwargs["quality"] = 95
        save_kwargs["optimize"] = True

    clean.save(str(out_path), **save_kwargs)
    img.close()
    clean.close()

    print(f"  ✅ {path.name}: 已清除 {len(exif)} 个 EXIF 标签")
    return True


def main():
    parser = argparse.ArgumentParser(
        description="图片元数据管理工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python image_metadata.py photo.jpg
  python image_metadata.py photo.jpg --strip -o clean.jpg
  python image_metadata.py ./photos/ --strip --output ./clean/
        """,
    )
    parser.add_argument("files", nargs="+", help="图片文件或目录")
    parser.add_argument("--strip", action="store_true", help="清除 EXIF 信息")
    parser.add_argument("--output", "-o", help="输出路径")
    parser.add_argument("--dry-run", action="store_true", help="预览模式")
    parser.add_argument("--format", choices=["text", "md"], default="text", help="输出格式")

    args = parser.parse_args()

    for f in args.files:
        p = Path(f)
        if p.is_dir():
            images = [img for img in p.iterdir() if img.suffix.lower() in (".jpg", ".jpeg", ".png")]
            if args.strip:
                out_dir = Path(args.output) if args.output else p / "clean"
                if not args.dry_run:
                    out_dir.mkdir(parents=True, exist_ok=True)
                for img in sorted(images):
                    out = out_dir / img.name if not args.dry_run else None
                    strip_metadata(str(img), str(out) if out else None, args.dry_run)
            else:
                for img in sorted(images):
                    show_metadata(str(img), args.format)
                    print()
        else:
            if args.strip:
                strip_metadata(f, args.output, args.dry_run)
            else:
                show_metadata(f, args.format)


if __name__ == "__main__":
    main()
