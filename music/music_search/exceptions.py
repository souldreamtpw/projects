'''
Author: souldream
Date: 2022-03-22 14:23:25
LastEditTime: 2022-03-23 22:52:22
LastEditors: souldream
Description: 
FilePath: \朵朵\music\exceptions.py
可以输入预定的版权声明、个性签名、空行等
'''


class RequestError(RuntimeError):
    """ 请求时的状态码错误 """

    def __init__(self, *args, **kwargs):
        pass


class ResponseError(RuntimeError):
    """ 得到的response状态错误 """

    def __init__(self, *args, **kwargs):
        pass


class DataError(RuntimeError):
    """ 得到的data中没有预期的内容 """

    def __init__(self, *args, **kwargs):
        pass


class ParameterError(RuntimeError):
    """ 输入的参数错误 """

    def __init__(self, *args, **kwargs):
        pass
