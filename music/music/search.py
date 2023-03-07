'''
Author: souldream
Date: 2022-04-20 11:47:20
LastEditTime: 2022-05-06 02:47:31
LastEditors: souldream
Description: 
可以输入预定的版权声明、个性签名、空行等
'''


import requests
import pandas as pd
from .netease import Netease
from .qq import QQ
from .kuwo import Kuwo
from .kugou import Kugou
from .migu import Migu

class MusicSource:
    def __init__(self, name, page):
        self.url = 'https://music.liuzhijin.cn/'
        self.name = name
        self.page = page
        self.result = []

    def search_netease(self):
        temp = Netease(self.url, self.name, self.page)
        self.result.extend(temp.search())

    def search_qq(self):
        temp = QQ(self.url, self.name, self.page)
        self.result.extend(temp.search())

    def search_kuwo(self):
        temp = Kuwo(self.url, self.name, self.page)
        self.result.extend(temp.search())

    
    def search_kugou(self):
        temp = Kugou(self.url, self.name, self.page)
        self.result.extend(temp.search())

    
    def search_migu(self):
        temp = Migu(self.url, self.name, self.page)
        self.result.extend(temp.search())

    def get_result(self):
        self.search_netease()
        # self.search_qq()
        # self.search_kugou()
        # self.search_kuwo()
        # self.search_migu()

        return self.result


if __name__ == '__main__':
    name = '多幸运'
    page = 5
    a = MusicSource(name, page)
    b = a.get_result()
    print(len(b))