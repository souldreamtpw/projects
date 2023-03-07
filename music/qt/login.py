'''
Author: souldream
Date: 2022-04-01 15:52:21
LastEditTime: 2022-04-26 11:03:09
LastEditors: souldream
Description: 
FilePath: \朵朵\qt\login.py
可以输入预定的版权声明、个性签名、空行等
'''

from PyQt5 import uic, QtWidgets, QtCore,QtGui
from mysql.update import Update
import time

class Login:
    def __init__(self):
        super().__init__()
        # 从文件中加载UI定义
        self.ui = uic.loadUi(r"ui\login.ui")
        self.ui.setWindowTitle('登陆')
        # 给按钮绑定事件
        self.ui.btn_login.clicked.connect(self.log_in)
        self.ui.btn_register.clicked.connect(self.reg)

        # 给组件设置透明度
        # op = QtWidgets.QGraphicsOpacityEffect()
        # op.setOpacity(0)
        # self.ui.btn_login.setGraphicsEffect(op)

        op = QtWidgets.QGraphicsOpacityEffect()
        op.setOpacity(0)
        self.ui.btn_register.setGraphicsEffect(op)

        # op = QtWidgets.QGraphicsOpacityEffect()
        # op.setOpacity(0)
        # self.ui.edit_password.setGraphicsEffect(op)
        # self.ui.edit_password.setAutoFillBackground(True)

        # op = QtWidgets.QGraphicsOpacityEffect()
        # op.setOpacity(1)
        # self.ui.edit_username.setGraphicsEffect(op)


    def log_in(self):
        user_id = self.ui.edit_username.text().strip()
        password = self.ui.edit_password.text().strip()

        if(user_id == '' or password == ''):
            QtWidgets.QMessageBox.warning(self.ui,'警告','请输入正确登陆信息')
        else:
            from mysql.get_information import Information
            inf = Information()
            self.inf = inf.get_user_data(user_id)
            if(self.inf):
                if(self.inf[1] == password):
                    from mysql.insert_information import Insert
                    input = Insert()
                    datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
                    input.insert_userlog(user_id,datetime)
                    # 关闭自己
                    self.ui.close()
                else:
                    QtWidgets.QMessageBox.warning(self.ui,'警告','密码错误')
            else:
                QtWidgets.QMessageBox.warning(self.ui,'警告','该用户名不存在，请先注册')
                self.ui.edit_username.clear()
                self.ui.edit_password.clear()



    def reg(self):
        global main_win
        # 实例化另外一个窗口
        from .register import Register
        main_win = Register()
        # 阻塞父窗口
        main_win.ui.setWindowModality(QtCore.Qt.ApplicationModal)
        # 显示新窗口
        main_win.ui.show()
        #等待窗口关闭
        main_win.ui.exec_()
