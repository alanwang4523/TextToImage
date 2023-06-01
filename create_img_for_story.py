# -*- coding: utf-8 -*-
"""
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * #
# *     _   _    _ _   _ _   __  _ _  __ _ _   _ _   _ _    * #
# *    / \ | |  / _` V  _  \ \ \/ ∧ \/ /  _` V  _  V  _` \  * #
# *   / Δ \| |_| (_l | | | |  \  / \  /| (_l | | | | (_) |  * #
# *  /_/ \_|___|\__∧_|_| |_|   \/   \/  \__∧_|_| |_|\__, |  * #
# *                                                 _ _| |  * #
# *             Author : AlanWang4523               \_ _,'  * #
# *              Mail  : alanwang4523@gmail.com             * #
# *              Date  : 2023-05-31                         * #
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * #

版本记录：

v1.0 2023-05-31
1、本脚本是把小说自动分段生成多张图片，可自定义背景色、字体、字体颜色、字体大小、行间距、字间距等

v2.0 2023-06-01
1、增加背景水印功能，支持自定义水印字体、水印颜色、水印大小、水印透明度、水印间隔

该脚本代码已免费开源到 Github，地址：https://github.com/alanwang4523/TextToImage
后续更新我会同步到上述 Github 上，可自行下载

"""
import sys
import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageChops


""" ************** 主图片的参数设置 ************** """
# 是否去除小说中的空白行
IS_DELETE_EMPTY_LINE = True

# 输出的图片宽高
WIDTH, HEIGHT = 1440, 2028

# 背景图颜色，RGBA，如浅绿色背景：(69, 139, 116)，颜色值取色可参考：https://tool.oschina.net/commons?type=3
BACKGROUND_COLOR = (0, 0, 0)

# 文字颜色，RGB
FONT_COLOR = (255, 255, 255)

# 中文字体库，请将此字体文件保存到脚本文件夹中
FONT_NAME = "yahei.ttf"

# 左右边距
HORIZONTAL_MARGIN = 200

# 上下边距
VERTICAL_MARGIN = 180

# 字体大小
FONT_SIZE = 40

# 行间距
LINE_SPACING = 46

# 字间距
CHARACTER_SPACING = 6


""" ************** 水印相关参数设置 ************** """
# 水印关键词
KEY_WATERMARK_TXT = ""

# 关键词字体，可以和主主文本不一致
KEY_WM_FONT = "yahei.ttf"

# 关键词水印文字颜色，RGB
KEY_WM_FONT_COLOR = (255, 255, 128)

# 关键词水印的透明度参数, 越小水印越浅，必须是 [0.0, 1.0] 之间
KEY_WM_OPACITY = 0.18

# 关键词水印大小
KEY_WM_SIZE = 50

# 关键词水印的旋转角度
KEY_WM_ROTATE_ANGLE = 30

# 两个关键词水印之间的水平间隔
KEY_WM_HORIZONTAL_SPACE = 120

# 两行关键词水印之间的水平间隔，即关键词水印行间距
KEY_WM_VERTICAL_SPACE = 120

# 关键词水印旋转角度
KEY_WM_ROTATION = 30


"""
# 设置透明度
"""
def set_opacity(im, opacity):
    assert opacity >= 0 and opacity <= 1

    alpha = im.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    im.putalpha(alpha)
    return im

"""
# 裁掉空白
"""
def crop_image(im):
    bg = Image.new(mode='RGBA', size=im.size)
    diff = ImageChops.difference(im, bg)
    del bg
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)
    return im


"""
# 生成关键词水印图
"""
def create_key_watermark():
    # 字体宽度
    wm_width = len(KEY_WATERMARK_TXT) * KEY_WM_SIZE

    # 创建水印图片
    watermark = Image.new(mode='RGBA', size=(wm_width, int(KEY_WM_SIZE * 2)))

    draw_txt = ImageDraw.Draw(im=watermark)
    draw_txt.text(xy=(0, int((watermark.size[1] - KEY_WM_SIZE) / 2)),
                    text=KEY_WATERMARK_TXT,
                    fill=KEY_WM_FONT_COLOR,
                    font=ImageFont.truetype(KEY_WM_FONT, size=KEY_WM_SIZE))
    # 裁剪空白
    watermark = crop_image(watermark)
    # 透明度
    set_opacity(watermark, KEY_WM_OPACITY)

    return watermark


def draw_watermark_to_img(im, mark):
    # 计算对角线长度
    img_w = im.size[0]
    img_h = im.size[1]
    mark_w = mark.size[0]
    mark_h = mark.size[1]
    d_len = int(math.sqrt(img_w*img_w + img_h*img_h))

    # 以对角线长度为宽高创建大图，确保旋转后能覆盖原图
    mark2 = Image.new(mode='RGBA', size=(d_len, d_len))

    # 在大图上生成水印文字
    y, idx = 0, 0
    while y < d_len:
        # 水印错开分布
        x = -int((mark_w + KEY_WM_HORIZONTAL_SPACE) * 0.5 * idx)
        idx = (idx + 1) % 2

        while x < d_len:
            # 在该位置粘贴mark水印图片
            mark2.paste(mark, (x, y))
            x += (mark_w + KEY_WM_HORIZONTAL_SPACE)
        y += (mark_h + KEY_WM_VERTICAL_SPACE)

    # 将大图旋转指定角度
    mark2 = mark2.rotate(KEY_WM_ROTATE_ANGLE)

    # 在原图上添加大图水印
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    im.paste(mark2, # 大图
        (int((img_w - d_len) / 2), int((img_h - d_len) / 2)), # 坐标
        mask=mark2.split()[3])
    del mark2
    return im

