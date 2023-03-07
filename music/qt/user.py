'''
Author: souldream
Date: 2022-04-05 13:26:37
LastEditTime: 2022-04-26 11:03:46
LastEditors: souldream
Description: 
可以输入预定的版权声明、个性签名、空行等
'''



from PyQt5 import uic, QtWidgets, QtCore,QtGui
import time
import os
from PIL import Image

class User:
    def __init__(self, user_inf):
        super().__init__()
        # 从文件中加载UI定义
        self.ui = uic.loadUi(r"ui\user.ui")
        self.inf = user_inf
        self.root = self.inf[0]
        self.ui.setWindowTitle('用户信息')
        self.ui.label_user.setText(self.inf[2])
        self.ui.label_user.setStyleSheet('QLabel{font-size:20px; font-family:等线}') 
        #样式是个键值对，用；隔开
        self.ui.label_signa.setText(self.inf[3])
        self.ui.label_signa.setStyleSheet('QLabel{font-size:15px; font-family:等线}') 
        self.ui.label_sex.setText(self.inf[4])
        self.ui.label_sex.setStyleSheet('QLabel{font-size:15px; font-family:等线}') 
        self.ui.label_birth.setText(self.inf[5])
        self.ui.label_birth.setStyleSheet('QLabel{font-size:15px; font-family:等线}') 
        self.ui.label_age.setText(self.inf[6])
        self.ui.label_age.setStyleSheet('QLabel{font-size:15px; font-family:等线}') 
        self.ui.label_zod.setText(self.inf[7])
        self.ui.label_zod.setStyleSheet('QLabel{font-size:15px; font-family:等线}') 
        self.ui.label_loti.setText(self.inf[8])
        self.ui.label_loti.setStyleSheet('QLabel{font-size:15px; font-family:等线}') 
        self.ui.label_photo.setPixmap(QtGui.QPixmap(self.inf[1]))

        
        
        # 设置图片填充方式
        self.ui.label_photo.setScaledContents(True)

        # 给按钮绑定事件
        self.ui.btn_quit.clicked.connect(self.quit)
        self.ui.btn_change.clicked.connect(self.change)

    def quit(self):
        from mysql.config import Opts
        opt = Opts()
        self.inf = opt.get_baseinf()
        self.root = self.inf[0]
        from mysql.insert_information import Insert
        input = Insert()
        datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
        input.insert_userlog(self.root,datetime)
        # 关闭自己
        self.ui.close()

    def change(self):
        from .login import Login
        main_win = Login()
        # 阻塞父窗口
        main_win.ui.setWindowModality(QtCore.Qt.ApplicationModal)
        # 显示新窗口
        main_win.ui.show()
        #等待窗口关闭
        main_win.ui.exec_()
        # 关闭自己
        self.ui.close()