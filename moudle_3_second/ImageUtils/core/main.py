# /usr/bin/env Python
# -*- coding:utf-8 -*-
# author: wanshican

import os
from PIL import Image
from openpyxl import Workbook

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class ImageSystem:
    def __init__(self, sourse_dir=os.path.join(BASE_DIR, 'db'), target_dir=os.path.join(BASE_DIR, 'db')):
        self.sourse_dir = sourse_dir
        self.target_dir = target_dir

    def save_image_info(self):
        image_dir_list = []
        image_info_list = []
        for root, dirs, files in os.walk(self.sourse_dir):
            for name in files:
                filename = os.path.join(root, name)
                if os.path.splitext(filename)[1] in ['.jpg', '.png', '.bmp']:
                    image_dir_list.append(filename)
        if image_dir_list:
            for item in image_dir_list:
                info_list = []
                image_name = item.split('\\')[-1]
                image_size = Image.open(item).size
                info_list.append(image_name)
                info_list.append(image_size)
                image_info_list.append(info_list)
            wb = Workbook()
            sh = wb.active
            sh['a1'].value = '文件名'
            sh['b1'].value = '文件大小'
            for row in range(2, len(image_info_list)+1):
                sh.cell(row=row, column=1).value = image_info_list[row-2][0]
                sh.cell(row=row, column=2).value = str(image_info_list[row-2][1][0]) + '*' + str(image_info_list[row-2][1][1])
            wb.save(os.path.join(self.target_dir, 'image_info.xlsx'))
            print('图片信息保存成功！')
        else:
            print('当前目录没有图片文件，请先添加！')

            

    def resize(self):
        pass

    def rotate(self):
        pass

def main():
    IS = ImageSystem()
    IS.save_image_info()

if __name__ == "__main__":
    main()