"""
# 将文本生成图片
"""
def create_image_with_text(i, text, out_path):
    # 创建一个新的空白图像
    image = Image.new("RGB", (WIDTH, HEIGHT), BACKGROUND_COLOR)

    # 创建字体对象
    font = ImageFont.truetype(FONT_NAME, FONT_SIZE)

    # 创建绘图对象
    draw = ImageDraw.Draw(image)

    # 划分行和计算总高度
    lines = text.split("\n")

    # 自动计算每行最大字符数
    max_chars_per_line = int((WIDTH - 2 * HORIZONTAL_MARGIN) / (FONT_SIZE + CHARACTER_SPACING))
    line_height = FONT_SIZE + LINE_SPACING

    y = VERTICAL_MARGIN

    # 在图像上绘制文本
    for line in lines:
        if line.strip() == '':
            y += line_height
            continue
        while line:
            chars_to_draw = line[:max_chars_per_line]
            line = line[max_chars_per_line:]
            x = HORIZONTAL_MARGIN
            for character in chars_to_draw:
                draw.text((x, y), character, fill=FONT_COLOR, font=font)
                x += (FONT_SIZE + CHARACTER_SPACING)
            y += line_height

    # 添加底部编号
    num_size = 30
    font = ImageFont.truetype(FONT_NAME, num_size)
    num = "{}".format(i + 1)
    x = (WIDTH - num_size) / 2
    y = HEIGHT - 100
    draw.text((x, y), num, fill=FONT_COLOR, font=font)

    return image


"""
# 将文本自动分成多段
"""
def handle_text(input_text_file, output_dir):
	img_count = 0
    # 打开要处理的文件
	with open(input_text_file, 'r', encoding='utf-8') as input_file:
        # 读取所有行
		all_lines = input_file.readlines()

		if IS_DELETE_EMPTY_LINE:
			# 删除所有空行
			all_lines = [line for line in all_lines if line.strip() != '']

		segments = []
		current_segment = ''

		# 自动计算每行最大字符数
		max_chars_per_line = int((WIDTH - 2 * HORIZONTAL_MARGIN) / (FONT_SIZE + CHARACTER_SPACING))
		line_height = FONT_SIZE + LINE_SPACING
		y = VERTICAL_MARGIN
		max_height = HEIGHT - VERTICAL_MARGIN
		# 根据设置的参数分段分屏
		for line in all_lines:
			while line:
				chars_to_draw = line[:max_chars_per_line]
				line = line[max_chars_per_line:]
				y += line_height

				if (y > max_height) :
					segments.append(current_segment)
					current_segment = ''
					y = VERTICAL_MARGIN

				current_segment += chars_to_draw

		segments.append(current_segment)

		img_count = len(segments)

		# 判断是否需要添加水印
		is_need_watermark = len(KEY_WATERMARK_TXT) > 0
		if is_need_watermark:
			watermark = create_key_watermark()

		for i, segment in enumerate(segments):
			print("正在生成第 {} 页...\n".format(i + 1))
			# print("{}".format(segment))
			output_filename = f'img_{i+1}.png'
			output_path = os.path.join(output_dir, output_filename)
			image = create_image_with_text(i, segment, output_path)
			if is_need_watermark:
				image = draw_watermark_to_img(image, watermark)
			# 将图像保存到文件
			image.save(output_path)
	return img_count


# 获取输入和输出文件名
input_file_path = sys.argv[1]
output_dir = os.path.dirname(os.path.abspath(input_file_path))

if len(sys.argv) > 2:
	KEY_WATERMARK_TXT = sys.argv[2]


def print_result(output_dir, img_count):
	# print("\n* * * * * * * * * * * * * * * * * * * * * * * * * * * * * *")
	print("\n===========================================================")
	print("本次共生成 {} 张图片，图片所在目录为：\n{}".format(img_count, output_dir))
	print("\n===========================================================")
	print("AlanWang 温馨提示：\n")
	print("本次要生成的小说文件为：{}".format(input_file_path))
	if len(KEY_WATERMARK_TXT) > 0:
		print("本次设置的水印关键词为：{}".format(KEY_WATERMARK_TXT))
	else:
		print("注意：本次未设置关键词水印！(如果确定不需要水印不用管)")
	print("\n请查看生成的图片，检查小说和关键词是否是本次要生成的内容.")
	print("===========================================================")

print("<===================================>")
print("要生成的小说文本为：{}".format(input_file_path))
print("要生成的小说关键词为：{}".format(KEY_WATERMARK_TXT))
print("开始生成图片，请稍后：\n")
img_count = handle_text(input_file_path, output_dir)
print("图片生成完成！")
print_result(output_dir, img_count)