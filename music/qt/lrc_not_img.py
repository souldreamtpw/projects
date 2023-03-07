'''
Author: souldream
Date: 2022-04-30 10:55:35
LastEditTime: 2022-05-01 15:14:57
LastEditors: souldream
Description: 
FilePath: \朵朵\qt\lrc_not_img.py
可以输入预定的版权声明、个性签名、空行等
'''

from PIL import Image
import os


class Lrc_not_img:
    def __init__(self, lrc, img_path, row, column):
        self.lrc = lrc
        self.img_path = img_path
        self.img = Image.open(img_path)
        self.row = row
        self.column = column

    def get_rank_img(self):
        save_path = "img/lrc"
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        left = self.lrc[0]
        right = self.lrc[0] + self.lrc[2]
        upper = self.lrc[1]
        lower = self.lrc[1] + self.lrc[3]
        cropped = self.img.crop((left, upper, right, lower))
        cropped.save("img/not_lrc/lrc.jpg")

    def get_small_img(self):
        img = Image.open(("img/not_lrc/lrc.jpg"))
        small_img_height = img.size[1] / self.row
        for j in range(self.row):
            left = 0
            right = self.column
            upper = j * small_img_height
            lower = (j + 1) * small_img_height
            cropped = img.crop((left, upper, right, lower))
            cropped.save("img/not_lrc/lrc_{}.jpg".format(j))



if __name__ == '__main__':
    # 四张图片的坐标( x, y, width, height)
    lrc = [620, 130, 520, 600]

    column = 520
    row = 12

    img_path = 'img/base/X播放界面.jpg'


    rank = Lrc_not_img(lrc, img_path, row, column)
    rank.get_rank_img()
    rank.get_small_img()
