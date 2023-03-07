'''
Author: souldream
Date: 2022-03-22 14:09:05
LastEditTime: 2022-03-23 22:52:12
LastEditors: souldream
Description: 
FilePath: \朵朵\music\api.py
可以输入预定的版权声明、个性签名、空行等
'''

import requests
from . import config
from .exceptions import RequestError, ResponseError, DataError


class MusicApi:
    # class property
    # 子类修改时使用deepcopy
    session = requests.Session()
    session.headers.update(config.get("fake_headers"))
    if config.get("proxies"):
        session.proxies.update(config.get("proxies"))
    session.headers.update({"referer": "http://www.google.com/"})

    @classmethod
    def request(cls, url, method="POST", data=None):
        if method == "GET":
            resp = cls.session.get(url, params=data, timeout=7)
        else:
            resp = cls.session.post(url, data=data, timeout=7)
        if resp.status_code != requests.codes.ok:
            raise RequestError(resp.text)
        if not resp.text:
            raise ResponseError("No response data.")
        return resp.json()

    @classmethod
    def requestInstance(cls, url, method="POST", data=None):
        if method == "GET":
            resp = cls.session.get(url, params=data, timeout=7)
        else:
            resp = cls.session.post(url, data=data, timeout=7)
        if resp.status_code != requests.codes.ok:
            raise RequestError(resp.text)
        if not resp.text:
            raise ResponseError("No response data.")
        return resp