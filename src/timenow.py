# -*- coding: utf-8 -*-
import time


class TimeNow(object):
    def __init__(self):
        pass

    @staticmethod
    def get_time():
        # 获取当前时间
        time_now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        return time_now