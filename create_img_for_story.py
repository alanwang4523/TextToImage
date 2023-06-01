# -*- coding: utf-8 -*-
import sys
import os
from PIL import Image, ImageDraw, ImageFont

# 生成图片的参数设置

# 是否去除小说中的空白行
IS_DELETE_EMPTY_LINE = True 

# 输出的图片宽高
WIDTH, HEIGHT = 1440, 2028 

# 背景图颜色，RGBA，如绿色背景：(0,128,0,0)
BACKGROUND_COLORE=(0,0,0,256) 

# 文字颜色，RGB
FONT_COLOR = (255, 255, 255) 

# 中文字体库，请将此字体文件保存到脚本文件夹中
FONT_NAME = "yahei.ttf"  

# 左右边距
HORIZONTAL_MATGIN = 200 

# 上下边距
VERTICAL_MATGIN = 180 

# 字体大小
FONT_SIZE = 40 

# 行间距
LINE_SPACING = 46 

# 字间距
CHARACTER_SPACING = 6 


"""
# 将文本生成图片
"""
def create_image_with_text(i, text, out_path):

    # 创建一个新的空白图像
    image = Image.new("RGB", (WIDTH, HEIGHT), BACKGROUND_COLORE)

    # 创建字体对象
    font = ImageFont.truetype(FONT_NAME, FONT_SIZE)

    # 创建绘图对象
    draw = ImageDraw.Draw(image)

    # 划分行和计算总高度
    lines = text.split("\n")

    # 自动计算每行最大字符数
    max_chars_per_line = int((WIDTH - 2 * HORIZONTAL_MATGIN) / (FONT_SIZE + CHARACTER_SPACING))
    line_height = FONT_SIZE + LINE_SPACING

    y = VERTICAL_MATGIN

    # 在图像上绘制文本
    for line in lines:
        # width, _ = draw.textsize(line, font=font)
        while line:
            chars_to_draw = line[:max_chars_per_line]
            line = line[max_chars_per_line:]
            x = HORIZONTAL_MATGIN
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
    # 将图像保存到文件
    image.save(out_path)


def handle_text(input_text_file: str, output_dir: str):
    # all_lines = []
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
		max_chars_per_line = int((WIDTH - 2 * HORIZONTAL_MATGIN) / (FONT_SIZE + CHARACTER_SPACING))
		line_height = FONT_SIZE + LINE_SPACING
		y = VERTICAL_MATGIN
		max_height = HEIGHT - VERTICAL_MATGIN
		# 根据设置的参数分段分屏
		for line in all_lines:
			# width, _ = draw.textsize(line, font=font)
			while line:
				chars_to_draw = line[:max_chars_per_line]
				line = line[max_chars_per_line:]
				y += line_height
				
				if (y > max_height) :
					segments.append(current_segment)
					current_segment = ''
					y = VERTICAL_MATGIN
	
				current_segment += chars_to_draw

		segments.append(current_segment)
		for i, segment in enumerate(segments):
			print("正在生成第 {} 页...\n".format(i+1))
			# print("{}".format(segment))
			output_filename = f'img_{i+1}.png'
			output_path = os.path.join(output_dir, output_filename)
			create_image_with_text(i, segment, output_path)


# 获取输入和输出文件名
input_file_path = sys.argv[1]
output_dir = os.path.dirname(os.path.abspath(input_file_path))

print("开始生成图片，要生成的小说文本为：{}".format(input_file_path))
handle_text(input_file_path, output_dir)
print("全部生成完成，图片所在目录为：\n{}".format(output_dir))