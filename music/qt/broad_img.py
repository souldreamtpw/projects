'''
Author: souldream
Date: 2022-05-01 15:15:22
LastEditTime: 2022-05-16 17:20:20
LastEditors: souldream
Description: 
FilePath: \朵朵\qt\broad_img.py
可以输入预定的版权声明、个性签名、空行等
'''
from PIL import Image
import os


class Broad_img:
    def __init__(self, lrc, img_path):
        self.lrc = lrc
        self.img_path = img_path
        self.img = Image.open(img_path)

    def get_rank_img(self):
        # 
        save_path = "img/lrc"
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        left = self.lrc[0]
        right = self.lrc[0] + self.lrc[2]
        upper = self.lrc[1]
        lower = self.lrc[1] + self.lrc[3]
        cropped = self.img.crop((left, upper, right, lower))
        cropped.save("img/broad/not.jpg")

if __name__ == '__main__':
    # 四张图片的坐标( x, y, width, height)
    lrc = [100, 130, 400, 400]

    img_path = 'img/base/X播放界面.jpg'


    rank = Broad_img(lrc, img_path)
    rank.get_rank_img()
