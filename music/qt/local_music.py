'''
Author: souldream
Date: 2022-03-25 19:53:39
LastEditTime: 2022-05-06 02:43:41
LastEditors: souldream
Description: 
FilePath: \朵朵\qt\local_music.py
可以输入预定的版权声明、个性签名、空行等
'''
from functools import partial
from PyQt5 import uic, QtWidgets, QtCore, QtGui

from music_search.source import *
from mysql.update import Update

import os
import re
import shutil
import lxml.etree as et
import lxml
import requests


class Local_music:
    def __init__(self, user_inf, music):
        super().__init__()
        # 从文件中加载UI定义
        self.ui = uic.loadUi(r"ui\local_music.ui")
        self.inf = user_inf
        self.column = 5
        self.row = 0
        self.root = self.inf[0]

        # 动态创建变量名
        self.check_list = locals()
        # 收藏地址
        self.user_path = 'temp/' + self.root 

        # 加载logo
        # self.ui.label_logo.setPixmap(QtGui.QPixmap(r'img\base\logo.jpg'))

        # 获取歌曲名称并嵌入搜索栏
        self.music = music
        self.ui.edit_search.setText(self.music)

        # 隐藏除关闭按钮的其他按钮
        # 隐藏菜单栏 QtCore.Qt.FramelessWindowHint
        self.ui.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.FramelessWindowHint)
        # 隐藏状态栏
        self.ui.statusBar().hide()

        # 填充界面
        self.ui.table_result.setStyleSheet("QTableWidget{border-image: url(img/base/search_background.png)}")

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

        # 音乐信息
        self.cur_path = ''
        self.song_list = []
        self.music_list = []
        self.url_list = []

        # 给按钮绑定事件
        self.ui.btn_heart.clicked.connect(self.heart)
        self.ui.btn_local.clicked.connect(self.local)
        self.ui.btn_search.clicked.connect(self.search)
        self.ui.btn_input.clicked.connect(self.input)
        self.ui.btn_set.clicked.connect(self.set)
        self.ui.btn_photo.clicked.connect(self.login)
        self.ui.btn_logo.clicked.connect(self.logo)
        self.ui.btn_down.clicked.connect(self.download)

        self.ui.btn_web.clicked.connect(self.getmusic2)
        self.ui.btn_all.clicked.connect(self.broad_all)
        self.ui.btn_close.clicked.connect(QtCore.QCoreApplication.quit)

        # 展示初始化
        self.ui.table_result.clear()

        # 加载搜索框
        url = os.getcwd() + os.path.sep + "jquery\index.html"
        self.ui.webview.load(QtCore.QUrl.fromLocalFile(url))

        # 加载本地音乐
        self.get_local_path()

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
        res = requests.get(url)
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

    def get_local_path(self):
        from mysql.get_information import Information
        inf = Information()
        try:
            self.cur_path = inf.get_local_path(self.root)[1]
            self.showMusicList()
        except:
            pass

    def input(self):
        if self.root == 'root':
            QtWidgets.QMessageBox.warning(self.ui,'警告','请先登录')
        else:
            self.cur_path = QtWidgets.QFileDialog.getExistingDirectory(
                None, "选取音乐文件夹", './')
            if self.cur_path:
                up = Update()
                up.update_musicpath(self.root, self.cur_path)
                self.showMusicList()

    def delete(self, index):
        idx = int(index[6:]) - 1
        # down_path = './down/' +  self.song_list[idx].strip() + ' - ' + self.music_list[idx].strip() + '.mp3'
        music_path = self.cur_path + '/' + self.song_list[idx].strip() + ' - ' + self.music_list[idx].strip() + '.mp3'
        try:
            os.remove(music_path)
            os.remove(music_path.replace('mp3', 'lrc'))
        except:
            pass
            # os.remove(down_path)
            # os.remove(down_path.replace('mp3', 'lrc'))
        self.song_list = []
        self.music_list = []
        self.url_list = []
        self.showMusicList()

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

    def getmusic(self):
        for temp in os.listdir(self.cur_path):
            if(re.split('[.]+', temp)[1] == 'mp3'):
                self.url_list.append(self.cur_path + '/' + temp)
                self.song_list.append(re.split('[-]+', temp)[0])
                self.music_list.append(temp.split(' - ')[1].split('.')[0])
            else:
                pass
            # path = './down'
        # if(os.path.exists(path)):
        #     for temp in os.listdir(path):
        #         self.url_list.append(self.cur_path + '/' + temp)
        #         self.song_list.append(re.split('[-]+', temp)[0])
        #         self.music_list.append(re.split('[-.]+', temp)[-2])
        # else:
        #     pass
