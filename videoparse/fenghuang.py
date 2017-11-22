# -*- coding: utf-8 -*-
# @Time    : 2017/11/16 20:23
# @Author  : Gavin

import re
import sys
import time
import requests
from contextlib import closing
from video.src.data import retry_get

reload(sys)
sys.setdefaultencoding('utf8')


# 除了VIP、推广、直通车、天天看、星期七、大放送之外都可以下载
class FengHuang(object):
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
                          ' Chrome/61.0.3163.100 Safari/537.36',
        }

    def fh_message(self, web_url):
        try:
            # 找出视频的Id(str)
            pattern = re.compile(r'http://v.ifeng.com/video_(.*?)\.shtml', re.S | re.I | re.M)
            video_id = pattern.findall(web_url)[0]
            # 构造请求视频原地址url
            req_url = 'http://tv.ifeng.com/h6/' + video_id + '/video.json?callback=callback&msg=' + video_id + '&rt=js'
            # 获取data数据(str)
            data = retry_get(req_url, self.headers)
            if "guid" in data:
                # 获取视频的uid
                pattern = re.compile(r'"guid":"(.*?)",', re.I | re.M | re.S)
            elif "vid" in data:
                # 获取视频的vid
                pattern = re.compile(r'"vid":"(.*?)",', re.I | re.M | re.S)
            cid = pattern.findall(data)[0]
            # 获取video_url(str)
            if "videoPlayUrl" in data:
                pattern = re.compile(r'"videoPlayUrl":"(.*?)",', re.I | re.M | re.S)
            elif "gqSrc" in data:
                pattern = re.compile(r'"gqSrc":"(.*?)",', re.I | re.M | re.S)
            else:
                pattern = re.compile(r'"bqSrc":"(.*?)",', re.I | re.M | re.S)
            video_url = pattern.findall(data)[0]
            # 获取视频的名称(str)
            if "title" in data:
                pattern = re.compile(r'"title":"(.*?)",', re.M | re.I | re.S)
            elif "name" in data:
                pattern = re.compile(r'"name":"(.*?)",', re.M | re.I | re.S)
            video_name = pattern.findall(data)[0]
            if '\u201c' in video_name:
                video_name = video_name.replace('\\u201c', '')
                video_name = video_name.replace('\\u201d', '')
            # 获取视频的上传时间(str)
            pattern = re.compile(r'"createdate":"(.*?)",', re.M | re.I | re.S)
            video_modify = pattern.findall(data)[0]
            # 获取视频的时长(str:s)
            pattern = re.compile(r'"duration":(.*?),', re.M | re.I | re.S)
            video_time = pattern.findall(data)[0]
            # 获取视频作者(str)
            if "mediaName" in data:
                pattern = re.compile(r'"mediaName":"(.*?)"', re.M | re.I | re.S)
            elif "columnName" in data:
                pattern = re.compile(r'"columnName":(.*?)', re.M | re.I | re.S)
            video_author = pattern.findall(data)[0]
            # 获取视频观看数(str)
            req_url = 'http://survey.news.ifeng.com/getaccumulator_weight.php?key=' + cid
            data = retry_get(req_url, self.headers)
            pattern = re.compile(r'{"browse":(.*?)}', re.M | re.I | re.S)
            video_view = pattern.findall(data)[0]
            # 视频点赞数(str)
            req_url = 'http://survey.news.ifeng.com/getaccumulator_ext.php?key=' + cid + 'ding'
            data = retry_get(req_url, self.headers)
            pattern = re.compile(r'{"browse":(.*?)}', re.M | re.I | re.S)
            video_support = pattern.findall(data)[0]
            # 视频不点赞数(str)
            req_url = 'http://survey.news.ifeng.com/getaccumulator_ext.php?key=' + cid + 'cai'
            data = retry_get(req_url, self.headers)
            pattern = re.compile(r'{"browse":(.*?)}', re.M | re.I | re.S)
            video_oppose = pattern.findall(data)[0]
            # 视频评论数(str)
            req_url = 'http://comment.ifeng.com/getv.php?job=3&format=js&docurl=' + cid
            data = retry_get(req_url, self.headers)
            count = 5
            while ("commentJsonVarStr" not in str(data)) and count > 0:
                data = retry_get(req_url, self.headers)
                time.sleep(10)
                count -= 1
            try:
                pattern = re.compile(r'var commentJsonVarStr___=(.*?);', re.M | re.I | re.S)
                video_comment = pattern.findall(data)[0]
            except Exception as e:
                video_comment = '0'
                print ('fenghuang.fh_message.video_comment: ' + str(e))
            # 获取视频path(str)
            # data = requests.get(web_url, headers=self.headers).content
            # pattern = re.compile(r'"categoryPath":"(.*?)",', re.M | re.I | re.S)
            # path = pattern.findall(data)[0]
            # 获取视频key(str)
            # pattern = re.compile(r'"skey":"(.*?)",', re.M | re.I | re.S)
            # key = pattern.findall(data)[0]
            # 获取视频大小(str)
            with closing(requests.get(video_url, stream=True)) as size:
                video_size = size.headers['content-length']
            return video_id, video_name, video_author, video_size, video_time, video_modify, video_view, video_oppose,\
                video_support, video_comment, video_url
        except Exception as e:
            print ('fenghuang.fh_message: ' + str(e))
