# -*- coding: utf-8 -*-
# @Time    : 2017/11/16 20:23
# @Author  : Gavin


class Log(object):
    def __init__(self):
        pass

    # 日志写入文件
    @staticmethod
    def log(message):
        with open(r'D:\pythondata\log\log.txt', 'a+') as file_mess:
            file_mess.write('\n' + message)
