'''
Author: souldream
Date: 2022-03-24 22:50:53
LastEditTime: 2022-05-06 02:44:21
LastEditors: souldream
Description: 
FilePath: \朵朵\qt\global_search.py
可以输入预定的版权声明、个性签名、空行等
'''
from re import A
from PyQt5 import uic, QtWidgets, QtCore, QtGui
# from music_search.source import *
from music.search import *
from functools import partial
import os
import lxml.etree as et
import requests as re

# 分类专区 精选视频 人气歌手
main_win = None
# # 初始化全局变量
# config.init()


class Global_search:
    def __init__(self, music, user_inf):
        super().__init__()
        # 从文件中加载UI定义
        self.ui = uic.loadUi(r"ui\global_search.ui")
        self.inf = user_inf
        self.column = 5
        self.row = 100
        self.root = self.inf[0]

        self.page = 1

        # 收藏地址
        self.user_path = 'temp/' + self.root 

        # 加载logo
        # self.ui.label_logo.setPixmap(QtGui.QPixmap(r'img\base\logo.jpg'))

        # 歌曲信息
        self.songs_list = []

        # 动态创建变量名
        self.check_list = locals()

        # 填充界面
        self.ui.table_result.setStyleSheet("QTableWidget{border-image: url(img/base/search_background.png)}")

        # 加载软件上一次关闭时的状态
        self.ui.label_photo.setPixmap(QtGui.QPixmap(self.inf[1]))
        self.ui.label_name.setText(self.inf[2])
        self.ui.label_name.setStyleSheet('color: rgb(255, 255, 255);font: 75 18pt "等线";')

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

        # 获取歌曲名称并嵌入搜索栏
        self.music = music
        self.ui.edit_search.setText(self.music)

        # 隐藏除关闭按钮的其他按钮
        # 隐藏菜单栏 QtCore.Qt.FramelessWindowHint
        self.ui.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.FramelessWindowHint)
        # 隐藏状态栏
        self.ui.statusBar().hide()

        # 给按钮绑定事件
        self.ui.btn_heart.clicked.connect(self.heart)
        self.ui.btn_local.clicked.connect(self.local)
        self.ui.btn_search.clicked.connect(self.search)
        self.ui.btn_set.clicked.connect(self.set)
        self.ui.btn_photo.clicked.connect(self.login)
        self.ui.btn_logo.clicked.connect(self.logo)
        self.ui.btn_down.clicked.connect(self.download)
        self.ui.btn_close.clicked.connect(QtCore.QCoreApplication.quit)

        self.show_result()
        self.music_number = 9
        self.like_music_list = []
        self.like_song_list = []
        # 行高
        self.height = 37
        self.get_like()
        self.showLike()
    def down_music(self, url, path):
        try:
            content = requests.get(url).content
            with open(path, mode='wb') as f:
                f.write(content)
            return 1
        except:
            QtWidgets.QMessageBox.warning(self.ui,'警告','无音源')
            return 0
    
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
    def fetch(self, url):
        # 请求并下载网页
        res = re.get(url)
        if res.status_code != 200:
            res.raise_for_status()
        else:
            return res.text
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
            self.set_like_button(i)

    def set_like_button(self, index):
        # 设置行高
        self.ui.table_like.setRowHeight(index, self.height)
        i = index
        # 播放歌曲
        self.check_list[f'music5{index}'] = QtWidgets.QPushButton(self.like_music_list[i] + ' - ' +  self.like_song_list[i])
        self.check_list[f'music5{index}'].setStyleSheet('QPushButton{border-image: url(img/like/like_%d.jpg);font: bold 13pt "华文仿宋";color: rgb(255, 255, 255);}'% (index))
        self.check_list[f'music5{index}'].clicked.connect(partial(self.like_broad, f'music5{index}', self.like_music_list, self.like_song_list))
        # btn.clicked.connect(lambda:self.comboxSelect('rrrrrrrrrrrr'))
        self.ui.table_like.setCellWidget(index, 0, self.check_list[f'music5{index}'])

    def logo(self):
        global main_win
        # 实例化另外一个窗口
        from .homepage import Homepage
        main_win = Homepage(self.inf)
        # 显示新窗口
        main_win.ui.show()
        # 关闭自己
        self.ui.close()

    def login(self):
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
            if (self.root == 'root'):
                self.logo()

    def show_result(self):
        # config.set("keyword", self.music)
        # test = MusicSource(config.get("keyword"), config.get("source").split())
        # if config.get("keyword"):
        #     self.songs_list = test.search()

        temp = MusicSource(self.music, self.page)
        self.songs_list = temp.get_result()

        # 设置列数
        self.ui.table_result.setColumnCount(self.column)
        # 设置行数
        if (len(self.songs_list) < 100):
            self.ui.table_result.setRowCount(len(self.songs_list))
        else:
            self.ui.table_result.setRowCount(self.row)
        # # 设置表头
        # self.ui.table_result.setHorizontalHeaderLabels(
        #     ["","","歌曲", "歌手", "专辑", "时长", "大小", "来源"])
        #self.ui.table_result.setVerticalHeaderLabels(["第一行", "第二行"])

        # header = ["歌曲", "歌手", "专辑", "时长", "大小", "来源"]
        header = ["歌曲", "歌手", "来源"]
        self.set_button(0, header)

        # 隐藏网格线
        self.ui.table_result.setShowGrid(False)
        # 隐藏表头
        self.ui.table_result.verticalHeader().setVisible(False)
        self.ui.table_result.horizontalHeader().setVisible(False)


        # 设置列宽
        self.ui.table_result.setColumnWidth(0, 42)
        self.ui.table_result.setColumnWidth(1, 42)
        self.ui.table_result.setColumnWidth(2, 440)
        self.ui.table_result.setColumnWidth(3, 240)
        self.ui.table_result.setColumnWidth(4, 150)
        # self.ui.table_result.setColumnWidth(5, 80)
        # self.ui.table_result.setColumnWidth(6, 80)
        # self.ui.table_result.setColumnWidth(7, 80)



        # 设置不可更改
        #self.ui.table_result.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        self.search_music()

    def set_button(self, index, data):
        # 设置行高
        self.ui.table_result.setRowHeight(index, 40)

        # self.check_list[f'heart{index}']= QtWidgets.QCheckBox()
        # # 勾选已收藏
        # music_path = './' + self.user_path + '/' +  data[1] + ' - ' + data[0] + '.mp3'
        # if(os.path.exists(music_path)):
        #     self.check_list[f'heart{index}'].setChecked(True)
        #     self.check_list[f'heart{index}'].setStyleSheet("QCheckBox{border-image: url(img/base/Rlike.png); background-color: rgb(246, 227, 178);}")
        # else:
        #     self.check_list[f'heart{index}'].setStyleSheet("QCheckBox{border-image: url(img/base/White.png); background-color: rgb(246, 227, 178);}")
        # self.check_list[f'heart{index}'].stateChanged.connect(partial(self.check, f'heart{index}', music_path))
        # self.ui.table_result.setCellWidget(index, 0, self.check_list[f'heart{index}'])
        if(index):
            # 收藏按钮
            self.check_list[f'heart{index}']= QtWidgets.QPushButton()
            music_path = './' + self.user_path + '/' +  data[1].strip() + ' - ' + data[0].strip() + '.mp3'
            if(os.path.exists(music_path)):
                self.check_list[f'heart{index}'].setStyleSheet("QPushButton{border-image: url(img/base/Rlike.png); background-color: rgb(246, 227, 178);}")
            else:
                self.check_list[f'heart{index}'].setStyleSheet("QPushButton{border-image: url(img/base/Wlike.png); background-color: rgb(246, 227, 178);}")


            self.check_list[f'heart{index}'].clicked.connect(partial(self.check, f'heart{index}', music_path))
            self.ui.table_result.setCellWidget(index, 0, self.check_list[f'heart{index}'])


            # 下载按钮
            self.check_list[f'download{index}']= QtWidgets.QPushButton()
            # 已下载
            music_path = './down/' +  data[1].strip() + ' - ' + data[0].strip() + '.mp3'
            if(os.path.exists(music_path)):
                self.check_list[f'download{index}'].setStyleSheet("QPushButton{border-image: url(img/base/down.png); background-color: rgb(246, 227, 178);}")
            else:
                self.check_list[f'download{index}'].setStyleSheet("QPushButton{border-image: url(img/base/download.png); background-color: rgb(246, 227, 178);}")
            self.check_list[f'download{index}'].clicked.connect(partial(self.down, f'download{index}', music_path))
            self.ui.table_result.setCellWidget(index, 1, self.check_list[f'download{index}'])

            # 播放歌曲
            self.check_list[f'music{index}'] = QtWidgets.QPushButton(data[0])
            self.check_list[f'music{index}'].setStyleSheet('QPushButton{border-image: url(img/base/search_background.png);font: 14pt "华文仿宋";background-color: rgb(246, 227, 178);}')
            self.check_list[f'music{index}'].clicked.connect(partial(self.broad, f'music{index}'))
            # btn.clicked.connect(lambda:self.comboxSelect('rrrrrrrrrrrr'))
            self.ui.table_result.setCellWidget(index, 2, self.check_list[f'music{index}'])

            # 歌手搜索
            self.check_list[f'song{index}'] = QtWidgets.QPushButton(data[1])
            self.check_list[f'song{index}'].setStyleSheet('QPushButton{border-image: url(img/base/search_background.png);font: 14pt "华文仿宋";background-color: rgb(246, 227, 178);}')
            self.check_list[f'song{index}'].clicked.connect(partial(self.search_song, f'song{index}'))
            # btn.clicked.connect(lambda:self.comboxSelect('rrrrrrrrrrrr'))
            self.ui.table_result.setCellWidget(index, 3, self.check_list[f'song{index}'])

            for i in range(2, len(data)):
                btn = QtWidgets.QPushButton(data[i])
                # 歌曲信息
                btn.setStyleSheet('QPushButton{border-image: url(img/base/search_background.png);font: 14pt "华文仿宋";background-color: rgb(246, 227, 178);}')
                # btn.clicked.connect(lambda:self.comboxSelect('rrrrrrrrrrrr'))
                self.ui.table_result.setCellWidget(index, i+2, btn)
        else:
            heart = QtWidgets.QPushButton()
            heart.setStyleSheet("QPushButton{border-image: url(img/base/search_background.png);background-color: rgb(246, 227, 178);}")
            self.ui.table_result.setCellWidget(index, 0, heart)
            down = QtWidgets.QPushButton()
            down.setStyleSheet("QPushButton{border-image: url(img/base/search_background.png);background-color: rgb(246, 227, 178);}")
            self.ui.table_result.setCellWidget(index, 1, down)
            for i in range(len(data)):
                btn = QtWidgets.QPushButton(data[i])
                # 歌曲信息
                btn.setStyleSheet('QPushButton{border-image: url(img/base/search_background.png);font: 20pt "华文仿宋";background-color: rgb(246, 227, 178);color: rgb(255, 178, 7);}')
                # btn.clicked.connect(lambda:self.comboxSelect('rrrrrrrrrrrr'))
                self.ui.table_result.setCellWidget(index, i+2, btn)

    def broad(self, index):
        from .broadcast import Broadcast
        idx = int(index[5:]) - 1
        save_path = './temp/music'
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        music = save_path+ '/' + self.songs_list[idx][2] + ' - ' + self.songs_list[idx][1] + '.mp3'
        lrc = save_path+ '/' + self.songs_list[idx][2] + ' - ' + self.songs_list[idx][1] + '.lrc'
        self.down_music(self.songs_list[idx][5], music)
        self.down_lrc(self.songs_list[idx][4], lrc)
        self.get_img(idx)

        music = self.songs_list[idx][2] + ' - ' + self.songs_list[idx][1] + '.mp3'
        lrc = self.songs_list[idx][2] + ' - ' + self.songs_list[idx][1] + '.lrc'
        photo = 'temp/music_img/' +  self.songs_list[idx][2].strip() + ' - ' + self.songs_list[idx][1].strip() + '.jpg'
        global main_win
        # 获取查询信息
        search_music = self.ui.edit_search.text().strip()
        # 实例化另外一个窗口
        main_win = Broadcast(self.inf, save_path, music, lrc, photo, 2, search_music)
        # 阻塞父窗口
        main_win.ui.setWindowModality(QtCore.Qt.ApplicationModal)
        # 显示新窗口
        main_win.ui.show()
        # 关闭自己
        self.ui.close()

    def search_song(self, index):
        global main_win
        # 获取查询信息
        music = self.check_list[index].text()
        # 实例化另外一个窗口
        from .global_search import Global_search
        main_win = Global_search(music, self.inf)
        # 显示新窗口
        main_win.ui.show()
        # 关闭自己
        self.ui.close()

    def down(self, index, music_path):
        # # 点下去
        # self.check_list[index].setStyleSheet("QPushButton{border-image: url(img/base/download.png); background-color: rgb(204, 204, 204);}")
        # save_path = QtWidgets.QFileDialog.getExistingDirectory(
        #     None, "选取保存文件夹", './')
        # if save_path:
        #     # 初始化全局变量
        #     config.init()
        #     config.set("outdir", save_path)
        #     idx = int(index[8:])
        #     self.songs_list[idx].download()
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

            if(self.root == 'root'):
                pass
            else:
                self.down(index, music_path)
        else:
            save_path = './down'
            if not os.path.exists(save_path):
                os.makedirs(save_path)

            if(os.path.exists(music_path)):
                self.check_list[index].setStyleSheet("QPushButton{border-image: url(img/base/down.png); background-color: rgb(246, 227, 178);}")
            else:
                # # 初始化全局变量
                # config.init()
                # config.set("outdir", save_path)
                idx = int(index[8:]) - 1
                music_path = save_path+ '/' + self.songs_list[idx][2] + ' - ' + self.songs_list[idx][1] + '.mp3'
                lrc_path = save_path+ '/' + self.songs_list[idx][2] + ' - ' + self.songs_list[idx][1] + '.lrc'
                self.down_music(self.songs_list[idx][5], music_path)
                self.down_lrc(self.songs_list[idx][4], lrc_path)
                self.get_img(idx)
                # self.songs_list[idx].download()
                # 回到初始值
                self.check_list[index].setStyleSheet("QPushButton{border-image: url(img/base/down.png); background-color: rgb(246, 227, 178);}")


    def check(self, index, music_path):
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

            if(self.root == 'root'):
                pass
            else:
                self.check(index, music_path)
        else:
            if not os.path.exists(self.user_path):
                os.makedirs(self.user_path)
            # # 勾选
            # if self.check_list[index].isChecked():
            #     # 初始化全局变量
            #     config.init()
            #     config.set("outdir", self.user_path)
            #     idx = int(index[5:])
            #     self.songs_list[idx].download()
            # # 未勾选
            # else:
            #     try:
            #         os.remove(music_path)
            #     except:
            #         pass
            if(os.path.exists(music_path)):
                try:
                    os.remove(music_path)
                    os.remove(music_path.replace('mp3', 'lrc'))
                    self.check_list[index].setStyleSheet("QPushButton{border-image: url(img/base/Wlike.png); background-color: rgb(246, 227, 178);}")
                except:
                    self.check_list[index].setStyleSheet("QPushButton{border-image: url(img/base/Wlike.png); background-color: rgb(246, 227, 178);}")
            else:
                # 初始化全局变量
                # config.init()
                # config.set("outdir", self.user_path)
                # self.songs_list[idx].download()
                idx = int(index[5:]) - 1 

                music_path = self.user_path + '/' + self.songs_list[idx][2] + ' - ' + self.songs_list[idx][1] + '.mp3'
                lrc_path = self.user_path + '/' + self.songs_list[idx][2] + ' - ' + self.songs_list[idx][1] + '.lrc'
                self.down_music(self.songs_list[idx][5], music_path)
                self.down_lrc(self.songs_list[idx][4], lrc_path)
                self.get_img(idx)
                self.check_list[index].setStyleSheet("QPushButton{border-image: url(img/base/Rlike.png); background-color: rgb(246, 227, 178);}")

    def down_lrc(self, lrc, path):
        try:
            with open(path,encoding='utf-8',mode='w+') as f:
                f.write(lrc)
        except:
            print('写入失败')

    def down_music(self, url, path):
        try:
            content = requests.get(url).content
            with open(path, mode='wb') as f:
                f.write(content)
        except:
            print('下载失败')

    def search_music(self):
        for index in range(len(self.songs_list)):
            result = []
            # path = './temp/music_img'
            # if not os.path.exists(path):
            #     os.makedirs(path)
            # img_path = path + '/' + str(index) + '.png'
            # self.get_img(self.songs_list[index][0], img_path)
            
            result.extend([self.songs_list[index][1], self.songs_list[index][2], self.songs_list[index][3]])
            self.set_button(index + 1, result)
            if (index > self.row):
                    break

    def get_img(self, idx):
        path = './temp/music_img'
        img_path = path + '/' + self.songs_list[idx][2] + ' - ' + self.songs_list[idx][1] + '.jpg'
        if not os.path.exists(path):
            os.makedirs(path)
        import requests
        res = requests.get(self.songs_list[idx][0])
        with open(img_path, 'wb') as f:
                f.write(res.content)


    # def search_music(self):
    #         # 遍历输出搜索列表
    #         for index, song in enumerate(self.songs_list):
    #             song.idx = index
    #             result = []
    #             result.extend([song.row[1], song.row[2], song.row[5],
    #                           song.row[4], song.row[3], song.row[6]])
    #             self.set_button(index + 1, result)
    #             if (index > self.row):
    #                 break

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
        self.music = self.ui.edit_search.text().strip()
        self.show_result()

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
