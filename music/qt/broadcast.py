'''
Author: souldream
Date: 2022-04-10 14:34:47
LastEditTime: 2022-05-08 16:12:59
LastEditors: souldream
Description: 
FilePath: \朵朵\qt\broadcast.py
可以输入预定的版权声明、个性签名、空行等
'''
from PyQt5 import uic, QtWidgets, QtCore, QtGui
import configparser
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent


import sys
import re
import os
import time
import random
import shutil
import bisect

# 进度条样式
slider_css = '''
QSlider::groove:horizontal {
    border: 1px solid #4A708B;
    background: #C0C0C0;
    height: 5px;
    border-radius: 1px;
    padding-left:-1px;
    padding-right:-1px;
    }
    
    QSlider::sub-page:horizontal {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
        stop:0 #B1B1B1, stop:1 #c4c4c4);
    background: qlineargradient(x1: 0, y1: 0.2, x2: 1, y2: 1,
        stop: 0 #5DCCFF, stop: 1 #1874CD);
    border: 1px solid #4A708B;
    height: 10px;
    border-radius: 2px;
    }
    
    QSlider::add-page:horizontal {
    background: #575757;
    border: 0px solid #777;
    height: 10px;
    border-radius: 2px;
    }
    
    QSlider::handle:horizontal 
    {
        background: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, 
        stop:0.6 #45ADED, stop:0.778409 rgba(255, 255, 255, 255));
    
        width: 11px;
        margin-top: -3px;
        margin-bottom: -3px;
        border-radius: 5px;
    }
    
    QSlider::handle:horizontal:hover {
        background: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0.6 #2A8BDA, 
        stop:0.778409 rgba(255, 255, 255, 255));
    
        width: 11px;
        margin-top: -3px;
        margin-bottom: -3px;
        border-radius: 5px;
    }
    
    QSlider::sub-page:horizontal:disabled {
    background: #00009C;
    border-color: #999;
    }
    
    QSlider::add-page:horizontal:disabled {
    background: #eee;
    border-color: #999;
    }
    
    QSlider::handle:horizontal:disabled {
    background: #eee;
    border: 1px solid #aaa;
    border-radius: 4px;
    }

'''
# 声音样式
voice_css = '''
QSlider {
	background-color: rgba(22, 22, 22, 0.7);
	padding-top: 15px;
	padding-bottom: 15px;
	border-radius: 5px;
}
 
QSlider::add-page:vertical {
	background-color: #FF7826;
	width:5px;
	border-radius: 2px;
}
 
QSlider::sub-page:vertical {
	background-color: #7A7B79;
	width:5px;
	border-radius: 2px;
}
 
QSlider::groove:vertical {
	background:transparent;
	width:6px;
}
 
QSlider::handle:vertical {
	height: 14px;
	width: 14px;
	margin: 0px -4px 0px -4px;
	border-radius: 7px;
	background: white;
}

'''

# 重写鼠标事件
class ClickJumpSlider(QtWidgets.QSlider):
    def mousePressEvent(self, event):
        # 获取上面的拉动块位置
        option = QtWidgets.QStyleOptionSlider()
        self.initStyleOption(option)
        rect = self.style().subControlRect(
            QtWidgets.QStyle.CC_Slider, option, QtWidgets.QStyle.SC_SliderHandle, self)
        if rect.contains(event.pos()):
            # 如果鼠标点击的位置在滑块上则交给Qt自行处理
            super(ClickJumpSlider, self).mousePressEvent(event)
            return
        if self.orientation() == QtCore.Qt.Horizontal:
            # 横向，要考虑invertedAppearance是否反向显示的问题
            self.setValue(self.style().sliderValueFromPosition(
                self.minimum(), self.maximum(),
                event.x() if not self.invertedAppearance() else (self.width(
                ) - event.x()), self.width()))
        else:
            # 纵向
            self.setValue(self.style().sliderValueFromPosition(
                self.minimum(), self.maximum(),
                (self.height() - event.y()) if not self.invertedAppearance(
                ) else event.y(), self.height()))