#################################################################################
#################################################################################
#################################################################################
    def showMusicList(self):
        self.getmusic()
        self.row = len(self.song_list) + 1
        # 设置列数
        self.ui.table_result.setColumnCount(self.column)
        # 设置行数
        self.ui.table_result.setRowCount(self.row)
        self.set_button(0)

        # 隐藏网格线
        self.ui.table_result.setShowGrid(False)
        # 隐藏表头
        self.ui.table_result.verticalHeader().setVisible(False)
        self.ui.table_result.horizontalHeader().setVisible(False)

        # 设置列宽
        self.ui.table_result.setColumnWidth(0, 40)
        self.ui.table_result.setColumnWidth(1, 40)
        self.ui.table_result.setColumnWidth(2, 40)
        self.ui.table_result.setColumnWidth(3, 410)
        self.ui.table_result.setColumnWidth(4, 410)

        for i in range(len(self.song_list)):
            self.set_button(i + 1)
    def set_button(self, index):
        # 设置行高
        self.ui.table_result.setRowHeight(index, 40)
        
            # music_path = './' + self.user_path + '/' +  self.song_list[i] + ' - ' + self.music_list[i] + '.mp3'
            # '''
            # 注:lambda变量的绑定是动态的,即绑定时,传递给槽的是变量,而不是当时变量的值.会导致绑定函数传参时输出的为最后一个参数
            # 使用partial进行传参
            # '''
            # self.check_list[f'check{i}']= QtWidgets.QCheckBox()
            # if(os.path.exists(music_path)):
            #     self.check_list[f'check{i}'].setChecked(True)
            # '''
            # 注:使用partial进行传参与使用lambda传参时语法不同
            # '''
            # self.check_list[f'check{i}'].stateChanged.connect(partial(self.check, f'check{i}'))
            # self.ui.table_result.setCellWidget(i, 0, self.check_list[f'check{i}'])
        if(index):
            # 收藏按钮
            i = index - 1
            self.check_list[f'heart{index}']= QtWidgets.QPushButton()
            music_path = './' + self.user_path + '/' +  self.song_list[i].strip() + ' - ' + self.music_list[i].strip() + '.mp3'
            if(os.path.exists(music_path)):
                self.check_list[f'heart{index}'].setStyleSheet("QPushButton{border-image: url(img/base/Rlike.png); background-color: rgb(246, 227, 178);}")
            else:
                self.check_list[f'heart{index}'].setStyleSheet("QPushButton{border-image: url(img/base/Wlike.png); background-color: rgb(246, 227, 178);}")


            self.check_list[f'heart{index}'].clicked.connect(partial(self.check, f'heart{index}'))
            self.ui.table_result.setCellWidget(index, 0, self.check_list[f'heart{index}'])


            # 下载按钮
            self.check_list[f'download{index}']= QtWidgets.QPushButton()
            # 已下载
            music_path = './down/' +  self.song_list[i].strip() + ' - ' + self.music_list[i].strip() + '.mp3'
            if(os.path.exists(music_path)):
                self.check_list[f'download{index}'].setStyleSheet("QPushButton{border-image: url(img/base/down.png); background-color: rgb(246, 227, 178);}")
            else:
                self.check_list[f'download{index}'].setStyleSheet("QPushButton{border-image: url(img/base/download.png); background-color: rgb(246, 227, 178);}")
            self.check_list[f'download{index}'].clicked.connect(partial(self.down, f'download{index}'))
            self.ui.table_result.setCellWidget(index, 1, self.check_list[f'download{index}'])

            # 删除按钮
            self.check_list[f'delete{index}']= QtWidgets.QPushButton()
            self.check_list[f'delete{index}'].setStyleSheet("QPushButton{border-image: url(img/base/delete.png); background-color: rgb(246, 227, 178);}")
            self.check_list[f'delete{index}'].clicked.connect(partial(self.delete, f'delete{index}'))
            self.ui.table_result.setCellWidget(index, 2, self.check_list[f'delete{index}'])

            # 播放歌曲
            self.check_list[f'music{index}'] = QtWidgets.QPushButton(self.music_list[i])
            self.check_list[f'music{index}'].setStyleSheet('QPushButton{border-image: url(img/base/search_background.png);font: 14pt "华文仿宋";background-color: rgb(246, 227, 178);}')
            self.check_list[f'music{index}'].clicked.connect(partial(self.broad, f'music{index}'))
            # btn.clicked.connect(lambda:self.comboxSelect('rrrrrrrrrrrr'))
            self.ui.table_result.setCellWidget(index, 3, self.check_list[f'music{index}'])

            # 歌手搜索
            self.check_list[f'song{index}'] = QtWidgets.QPushButton(self.song_list[i])
            self.check_list[f'song{index}'].setStyleSheet('QPushButton{border-image: url(img/base/search_background.png);font: 14pt "华文仿宋";background-color: rgb(246, 227, 178);}')
            self.check_list[f'song{index}'].clicked.connect(partial(self.search_song, f'song{index}'))
            # btn.clicked.connect(lambda:self.comboxSelect('rrrrrrrrrrrr'))
            self.ui.table_result.setCellWidget(index, 4, self.check_list[f'song{index}'])


        else:
            data = ["歌曲", "歌手"]
            heart = QtWidgets.QPushButton()
            heart.setStyleSheet("QPushButton{border-image: url(img/base/search_background.png);background-color: rgb(246, 227, 178);}")
            self.ui.table_result.setCellWidget(index, 0, heart)
            down = QtWidgets.QPushButton()
            down.setStyleSheet("QPushButton{border-image: url(img/base/search_background.png);background-color: rgb(246, 227, 178);}")
            self.ui.table_result.setCellWidget(index, 1, down)
            delete= QtWidgets.QPushButton()
            delete.setStyleSheet("QPushButton{border-image: url(img/base/search_background.png); background-color: rgb(246, 227, 178);}")
            self.ui.table_result.setCellWidget(index, 2, delete)
            for i in range(len(data)):
                btn = QtWidgets.QPushButton(data[i])
                # 歌曲信息
                btn.setStyleSheet('QPushButton{border-image: url(img/base/search_background.png);font: 20pt "华文仿宋";background-color: rgb(246, 227, 178);color: rgb(255, 178, 7);}')
                # btn.clicked.connect(lambda:self.comboxSelect('rrrrrrrrrrrr'))
                self.ui.table_result.setCellWidget(index, i+3, btn)
