# -*- coding: utf-8 -*-
import os
from os.path import join, getsize


class FileSize(object):
    def __init__(self, file_url):
        self.file_url = file_url

    def file_size(self):
        # 实时获取文件的大小
        size = 0
        for root, dirs, files in os.walk(self.file_url):
            size = size + sum([getsize(join(root, name)) for name in files])
        return size