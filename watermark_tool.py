
# 图片批量加水印命令行工具
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="批量为图片添加拍摄日期水印")
    parser.add_argument('img_dir', type=str, help='图片所在目录路径')
    parser.add_argument('--font_size', type=int, default=32, help='水印字体大小，默认32')
    parser.add_argument('--color', type=str, default='#FFFFFF', help='水印字体颜色，默认白色')
    parser.add_argument('--position', type=str, choices=['left_top', 'center', 'right_bottom'], default='right_bottom', help='水印位置')
    return parser.parse_args()


import os
from PIL import Image
import piexif

def get_date_from_exif(img_path):
    try:
        exif_dict = piexif.load(img_path)
        date_str = exif_dict['Exif'].get(piexif.ExifIFD.DateTimeOriginal)
        if date_str:
            # exif 字节转字符串
            date_str = date_str.decode('utf-8')
            # 只取年月日
            return date_str.split(' ')[0].replace(':', '-')
    except Exception as e:
        pass
    return None

def find_images(directory):
    exts = ('.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG')
    for root, _, files in os.walk(directory):
        for f in files:
            if f.endswith(exts):
                yield os.path.join(root, f)

if __name__ == "__main__":
    args = parse_args()
    print(f"图片目录: {args.img_dir}")
    print(f"字体大小: {args.font_size}")
    print(f"颜色: {args.color}")
    print(f"水印位置: {args.position}")

    for img_path in find_images(args.img_dir):
        date = get_date_from_exif(img_path)
        print(f"图片: {img_path}")
        if date:
            print(f"  拍摄日期: {date}")
        else:
            print("  未找到拍摄日期 exif 信息")
