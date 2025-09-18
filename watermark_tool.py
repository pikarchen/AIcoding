
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
from PIL import Image, ImageDraw, ImageFont
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


def add_watermark(img_path, text, font_size, color, position, out_path):
    image = Image.open(img_path).convert('RGBA')
    txt_layer = Image.new('RGBA', image.size, (255,255,255,0))
    draw = ImageDraw.Draw(txt_layer)
    # 字体选择，兼容性考虑用默认字体
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        font = ImageFont.load_default()
    text_size = draw.textbbox((0,0), text, font=font)
    text_w = text_size[2] - text_size[0]
    text_h = text_size[3] - text_size[1]
    # 位置计算
    if position == 'left_top':
        xy = (10, 10)
    elif position == 'center':
        xy = ((image.width - text_w)//2, (image.height - text_h)//2)
    else: # right_bottom
        xy = (image.width - text_w - 10, image.height - text_h - 10)
    # 颜色支持 #RRGGBB 或 #RRGGBBAA
    if color.startswith('#'):
        color_rgba = tuple(int(color[i:i+2], 16) for i in (1, 3, 5)) + (180,)
    else:
        color_rgba = (255,255,255,180)
    draw.text(xy, text, font=font, fill=color_rgba)
    watermarked = Image.alpha_composite(image, txt_layer).convert('RGB')
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    watermarked.save(out_path)

def main():
    args = parse_args()
    print(f"图片目录: {args.img_dir}")
    print(f"字体大小: {args.font_size}")
    print(f"颜色: {args.color}")
    print(f"水印位置: {args.position}")

    out_dir = args.img_dir.rstrip('/\\') + '_watermark'
    for img_path in find_images(args.img_dir):
        date = get_date_from_exif(img_path)
        print(f"图片: {img_path}")
        if date:
            print(f"  拍摄日期: {date}")
            rel_path = os.path.relpath(img_path, args.img_dir)
            out_path = os.path.join(out_dir, rel_path)
            add_watermark(img_path, date, args.font_size, args.color, args.position, out_path)
            print(f"  已保存: {out_path}")
        else:
            print("  未找到拍摄日期 exif 信息，跳过水印")

if __name__ == "__main__":
    main()
