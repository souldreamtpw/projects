'''
Author: souldream
Date: 2022-04-01 18:23:07
LastEditTime: 2022-05-06 02:22:32
LastEditors: souldream
Description: 
FilePath: \朵朵\qt\register.py
可以输入预定的版权声明、个性签名、空行等
'''

from PyQt5 import uic, QtWidgets, QtCore,QtGui
from mysql.update import Update


class Register:
    def __init__(self):
        # 从文件中加载UI定义
        # 从 UI 定义中动态 创建一个相应的窗口对象
        self.ui = uic.loadUi(r"ui\register.ui")
        self.ui.setWindowTitle('注册')
        # 给按钮绑定事件
        self.ui.btn_register.clicked.connect(self.reg)

    def reg(self):
        global main_win
        user_id = self.ui.edit_username.text().strip()
        password = self.ui.edit_password.text().strip()

        from mysql.get_information import Information
        inf = Information()
        self.inf = inf.get_user_data(user_id)
        if(self.inf):
            QtWidgets.QMessageBox.warning(self.ui,'警告','该用户名已存在')
        else:
            length = 0
            for i in user_id:
                if ('\u4e00' <= i <= '\u9fff'):
                    length += 2
                else:
                    length += 1
            # 判断账号密码是否合法
            if (length > 20 or length < 6):
                QtWidgets.QMessageBox.warning(self.ui,'警告','请输入合法的用户名')
            elif (len(password) > 20 or len(password) < 6):
                QtWidgets.QMessageBox.warning(self.ui,'警告','请输入合法的密码')
            else:
                from mysql.insert_information import Insert
                input = Insert()
                input.insert_userdata(user_id, password)
                input.insert_userinf(user_id)
                input.insert_musicpath(user_id, '')
                # global main_win
                # # 实例化另外一个窗口
                # from .login import Login
                # main_win = Login()
                # # 阻塞父窗口
                # main_win.ui.setWindowModality(QtCore.Qt.ApplicationModal)
                # # 显示新窗口
                # main_win.ui.show()
                # 关闭自己
                self.ui.close()
            
