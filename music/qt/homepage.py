'''
Author: souldream
Date: 2022-03-24 12:54:12
LastEditTime: 2022-05-06 02:46:55
LastEditors: souldream
Description: 
FilePath: \朵朵\qt\homepage.py
可以输入预定的版权声明、个性签名、空行等
'''
from PyQt5 import uic, QtWidgets, QtCore, QtGui
import sys
from functools import partial
import requests

from PyQt5.QtWebEngineWidgets import QWebEngineView

import os
import lxml.etree as et
import lxml
import requests as re
import pymysql

# 分类专区 精选视频 人气歌手
main_win = None


class Homepage:
    def __init__(self, user_inf):
        super().__init__()
        # 从文件中加载UI定义
        self.ui = uic.loadUi(r"ui\homepage.ui")
        self.inf = user_inf
        self.root = self.inf[0]

        # 加载logo
        # self.ui.label_logo.setPixmap(QtGui.QPixmap(r'img\base\logo.jpg'))

        self.music_list1 = []
        self.song_list1 = []
        self.music_list2 = []
        self.song_list2 = []
        self.music_list3 = []
        self.song_list3 = []
        self.music_list4 = []
        self.song_list4 = []
        self.like_music_list = []
        self.like_song_list = []

        self.ui.setWindowTitle('朵朵')
        # 隐藏除关闭按钮的其他按钮
        # 隐藏菜单栏 QtCore.Qt.FramelessWindowHint
        self.ui.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.FramelessWindowHint)
        # 隐藏状态栏
        self.ui.statusBar().hide()

        self.column = 2


        self.music_number = 9

        # 榜单列宽
        self.column1 = 128
        self.column2 = 100
        # 行高
        self.height = 37

        # 动态创建变量名
        self.check_list = locals()

        # 加载软件上一次关闭时的状态
        self.ui.label_photo.setPixmap(QtGui.QPixmap(self.inf[1]))
        self.ui.label_name.setText(self.inf[2])
        self.ui.label_name.setStyleSheet('color: rgb(255, 255, 255);font: 75 16pt "等线";')
        
        # 设置图片填充方式
        # self.ui.label_logo.setScaledContents(True)
        self.ui.label_photo.setScaledContents(True)

        # 给组件设置透明度
        op = QtWidgets.QGraphicsOpacityEffect()
        op.setOpacity(0)
        self.ui.btn_photo.setGraphicsEffect(op)
        op = QtWidgets.QGraphicsOpacityEffect()
        op.setOpacity(0)
        self.ui.btn_logo.setGraphicsEffect(op)

        # 给按钮绑定事件
        self.ui.btn_heart.clicked.connect(self.heart)
        self.ui.btn_local.clicked.connect(self.local)
        self.ui.btn_search.clicked.connect(self.search)
        self.ui.btn_set.clicked.connect(self.set)
        self.ui.btn_photo.clicked.connect(self.login)
        self.ui.btn_logo.clicked.connect(self.logo)
        self.ui.btn_down.clicked.connect(self.download)
        self.ui.btn_close.clicked.connect(QtCore.QCoreApplication.quit)
        # self.ui.btn_min.clicked.connect(self.showMinimized)

        # 加载轮播图
        url = os.getcwd() + os.path.sep + "history/index.html"
        # url = os.getcwd() + os.path.sep + "jquery2/accordion.html"
        # url = os.getcwd() + os.path.sep + "jquery2/carousel.html"
        self.ui.webview.load(QtCore.QUrl.fromLocalFile(url))

        # 加载榜单
        self.get_rank()
        # self.center()


    def center(self):
        screen=QtWidgets.QDesktopWidget().screenGeometry()#获取屏幕分辨率
