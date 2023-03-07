'''
Author: souldream
Date: 2022-03-22 14:23:25
LastEditTime: 2022-03-24 13:41:21
LastEditors: souldream
Description: 
FilePath: \朵朵\music\source.py
可以输入预定的版权声明、个性签名、空行等
'''
import threading
import importlib
import traceback

from . import config
from .exceptions import *

class MusicSource:
    def __init__(self, keyword, sources_list):
        self.keyword = keyword
        self.sources_list = sources_list

    def search(self):
        sources_map = {
            "baidu": "baidu",
            "kugou": "kugou",
            "netease": "netease",
            "163": "netease",
            "qq": "qq",
            "migu": "migu",
        }
        thread_pool = []
        ret_songs_list = []
        ret_errors = []


        for source_key in self.sources_list:
            if not source_key in sources_map:
                raise ParameterError("Invalid music source.")
            t = threading.Thread(
                target=self.search_thread,
                args=(sources_map.get(source_key), self.keyword, ret_songs_list, ret_errors),
            )
            thread_pool.append(t)
            t.start()

        for t in thread_pool:
            t.join()


        # 对搜索结果排序和去重
        if not config.get("nomerge"):
            ret_songs_list.sort(
                key=lambda song: (song.singer, song.title, song.size), reverse=True
            )
            tmp_list = []
            for i in range(len(ret_songs_list)):
                # 如果名称、歌手都一致的话就去重，保留最大的文件
                if (
                    i > 0
                    and ret_songs_list[i].size <= ret_songs_list[i - 1].size
                    and ret_songs_list[i].title == ret_songs_list[i - 1].title
                    and ret_songs_list[i].singer == ret_songs_list[i - 1].singer
                ):
                    continue
                tmp_list.append(ret_songs_list[i])
            ret_songs_list = tmp_list

        return ret_songs_list

    def search_thread(self, source, keyword, ret_songs_list, ret_errors):
        # addon = importlib.import_module(".addons." + source, __package__)
        # ret_songs_list += addon.search(keyword)
        try:
            addon = importlib.import_module(".addons." + source, __package__)
            ret_songs_list += addon.search(keyword)
        except (RequestError, ResponseError, DataError) as e:
            ret_errors.append((source, e))
        except Exception as e:
            # 最后一起输出错误信息免得影响搜索结果列表排版
            err = traceback.format_exc() if config.get("verbose") else str(e)
            ret_errors.append((source, err))

    def single(self, url):
        sources_map = {
            # "baidu.com": "baidu",
            # "flac": "flac",
            # "kugou.com": "kugou",
            "163.com": "netease",
            # "qq.com": "qq",
            # "xiami.com": "xiami",
        }
        sources = [v for k, v in sources_map.items() if k in url]
        if not sources:
            raise ParameterError("Invalid url.")
        source = sources[0]
        try:
            addon = importlib.import_module(".addons." + source, __package__)
            song = addon.single(url)
            return song
        except (RequestError, ResponseError, DataError) as e:
            pass
        except Exception as e:
            # 最后一起输出错误信息免得影响搜索结果列表排版
            err = traceback.format_exc() if config.get("verbose") else str(e)
            self.logger.error(err)

    def playlist(self, url) -> list:
        sources_map = {
            # "baidu.com": "baidu",
            # "flac": "flac",
            "kugou.com": "kugou",
            "163.com": "netease",
            # "qq.com": "qq",
            # "xiami.com": "xiami",
        }
        sources = [v for k, v in sources_map.items() if k in url]
        if not sources:
            raise ParameterError("Invalid url.")
        source = sources[0]
        ret_songs_list = []
        try:
            addon = importlib.import_module(".addons." + source, __package__)
            ret_songs_list = addon.playlist(url)
        except (RequestError, ResponseError, DataError) as e:
            self.logger.error(e)
        except Exception as e:
            # 最后一起输出错误信息免得影响搜索结果列表排版
            err = traceback.format_exc() if config.get("verbose") else str(e)
            self.logger.error(err)

        return ret_songs_list


if __name__ == '__main__':
    # 初始化全局变量
    config.init()
    config.set("keyword", '孤勇者')

    test = MusicSource(config.get("keyword"), config.get("source").split())
    if config.get("keyword"):
        songs_list = test.search()
        # 遍历输出搜索列表
        for index, song in enumerate(songs_list):
            song.idx = index
            print(song.row)

    # 下载列表
    selected_list = [2]

    for idx in selected_list:
        songs_list[idx].download()