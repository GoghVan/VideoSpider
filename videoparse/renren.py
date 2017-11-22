# -*- coding: utf-8 -*-
# @Time    : 2017/11/16 20:23
# @Author  : Gavin

import re
import sys
import json
from video.src.data import retry_post

reload(sys)
sys.setdefaultencoding('utf8')


class RenRen(object):
    def __init__(self):
        # 添加客户端版本信息
        self.header = {
            'clientVersion': '0.1.0',
            'clientType': 'web',
        }

    def rr_url(self, web_url):
        try:
            # 获取视频的ID
            video_id = re.search(r'[0-9]+', web_url).group()
            # 调用视频接口
            api_url = 'http://api.rr.tv/v3plus/video/getVideoPlayLinkByVideoId'
            # 发送请求获取数据
            data = {'videoId': video_id}
            req_js = retry_post(api_url, data, self.header)
            # 将JSON数据转换为Python数据
            req_py = json.loads(req_js)
            # 获取视频地址URL
            video_url = str(req_py["data"]["playLink"])
            return video_url
        except Exception as e:
            print ('renren.rr_url: ' + str(e))

    def rr_message(self, web_url):
        try:
            # 获取视频的ID
            video_id = re.search(r'[0-9]+', web_url).group()
            # 调用信息接口
            api_url = 'http://web.rr.tv/v3plus/video/detail'
            data = {'videoId': video_id}
            # 发送请求获取数据
            req_js = retry_post(api_url, data, self.header)
            # 将JSON转为Python
            req_py = json.loads(req_js)
            # 获取视频名称
            video_name = str(req_py["data"]["videoDetailView"]["title"])
            # 获取视频作者
            video_author = str(req_py["data"]["videoDetailView"]["author"]["nickName"])
            # 获取视频评论数
            video_comment = str(req_py["data"]["videoDetailView"]["commentCount"])
            # 获取视频点赞数
            video_support = str(req_py["data"]["videoDetailView"]["favCount"])
            # 获取视频时长
            video_time = str(req_py["data"]["videoDetailView"]["duration"])
            # 获取视频观看次数
            video_view = str(req_py["data"]["videoDetailView"]["viewCount"])
            # 视频大小
            video_size = str(req_py["data"]["videoDetailView"]["videoFileView"][1]["fileSize"])
            return video_id, video_name, video_author, video_size, video_time, video_view, video_support, video_comment
        except Exception as e:
            print ('renren.rr_message: ' + str(e))
