'''
Author: souldream
Date: 2022-03-26 19:08:47
LastEditTime: 2022-04-01 21:50:57
LastEditors: souldream
Description: 
FilePath: \朵朵\mysql\get_information.py
可以输入预定的版权声明、个性签名、空行等
'''
import pymysql
from .config import Opts

class Information:
    def __init__(self):
        opt = Opts()
        self.config = opt.get_config()

    def get_user_log(self):
        conn = pymysql.connect(**self.config)
        # 获取游标
        cursor = conn.cursor()
        sql = '''select * from user_log order by time DESC limit 1;'''
        cursor.execute(sql)
        try:
            inf = list(cursor.fetchall()[0])
        except:
            inf = []
        conn.commit()
        cursor.close()
        conn.close()
        return inf

    def get_user_inf(self, user_id):
        conn = pymysql.connect(**self.config)
        # 获取游标
        cursor = conn.cursor()
        sql = ''' select * from user_inf where user_id ='{}' '''.format(user_id)
        cursor.execute(sql)
        try:
            inf = list(cursor.fetchall()[0])
        except:
            inf = []
        conn.commit()
        cursor.close()
        conn.close()
        return inf

    def get_local_path(self, user_id):
        conn = pymysql.connect(**self.config)
        # 获取游标
        cursor = conn.cursor()
        sql = ''' select * from music_path where user_id ='{}' '''.format(user_id)
        cursor.execute(sql)
        try:
            inf = list(cursor.fetchall()[0])
        except:
            inf = []
        conn.commit()
        cursor.close()
        conn.close()
        return inf

    def get_user_data(self, user_id):
        conn = pymysql.connect(**self.config)
        # 获取游标
        cursor = conn.cursor()
        sql = ''' select * from user_data where user_id ='{}' '''.format(user_id)
        cursor.execute(sql)
        try:
            inf = list(cursor.fetchall()[0])
        except:
            inf = []
        conn.commit()
        cursor.close()
        conn.close()
        return inf