'''
Author: souldream
Date: 2022-03-26 16:05:09
LastEditTime: 2022-04-08 19:23:20
LastEditors: souldream
Description: 
FilePath: \朵朵\mysql\create_database.py
可以输入预定的版权声明、个性签名、空行等
'''
import pymysql

from .config import Opts


class Create:
    def __init__(self):
        opt = Opts()
        self.config, self.database  = opt.get_conn()

    def createDatabase(self):
        conn = pymysql.connect(**self.config)
        # 获取游标
        cursor = conn.cursor()
        # sql创建数据库
        sql = "create database if not exists " + self.database
        self.config['db'] = self.database
        cursor.execute(sql)
        # 关闭游标
        cursor.close()
        # 关闭数据库
        conn.close()


    def createTable(self):
        conn = pymysql.connect(**self.config)
        # 获取游标
        cursor = conn.cursor()
        sql = self.get_sql()
        for i in sql:
            cursor.execute(i)
        conn.commit()
        cursor.close()
        conn.close()

    def get_sql(self):
        # 最后登录用户
        user_log =   """CREATE TABLE user_log(
                    user_id VARCHAR(255) NOT NULL,
                    time DATETIME not null,
                    PRIMARY KEY(time))
                    """
        # 用户信息
        user_inf = """CREATE TABLE user_inf(
                    user_id VARCHAR(255) NOT NULL,
                    photo  varchar(255) not null,
                    name varchar(255) not null,
                    signature varchar(255) not null,
                    sex varchar(255) not null,
                    birthday varchar(255) not null,
                    age varchar(255) not null,
                    constellation varchar(255) not null,
                    location varchar(255) not null,
                    PRIMARY KEY(user_id))
                    """
        # 本地音乐地址
        music_path = """CREATE TABLE music_path(
                    user_id VARCHAR(255) NOT NULL,
                    path  varchar(255) not null,
                    PRIMARY KEY(user_id))
                    """
        # 用户账号信息
        user_data = """CREATE TABLE user_data(
                    user_id VARCHAR(255) NOT NULL,
                    password  varchar(255) not null,
                    PRIMARY KEY(user_id))
                    """
        table = [user_log, user_inf, music_path, user_data]
        return table