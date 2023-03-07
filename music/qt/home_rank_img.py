'''
Author: souldream
Date: 2022-05-01 15:52:52
LastEditTime: 2022-05-01 15:52:52
LastEditors: souldream
Description: 
FilePath: \朵朵\qt\home_like_img.py
可以输入预定的版权声明、个性签名、空行等
'''
from PIL import Image
import os

class Home_rank_img:
    def __init__(self, ranks, img_path, row, column):
        self.ranks = ranks
        self.img_path = img_path
        self.img = Image.open(img_path)
        self.row = row
        self.column = column

    def get_rank_img(self):
        for i in range(len(self.ranks)):
            save_path = "img/rank/rank{}".format(i + 1)
            if not os.path.exists(save_path):
                os.makedirs(save_path)
            left = self.ranks[i][0]
            right = self.ranks[i][0] + self.ranks[i][2]
            upper = self.ranks[i][1]
            lower = self.ranks[i][1] + self.ranks[i][3]
            cropped = self.img.crop((left, upper, right, lower))
            cropped.save("img/rank/rank{}/rank{}.jpg".format(i + 1, i + 1))


    def get_small_img(self):
        for i in range(len(self.ranks)):
            img = Image.open(("img/rank/rank{}/rank{}.jpg".format(i + 1, i + 1)))
            small_img_height = img.size[1] / self.row
            for j in range(len(self.column) * self.row):
                left = j % 2 * self.column[0]
                right = self.column[0] + (j % 2) * self.column[1]
                upper = j // 2 * small_img_height
                lower = (j // 2 + 1) * small_img_height
                cropped = img.crop((left, upper, right, lower))
                cropped.save("img/rank/rank{}/rank{}_{}.jpg".format(i + 1, i + 1, j))



if __name__ == '__main__':
    # 四张图片的坐标( x, y, width, height)
    rank1 = [200, 497, 230, 372]
    rank2 = [440, 497, 230, 372]
    rank3 = [680, 497, 230, 372]
    rank4 = [920, 497, 230, 372]

    column = [128, 120]
    row = 10

    ranks = [rank1, rank2, rank3, rank4]
    img_path = 'img/base/主界面.jpg'


    rank = Home_rank_img(ranks, img_path, row, column)
    rank.get_rank_img()
    rank.get_small_img()