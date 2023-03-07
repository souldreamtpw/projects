'''
Author: souldream
Date: 2022-03-25 23:16:15
LastEditTime: 2022-04-26 11:03:38
LastEditors: souldream
Description: 
FilePath: \朵朵\qt\set.py
可以输入预定的版权声明、个性签名、空行等
'''
from PyQt5 import uic, QtWidgets, QtCore, QtGui
from mysql.update import Update
import datetime
import os
from PIL import Image

class Set:
    def __init__(self, user_inf):
        super().__init__()
        # 从文件中加载UI定义
        self.ui = uic.loadUi(r"ui\set.ui")
        self.ui.setWindowTitle('设置')
        self.inf = user_inf
        self.root = self.inf[0]
        self.city = ['河北省', '山西省', '辽宁省', '吉林省', '黑龙江省', '江苏省', '浙江省', '安徽省', '福建省', '江西省', '山东省', '河南省', '湖北省', '湖南省', '广东省', '海南省', '四川省', '贵州省', '云南省', '陕西省', '甘肃省', '青海省', '台湾省',
                                    '北京市', '天津市', '上海市', '重庆市', '内蒙古自治区', '广西壮族自治区', '宁夏回族自治区', '新疆维吾尔自治区', '西藏自治区']
        self.ui.cbox_city.addItems(self.city)
        self.ui.cbox_city.setEditable(True) # 需要先设置可编辑
        self.ui.cbox_city.lineEdit().setAlignment(QtCore.Qt.AlignCenter) # 再设置居中方式

        self.ui.edit_name.setText(self.inf[2])
        self.ui.label_photo.setPixmap(QtGui.QPixmap(self.inf[1]))
        self.ui.edit_signa.setText(self.inf[3])
        if (self.inf[4] == '男'):
            self.ui.cbox_sex.setCurrentIndex(0)
        else:
            self.ui.cbox_sex.setCurrentIndex(1)
        self.ui.cbox_sex.setEditable(True) # 需要先设置可编辑
        self.ui.cbox_sex.lineEdit().setAlignment(QtCore.Qt.AlignCenter) # 再设置居中方式

        self.ui.dateEdit.setDisplayFormat('yyyy-MM-dd')
        # 设置日历控件允许弹出
        self.ui.dateEdit.setCalendarPopup(True)
        self.ui.dateEdit.dateChanged.connect(self.onDateChanged)

        time = self.inf[5].split('-')
        year = int(time[0])
        month = int(time[1])
        day = int(time[2])
        self.ui.dateEdit.setDate(QtCore.QDate(year, month, day))

        self.ui.label_age.setText(str(self.get_age(year, month, day)))
        self.zodiac(month, day)

        self.ui.label_zod.setText(self.zodiac(month, day))

        idx = self.city.index(self.inf[8])
        self.ui.cbox_city.setCurrentIndex(idx)

        # 设置图片填充方式
        self.ui.label_photo.setScaledContents(True)

        op = QtWidgets.QGraphicsOpacityEffect()
        op.setOpacity(0)
        self.ui.btn_photo.setGraphicsEffect(op)

        
        op = QtWidgets.QGraphicsOpacityEffect()
        op.setOpacity(0)
        self.ui.btn_cancel.setGraphicsEffect(op)

        op = QtWidgets.QGraphicsOpacityEffect()
        op.setOpacity(0)
        self.ui.btn_ok.setGraphicsEffect(op)

        # 给按钮绑定事件
        self.ui.btn_cancel.clicked.connect(self.cancle)
        self.ui.btn_ok.clicked.connect(self.ok)
        self.ui.btn_photo.clicked.connect(self.photo)

    def onDateChanged(self):
        time = self.ui.dateEdit.date().toString(QtCore.Qt.ISODate).split('-')
        year = int(time[0])
        month = int(time[1])
        day = int(time[2])
        self.ui.dateEdit.setDate(QtCore.QDate(year, month, day))
        self.ui.label_age.setText(str(self.get_age(year, month, day)))
        self.zodiac(month, day)
        self.ui.label_zod.setText(self.zodiac(month, day))

    def get_age(self, year, month, day):
        today = datetime.date.today()
        birthday = datetime.date(year, month, day)
        age = round((today - birthday).days/365, 7)
        return int(age)

    def zodiac(self, cmonth, cdate):
        # 星座判断列表
        sdate = [20, 19, 21, 20, 21, 22, 23, 23, 23, 24, 23, 22]
        # 星座表
        conts = ['摩羯座', '水瓶座', '双鱼座', '白羊座', '金牛座', '双子座',
                 '巨蟹座', '狮子座', '处女座', '天秤座', '天蝎座', '射手座', '摩羯座']
        # 星座表对应标志
        # signs=['♑','♒','♓','♈','♉','♊','♋','♌','♍','♎','♏','♐','♑']
        if int(cdate) < sdate[int(cmonth)-1]:
            # 如果日数据早于对应月列表中对应的日期
            return(conts[int(cmonth)-1])
        else:
            # 否则输出星座列表下一月对应的星座
            return(conts[int(cmonth)])

    def cancle(self):
        # 关闭自己
        self.ui.close()

    def ok(self):
        a = ['男', '女']
        if (self.ui.cbox_sex.currentText() not in a):
            QtWidgets.QMessageBox.warning(self.ui,'警告','请输入正确信息')
        elif(self.ui.cbox_city.currentText() not in self.city):
            QtWidgets.QMessageBox.warning(self.ui,'警告','请输入正确信息')
        else:
            up = Update()
            self.inf[2] = self.ui.edit_name.text()
            self.inf[3] = self.ui.edit_signa.toPlainText()
            self.inf[4] = self.ui.cbox_sex.currentText()

            self.inf[5] = self.ui.dateEdit.date().toString(QtCore.Qt.ISODate)
            self.inf[6] = self.ui.label_age.text()
            self.inf[7] = self.ui.label_zod.text()
            self.inf[8] = self.ui.cbox_city.currentText()
            # print(self.inf)
            up.update_userinf(self.inf)
            # 关闭自己
            self.ui.close()

    def photo(self):
        filepath = QtWidgets.QFileDialog.getOpenFileName(
            None, "Open", "", "*.jpg;;*.png;;All Files(*)")[0]
        if filepath:
            self.inf[1] = self.circle(filepath)
            self.ui.label_photo.setPixmap(QtGui.QPixmap(self.inf[1]))

    def circle(self, img_path):
        path_name = 'temp/photo'
        cir_file_name = self.root + '.png'
        cir_path = path_name + '/' + cir_file_name
        ima = Image.open(img_path).convert("RGBA")
        size = ima.size
        # 因为是要圆形，所以需要正方形的图片
        r2 = min(size[0], size[1])
        if size[0] != size[1]:
            ima = ima.resize((r2, r2), Image.ANTIALIAS)
        # 最后生成圆的半径
        r3 = int(r2/2)
        imb = Image.new('RGBA', (r3*2, r3*2),(255,255,255,0))
        pima = ima.load() # 像素的访问对象
        pimb = imb.load()
        r = float(r2/2) #圆心横坐标

        for i in range(r2):
            for j in range(r2):
                lx = abs(i-r) #到圆心距离的横坐标
                ly = abs(j-r)#到圆心距离的纵坐标
                l = (pow(lx,2) + pow(ly,2))** 0.5 # 三角函数 半径
                if l < r3:
                    pimb[i-(r-r3),j-(r-r3)] = pima[i,j]

        imb.save(cir_path)
        return cir_path

