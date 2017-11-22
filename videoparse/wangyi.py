# -*- coding: utf-8 -*-
# @Time    : 2017/11/16 20:23
# @Author  : Gavin

import re
import sys
import json
import urllib
import requests
from contextlib import closing
from video.src.data import retry_get

reload(sys)
sys.setdefaultencoding("utf-8")


# http://v.163.com/paike 、http://v.163.com/zixun/ 、 http://v.163.com/jishi/ 仅限这些地址下的分支视频
class WangYi(object):
    def __init__(self):
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/'
                          '61.0.3163.100 Safari/537.36',
        }

    def wy_url(self, web_url):
        try:
            video_url = ''
            # 从html中找到标准视频的真实下载地址（str)
            # html = requests.get(web_url, headers=header)
            # pattern = re.compile(r'source src="(.*?)"', re.S | re.M | re.I)
            # real_s_url = pattern.findall(html.text)[0].encode('utf8')

            # 构造url，访问服务器，获取xml数据
            html = requests.get(web_url, headers=self.header)
            pattern = re.compile(r'topicid : "(.*?)"', re.S | re.M | re.I)
            cid = pattern.findall(html.text)[0].encode('utf8')  # 获取topicid
            sc = [web_url][0]  # 将url进行list处理
            # 构造url
            req_url = 'http://xml.ws.126.net/video/' + sc[-7] + '/' + sc[-6] + '/' + cid + '_' + sc[-14: -5] + '.xml'  #
            # 获取xml数据
            xml_data = retry_get(req_url, self.header)
            pattern = re.compile(r'<flv>(.*?)</flv>', re.S | re.M | re.I)
            flv_url = pattern.findall(xml_data)
            flag1 = flag2 = 0
            for hd_url in flv_url:
                if '/SHD/' in hd_url:
                    video_url = hd_url
                    break
                if '/HD/' in hd_url:
                    video_url = hd_url
                    flag1 = 1
                else:
                    flag2 = 0
                if not(flag1 == 1 and flag2 == 0):
                    video_url = hd_url
            return video_url
        except Exception as e:
            print ("wangyi.wy_url: " + str(e))

    def wy_message(self, web_url):
        try:
            html = requests.get(web_url, headers=self.header)
            video_url = self.wy_url(web_url)
            # 视频大小
            with closing(requests.get(video_url, stream=True)) as size:
                video_size = size.headers['content-length']
            pattern = re.compile(r'<span class="item">(.*?)</span>')
            author = pattern.findall(html.text)
            # 视频作者
            video_author = ''
            flag1 = flag2 = 0
            for item in author:
                if '来源：' in item:
                    video_author = str(item)[9:len(str(item))]
                    flag1 = 1
                else:
                    flag2 = 0
                if '上传者：' in item:
                    video_author = str(item)[12:len(str(item))]
                    break
                if not(flag1 == 1 and flag2 == 0):
                    video_author = 'author missing'
            pattern = re.compile(r'topicid : "(.*?)"', re.S | re.M | re.I)
            # 获取topicid
            cid = pattern.findall(html.text)[0].encode('utf8')
            # 将url进行list处理
            sc = [web_url][0]
            # 构造url
            req_url = 'http://xml.ws.126.net/video/' + sc[-7] + '/' + sc[-6] + '/' + cid + '_' + sc[-14: -5] + '.xml'
            # 获取xml数据
            xml_data = retry_get(req_url, self.header)
            pattern = re.compile(r'<title>(.*?)</title>', re.S | re.M | re.I)
            name = pattern.findall(xml_data)[0]
            # 视频名称
            video_name = urllib.unquote(name)
            pattern = re.compile(r'<totaltime>(.*?)</totaltime>', re.S | re.M | re.I)
            # 视频播放时长
            video_time = pattern.findall(xml_data)[0]
            pattern = re.compile(r'vid : "(.*?)"', re.S | re.M | re.I)
            # 视频id
            video_id = pattern.findall(html.text)[0].encode('utf8')
            pattern = re.compile(r'"productKey" : "(.*?)"', re.S | re.M | re.I)
            product_key = pattern.findall(html.text)[0].encode('utf8')
            try:
                pattern = re.compile(r'"docId" :  "(.*?)"', re.S | re.M | re.I)
                doc_id = pattern.findall(html.text)[0].encode('utf8')
            except:
                pattern = re.compile(r'"docId" : "(.*?)"', re.S | re.M | re.I)
                doc_id = pattern.findall(html.text)[0].encode('utf8')
            # 构造获取视频其他信息的url
            mess_url = 'http://sdk.comment.163.com/api/v1/products/' + product_key + '/threads/' + doc_id
            req_mess = retry_get(mess_url, self.header)
            message = json.loads(req_mess)
            # 视频的上传时间
            video_modify = message['modifyTime'].encode('utf8')
            # 视频的评论数
            video_comment = str(message['tcount'])
            # 视频评论的反对数
            video_comment_against = str(message['cmtAgainst'])
            # 视频评论的点赞数
            video_comment_fav = str(message['cmtVote'])
            mess_url = 'http://so.v.163.com/vote/' + video_id + '.js'
            req_mess = retry_get(mess_url, self.header)
            pattern = re.compile(r'"hits":(.*?),', re.M | re.S | re.I)
            # 视频的观看数
            video_view = pattern.findall(req_mess)[0]
            pattern = re.compile(r'"opposecount":(.*?),')
            # 视频的反对数
            video_oppose = pattern.findall(req_mess)[0]
            pattern = re.compile(r'"supportcount":(.*?),')
            # 视频的点赞数
            video_support = pattern.findall(req_mess)[0]
            return video_id, video_name, video_author, video_size, video_time, video_modify, video_view, video_oppose,\
                video_support, video_comment, video_comment_fav, video_comment_against
        except Exception as e:
            print ("wangyi.wy_message: " + str(e))
