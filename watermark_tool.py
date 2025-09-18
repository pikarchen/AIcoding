
# 图片批量加水印命令行工具
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="批量为图片添加拍摄日期水印")
    parser.add_argument('img_dir', type=str, help='图片所在目录路径')
    parser.add_argument('--font_size', type=int, default=32, help='水印字体大小，默认32')
    parser.add_argument('--color', type=str, default='#FFFFFF', help='水印字体颜色，默认白色')
    parser.add_argument('--position', type=str, choices=['left_top', 'center', 'right_bottom'], default='right_bottom', help='水印位置')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    print(f"图片目录: {args.img_dir}")
    print(f"字体大小: {args.font_size}")
    print(f"颜色: {args.color}")
    print(f"水印位置: {args.position}")
