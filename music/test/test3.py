'''
Author: souldream
Date: 2022-04-19 13:46:37
LastEditTime: 2022-04-20 17:11:58
LastEditors: souldream
Description: 
FilePath: \朵朵\test\test3.py
可以输入预定的版权声明、个性签名、空行等
'''
import requests
url = 'https://img-blog.csdnimg.cn/20200924162143340.jpg'
res = requests.get(url)
with open('test.jpg', 'wb') as f:
    f.write(res.content)