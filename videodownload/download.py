# -*- coding: utf-8 -*-
# @Time    : 2017/11/16 20:23
# @Author  : Gavin

import os
import time
import requests
from contextlib import closing
from video.src.timenow import TimeNow
from video.src.log import Log
from video.src.progressbar import ProgressBar


class DownloadVideo(object):

    def __init__(self, video_url, video_message, video_file):
        self.video_url = video_url
        self.video_message = video_message
        self.video_file = video_file
        self.path = 'F:/SoftProgram/Videos/'

    def video_download(self):
        # 视频下载
        try:
            with closing(requests.get(self.video_url, stream=True)) as response:
                chunk_size = 1024
                content_size = int(response.headers['content-length'])

                if '.mp4' in self.video_url:
                    file_f = self.path + self.video_file + '/' + self.video_message + '.mp4'
                elif '.flv' in self.video_url:
                    file_f = self.path + self.video_file + '/' + self.video_message + '.flv'
                else:
                    file_f = self.path + self.video_file + '/' + self.video_message + '.mp4'
                if 'souhu' in file_f and os.path.exists(file_f):
                    flag = 1
                else:
                    flag = 0
                if (os.path.exists(file_f) and os.path.getsize(file_f) == content_size or flag):
                    mess = TimeNow.get_time() + ' 注意 : [ ' + self.video_message + ' ] 文件或信息已存在，请注意查看！'
                    print (mess)
                    Log.log(mess)
                else:
                    progress = ProgressBar(time.time(), TimeNow.get_time(), self.video_message.encode('utf8'), total=content_size,
                                           unit="KB", chunk_size=chunk_size, run_status="正在下载", fin_status="下载完成")
                    with open(file_f, "wb") as f:
                        for data in response.iter_content(chunk_size=chunk_size):
                            f.write(data)
                            progress.refresh(count=len(data))
            return file_f
        except Exception as e:
            print ('download.video_download: ' + str(e))
