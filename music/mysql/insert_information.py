'''
Author: souldream
Date: 2022-04-01 20:39:48
LastEditTime: 2022-04-08 19:28:14
LastEditors: souldream
Description: 
FilePath: \朵朵\mysql\insert_information.py
可以输入预定的版权声明、个性签名、空行等
'''
import pymysql
from .config import Opts

class Insert:
    def __init__(self):
        self.opt = Opts()
        self.config = self.opt.get_config()

    def insert_userdata(self, user_id, password):
        conn = pymysql.connect(**self.config)
        # 获取游标
        cursor = conn.cursor()
        sql = 'insert into user_data values("{}","{}")'.format(user_id, password)
        # 提交事务
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()

    def insert_userinf(self, user_id):
        conn = pymysql.connect(**self.config)
        # 获取游标
        cursor = conn.cursor()
        data = self.opt.get_baseinf()
        sql = 'insert into user_inf values("{}","{}","{}","{}","{}","{}","{}","{}","{}")'.format(user_id, data[1].replace('\\','/'), data[2], data[3], data[4], data[5], data[6], data[7], data[8])
        # 提交事务
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()

    def insert_userlog(self, user_id, datetime):
        conn = pymysql.connect(**self.config)
        # 获取游标
        cursor = conn.cursor()
        data = self.opt.get_baseinf()
        sql = 'insert into user_log values("{}","{}")'.format(user_id, datetime)
        # 提交事务
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()
    
    def insert_musicpath(self, user_id, musicpath):
        conn = pymysql.connect(**self.config)
        # 获取游标
        cursor = conn.cursor()
        data = self.opt.get_baseinf()
        sql = 'insert into music_path values("{}","{}")'.format(user_id, musicpath)
        # 提交事务
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()