#QtWidgets.QDesktopWidget().screenGeometry()中QDesktopWidget()也有括号
        size=self.ui.geometry()#获取窗口尺寸
        self.ui.move((screen.width()-size.width())/2,(screen.height()-size.height())/2)#利用move函数窗口居中

    def get_rank(self):
        self.get_like()
        self.showLike()
        self.get_rank1()
        self.showMusicList1()
        self.get_rank2()
        self.showMusicList2()
        self.get_rank3()
        self.showMusicList3()
        self.get_rank4()
        self.showMusicList4()

    def showLike(self):
        self.row = len(self.like_music_list)
        # 设置列数
        self.ui.table_like.setColumnCount(1)
        # 设置行数
        self.ui.table_like.setRowCount(self.row)
        # 隐藏网格线
        self.ui.table_like.setShowGrid(False)
        # 隐藏表头
        self.ui.table_like.verticalHeader().setVisible(False)
        self.ui.table_like.horizontalHeader().setVisible(False)
        # 设置列宽
        self.ui.table_like.setColumnWidth(0, 181)
        # self.ui.table_like.setColumnWidth(1, self.column2)
        for i in range(len(self.like_music_list)):
            self.set_button(i)

    def set_button(self, index):
        # 设置行高
        self.ui.table_like.setRowHeight(index, self.height)
        i = index
        # 播放歌曲
        self.check_list[f'music5{index}'] = QtWidgets.QPushButton(self.like_music_list[i] + ' - ' +  self.like_song_list[i])
        self.check_list[f'music5{index}'].setStyleSheet('QPushButton{border-image: url(img/like/like_%d.jpg);font: bold 13pt "华文仿宋";color: rgb(255, 255, 255);}'% (index))
        self.check_list[f'music5{index}'].clicked.connect(partial(self.like_broad, f'music5{index}', self.like_music_list, self.like_song_list))
        # btn.clicked.connect(lambda:self.comboxSelect('rrrrrrrrrrrr'))
        self.ui.table_like.setCellWidget(index, 0, self.check_list[f'music5{index}'])

    def showMusicList1(self):
        self.row = len(self.song_list1) + 1
        # 设置列数
        self.ui.table_music1.setColumnCount(self.column)
        # 设置行数
        self.ui.table_music1.setRowCount(self.row)
        self.set_button1(0)
        # 隐藏网格线
        self.ui.table_music1.setShowGrid(False)
        # 隐藏表头
        self.ui.table_music1.verticalHeader().setVisible(False)
        self.ui.table_music1.horizontalHeader().setVisible(False)
        # 设置列宽
        self.ui.table_music1.setColumnWidth(0, self.column1)
        self.ui.table_music1.setColumnWidth(1, self.column2)
        for i in range(len(self.song_list1)):
            self.set_button1(i + 1)
        

    def set_button1(self, index):
        # 设置行高
        self.ui.table_music1.setRowHeight(index, self.height)
        if(index):
            i = index - 1
            # 播放歌曲
            self.check_list[f'music1{index}'] = QtWidgets.QPushButton(self.music_list1[i])
            self.check_list[f'music1{index}'].setStyleSheet('QPushButton{border-image: url(img/rank/rank1/rank1_%d.jpg);font: bold 14pt "华文仿宋";background-color: rgb(246, 227, 178);}'% (index * 2 + 0))
            self.check_list[f'music1{index}'].clicked.connect(partial(self.broad, f'music1{index}', self.music_list1, self.song_list1))
            # btn.clicked.connect(lambda:self.comboxSelect('rrrrrrrrrrrr'))
            self.ui.table_music1.setCellWidget(index, 0, self.check_list[f'music1{index}'])
            # 歌手搜索
            self.check_list[f'song1{index}'] = QtWidgets.QPushButton(self.song_list1[i])
            self.check_list[f'song1{index}'].setStyleSheet('QPushButton{border-image: url(img/rank/rank1/rank1_%d.jpg);font: bold 14pt "华文仿宋";background-color: rgb(246, 227, 178);}'% (index * 2 + 1))
            self.check_list[f'song1{index}'].clicked.connect(partial(self.search_song1, f'song1{index}'))
            # btn.clicked.connect(lambda:self.comboxSelect('rrrrrrrrrrrr'))
            self.ui.table_music1.setCellWidget(index, 1, self.check_list[f'song1{index}'])
        else:
            data = ["歌曲", "歌手"]
            for i in range(len(data)):
                btn = QtWidgets.QPushButton(data[i])
                # 歌曲信息
                btn.setStyleSheet('QPushButton{border-image: url(img/rank/rank1/rank1_%d.jpg);font: bold 14pt "华文仿宋";background-color: rgb(246, 227, 178);color: rgb(255, 178, 7);}'% (index * 2 + i))
                # btn.clicked.connect(lambda:self.comboxSelect('rrrrrrrrrrrr'))
                self.ui.table_music1.setCellWidget(index, i, btn)
    def showMusicList2(self):
        self.row = len(self.song_list2) + 1
        # 设置列数
        self.ui.table_music2.setColumnCount(self.column)
        # 设置行数
        self.ui.table_music2.setRowCount(self.row)
        self.set_button2(0)
        # 隐藏网格线
        self.ui.table_music2.setShowGrid(False)
        # 隐藏表头
        self.ui.table_music2.verticalHeader().setVisible(False)
        self.ui.table_music2.horizontalHeader().setVisible(False)
        # 设置列宽
        self.ui.table_music2.setColumnWidth(0, self.column1)
        self.ui.table_music2.setColumnWidth(1, self.column2)
        for i in range(len(self.song_list2)):
            self.set_button2(i + 1)
        

    def set_button2(self, index):
        # 设置行高
        self.ui.table_music2.setRowHeight(index, self.height)
        if(index):
            i = index - 1
            # 播放歌曲
            self.check_list[f'music2{index}'] = QtWidgets.QPushButton(self.music_list2[i])
            self.check_list[f'music2{index}'].setStyleSheet('QPushButton{border-image: url(img/rank/rank2/rank2_%d.jpg);font: bold 14pt "华文仿宋";background-color: rgb(246, 227, 178);}'% (index * 2 + 0))
            self.check_list[f'music2{index}'].clicked.connect(partial(self.broad, f'music2{index}', self.music_list2, self.song_list2))
            # btn.clicked.connect(lambda:self.comboxSelect('rrrrrrrrrrrr'))
            self.ui.table_music2.setCellWidget(index, 0, self.check_list[f'music2{index}'])
            # 歌手搜索
            self.check_list[f'song2{index}'] = QtWidgets.QPushButton(self.song_list2[i])
            self.check_list[f'song2{index}'].setStyleSheet('QPushButton{border-image: url(img/rank/rank2/rank2_%d.jpg);font: bold 14pt "华文仿宋";background-color: rgb(246, 227, 178);}' % (index * 2 + 1))
            self.check_list[f'song2{index}'].clicked.connect(partial(self.search_song2, f'song2{index}'))
            # btn.clicked.connect(lambda:self.comboxSelect('rrrrrrrrrrrr'))
            self.ui.table_music2.setCellWidget(index, 1, self.check_list[f'song2{index}'])
        else:
            data = ["歌曲", "歌手"]
            for i in range(len(data)):
                btn = QtWidgets.QPushButton(data[i])
                # 歌曲信息
                btn.setStyleSheet('QPushButton{border-image: url(img/rank/rank2/rank2_%d.jpg);font: bold 14pt "华文仿宋";background-color: rgb(246, 227, 178);color: rgb(255, 178, 7);}' % (index * 2 + i))
                # btn.clicked.connect(lambda:self.comboxSelect('rrrrrrrrrrrr'))
                self.ui.table_music2.setCellWidget(index, i, btn)
    def showMusicList3(self):
        self.row = len(self.song_list3) + 1
        # 设置列数
        self.ui.table_music3.setColumnCount(self.column)
        # 设置行数
        self.ui.table_music3.setRowCount(self.row)
        self.set_button3(0)
        # 隐藏网格线
        self.ui.table_music3.setShowGrid(False)
        # 隐藏表头
        self.ui.table_music3.verticalHeader().setVisible(False)
        self.ui.table_music3.horizontalHeader().setVisible(False)
        # 设置列宽
        self.ui.table_music3.setColumnWidth(0, self.column1)
        self.ui.table_music3.setColumnWidth(1, self.column2)
        for i in range(len(self.song_list3)):
            self.set_button3(i + 1)
        

    def set_button3(self, index):
        # 设置行高
        self.ui.table_music3.setRowHeight(index, self.height)
        if(index):
            i = index - 1
            # 播放歌曲
            self.check_list[f'music3{index}'] = QtWidgets.QPushButton(self.music_list3[i])
            self.check_list[f'music3{index}'].setStyleSheet('QPushButton{border-image: url(img/rank/rank3/rank3_%d.jpg);font: bold 14pt "华文仿宋";background-color: rgb(246, 227, 178);}'% (index * 2 + 0))
            self.check_list[f'music3{index}'].clicked.connect(partial(self.broad, f'music3{index}', self.music_list3, self.song_list3))
            # btn.clicked.connect(lambda:self.comboxSelect('rrrrrrrrrrrr'))
            self.ui.table_music3.setCellWidget(index, 0, self.check_list[f'music3{index}'])
            # 歌手搜索
            self.check_list[f'song3{index}'] = QtWidgets.QPushButton(self.song_list3[i])
            self.check_list[f'song3{index}'].setStyleSheet('QPushButton{border-image: url(img/rank/rank3/rank3_%d.jpg);font: bold 14pt "华文仿宋";background-color: rgb(246, 227, 178);}'% (index * 2 + 1))
            self.check_list[f'song3{index}'].clicked.connect(partial(self.search_song3, f'song3{index}'))
            # btn.clicked.connect(lambda:self.comboxSelect('rrrrrrrrrrrr'))
            self.ui.table_music3.setCellWidget(index, 1, self.check_list[f'song3{index}'])
        else:
            data = ["歌曲", "歌手"]
            for i in range(len(data)):
                btn = QtWidgets.QPushButton(data[i])
                # 歌曲信息
                btn.setStyleSheet('QPushButton{border-image: url(img/rank/rank3/rank3_%d.jpg);font: bold 14pt "华文仿宋";background-color: rgb(246, 227, 178);color: rgb(255, 178, 7);}'% (index * 2 + i))
                # btn.clicked.connect(lambda:self.comboxSelect('rrrrrrrrrrrr'))
                self.ui.table_music3.setCellWidget(index, i, btn)

    def showMusicList4(self):
        self.row = len(self.song_list4) + 1
        # 设置列数
        self.ui.table_music4.setColumnCount(self.column)
        # 设置行数
        self.ui.table_music4.setRowCount(self.row)
        self.set_button4(0)
        # 隐藏网格线
        self.ui.table_music4.setShowGrid(False)
        # 隐藏表头
        self.ui.table_music4.verticalHeader().setVisible(False)
        self.ui.table_music4.horizontalHeader().setVisible(False)
        # 设置列宽
        self.ui.table_music4.setColumnWidth(0, self.column1)
        self.ui.table_music4.setColumnWidth(1, self.column2)
        for i in range(len(self.song_list4)):
            self.set_button4(i + 1)
        

    def set_button4(self, index):
        # 设置行高
        self.ui.table_music4.setRowHeight(index, self.height)
        if(index):
            i = index - 1
            # 播放歌曲
            self.check_list[f'music4{index}'] = QtWidgets.QPushButton(self.music_list4[i])
            self.check_list[f'music4{index}'].setStyleSheet('QPushButton{border-image: url(img/rank/rank4/rank4_%d.jpg);font: bold 10pt "Segoe UI Emoji";background-color: rgb(246, 227, 178);}'% (index * 2 + 0))
            self.check_list[f'music4{index}'].clicked.connect(partial(self.broad, f'music4{index}', self.music_list4, self.song_list4))
            # btn.clicked.connect(lambda:self.comboxSelect('rrrrrrrrrrrr'))
            self.ui.table_music4.setCellWidget(index, 0, self.check_list[f'music4{index}'])
            # 歌手搜索
            self.check_list[f'song4{index}'] = QtWidgets.QPushButton(self.song_list4[i])
            self.check_list[f'song4{index}'].setStyleSheet('QPushButton{border-image: url(img/rank/rank4/rank4_%d.jpg);font: bold 10pt "Segoe UI Emoji";background-color: rgb(246, 227, 178);}'% (index * 2 + 1))
            self.check_list[f'song4{index}'].clicked.connect(partial(self.search_song4, f'song4{index}'))
            # btn.clicked.connect(lambda:self.comboxSelect('rrrrrrrrrrrr'))
            self.ui.table_music4.setCellWidget(index, 1, self.check_list[f'song4{index}'])
        else:
            data = ["歌曲", "歌手"]
            for i in range(len(data)):
                btn = QtWidgets.QPushButton(data[i])
                # 歌曲信息
                btn.setStyleSheet('QPushButton{border-image: url(img/rank/rank4/rank4_%d.jpg);font: bold 14pt "华文仿宋";background-color: rgb(246, 227, 178);color: rgb(255, 178, 7);}'% (index * 2 + i))
                # btn.clicked.connect(lambda:self.comboxSelect('rrrrrrrrrrrr'))
                self.ui.table_music4.setCellWidget(index, i, btn)
    def broad(self, index, music_list, song_list):
        self.music_list = music_list
        self.song_list = song_list
        idx = int(index[6:]) - 1
        get_music = self.music_list[idx].strip() + ' ' + self.song_list[idx].strip()
        from music.get_rank_music import Get_rank_music
        temp = Get_rank_music(get_music)
        data = temp.get_result()
        save_path = './temp/music'
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        music = save_path+ '/' + self.song_list[idx] + ' - ' + self.music_list[idx] + '.mp3'
        lrc = save_path+ '/' + self.song_list[idx] + ' - ' + self.music_list[idx] + '.lrc'
        
        if(self.down_music(data[5], music)):
            self.down_lrc(data[4], lrc)

            from .broadcast import Broadcast
            photo = 'temp/music_img/' +  self.song_list[idx].strip() + ' - ' + self.music_list[idx].strip() + '.jpg'
            self.get_img(data, photo)
            music = self.song_list[idx] + ' - ' + self.music_list[idx] + '.mp3'
            lrc = self.song_list[idx] + ' - ' + self.music_list[idx] + '.lrc'
            global main_win
            # 获取查询信息
            search_music = self.ui.edit_search.text().strip()
            # 实例化另外一个窗口
            main_win = Broadcast(self.inf, save_path, music, lrc, photo, 4, search_music)
            # 阻塞父窗口
            main_win.ui.setWindowModality(QtCore.Qt.ApplicationModal)
            # 显示新窗口
            main_win.ui.show()
            # 关闭自己
            self.ui.close()

    def like_broad(self, index, music_list, song_list):
        self.music_list = music_list
        self.song_list = song_list
        idx = int(index[6:])
        get_music = self.music_list[idx].strip() + ' ' + self.song_list[idx].strip()
        from music.get_rank_music import Get_rank_music
        temp = Get_rank_music(get_music)
        data = temp.get_result()
        save_path = './temp/music'
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        music = save_path+ '/' + self.song_list[idx] + ' - ' + self.music_list[idx] + '.mp3'
        lrc = save_path+ '/' + self.song_list[idx] + ' - ' + self.music_list[idx] + '.lrc'
        
        if(self.down_music(data[5], music)):
            self.down_lrc(data[4], lrc)

            from .broadcast import Broadcast
            photo = 'temp/music_img/' +  self.song_list[idx].strip() + ' - ' + self.music_list[idx].strip() + '.jpg'
            self.get_img(data, photo)
            music = self.song_list[idx] + ' - ' + self.music_list[idx] + '.mp3'
            lrc = self.song_list[idx] + ' - ' + self.music_list[idx] + '.lrc'
            global main_win
            # 获取查询信息
            search_music = self.ui.edit_search.text().strip()
            # 实例化另外一个窗口
            main_win = Broadcast(self.inf, save_path, music, lrc, photo, 4, search_music)
            # 阻塞父窗口
            main_win.ui.setWindowModality(QtCore.Qt.ApplicationModal)
            # 显示新窗口
            main_win.ui.show()
            # 关闭自己
            self.ui.close()
    
    def down_music(self, url, path):
        if not os.path.exists(path):
            try:
                content = requests.get(url).content
                with open(path, mode='wb') as f:
                    f.write(content)
                return 1
            except:
                QtWidgets.QMessageBox.warning(self.ui,'警告','无音源')
                return 0
        else:
            return 1
    
    def down_lrc(self, lrc, path):
        try:
            with open(path,encoding='utf-8',mode='w+') as f:
                f.write(lrc)
        except:
            print('写入失败')

    def get_img(self, data, photo_path):
        path = './temp/music_img'
        # img_path = path + '/' + data[2] + ' - ' + data[1] + '.jpg'
        if not os.path.exists(path):
            os.makedirs(path)
        import requests
        res = requests.get(data[0])
        with open(photo_path, 'wb') as f:
                f.write(res.content)


    def search_song1(self, index):
        idx = int(index[5:]) - 1
        global main_win
        # 获取查询信息
        music = self.song_list1[idx].strip()
        # 实例化另外一个窗口
        from .global_search import Global_search
        main_win = Global_search(music, self.inf)
        # 显示新窗口
        main_win.ui.show()
        # 关闭自己
        self.ui.close()
    def search_song2(self, index):
        idx = int(index[5:]) - 1
        global main_win
        # 获取查询信息
        music = self.song_list2[idx].strip()
        # 实例化另外一个窗口
        from .global_search import Global_search
        main_win = Global_search(music, self.inf)
        # 显示新窗口
        main_win.ui.show()
        # 关闭自己
        self.ui.close()
    def search_song3(self, index):
        idx = int(index[5:]) - 1
        global main_win
        # 获取查询信息
        music = self.song_list3[idx].strip()
        # 实例化另外一个窗口
        from .global_search import Global_search
        main_win = Global_search(music, self.inf)
        # 显示新窗口
        main_win.ui.show()
        # 关闭自己
        self.ui.close()
    def search_song4(self, index):
        idx = int(index[5:]) - 1
        global main_win
        # 获取查询信息
        music = self.song_list4[idx].strip()
        # 实例化另外一个窗口
        from .global_search import Global_search
        main_win = Global_search(music, self.inf)
        # 显示新窗口
        main_win.ui.show()
        # 关闭自己
        self.ui.close()
    def fetch(self, url):
        # 请求并下载网页
        res = re.get(url)
        if res.status_code != 200:
            res.raise_for_status()
        else:
            return res.text

    # 猜你喜欢
    def get_like(self):
        url = 'https://y.qq.com/n/ryqq/toplist/4'
        # 1. 请求入口页面
        selector = et.HTML(self.fetch(url))
        for i in range(self.music_number + 1):
            music = selector.xpath('//*[@id="app"]/div/div[2]/div[2]/div[3]/ul[2]/li[{}]/div/div[3]/span/a[2]/text()'.format(i+1))
            song = selector.xpath('//*[@id="app"]/div/div[2]/div[2]/div[3]/ul[2]/li[{}]/div/div[4]/a/text()'.format(i+1))
            self.like_music_list.extend(music)
            if(len(song) == 1):
                self.like_song_list.extend(song)
            else:
                temp = song[0]
                for i in range(1, len(song)):
                    temp += '/' + song[i]
                self.like_song_list.append(temp)

    # 热歌榜
    def get_rank1(self):
        url = 'https://y.qq.com/n/ryqq/toplist/26'
        # 1. 请求入口页面
        selector = et.HTML(self.fetch(url))
        for i in range(self.music_number):
            music = selector.xpath('//*[@id="app"]/div/div[2]/div[2]/div[3]/ul[2]/li[{}]/div/div[3]/span/a[2]/text()'.format(i+1))
            song = selector.xpath('//*[@id="app"]/div/div[2]/div[2]/div[3]/ul[2]/li[{}]/div/div[4]/a/text()'.format(i+1))
            self.music_list1.extend(music)
            if(len(song) == 1):
                self.song_list1.extend(song)
            else:
                temp = song[0]
                for i in range(1, len(song)):
                    temp += '/' + song[i]
                self.song_list1.append(temp)

    # 新歌榜
    def get_rank2(self):
        url = 'https://y.qq.com/n/ryqq/toplist/27'
        # 1. 请求入口页面
        selector = et.HTML(self.fetch(url))
        for i in range(self.music_number):
            music = selector.xpath('//*[@id="app"]/div/div[2]/div[2]/div[3]/ul[2]/li[{}]/div/div[3]/span/a[2]/text()'.format(i+1))
            song = selector.xpath('//*[@id="app"]/div/div[2]/div[2]/div[3]/ul[2]/li[{}]/div/div[4]/a/text()'.format(i+1))
            self.music_list2.extend(music)
            if(len(song) == 1):
                self.song_list2.extend(song)
            else:
                temp = song[0]
                for i in range(1, len(song)):
                    temp += '/' + song[i]
                self.song_list2.append(temp)

    # 内地榜
    def get_rank3(self):
        url = 'https://y.qq.com/n/ryqq/toplist/5'
        # 1. 请求入口页面
        selector = et.HTML(self.fetch(url))
        for i in range(self.music_number):
            music = selector.xpath('//*[@id="app"]/div/div[2]/div[2]/div[3]/ul[2]/li[{}]/div/div[3]/span/a[2]/text()'.format(i+1))
            song = selector.xpath('//*[@id="app"]/div/div[2]/div[2]/div[3]/ul[2]/li[{}]/div/div[4]/a/text()'.format(i+1))
            self.music_list3.extend(music)
            if(len(song) == 1):
                self.song_list3.extend(song)
            else:
                temp = song[0]
                for i in range(1, len(song)):
                    temp += '/' + song[i]
                self.song_list3.append(temp)

    # 欧美榜
    def get_rank4(self):
        url = 'https://y.qq.com/n/ryqq/toplist/3'
        # 1. 请求入口页面
        selector = et.HTML(self.fetch(url))
        for i in range(self.music_number):
            music = selector.xpath('//*[@id="app"]/div/div[2]/div[2]/div[3]/ul[2]/li[{}]/div/div[3]/span/a[2]/text()'.format(i+1))
            song = selector.xpath('//*[@id="app"]/div/div[2]/div[2]/div[3]/ul[2]/li[{}]/div/div[4]/a/text()'.format(i+1))
            self.music_list4.extend(music)
            if(len(song) == 1):
                self.song_list4.extend(song)
            else:
                temp = song[0]
                for i in range(1, len(song)):
                    temp += '/' + song[i]
                self.song_list4.append(temp)

            
    def logo(self):
        pass

    def login(self):
        global main_win
        if self.root == 'root':
            from .login import Login
            main_win = Login()
            # 阻塞父窗口
            main_win.ui.setWindowModality(QtCore.Qt.ApplicationModal)
            # 显示新窗口
            main_win.ui.show()
            #等待窗口关闭
            main_win.ui.exec_()
            from mysql.get_information import Information
            inf = Information()
            user = inf.get_user_log()
            try:
                self.inf = inf.get_user_inf(user[0])
                self.root = self.inf[0]
                self.ui.label_photo.setPixmap(QtGui.QPixmap(self.inf[1]))
                self.ui.label_name.setText(self.inf[2])
            except:
                pass
        else:
            from .user import User
            main_win = User(self.inf)
            # 阻塞父窗口
            main_win.ui.setWindowModality(QtCore.Qt.ApplicationModal)
            # 显示新窗口
            main_win.ui.show()
            #等待窗口关闭
            main_win.ui.exec_()
            from mysql.get_information import Information
            inf = Information()
            try:
                user = inf.get_user_log()
                self.inf = inf.get_user_inf(user[0])
                self.root = self.inf[0]
                self.ui.label_photo.setPixmap(QtGui.QPixmap(self.inf[1]))
                self.ui.label_name.setText(self.inf[2])
            except:
                from mysql.config import Opts
                opt = Opts()
                self.inf = opt.get_baseinf()
                self.root = self.inf[0]
                self.ui.label_photo.setPixmap(QtGui.QPixmap(self.inf[1]))
                self.ui.label_name.setText(self.inf[2])

    def set(self):
        global main_win
        if self.root == 'root':
            from .login import Login
            main_win = Login()
            # 阻塞父窗口
            main_win.ui.setWindowModality(QtCore.Qt.ApplicationModal)
            # 显示新窗口
            main_win.ui.show()
            #等待窗口关闭
            main_win.ui.exec_()
            from mysql.get_information import Information
            inf = Information()
            user = inf.get_user_log()
            try:
                self.inf = inf.get_user_inf(user[0])
                self.root = self.inf[0]
                self.ui.label_photo.setPixmap(QtGui.QPixmap(self.inf[1]))
                self.ui.label_name.setText(self.inf[2])
            except:
                pass
        else:
            # 实例化另外一个窗口
            from .set import Set
            main_win = Set(self.inf)
            # 阻塞父窗口
            main_win.ui.setWindowModality(QtCore.Qt.ApplicationModal)
            # 显示新窗口
            main_win.ui.show()
            #等待窗口关闭
            main_win.ui.exec_()
            from mysql.get_information import Information
            inf = Information()
            self.inf = inf.get_user_inf(self.root)
            self.ui.label_photo.setPixmap(QtGui.QPixmap(self.inf[1]))
            self.ui.label_name.setText(self.inf[2])

    def heart(self):
        global main_win
        if self.root == 'root':
            from .login import Login
            main_win = Login()
            # 阻塞父窗口
            main_win.ui.setWindowModality(QtCore.Qt.ApplicationModal)
            # 显示新窗口
            main_win.ui.show()
            #等待窗口关闭
            main_win.ui.exec_()
            from mysql.get_information import Information
            inf = Information()
            user = inf.get_user_log()
            try:
                self.inf = inf.get_user_inf(user[0])
                self.root = self.inf[0]
                self.ui.label_photo.setPixmap(QtGui.QPixmap(self.inf[1]))
                self.ui.label_name.setText(self.inf[2])
            except:
                pass
        else:
            # 获取查询信息
            music = self.ui.edit_search.text().strip()
            # 实例化另外一个窗口
            from .collection import Collection
            main_win = Collection(self.inf, music)
            # 显示新窗口
            main_win.ui.show()
            # 关闭自己
            self.ui.close()

    def local(self):
        global main_win
        if self.root == 'root':
            from .login import Login
            main_win = Login()
            # 阻塞父窗口
            main_win.ui.setWindowModality(QtCore.Qt.ApplicationModal)
            # 显示新窗口
            main_win.ui.show()
            #等待窗口关闭
            main_win.ui.exec_()
            from mysql.get_information import Information
            inf = Information()
            user = inf.get_user_log()
            try:
                self.inf = inf.get_user_inf(user[0])
                self.root = self.inf[0]
                self.ui.label_photo.setPixmap(QtGui.QPixmap(self.inf[1]))
                self.ui.label_name.setText(self.inf[2])
            except:
                pass
        else:
            # 获取查询信息
            music = self.ui.edit_search.text().strip()
            # 实例化另外一个窗口
            from .local_music import Local_music
            main_win = Local_music(self.inf, music)
            # 显示新窗口
            main_win.ui.show()
            # 关闭自己
            self.ui.close()

    def search(self):
        global main_win
        # 获取查询信息
        music = self.ui.edit_search.text().strip()
        # 实例化另外一个窗口
        from .global_search import Global_search
        print(self.inf)
        main_win = Global_search(music, self.inf)
        # 显示新窗口
        main_win.ui.show()
        # 关闭自己
        self.ui.close()

    def download(self):
        global main_win
        if self.root == 'root':
            from .login import Login
            main_win = Login()
            # 阻塞父窗口
            main_win.ui.setWindowModality(QtCore.Qt.ApplicationModal)
            # 显示新窗口
            main_win.ui.show()
            #等待窗口关闭
            main_win.ui.exec_()
            from mysql.get_information import Information
            inf = Information()
            user = inf.get_user_log()
            try:
                self.inf = inf.get_user_inf(user[0])
                self.root = self.inf[0]
                self.ui.label_photo.setPixmap(QtGui.QPixmap(self.inf[1]))
                self.ui.label_name.setText(self.inf[2])
            except:
                pass
        else:
            # 获取查询信息
            music = self.ui.edit_search.text().strip()
            # 实例化另外一个窗口
            from .download import Download
            main_win = Download(self.inf, music)
            # 显示新窗口
            main_win.ui.show()
            # 关闭自己
            self.ui.close()