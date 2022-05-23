#! /bin/python3
import sys
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from bitarray import bitarray


def print_import(text):
    print(text)
    print('-------------------------')


def load_chinese(file_name):
    with open(file_name) as fp:
        charts = fp.readline()
        return charts


def binarization(img):
    img_np = np.array(img)
    img_result_list = bitarray()
    for pix_line in img_np:
        for pix in pix_line:
            if pix[3] >= 255/2:
                img_result_list.append(1)
            else:
                img_result_list.append(0)
    return img_result_list.tobytes()


def convert_chart(chart, font, size, line_uplift):
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    if not line_uplift == 0:
        draw.text((0, 0 - line_uplift), chart, font=font, fill='black')
    else:
        draw.text((0, 0), chart, font=font, fill='black')
    img_np = binarization(img)
    return img_np

def write_line(fp, s):
    fp.writelines(s+'\n')

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print_import(
            '参数缺失，python3 convert.py xxx.otf xxx.txt size line_uplift')
        exit(-1)
    print_import('字形文件%s，筛选字符集文件%s' % (sys.argv[1], sys.argv[2]))

    size = int(sys.argv[3])
    line_uplift = int(sys.argv[4])

    charts = load_chinese(sys.argv[2])
    print_import('读取筛选字符集文件\nover')

    font = ImageFont.truetype(sys.argv[1], size)
    print_import('读取字形文件\nover')

    with open('build/font_bitmap.h', 'w') as fp:
        write_line(fp, '#include "SimpleMap.h"')
        write_line(fp, '#define _PIXEL_LEN ' + str(size))
        write_line(fp, '#define _BYTE_LEN ' + str(size**2//8))
        write_line(fp, 'const uint8_t FONT_BITMAP[][_BYTE_LEN] PROGMEM = {')

        # each char convert to hex bitmap
        for chart in charts:
            char_bin_data = convert_chart(chart, font, size, line_uplift)
            hex_str = char_bin_data.hex()
            hex_str_out = '0x'
            for i, hex_str_char in enumerate(hex_str):
                hex_str_out += hex_str_char
                if not i%2==0:
                    hex_str_out += ', 0x'
            hex_str_out=hex_str_out[:-4]
            write_line(fp, '{'+str(hex_str_out)+'},')
        write_line(fp, '};')
        # mapping
        write_line(fp, 'void _bitmap_mapping_init(SimpleMap<String, int> *font_map) {')
        for i,chart in enumerate(charts):
            # special char replace
            if chart=='"':
                chart = '\\"'
            if chart=='\\':
                chart = '\\\\'
            write_line(fp, 'font_map->put("'+chart+'",  '+str(i)+');')
        write_line(fp, '}')
    print_import('写入头文件\nover')
