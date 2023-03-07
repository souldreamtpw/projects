'''
Author: souldream
Date: 2022-04-24 00:26:29
LastEditTime: 2022-04-24 11:26:17
LastEditors: souldream
Description: 
可以输入预定的版权声明、个性签名、空行等
'''
from .qq import QQ

class Get_rank_music:
    def __init__(self, name):
        self.url = 'https://music.liuzhijin.cn/'
        self.name = name
        self.result = []

    def search_qq(self):
        temp = QQ(self.url, self.name, 1)
        self.result.extend(temp.search()[0])

    def get_result(self):
        self.search_qq()

        return self.result