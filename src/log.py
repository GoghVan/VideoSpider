# -*- coding: utf-8 -*-


class Log(object):
    def __init__(self):
        pass

    # 日志写入文件
    @staticmethod
    def log(message):
        with open(r'F:\SoftProgram\log\log.txt', 'a+') as file_mess:
            file_mess.write('\n' + message)