#################################################################################
#################################################################################
#################################################################################
    def broad(self, index):
        idx = int(index[5:]) - 1
        from .broadcast import Broadcast
        music = self.song_list[idx].strip() + ' - ' + self.music_list[idx].strip() + '.mp3'
        lrc = self.song_list[idx].strip() + ' - ' + self.music_list[idx].strip() + '.lrc'
        photo = 'temp/music_img/' +  self.song_list[idx].strip() + ' - ' + self.music_list[idx].strip() + '.jpg'
        global main_win
        # 获取查询信息
        search_music = self.ui.edit_search.text().strip()
        # 实例化另外一个窗口
        main_win = Broadcast(self.inf, self.cur_path, music, lrc, photo, 3, search_music)
        # 阻塞父窗口
        main_win.ui.setWindowModality(QtCore.Qt.ApplicationModal)
        # 显示新窗口
        main_win.ui.show()
        # 关闭自己
        self.ui.close()
    def broad_all(self):
        idx = 0
        from .broadcast import Broadcast
        music = self.song_list[idx].strip() + ' - ' + self.music_list[idx].strip() + '.mp3'
        lrc = self.song_list[idx].strip() + ' - ' + self.music_list[idx].strip() + '.lrc'
        photo = 'temp/music_img/' +  self.song_list[idx].strip() + ' - ' + self.music_list[idx].strip() + '.jpg'
        global main_win
        # 获取查询信息
        search_music = self.ui.edit_search.text().strip()
        # 实例化另外一个窗口
        main_win = Broadcast(self.inf, self.cur_path, music, lrc, photo, 3, search_music)
        # 阻塞父窗口
        main_win.ui.setWindowModality(QtCore.Qt.ApplicationModal)
        # 显示新窗口
        main_win.ui.show()
        # 关闭自己
        self.ui.close()

    def search_song(self, index):
        idx = int(index[4:]) - 1
        global main_win
        # 获取查询信息
        music = self.song_list[idx].strip()
        # 实例化另外一个窗口
        from .global_search import Global_search
        main_win = Global_search(music, self.inf)
        # 显示新窗口
        main_win.ui.show()
        # 关闭自己
        self.ui.close()



    def down(self, index):
        idx = int(index[8:]) - 1
        save_path = './down'
        copy_path = save_path + '/' +  self.song_list[idx].strip() + ' - ' + self.music_list[idx].strip() + '.mp3'
        music_path = self.cur_path + '/' + self.song_list[idx].strip() + ' - ' + self.music_list[idx].strip() + '.mp3'
        # music_path_2 = 'down/' + self.song_list[idx].strip() + ' - ' + self.music_list[idx].strip() + '.mp3'
        # # 判断是否勾选
        # if self.check_list[index].isChecked():
        #     # 勾选
        #     shutil.copyfile(music_path, copy_path)
        # else:
        #     # 未勾选
        #     os.remove(copy_path)
        
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        if(os.path.exists(copy_path)):
            pass
        else:
            try:
                shutil.copyfile(music_path, copy_path)
                shutil.copyfile(music_path.replace('mp3', 'lrc'), copy_path.replace('mp3', 'lrc'))
                self.check_list[index].setStyleSheet("QPushButton{border-image: url(img/base/down.png); background-color: rgb(246, 227, 178);}")
            except:
                print(music_path)
                print('下载失败')
                # shutil.copyfile(music_path_2, copy_path)
                self.check_list[index].setStyleSheet("QPushButton{border-image: url(img/base/down.png); background-color: rgb(246, 227, 178);}")

    def check(self, index):
        idx = int(index[5:]) - 1
        copy_path = './' + self.user_path + '/' +  self.song_list[idx].strip() + ' - ' + self.music_list[idx].strip() + '.mp3'
        music_path = self.cur_path + '/' + self.song_list[idx].strip() + ' - ' + self.music_list[idx].strip() + '.mp3'
        # music_path_2 = 'down/' + self.song_list[idx].strip() + ' - ' + self.music_list[idx].strip() + '.mp3'
        # # 判断是否勾选
        # if self.check_list[index].isChecked():
        #     # 勾选
        #     shutil.copyfile(music_path, copy_path)
        # else:
        #     # 未勾选
        #     os.remove(copy_path)
        if not os.path.exists(self.user_path):
            os.makedirs(self.user_path)

        if(os.path.exists(copy_path)):
            try:
                os.remove(copy_path)
                os.remove(copy_path.replace('mp3', 'lrc'))
                self.check_list[index].setStyleSheet("QPushButton{border-image: url(img/base/Wlike.png); background-color: rgb(246, 227, 178);}")
            except:
                self.check_list[index].setStyleSheet("QPushButton{border-image: url(img/base/Wlike.png); background-color: rgb(246, 227, 178);}")
        else:
            try:
                shutil.copyfile(music_path.replace('mp3', 'lrc'), copy_path.replace('mp3', 'lrc'))
                shutil.copyfile(music_path, copy_path)
                self.check_list[index].setStyleSheet("QPushButton{border-image: url(img/base/Rlike.png); background-color: rgb(246, 227, 178);}")
            except:
                # shutil.copyfile(music_path_2, copy_path)
                self.check_list[index].setStyleSheet("QPushButton{border-image: url(img/base/Rlike.png); background-color: rgb(246, 227, 178);}")

    def set(self):
        if self.root == 'root':
            QtWidgets.QMessageBox.warning(self.ui,'警告','请先登录')
        else:
            global main_win
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
            self.inf = self.inf = inf.get_user_inf(self.root)
            self.ui.label_photo.setPixmap(QtGui.QPixmap(self.inf[1]))
            self.ui.label_name.setText(self.inf[2])
    def heart(self):
        global main_win
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
        pass

    def search(self):
        global main_win
        # 获取查询信息
        music = self.ui.edit_search.text().strip()
        # 实例化另外一个窗口
        from .global_search import Global_search
        main_win = Global_search(music, self.inf)
        # 显示新窗口
        main_win.ui.show()
        # 关闭自己
        self.ui.close()

    def download(self):
        global main_win
        # 获取查询信息
        music = self.ui.edit_search.text().strip()
        # 实例化另外一个窗口
        from .download import Download
        main_win = Download(self.inf, music)
        # 显示新窗口
        main_win.ui.show()
        # 关闭自己
        self.ui.close()

    def getmusic2(self):
        self.ui.webview.page().runJavaScript('submitFn();', self.loacl_search)

    def loacl_search(self, result):
        if (result == ''):
            self.song_list = []
            self.music_list = []
            self.url_list = []
            self.showMusicList()
        else:
            self.song_list2 = []
            self.music_list2 = []
            self.url_list2 = []
            for i in range(len(self.song_list)):
                if(result in self.song_list[i]):
                    self.song_list2.append(self.song_list[i])
                    self.music_list2.append(self.music_list[i])
                    self.url_list2.append(self.url_list[i])



            for i in range(len(self.song_list)):
                if(result in self.music_list[i]):
                    self.song_list2.append(self.song_list[i])
                    self.music_list2.append(self.music_list[i])
                    self.url_list2.append(self.url_list[i])
            self.showMusicList2()

    def showMusicList2(self):
        self.row = len(self.song_list2) + 1
        # 设置列数
        self.ui.table_result.setColumnCount(self.column)
        # 设置行数
        self.ui.table_result.setRowCount(self.row)
        self.set_button2(0)

        # 隐藏网格线
        self.ui.table_result.setShowGrid(False)
        # 隐藏表头
        self.ui.table_result.verticalHeader().setVisible(False)
        self.ui.table_result.horizontalHeader().setVisible(False)

        # 设置列宽
        self.ui.table_result.setColumnWidth(0, 40)
        self.ui.table_result.setColumnWidth(1, 40)
        self.ui.table_result.setColumnWidth(2, 40)
        self.ui.table_result.setColumnWidth(3, 410)
        self.ui.table_result.setColumnWidth(4, 410)

        for i in range(len(self.song_list2)):
            self.set_button2(i + 1)

    def set_button2(self, index):
        # 设置行高
        self.ui.table_result.setRowHeight(index, 40)
        
            # music_path = './' + self.user_path + '/' +  self.song_list[i] + ' - ' + self.music_list[i] + '.mp3'
            # '''
            # 注:lambda变量的绑定是动态的,即绑定时,传递给槽的是变量,而不是当时变量的值.会导致绑定函数传参时输出的为最后一个参数
            # 使用partial进行传参
            # '''
            # self.check_list[f'check{i}']= QtWidgets.QCheckBox()
            # if(os.path.exists(music_path)):
            #     self.check_list[f'check{i}'].setChecked(True)
            # '''
            # 注:使用partial进行传参与使用lambda传参时语法不同
            # '''
            # self.check_list[f'check{i}'].stateChanged.connect(partial(self.check, f'check{i}'))
            # self.ui.table_result.setCellWidget(i, 0, self.check_list[f'check{i}'])
        if(index):
            # 收藏按钮
            i = index - 1
            self.check_list[f'heart2{index}']= QtWidgets.QPushButton()
            music_path = './' + self.user_path + '/' +  self.song_list2[i].strip() + ' - ' + self.music_list2[i].strip() + '.mp3'
            if(os.path.exists(music_path)):
                self.check_list[f'heart2{index}'].setStyleSheet("QPushButton{border-image: url(img/base/Rlike.png); background-color: rgb(246, 227, 178);}")
            else:
                self.check_list[f'heart2{index}'].setStyleSheet("QPushButton{border-image: url(img/base/Wlike.png); background-color: rgb(246, 227, 178);}")


            self.check_list[f'heart2{index}'].clicked.connect(partial(self.check2, f'heart2{index}'))
            self.ui.table_result.setCellWidget(index, 0, self.check_list[f'heart2{index}'])


            # 下载按钮
            self.check_list[f'download2{index}']= QtWidgets.QPushButton()
            # 已下载
            music_path = './down/' +  self.song_list2[i].strip() + ' - ' + self.music_list2[i].strip() + '.mp3'
            if(os.path.exists(music_path)):
                self.check_list[f'download2{index}'].setStyleSheet("QPushButton{border-image: url(img/base/down.png); background-color: rgb(246, 227, 178);}")
            else:
                self.check_list[f'download2{index}'].setStyleSheet("QPushButton{border-image: url(img/base/download.png); background-color: rgb(246, 227, 178);}")
            self.check_list[f'download2{index}'].clicked.connect(partial(self.down2, f'download2{index}'))
            self.ui.table_result.setCellWidget(index, 1, self.check_list[f'download2{index}'])

            # 删除按钮
            self.check_list[f'delete2{index}']= QtWidgets.QPushButton()
            self.check_list[f'delete2{index}'].setStyleSheet("QPushButton{border-image: url(img/base/delete.png); background-color: rgb(246, 227, 178);}")
            self.check_list[f'delete2{index}'].clicked.connect(partial(self.delete2, f'delete2{index}'))
            self.ui.table_result.setCellWidget(index, 2, self.check_list[f'delete2{index}'])

            # 播放歌曲
            self.check_list[f'music2{index}'] = QtWidgets.QPushButton(self.music_list2[i])
            self.check_list[f'music2{index}'].setStyleSheet('QPushButton{border-image: url(img/base/search_background.png);font: 14pt "华文仿宋";background-color: rgb(246, 227, 178);}')
            self.check_list[f'music2{index}'].clicked.connect(partial(self.broad2, f'music2{index}'))
            # btn.clicked.connect(lambda:self.comboxSelect('rrrrrrrrrrrr'))
            self.ui.table_result.setCellWidget(index, 3, self.check_list[f'music2{index}'])

            # 歌手搜索
            self.check_list[f'song2{index}'] = QtWidgets.QPushButton(self.song_list2[i])
            self.check_list[f'song2{index}'].setStyleSheet('QPushButton{border-image: url(img/base/search_background.png);font: 14pt "华文仿宋";background-color: rgb(246, 227, 178);}')
            self.check_list[f'song2{index}'].clicked.connect(partial(self.search_song2, f'song2{index}'))
            # btn.clicked.connect(lambda:self.comboxSelect('rrrrrrrrrrrr'))
            self.ui.table_result.setCellWidget(index, 4, self.check_list[f'song2{index}'])
        else:
            data = ["歌曲", "歌手"]
            heart = QtWidgets.QPushButton()
            heart.setStyleSheet("QPushButton{border-image: url(img/base/search_background.png);background-color: rgb(246, 227, 178);}")
            self.ui.table_result.setCellWidget(index, 0, heart)
            down = QtWidgets.QPushButton()
            down.setStyleSheet("QPushButton{border-image: url(img/base/search_background.png);background-color: rgb(246, 227, 178);}")
            self.ui.table_result.setCellWidget(index, 1, down)
            delete= QtWidgets.QPushButton()
            delete.setStyleSheet("QPushButton{border-image: url(img/base/search_background.png); background-color: rgb(246, 227, 178);}")
            self.ui.table_result.setCellWidget(index, 2, delete)
            for i in range(len(data)):
                btn = QtWidgets.QPushButton(data[i])
                # 歌曲信息
                btn.setStyleSheet('QPushButton{border-image: url(img/base/search_background.png);font: 20pt "华文仿宋";background-color: rgb(246, 227, 178);color: rgb(255, 178, 7);}')
                # btn.clicked.connect(lambda:self.comboxSelect('rrrrrrrrrrrr'))
                self.ui.table_result.setCellWidget(index, i+3, btn)

    def check2(self, index):
        idx = int(index[6:]) - 1
        copy_path = './' + self.user_path + '/' +  self.song_list2[idx].strip() + ' - ' + self.music_list2[idx].strip() + '.mp3'
        music_path = self.cur_path + '/' + self.song_list2[idx].strip() + ' - ' + self.music_list2[idx].strip() + '.mp3'
        # music_path_2 = 'down/' + self.song_list[idx].strip() + ' - ' + self.music_list[idx].strip() + '.mp3'
        # # 判断是否勾选
        # if self.check_list[index].isChecked():
        #     # 勾选
        #     shutil.copyfile(music_path, copy_path)
        # else:
        #     # 未勾选
        #     os.remove(copy_path)
        if not os.path.exists(self.user_path):
            os.makedirs(self.user_path)
        if(os.path.exists(copy_path)):
            try:
                os.remove(copy_path)
                os.remove(copy_path.replace('mp3', 'lrc'))
                self.check_list[index].setStyleSheet("QPushButton{border-image: url(img/base/Wlike.png); background-color: rgb(246, 227, 178);}")
            except:
                self.check_list[index].setStyleSheet("QPushButton{border-image: url(img/base/Wlike.png); background-color: rgb(246, 227, 178);}")
        else:
            try:
                shutil.copyfile(music_path, copy_path)
                shutil.copyfile(music_path.replace('mp3', 'lrc'), copy_path.replace('mp3', 'lrc'))
                self.check_list[index].setStyleSheet("QPushButton{border-image: url(img/base/Rlike.png); background-color: rgb(246, 227, 178);}")
            except:
                # shutil.copyfile(music_path_2, copy_path)
                self.check_list[index].setStyleSheet("QPushButton{border-image: url(img/base/Rlike.png); background-color: rgb(246, 227, 178);}")

    def broad2(self, index):
        idx = int(index[6:]) - 1
        from .broadcast import Broadcast
        music = self.song_list2[idx].strip() + ' - ' + self.music_list2[idx].strip() + '.mp3'
        lrc = self.song_list2[idx].strip() + ' - ' + self.music_list2[idx].strip() + '.lrc'
        photo = 'temp/music_img/' +  self.song_list[idx].strip() + ' - ' + self.music_list[idx].strip() + '.jpg'
        global main_win
        # 获取查询信息
        search_music = self.ui.edit_search.text().strip()
        # 实例化另外一个窗口
        main_win = Broadcast(self.inf, self.cur_path, music, lrc, photo, 3, search_music)
        # 阻塞父窗口
        main_win.ui.setWindowModality(QtCore.Qt.ApplicationModal)
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

    def delete2(self, index):
        idx = int(index[7:]) - 1
        path = './down/' +  self.song_list[idx].strip() + ' - ' + self.music_list[idx].strip() + '.mp3'
        os.remove(path)
        os.remove(path.replace('mp3', 'lrc'))
        self.song_list2 = []
        self.music_list2 = []
        self.url_list2 = []
        self.showMusicList2()

    def down2(self, index):
        idx = int(index[9:]) - 1
        save_path = './down'
        copy_path = save_path + '/' +  self.song_list2[idx].strip() + ' - ' + self.music_list2[idx].strip() + '.mp3'
        music_path = self.cur_path + '/' + self.song_list2[idx].strip() + ' - ' + self.music_list2[idx].strip() + '.mp3'
        # music_path_2 = 'down/' + self.song_list[idx].strip() + ' - ' + self.music_list[idx].strip() + '.mp3'
        # # 判断是否勾选
        # if self.check_list[index].isChecked():
        #     # 勾选
        #     shutil.copyfile(music_path, copy_path)
        # else:
        #     # 未勾选
        #     os.remove(copy_path)
        
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        if(os.path.exists(copy_path)):
            pass
        else:
            try:
                shutil.copyfile(music_path, copy_path)
                shutil.copyfile(music_path.replace('mp3', 'lrc'), copy_path.replace('mp3', 'lrc'))
                self.check_list[index].setStyleSheet("QPushButton{border-image: url(img/base/down.png); background-color: rgb(246, 227, 178);}")
            except:
                # shutil.copyfile(music_path_2, copy_path)
                self.check_list[index].setStyleSheet("QPushButton{border-image: url(img/base/down.png); background-color: rgb(246, 227, 178);}")
