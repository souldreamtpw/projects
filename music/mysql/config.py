'''
Author: souldream
Date: 2022-03-26 17:30:44
LastEditTime: 2022-04-10 19:48:27
LastEditors: souldream
Description: 
FilePath: \朵朵\mysql\config.py
可以输入预定的版权声明、个性签名、空行等
'''


class Opts:
    def __init__(self):
        self.database = '朵朵'

        # 连接配置信息
        self.config = {
            'host': 'localhost',    # 服务器地址
            'port': 3306,           # 端口号
            'user': 'root',         # 用户名
            'passwd': '123456',     # 密码
            'charset': 'utf8'       # 连接编码
        }

    def get_baseinf(self):
        user = 'root'
        photo = r'temp\photo\root.png'
        name = '朵朵'
        signature = '来交个朋友吧'
        sex = '女'
        birthday = '2000-08-14'
        age = '21'
        constellation = '狮子座'
        location = '重庆市'

        return [user, photo, name, signature, sex, birthday, age, constellation, location]

    def get_conn(self):
        return self.config, self.database

    def get_config(self):
        self.config['db'] = self.database
        return self.config
