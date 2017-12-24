# -*- coding: utf-8 -*-
# @Time    : 2017/11/16 20:23
# @Author  : Gavin

import re
import sys
import json
import time
from video.src.log import Log
from video.src.data import retry_get
from video.src.timenow import TimeNow

reload(sys)
sys.setdefaultencoding('utf8')


# 由于芒果TV的服务器是电信的，移动网访问会经常报HTTP或connect的相关错误，换到电信网下就好了
class MangoTV(object):
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
                          ' Chrome/61.0.3163.100 Safari/537.36',
        }

    def mg_message(self, web_url):
        try:
            # 获取视频vid、cid
            try:
                pattern = re.compile(r'/(\d+).html')
                vid = pattern.findall(web_url)[0]
                pattern = re.compile(r'/(\d+)/')
                cid = pattern.findall(web_url)[0]
            except:
                data = retry_get(web_url, self.headers)
                pattern = re.compile(r'vid: (\d+),')
                vid = pattern.findall(data)[0]
                pattern = re.compile(r'cid: (\d+),')
                cid = pattern.findall(data)[0]
            video_id = vid
            # 构造请求url
            req_url = 'https://pcweb.api.mgtv.com/player/video?' + 'video_id=' + vid + '&cid=' + cid
            # 获取数据
            data = retry_get(req_url, self.headers)
            # 将数据python化
            data_json = json.loads(data)
            # 获取视频名称
            try:
                video_author = data_json['data']['info']['title'].encode('utf8')
                video_name = video_author + '-' + data_json['data']['info']['desc'].encode('utf8')
            except:
                try:
                    pattern = re.compile(r'"title":"(.*?)",')
                    video_author = pattern.findall(data)[0]
                    pattern = re.compile(r'"desc":"(.*?)",')
                    video_name = video_author + '-' + pattern.findall(data)[0]
                except:
                    pattern = re.compile(r'"desc":"(.*?)",')
                    video_name = pattern.findall(data)[0]
                    video_author = ''
            # 获取视频时长
            try:
                video_modify = data_json['data']['info']['series'].encode('utf8')
            except:
                pattern = re.compile(r'"series":"(.*?)",')
                video_modify = pattern.findall(data)[0]
            # 获取视频长传时间
            try:
                video_time = data_json['data']['info']['duration'].encode('utf8')
            except:
                pattern = re.compile(r'"duration":"(.*?)",')
                video_time = pattern.findall(data)[0]
            # 获取stream_domain
            try:
                stream_domain = data_json['data']['stream_domain'].encode('utf8')
            except:
                pattern = re.compile(r'http://web-disp\d*.titan.mgtv.com')
                stream_domain = pattern.findall(data)
            # 获取stream_url
            try:
                stream_url = []
                stream = data_json['data']['stream']
                for each_stream in stream:
                    stream_url.append(each_stream['url'].encode('utf8'))
            except:
                # 获取stream
                pattern = re.compile(r'"stream":\[(.*?)\]', re.S)
                stream = pattern.findall(data)[0]
                # 获取stream_url
                pattern = re.compile(r'"url":"(.*?)"')
                stream_url = pattern.findall(stream)
            # 构造url为获取原视频地址部分参数
            if len(stream_domain) == len(stream_url):
                req_url_para_list = stream_domain[len(stream_domain) - 1] \
                                    + stream_url[len(stream_url) - 1]
            else:
                req_url_para_list = stream_domain[0] + stream_url[0]
            # 获取原视频url地址相关参数1
            data = retry_get(req_url_para_list, self.headers)
            data_json = json.loads(data)
            try:
                info = data_json['info'].encode('utf8')
            except:
                pattern = re.compile(r'"info":"(.*?)"')
                info = pattern.findall(data)[0]
            # 获取原视频地址参数1
            pattern = re.compile(r'(^http:.*?mp4)')
            para_list_1 = pattern.findall(info)[0]
            # 获取原视频url地址相关参数1集合(不能开myeclipse)
            try:
                data = retry_get(info, self.headers, timeout=30)
            except Exception as e:
                count = 5
                while str(e) == "('Connection aborted.', error(10054, ''))" and count > 0:
                    time.sleep(10)
                    try:
                        count -= 1
                        data = retry_get(info, self.headers, timeout=30)
                    except Exception as e:
                        mess = TimeNow.get_time() + ' ' + 'mangotv.mg_message: ' + str(e)
                        Log.log(mess)
                        print (mess)
                        print ('videoparse.mangotv.mg_message.Connection aborted(122): ' + str(e))
            # 获取原视频大小集合
            pattern = re.compile(r'#EXT-MGTV-File-SIZE:(\d+)')
            video_size = pattern.findall(data)
            # 获取原视频地址参数2
            pattern = re.compile(r',([^0-9|A-Z].*?mp4\.ts\?.*?)#', re.S)
            para_list_2 = pattern.findall(data)
            # 获取视频原地址集合
            video_url = []
            for para_list in para_list_2:
                original_url = para_list_1 + '/' + para_list.replace("\n", "")
                video_url.append(original_url)
            # 构造请求url
            req_url = 'https://vc.mgtv.com/v2/dynamicinfo?vid=' + vid
            # 获取数据
            data = retry_get(req_url, self.headers)
            json_data = json.loads(data)
            # 获取视频播放量
            video_view = str(json_data['data']['all'])
            # 获取视频点赞数
            video_support = str(json_data['data']['like'])
            # 获取视频不点赞数
            video_oppose = str(json_data['data']['unlike'])
            return video_id, video_name, video_author, video_size, video_time, video_modify, video_view, video_oppose,\
                video_support, video_url
        except Exception as e:
            print ('videoparse.mangotv.mg_message(148): ' + str(e))
