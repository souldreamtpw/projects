'''
Author: souldream
Date: 2022-04-19 13:46:37
LastEditTime: 2022-04-20 18:38:04
LastEditors: souldream
Description: 
FilePath: \朵朵\test\test2.py
可以输入预定的版权声明、个性签名、空行等
'''
import requests
import os

def song_download(url,title,author):

    # 下载（这种读写文件的下载方式适合少量文件的下载）
    content = requests.get(url).content
    with open(file = r'C:\Users\souldream\Desktop\朵朵\temp\duoduo\\' + title + author + '.mp3',mode='wb') as f:
        f.write(content)
    print('下载完毕,{0}-{1},请试听'.format(title,author))

url = 'http://music.163.com/song/media/outer/url?id=1901371647.mp3'

title = 'a'
author = 'b'

song_download(url, title, author)