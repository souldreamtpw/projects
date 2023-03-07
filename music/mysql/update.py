'''
Author: souldream
Date: 2022-03-26 20:36:51
LastEditTime: 2022-04-09 18:53:45
LastEditors: souldream
Description: 
可以输入预定的版权声明、个性签名、空行等
'''

import pymysql
from .config import Opts

class Update:
    def __init__(self):
        opt = Opts()
        self.config = opt.get_config()

    def update_userinf(self,data):
        conn = pymysql.connect(**self.config)
        # 获取游标
        cursor = conn.cursor()
        sql = '''update user_inf set photo = '{}', name = '{}', signature = '{}', sex = '{}', birthday = '{}', age = '{}', constellation = '{}', location = '{}' where user_id='{}' '''.format(data[1].replace('\\','/'), data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[0])
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()
    

    def update_musicpath(self, user_id, musicpath):
        conn = pymysql.connect(**self.config)
        # 获取游标
        cursor = conn.cursor()
        sql = '''update music_path set path = '{}' where user_id='{}' '''.format(musicpath, user_id)
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()