class Lyric(object):
    def __init__(self, path):
        self.path = path

    def get_lrc(self, path):
        # 打开文件
        file = open(path, "r", encoding="utf-8")
        # 读取文件全部内容
        lyric = file.readlines()
        temp = 0
        for i in range(len(lyric)):
            lyric[i] = lyric[i].rstrip("\n")
        # 添加歌词
        for i in range(len(lyric)):
            if('[00:00.00]' in lyric[i]) or ('[00:00.000]' in lyric[i]):
                temp = i
            else:
                break

        return lyric[temp + 1:]

    def delete_lrc(self, lyric):
        # 删除空白段
        del_lrc = []
        for i in range(len(lyric)):
            if(lyric[i][1] == ''):
                del_lrc.append(i)
        del_lrc.reverse()
        for i in del_lrc:
            lyric.pop(i)

        del_lrc = []
        for i in range(len(lyric)):
            if(lyric[i][0] == ''):
                del_lrc.append(i)
        del_lrc.reverse()
        for i in del_lrc:
            lyric.pop(i)

        return lyric

    def analysis(self):
        # 将时间转化为毫秒级
        fd = self.get_lrc(self.path)
        l1 = []
        # 解析字符串
        for i in fd:
            tp = i[1:].split("]")
            for t in tp[:-1]:
                l1.append([t, tp[-1]])

        l1 = self.delete_lrc(l1)
        # 转换为毫秒数
        for i in l1:
            res = re.split(r'[/.:]', i[0])
            rs = []
            for j in res:
                if i[0] == '0':
                    rs.append(int(j[1:]))
                else:
                    rs.append(int(j))
            i[0] = rs[0] * 60 * 1000 + rs[1] * 1000 + rs[2]
        # 排序
        l1.sort(key=lambda ele: ele[0])
        return l1


