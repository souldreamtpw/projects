'''
Author: souldream
Date: 2022-03-23 12:09:44
LastEditTime: 2022-05-06 02:15:36
LastEditors: souldream
Description: 
FilePath: \朵朵\main.py
可以输入预定的版权声明、个性签名、空行等
'''
from PyQt5 import uic, QtWidgets, QtCore
import sys
import pymysql

# from music_search.source import *
from qt import *
from mysql import *

# 数据库初始化
opt = Opts()
config = opt.get_config()
try:
    pymysql.connect(**config)
except:
    mysql = Create()
    # 创建数据库
    mysql.createDatabase()
    # 创建表
    mysql.createTable()

# 页面信息初始化
inf = Information()
user = inf.get_user_log()

if user:
    if user[0] == 'root':
        last_user_inf = opt.get_baseinf()
    else:
        last_user_inf = inf.get_user_inf(user[0])
else:
    last_user_inf = opt.get_baseinf()



# 四张榜单的坐标( x, y, width, height)
rank1 = [200, 497, 230, 372]
rank2 = [440, 497, 230, 372]
rank3 = [680, 497, 230, 372]
rank4 = [920, 497, 230, 372]
# 列宽
column = [128, 100]
row = 10

ranks = [rank1, rank2, rank3, rank4]
img_path = 'img/base/主界面.jpg'


rank = Home_rank_img(ranks, img_path, row, column)
rank.get_rank_img()
rank.get_small_img()

# 猜你喜欢的坐标( x, y, width, height)
like = [8, 497, 181, 372]

column = 181
row = 10

img_path = 'img/base/主界面.jpg'


rank = Home_like_img(like, img_path, row, column)
rank.get_rank_img()
rank.get_small_img()

# 歌词的坐标( x, y, width, height)
lrc = [620, 130, 520, 600]

column = 520
row = 12

img_path = 'img/base/X播放界面.jpg'


rank = Lrc_img(lrc, img_path, row, column)
rank.get_rank_img()
rank.get_small_img()

# 歌词的坐标( x, y, width, height)
lrc = [620, 130, 520, 600]

column = 520
row = 12

img_path = 'img/base/X播放界面2.jpg'


rank = Lrc_not_img(lrc, img_path, row, column)
rank.get_rank_img()
rank.get_small_img()

# 四张图片的坐标( x, y, width, height)
lrc = [100, 130, 400, 400]

img_path = 'img/base/X播放界面.jpg'


rank = Broad_img(lrc, img_path)
rank.get_rank_img()


# 保证运行界面与ui预览界面一致
QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
app = QtWidgets.QApplication(sys.argv)
window = Homepage(last_user_inf)
window.ui.show()
# 建立循环
sys.exit(app.exec_())
