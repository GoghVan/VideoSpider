# -*- coding: utf-8 -*-
import sys
from video.src.log import *


class ProgressBar(object):
    # 进度显示条
    def __init__(self, time_now, title, count=0.0, run_status=None, fin_status=None, total=100.0, unit='',
                 sep='/', chunk_size=1.0):
        super(ProgressBar, self).__init__()
        self.info = "%s 视频 : [ %s ] %s %.2f %s %s %.2f %s"
        self.time_now = time_now
        self.title = title
        self.total = total
        self.count = count
        self.chunk_size = chunk_size
        self.status = run_status or ""
        self.fin_status = fin_status or " " * len(self.statue)
        self.unit = unit
        self.seq = sep

    def __get_info(self):
        # 【名称】状态 进度 单位 分割线 总数 单位
        _info = self.info % (self.time_now, self.title, self.status, self.count / self.chunk_size,
                             self.unit, self.seq, self.total / self.chunk_size, self.unit)
        return _info

    def refresh(self, count=1, status=None):
        self.count += count
        self.status = status or self.status
        sys.stdout.write('\r')
        sys.stdout.write(self.__get_info())
        sys.stdout.flush()
        if self.count >= self.total:
            self.status = status or self.fin_status
            sys.stdout.write('\r')
            sys.stdout.write(self.__get_info())
            sys.stdout.write('\n')
            Log.log(self.__get_info())