class Broadcast(QtWidgets.QMainWindow):
    def __init__(self, user_inf, path, music, lrc, photo, mark, search_music):
        super().__init__()
        # 从文件中加载UI定义
        self.ui = uic.loadUi(r"ui\broadcast.ui")
        # 当前用户
        self.inf = user_inf
        self.root = self.inf[0]
        self.mark = mark

        # 搜索的音乐
        self.search_music = search_music

        # 设置图片填充方式
        # self.ui.label_logo.setScaledContents(True)
        self.ui.label_photo.setScaledContents(True)
        self.ui.label_photo2.setScaledContents(True)

        # 加载软件上一次关闭时的状态
        self.ui.label_photo.setPixmap(QtGui.QPixmap(self.inf[1]))

        if not os.path.exists(photo):
            self.ui.label_photo2.setPixmap(QtGui.QPixmap('img/broad/not_img.jpg'))
        else:
            self.ui.label_photo2.setPixmap(QtGui.QPixmap(photo))

        self.ui.label_name.setText(self.inf[2])

        self.ui.label_music.setText(music.replace('mp3', ''))
        self.ui.label_music.setStyleSheet("QLabel{color: rgb(246, 227, 178);font: 20pt '华文行楷';}")
        self.ui.label_music.setAlignment(QtCore.Qt.AlignCenter)

        # 音乐地址
        self.music_path = path
        # print(self.music_path)
        # 当前音乐
        self.music = music
        # 音乐列表
        self.music_list = self.get_music_list()
        # print(self.music_list)
        # 当前播放音乐
        self.play_id = self.music_list.index(music)
        # 音乐完整地址
        self.play_music_path = self.music_path + '/' + music
        self.play_lrc_path = path + '/' + lrc
        # 歌曲数量
        self.music_number = len(self.music_list)

        # 收藏地址
        self.user_path = 'temp/' + self.root
        # 下载地址
        self.down_path = './down/' + self.play_music_path.split('/')[-1]
        # 收藏地址
        self.heart_music_path = self.user_path + \
            '/' + self.play_music_path.split('/')[-1]

        self.player = QMediaPlayer()

        self.ui.btn_play.setStyleSheet(
            "QPushButton{border-image: url(img/broad/play.png)}")
        self.ui.btn_frount.setStyleSheet(
            "QPushButton{border-image: url(img/broad/prev.png)}")
        self.ui.btn_next.setStyleSheet(
            "QPushButton{border-image: url(img/broad/next.png)}")
        self.ui.btn_order.setStyleSheet(
            "QPushButton{border-image: url(img/broad/sequential.png)}")
        self.ui.label_start.setText('00:00')
        self.ui.label_end.setText('00:00')

        # 播放器状态 0为暂停
        self.state = 0
        # 播放模式 0表示顺序播放 1表示随机播放 2表示单曲循环
        self.playMode = 0

        # 计时器
        self.timer = QtCore.QTimer()
        self.timer.start(1000)
        self.timer.timeout.connect(self.mode)
        self.temp = 0

        # 进度条
        # 隐藏网格线
        self.ui.bar.setShowGrid(False)
        # 隐藏表头
        self.ui.bar.verticalHeader().setVisible(False)
        self.ui.bar.horizontalHeader().setVisible(False)
        # 设置列数
        self.ui.bar.setColumnCount(1)
        # 设置行数
        self.ui.bar.setRowCount(1)
        self.slider = ClickJumpSlider(QtCore.Qt.Horizontal)
        self.ui.bar.setCellWidget(0, 0, self.slider)
        self.ui.bar.setRowHeight(0, 8)
        self.ui.bar.setColumnWidth(0, 691)
        self.slider.setStyleSheet(slider_css)

        # 隐藏网格线
        self.ui.bar_voice.setShowGrid(False)
        # 隐藏表头
        self.ui.bar_voice.verticalHeader().setVisible(False)
        self.ui.bar_voice.horizontalHeader().setVisible(False)
        # 设置列数
        self.ui.bar_voice.setColumnCount(1)
        # 设置行数
        self.ui.bar_voice.setRowCount(1)
        self.voice = ClickJumpSlider(QtCore.Qt.Vertical)
        self.ui.bar_voice.setCellWidget(0, 0, self.voice)
        self.ui.bar_voice.setColumnWidth(0, 20)
        self.ui.bar_voice.setRowHeight(0, 100)
        self.voice.setStyleSheet(voice_css)

        # 设置进制滑动
        self.ui.table_lrc.setDisabled(True)

        # 设置初始音量
        self.voice.setValue(100)
        self.player.setVolume(self.voice.value())

        # 动态创建变量名
        self.label = locals()

        # 隐藏除关闭按钮的其他按钮
        # 隐藏菜单栏 QtCore.Qt.FramelessWindowHint
        self.ui.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.FramelessWindowHint)
        # 隐藏状态栏
        self.ui.statusBar().hide()

        # 给按钮绑定事件
        self.ui.btn_heart.clicked.connect(self.check)
        self.ui.btn_play.clicked.connect(self.play)
        self.ui.btn_frount.clicked.connect(self.frount)
        self.ui.btn_next.clicked.connect(self.next)
        self.ui.btn_order.clicked.connect(self.order)
        self.ui.btn_down.clicked.connect(self.down)
        self.slider.sliderMoved[int].connect(
            lambda: self.player.setPosition(self.slider.value()))
        self.slider.valueChanged.connect(self.changeValue)
        self.slider.valueChanged.connect(self.Volume)
        self.ui.btn_down.clicked.connect(self.down)
        self.ui.btn_set.clicked.connect(self.set)
        self.ui.btn_photo.clicked.connect(self.login)
        self.ui.btn_logo.clicked.connect(self.back)
        self.ui.btn_voice.clicked.connect(self.setvoice)
        self.ui.btn_close.clicked.connect(QtCore.QCoreApplication.quit)

        # 勾选已收藏
        self.judge_heart()
        # 勾选下载
        self.judge_down()
        # 判断是否存在歌词
        self.lrc_exists = self.judge_lrc()

        # 音量显示或隐藏
        self.ui.bar_voice.setVisible(False)

        # 音量按钮
        self.voice_state = 1
        # 歌词
        self.get_lrc()
        # 当前歌词位置：
        self.lrc_index = 0
        # 上一句歌词位置
        self.frount_lrc_index = 0
        # 开始播放
        self.play()

    def setvoice(self):
        # 设置音量
        if(self.voice_state):
            self.ui.bar_voice.setVisible(True)
            self.voice_state = 0
        else:
            self.ui.bar_voice.setVisible(False)
            self.voice_state = 1

    def back(self):
        # 确认返回页面
        if (self.mark == 0):
            self.heart()
        elif(self.mark == 1):
            self.download()
        elif(self.mark == 2):
            self.search()
        elif(self.mark == 3):
            self.local()
        elif(self.mark == 4):
            self.logo()
        else:
            self.logo()

    def search(self):
        self.player.stop()
        global main_win
        # 实例化另外一个窗口
        from .global_search import Global_search
        main_win = Global_search(self.search_music, self.inf)
        # 显示新窗口
        main_win.ui.show()
        # 关闭自己
        self.ui.close()

    def logo(self):
        self.player.stop()
        global main_win
        # 实例化另外一个窗口
        from .homepage import Homepage
        main_win = Homepage(self.inf)
        # 显示新窗口
        main_win.ui.show()
        # 关闭自己
        self.ui.close()

    def heart(self):
        self.player.stop()
        global main_win
        # 实例化另外一个窗口
        from .collection import Collection
        main_win = Collection(self.inf, self.search_music)
        # 显示新窗口
        main_win.ui.show()
        # 关闭自己
        self.ui.close()

    def local(self):
        self.player.stop()
        global main_win
        # 实例化另外一个窗口
        from .local_music import Local_music
        main_win = Local_music(self.inf, self.search_music)
        # 显示新窗口
        main_win.ui.show()
        # 关闭自己
        self.ui.close()

    def download(self):
        self.player.stop()
        global main_win
        # 实例化另外一个窗口
        from .download import Download
        main_win = Download(self.inf, self.search_music)
        # 显示新窗口
        main_win.ui.show()
        # 关闭自己
        self.ui.close()

    def set(self):
        global main_win
        if self.root == 'root':
            from .login import Login
            main_win = Login()
            # 阻塞父窗口
            main_win.ui.setWindowModality(QtCore.Qt.ApplicationModal)
            # 显示新窗口
            main_win.ui.show()
            # 等待窗口关闭
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
            # 等待窗口关闭
            main_win.ui.exec_()
            from mysql.get_information import Information
            inf = Information()
            self.inf = self.inf = inf.get_user_inf(self.root)
            self.ui.label_photo.setPixmap(QtGui.QPixmap(self.inf[1]))
            self.ui.label_name.setText(self.inf[2])

    def login(self):
        if self.root == 'root':
            from .login import Login
            main_win = Login()
            # 阻塞父窗口
            main_win.ui.setWindowModality(QtCore.Qt.ApplicationModal)
            # 显示新窗口
            main_win.ui.show()
            # 等待窗口关闭
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
            # 等待窗口关闭
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

    def judge_lrc(self):
        if(os.path.exists(self.play_lrc_path)):
            return 1
        else:
            return 0

    def get_music_list(self):
        music_list = []
        filenames = os.listdir(self.music_path)
        for filename in filenames:
            # 分解文件扩展名
            name, category = os.path.splitext(self.music_path+filename)
            if category == '.mp3':
                music_list.append(filename)
        return music_list

    def get_lrc_list(self):
        lrc_list = []
        filenames = os.listdir(self.music_path)
        for filename in filenames:
            # 分解文件扩展名
            name, category = os.path.splitext(self.music_path+filename)
            if category == '.lrc':
                lrc_list.append(filename)
        return lrc_list

    def get_lrc(self):
        # 歌词播放位置
        self.lrc_play_index = 5
        if(self.lrc_exists):
            # 获取歌词
            ly = Lyric(self.play_lrc_path)
            self.ls = ly.analysis()
            if(len(self.ls) == 0):
                self.lrc_exists = 0
                self.lrc_row = 1
            else:
                self.lrc_time = []
                for i in self.ls:
                    self.lrc_time.append(i[0])
                self.lrc_row = len(self.ls)
        else:
            self.lrc_row = 1

        self.lrc_column = 1
        # 设置列数
        self.ui.table_lrc.setColumnCount(self.lrc_column)
        # 设置行数
        if(self.lrc_row + self.lrc_play_index < 13):
            temp = 12
        else:
            temp = self.lrc_row + self.lrc_play_index
        
        self.ui.table_lrc.setRowCount(temp)
        # 隐藏网格线
        self.ui.table_lrc.setShowGrid(False)
        # 设置列宽
        self.ui.table_lrc.setColumnWidth(0, 520)
        # 隐藏表头
        self.ui.table_lrc.verticalHeader().setVisible(False)
        self.ui.table_lrc.horizontalHeader().setVisible(False)
        # 隐藏下方水平的进度条
        self.ui.table_lrc.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        # 隐藏竖直进度条
        self.ui.table_lrc.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)

        for i in range(self.lrc_play_index):
            self.ui.table_lrc.setRowHeight(i, 50)
            self.label[f'label{i}'] = QtWidgets.QLabel()
            self.label[f'label{i}'].setStyleSheet("QLabel{border-image: url(img/lrc/lrc_%d.jpg);}" % (i))
            self.ui.table_lrc.setCellWidget(i, 0, self.label[f'label{i}'])

        if(self.lrc_exists):
            for i in range(self.lrc_row):
                self.ui.table_lrc.setRowHeight(i + self.lrc_play_index, 50)
                self.label[f'label{i + self.lrc_play_index}'] = QtWidgets.QLabel()
                temp = i + 5 
                if(temp > 11):
                    temp = 11
                self.label[f'label{i + self.lrc_play_index}'].setStyleSheet("QLabel{border-image: url(img/lrc/lrc_%d.jpg); color: rgb(246, 227, 178);font: 18pt '华文行楷';}" % (temp))
                self.label[f'label{i + self.lrc_play_index}'].setText(self.ls[i][1])
                self.label[f'label{i + self.lrc_play_index}'].setAlignment(QtCore.Qt.AlignCenter)
                self.ui.table_lrc.setCellWidget(i + self.lrc_play_index, 0, self.label[f'label{i + self.lrc_play_index}'])

                item = QtWidgets.QTableWidgetItem()
                # item.setText(self.ls[i][1])
                # # 文本居中
                # item.setTextAlignment(
                #     QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                # item.setFont(QtGui.QFont('华文行楷', 18, QtGui.QFont.Black))
                # item.setForeground(QtGui.QBrush(QtGui.QColor(255, 0, 0)))
                self.ui.table_lrc.setItem(i + self.lrc_play_index, 0, item)
        else:
            # for i in range(self.lrc_play_index):
            #     self.ui.table_lrc.setRowHeight(i, 50)
            #     self.label[f'label{i}'] = QtWidgets.QLabel()
            #     self.label[f'label{i}'].setStyleSheet("QLabel{border-image: url(img/not_lrc/lrc_%d.jpg);}" % (i))
            #     self.ui.table_lrc.setCellWidget(i, 0, self.label[f'label{i}'])
            self.ui.table_lrc.setRowHeight(self.lrc_play_index, 50)

            self.label[f'label{i + self.lrc_play_index}'] = QtWidgets.QLabel()
            self.label[f'label{i + self.lrc_play_index}'].setStyleSheet("QLabel{border-image: url(img/not_lrc/lrc_5.jpg); color: rgb(246, 227, 178);font: 18pt '华文行楷';}")
            # self.label[f'label{i + self.lrc_play_index}'].setText('sssssssssssssssssssssssssssssssssss')
            # self.label[f'label{i + self.lrc_play_index}'].setAlignment(QtCore.Qt.AlignCenter)
            self.ui.table_lrc.setCellWidget(self.lrc_play_index, 0, self.label[f'label{i + self.lrc_play_index}'])

            for i in range(self.lrc_play_index + 1, 12):
                self.ui.table_lrc.setRowHeight(i, 50)
                label = QtWidgets.QLabel()
                label.setStyleSheet("QLabel{border-image: url(img/not_lrc/lrc_%d.jpg); color: rgb(246, 227, 178);font: 18pt '华文行楷';}" % (i))
                self.ui.table_lrc.setCellWidget(i, 0, label)

            # item = QtWidgets.QTableWidgetItem()
            # item.setText('sssssssssssssssssssssssssssssssssss')
            # item.setFont(QtGui.QFont('华文行楷', 18, QtGui.QFont.Black))
            # item.setForeground(QtGui.QBrush(QtGui.QColor(255, 0, 0)))
            # # 文本居中
            # item.setTextAlignment(QtCore.Qt.AlignHCenter |
            #                       QtCore.Qt.AlignVCenter)
            # self.ui.table_lrc.setItem(self.lrc_play_index, 0, item)

    def show_lrc(self):
        num = 20
        if(abs((self.slider.value() - self.temp) / 1000) > 1):
            self.lrc_index = bisect.bisect(
                self.lrc_time, self.slider.value()) - 1
            if(self.lrc_index == -1):
                self.lrc_index = 0
                # print(self.ls[self.lrc_index][1])
                # item = QtWidgets.QTableWidgetItem()
                # item.setText(self.ls[self.lrc_index][1])
                # # 文本居中
                # item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
                # self.ui.table_lrc.setItem(self.lrc_play_index, 0, item)
                # self.ui.table_lrc.item(self.frount_lrc_index + self.lrc_play_index,
                #                        0).setForeground(QtGui.QBrush(QtGui.QColor(0, 0, 0)))
                # self.label[f'label{self.frount_lrc_index}'].setStyleSheet("QLabel{border-image: url(img/lrc/lrc_0.jpg); color: rgb(246, 227, 178);font: 18pt '华文行楷';}")
                # 定位到指定行
                if(self.lrc_index > self.lrc_row + self.lrc_play_index - 12):
                    self.label[f'label{self.frount_lrc_index + self.lrc_play_index}'].setStyleSheet("QLabel{border-image: url(img/lrc/lrc_5.jpg); color: rgb(246, 227, 178);font: %dpt '华文行楷';}" % (num))
                    for i in range(12):
                        self.label[f'label{self.lrc_row + self.lrc_play_index + i - 12}'].setStyleSheet("QLabel{border-image: url(img/lrc/lrc_%d.jpg); color: rgb(246, 227, 178);font: %dpt '华文行楷';}" % (i, num))
                    self.ui.table_lrc.verticalScrollBar().setSliderPosition(self.lrc_index)
                    self.label[f'label{self.lrc_index + self.lrc_play_index}'].setStyleSheet("QLabel{border-image: url(img/lrc/lrc_%d.jpg); color: rgb(255, 255, 255);font: %dpt '华文行楷';}"% (self.lrc_index - self.lrc_row + 12), num)
                else:
                    self.label[f'label{self.frount_lrc_index + self.lrc_play_index}'].setStyleSheet("QLabel{border-image: url(img/lrc/lrc_5.jpg); color: rgb(246, 227, 178);font: %dpt '华文行楷';}" % (num))
                    self.ui.table_lrc.verticalScrollBar().setSliderPosition(self.lrc_index)
                    self.label[f'label{self.lrc_index + self.lrc_play_index}'].setStyleSheet("QLabel{border-image: url(img/lrc/lrc_5.jpg); color: rgb(255, 255, 255);font: %dpt '华文行楷';}" % (num))
                    for i in range(self.lrc_play_index - 1, -1, -1):
                        self.label[f'label{self.lrc_index + self.lrc_play_index - (self.lrc_play_index - i)}'].setStyleSheet("QLabel{border-image: url(img/lrc/lrc_%d.jpg); color:rgb(246, 227, 178);font: %dpt '华文行楷';}" % (i, num))
                    for i in range(self.lrc_play_index + 1, 12):
                            self.label[f'label{self.lrc_index + self.lrc_play_index + (i - 5)}'].setStyleSheet("QLabel{border-image: url(img/lrc/lrc_%d.jpg); color: rgb(246, 227, 178);font: %dpt '华文行楷';}" % (i, num))
                # self.label[f'label{self.lrc_play_index}'].setStyleSheet("QLabel{border-image: url(img/lrc/lrc_11.jpg); color: rgb(0, 0, 0);font: 18pt '华文行楷'}")
                # self.ui.table_lrc.item(self.lrc_index + self.lrc_play_index,
                #                        0).setForeground(QtGui.QBrush(QtGui.QColor(246, 227, 178)))
                self.frount_lrc_index = self.lrc_index
                self.lrc_index += 1
                if(self.lrc_index == self.lrc_row):
                    self.lrc_index = self.lrc_row - 1
        else:
            if(self.ls[self.lrc_index][0] < self.player.position()):
                    # print(self.ls[self.lrc_index][1])
                    # item = QtWidgets.QTableWidgetItem()
                    # item.setText(self.ls[self.lrc_index][1])
                    # # 文本居中
                    # item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
                    # self.ui.table_lrc.setItem(self.lrc_play_index, 0, item)
                    # self.ui.table_lrc.item(self.frount_lrc_index + self.lrc_play_index,
                    #                        0).setForeground(QtGui.QBrush(QtGui.QColor(0, 0, 0)))
                    # 定位到指定行
                    if(self.lrc_index > self.lrc_row + self.lrc_play_index - 12):
                        self.label[f'label{self.frount_lrc_index + self.lrc_play_index}'].setStyleSheet("QLabel{border-image: url(img/lrc/lrc_5.jpg); color: rgb(246, 227, 178);font: %dpt '华文行楷';}" % (num))
                        for i in range(12):
                            self.label[f'label{self.lrc_row + self.lrc_play_index + i - 12}'].setStyleSheet("QLabel{border-image: url(img/lrc/lrc_%d.jpg); color: rgb(246, 227, 178);font: %dpt '华文行楷';}" % (i, num))
                        self.ui.table_lrc.verticalScrollBar().setSliderPosition(self.lrc_index)
                        self.label[f'label{self.lrc_index + self.lrc_play_index}'].setStyleSheet("QLabel{border-image: url(img/lrc/lrc_%d.jpg); color: rgb(255, 255, 255);font: %dpt '华文行楷';}"% (self.lrc_index - self.lrc_row + 12, num))
                    else:
                        self.label[f'label{self.frount_lrc_index + self.lrc_play_index}'].setStyleSheet("QLabel{border-image: url(img/lrc/lrc_5.jpg); color: rgb(246, 227, 178);font: %dpt '华文行楷';}" % (num))
                        self.ui.table_lrc.verticalScrollBar().setSliderPosition(self.lrc_index)
                        self.label[f'label{self.lrc_index + self.lrc_play_index}'].setStyleSheet("QLabel{border-image: url(img/lrc/lrc_5.jpg); color: rgb(255, 255, 255);font: %dpt '华文行楷';}" %(num))
                        for i in range(self.lrc_play_index - 1, -1, -1):
                            self.label[f'label{self.lrc_index + self.lrc_play_index - (self.lrc_play_index - i)}'].setStyleSheet("QLabel{border-image: url(img/lrc/lrc_%d.jpg); color:rgb(246, 227, 178);font: %dpt '华文行楷';}" % (i, num))
                        for i in range(self.lrc_play_index + 1, 12):
                            self.label[f'label{self.lrc_index + self.lrc_play_index + (i - 5)}'].setStyleSheet("QLabel{border-image: url(img/lrc/lrc_%d.jpg); color: rgb(246, 227, 178);font: %dpt '华文行楷';}" % (i, num))
                    # self.ui.table_lrc.item(self.lrc_index + self.lrc_play_index, 0).setForeground(
                    #     QtGui.QBrush(QtGui.QColor(246, 227, 178)))
                    self.frount_lrc_index = self.lrc_index
                    self.lrc_index += 1
                    if(self.lrc_index == self.lrc_row):
                        self.lrc_index = self.lrc_row - 1

    def down(self):
        global main_win
        if self.root == 'root':
            from .login import Login
            main_win = Login()
            # 阻塞父窗口
            main_win.ui.setWindowModality(QtCore.Qt.ApplicationModal)
            # 显示新窗口
            main_win.ui.show()
            # 等待窗口关闭
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
                self.down()
        else:
            save_path = './down'
            if not os.path.exists(save_path):
                os.makedirs(save_path)
            if(os.path.exists(self.down_path)):
                pass
            else:
                shutil.copyfile(self.play_music_path, self.down_path)
                shutil.copyfile(self.play_music_path.replace(
                    'mp3', 'lrc'), self.down_path.replace('mp3', 'lrc'))
                self.ui.btn_down.setStyleSheet(
                    "QPushButton{border-image: url(img/base/down.png);}")

    def check(self):
        global main_win
        if self.root == 'root':
            from .login import Login
            main_win = Login()
            # 阻塞父窗口
            main_win.ui.setWindowModality(QtCore.Qt.ApplicationModal)
            # 显示新窗口
            main_win.ui.show()
            # 等待窗口关闭
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
                self.check()
        else:
            if not os.path.exists(self.user_path):
                os.makedirs(self.user_path)
            if (os.path.exists(self.heart_music_path)):
                os.remove(self.heart_music_path)
                os.remove(self.heart_music_path.replace('mp3', 'lrc'))
                self.ui.btn_heart.setStyleSheet(
                    "QPushButton{border-image: url(img/base/Wlike.png);}")
            else:
                shutil.copyfile(self.play_music_path, self.heart_music_path)
                shutil.copyfile(self.play_music_path.replace('mp3', 'lrc'), self.heart_music_path.replace('mp3', 'lrc'))
                self.ui.btn_heart.setStyleSheet(
                    "QPushButton{border-image: url(img/base/Rlike.png);}")

    def judge_down(self):
        if(os.path.exists(self.down_path)):
            self.ui.btn_down.setStyleSheet(
                "QPushButton{border-image: url(img/base/down.png);}")
        else:
            self.ui.btn_down.setStyleSheet(
                "QPushButton{border-image: url(img/base/download.png);}")

    def judge_heart(self):
        self.heart_music_path = self.user_path + \
            '/' + self.play_music_path.split('/')[-1]
        if(os.path.exists(self.heart_music_path)):
            self.ui.btn_heart.setStyleSheet(
                "QPushButton{border-image: url(img/base/Rlike.png);;}")
        else:
            self.ui.btn_heart.setStyleSheet(
                "QPushButton{border-image: url(img/base/Wlike.png);;}")

    def Volume(self):
        self.player.setVolume(self.voice.value())
        self.set_voice_img(self.voice.value())

    def set_voice_img(self, voice):
        if(voice > 0):
            self.ui.btn_voice.setStyleSheet(
                "QPushButton{border-image: url(img/broad/voice99.png)}")
        else:
            self.ui.btn_voice.setStyleSheet(
                "QPushButton{border-image: url(img/broad/voice0.png)}")

    def changeValue(self):
        if (abs((self.slider.value() - self.temp) / 1000) > 1):
            self.player.setPosition(self.slider.value())

    def order(self):
        self.playMode += 1
        if (self.playMode > 2):
            self.playMode = 0
            self.ui.btn_order.setStyleSheet(
                "QPushButton{border-image: url(img/broad/sequential.png)}")
        elif (self.playMode == 0):
            self.ui.btn_order.setStyleSheet(
                "QPushButton{border-image: url(img/broad/sequential.png)}")
        elif (self.playMode == 1):
            self.ui.btn_order.setStyleSheet(
                "QPushButton{border-image: url(img/broad/random.png)}")
        else:
            self.ui.btn_order.setStyleSheet(
                "QPushButton{border-image: url(img/broad/cycle.png)}")

    # 自动播放
    def mode(self):
        if self.state:
            self.slider.setMinimum(0)
            self.slider.setMaximum(self.player.duration())
            self.slider.setValue(self.slider.value() + 1000)
            if self.player.position() == self.player.duration():
                if self.playMode == 2:
                    self.player.play()
                    self.slider.setValue(0)
                    self.judge_heart()
                    self.judge_down()
                    self.get_lrc()
                    #self.lrc_index = 0
                else:
                    #self.lrc_index = 0
                    self.next()
        self.ui.label_start.setText(time.strftime(
            '%M:%S', time.localtime(self.player.position()/1000)))
        self.ui.label_start.setStyleSheet(
            'font: 10pt "等线"; color: rgb(255, 255, 255);')
        if(self.lrc_exists):
            self.show_lrc()
        self.temp = self.slider.value()
        self.ui.label_end.setText(time.strftime(
            '%M:%S', time.localtime(self.player.duration()/1000)))
        self.ui.label_end.setStyleSheet(
            'font: 10pt "等线"; color: rgb(255, 255, 255);')

    def f_getid(self):
        if (self.playMode == 0):
            self.play_id -= 1
        elif (self.playMode == 1):
            temp = random.randint(0, self.music_number - 1)
            while(temp == self.play_id):
                temp = random.randint(0, self.music_number - 1)
            self.play_id = temp
        else:
            self.play_id -= 1

    def n_getid(self):
        if (self.playMode == 0):
            self.play_id += 1
        elif (self.playMode == 1):
            temp = random.randint(0, self.music_number - 1)
            while(temp == self.play_id):
                temp = random.randint(0, self.music_number - 1)
            self.play_id = temp
        else:
            self.play_id += 1

    def frount(self):
        self.f_getid()
        self.slider.setValue(0)
        if (self.play_id < 0):
            self.play_id = self.music_number - 1
        self.play_music_path = self.music_path + \
            '/' + self.music_list[self.play_id]
        img_path = 'temp/music_img/' + self.music_list[self.play_id].replace('mp3', 'jpg')
        if not os.path.exists(img_path):
            self.ui.label_photo2.setPixmap(QtGui.QPixmap('img/broad/not_img.jpg'))
        else:
            self.ui.label_photo2.setPixmap(QtGui.QPixmap(img_path))
        # print('temp/music_img/' + self.music_list[self.play_id].replace('mp3', 'jpg'))
        self.ui.label_music.setText(self.music_list[self.play_id].replace('.mp3', ''))
        self.ui.label_music.setStyleSheet("QLabel{color: rgb(246, 227, 178);font: 20pt '华文行楷';}")
        self.ui.label_music.setAlignment(QtCore.Qt.AlignCenter)
        self.down_path = './down/' + self.music_list[self.play_id]
        self.play_lrc_path = os.path.splitext(self.play_music_path)[0] + '.lrc'
        self.lrc_exists = self.judge_lrc()
        self.frount_lrc_index = 0
        self.lrc_index = 0
        # 歌词
        self.get_lrc()
        self.state = 1
        self.player.setMedia(QMediaContent(QtCore.QUrl(self.play_music_path)))
        self.judge_heart()
        self.judge_down()
        self.ui.btn_play.setStyleSheet(
            "QPushButton{border-image: url(img/broad/pause.png)}")
        self.player.play()

    def next(self):
        self.n_getid()
        self.slider.setValue(0)
        if (self.play_id == self.music_number):
            self.play_id = 0
        self.play_music_path = self.music_path + \
            '/' + self.music_list[self.play_id]
        img_path = 'temp/music_img/' + self.music_list[self.play_id].replace('mp3', 'jpg')
        if not os.path.exists(img_path):
            self.ui.label_photo2.setPixmap(QtGui.QPixmap('img/broad/not_img.jpg'))
        else:
            self.ui.label_photo2.setPixmap(QtGui.QPixmap(img_path))
        self.ui.label_music.setText(self.music_list[self.play_id].replace('.mp3', ''))
        self.ui.label_music.setStyleSheet("QLabel{color: rgb(246, 227, 178);font: 20pt '华文行楷';}")
        self.ui.label_music.setAlignment(QtCore.Qt.AlignCenter)
        self.down_path = './down/' + self.music_list[self.play_id]
        self.play_lrc_path = os.path.splitext(self.play_music_path)[0] + '.lrc'
        self.frount_lrc_index = 0
        self.lrc_index = 0
        self.lrc_exists = self.judge_lrc()
        # 歌词
        self.get_lrc()
        self.state = 1
        self.player.setMedia(QMediaContent(QtCore.QUrl(self.play_music_path)))
        self.judge_heart()
        self.judge_down()
        self.ui.btn_play.setStyleSheet(
            "QPushButton{border-image: url(img/broad/pause.png)}")
        self.player.play()

    def play(self):
        if not self.player.isAudioAvailable():
            self.player.setMedia(QMediaContent(
                QtCore.QUrl(self.play_music_path)))
        if self.state:
            self.state = 0
            self.ui.btn_play.setStyleSheet(
                "QPushButton{border-image: url(img/broad/play.png)}")
            self.player.pause()
        else:
            self.state = 1
            self.ui.btn_play.setStyleSheet(
                "QPushButton{border-image: url(img/broad/pause.png)}")
            self.changeValue()
            self.player.play()


if __name__ == '__main__':
    # 保证运行界面与ui预览界面一致
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QtWidgets.QApplication(sys.argv)
    root = ['duoduo', 'temp/photo/root.png', '朵朵',
            '来交个朋友吧', '女', '2000-08-14', '21', '狮子座', '重庆市']
    photo = r'temp\music_img\张韶涵 - 破茧.jpg'.replace('\\', '/')
    path = 'result'
    music = '张韶涵 - 破茧.mp3'
    lrc = '张韶涵 - 破茧.lrc'
    window = Broadcast(root, path, music, lrc, photo)
    window.ui.show()
    # 建立循环
    sys.exit(app.exec_())
