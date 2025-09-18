# 图片批量加水印命令行工具

## 功能简介
- 批量读取指定目录下图片，提取 exif 拍摄日期作为水印
- 支持自定义字体大小、颜色和水印位置
- 处理后图片自动保存到新目录（原目录名_watermark）

## 使用方法
```bash
python watermark_tool.py <图片目录> [--font_size 32] [--color #FFFFFF] [--position right_bottom]
```

- `img_dir`：必填，图片所在目录
- `--font_size`：可选，水印字体大小，默认32
- `--color`：可选，水印颜色，默认白色
- `--position`：可选，水印位置，left_top/center/right_bottom，默认右下角

## 依赖
- Pillow
- piexif

安装依赖：
```bash
pip install -r requirements.txt
```

## 示例
```bash
python watermark_tool.py ./photos --font_size 40 --color #FF0000 --position left_top
```

## 目录结构
```
|-- watermark_tool.py
|-- requirements.txt
|-- README.md
```
