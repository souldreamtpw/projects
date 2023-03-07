'''
Author: souldream
Date: 2022-04-25 18:03:37
LastEditTime: 2022-04-25 20:02:26
LastEditors: souldream
Description: 
可以输入预定的版权声明、个性签名、空行等
'''
import requests

class Migu:
    def __init__(self, url, name, page):
        self.url = url
        self.name = name
        self.platfrom = 'migu'
        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
            # 判断请求是异步还是同步
            "x-requested-with": "XMLHttpRequest"}
        self.page = page


        # 歌手图片
        self.pic_list = ''
        # 歌曲
        self.title_list = ''
        # 歌手
        self.author_list = ''
        # 来源
        self.type_list = ''
        # 歌词 
        self.lrc_list = ''
        # 下载地址
        self.url_list = ''

        # 最终结果
        self.result = []


    def search(self):
        for i in range(self.page):
            param = {
                "input": self.name,
                "filter": "name",
                "type": self.platfrom,
                "page": i+1,}
            
            res = requests.post(url=self.url,data=param,headers=self.headers)
            json_text = res.json()

            for temp in json_text['data']:
                self.pic_list = temp['pic']
                self.title_list = temp['title'].strip()
                self.author_list = temp['author'].strip()
                # self.type_list = temp['type']
                self.type_list = '咪咕'
                self.lrc_list = temp['lrc']
                self.url_list = temp['url']
                self.result.append([self.pic_list, self.title_list, self.author_list, self.type_list, self.lrc_list, self.url_list])
        
        return self.result


if __name__ == '__main__':
    url = 'https://music.liuzhijin.cn/'
    name = '多幸运'
    page = 5
    a = Migu(url, name, page)
    b = a.search()
    print(b)