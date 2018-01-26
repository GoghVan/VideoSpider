# -*- coding: utf-8 -*-
# @Time    : 2017/11/16 20:23
# @Author  : Gavin

import re
import sys
import time
import json
import random
from video.src.data import retry_get

reload(sys)
sys.setdefaultencoding('utf8')


class SouHu(object):
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
                          ' Chrome/61.0.3163.100 Safari/537.36',
        }

    def sh_message(self, web_url):
        try:
            data = retry_get(web_url, self.headers)
            # 获取视频vid(video_id)
            if re.match(r'http://share.vrs.sohu.com', web_url):
                pattern = re.compile(r'id=(\d+)', re.M | re.I | re.S)
                video_id = pattern.findall(web_url)
            else:
                try:
                    pattern = re.compile(r'\Wvid\s*[\:=]\s*[\'"]?(\d+)[\'"]?')
                    video_id = pattern.findall(data)[0]
                except:
                    pattern = re.compile(r'var vid=(\d+);')
                    video_id = pattern.findall(data)[0]
            if '/n' in web_url:
                req_url = 'http://hot.vrs.sohu.com/vrs_flash.action?vid=%s' % video_id
                data = json.loads(retry_get(req_url, self.headers))
                for qtyp in ["oriVid", "superVid", "highVid", "norVid", "relativeId"]:
                    if 'data' in data:
                        hqvid = data['data'][qtyp]
                    else:
                        hqvid = data[qtyp]
                    if hqvid != 0 and hqvid != video_id:
                        req_url = 'http://hot.vrs.sohu.com/vrs_flash.action?vid=%s' % hqvid
                        data = json.loads(retry_get(req_url, self.headers))
                        if not 'allot' in data:
                            continue
                        break
                # 一些参数
                host = data['allot']
                # prot = data['prot']
                # tvid = data['tvid']
                # 视频名称
                video_name = str(data['data']['tvName'])
                # 视频大小
                video_size = str(sum(data['data']['clipsBytes']))
                # 视频作者
                video_author = str(data['keyword'])
                # 视频上传时间
                video_modify = str(data['tv_application_time'])
                # 视频时长
                video_time = str(data['data']['totalDuration'])
                # 获取视频原url
                video_url = []
                for su, clip, ck in zip(data['data']['su'], data['data']['clipsURL'], data['data']['ck']):
                    req_url = 'http://' + host + '/?prot=9&prod=flash&pt=1&file=' + clip + '&new=' + su + '&key=' + \
                        ck + '&vid=' + video_id + '&uid=' + str(int(time.time()*1000)) + '&t=' + str(random.random()) \
                              + '&rb=1'
                    data = json.loads(retry_get(req_url, self.headers))
                    video_url.append(str(data['url']))
                # 构造url
                req_url = 'https://count.vrs.sohu.com/count/queryext.action?vids=%s&callback=playCountVrs' % video_id
                # 视频观看数
                data = retry_get(req_url, self.headers)
                pattern = re.compile(r'"total":(\d+),', re.M | re.I | re.S)
                video_view = pattern.findall(data)[0]
                return video_id, video_name, video_author, video_size, video_time, video_modify, video_view, video_url
            else:
                # 视频上传时间
                pattern = re.compile(r',uploadTime: \'(.*?)\'', re.M | re.I | re.S)
                video_modify = pattern.findall(data)[0]
                # # 构造url
                req_url = "http://my.tv.sohu.com/play/videonew.do?vid=%s&referer=http://my.tv.sohu.com" % video_id
                # 一些参数
                data = json.loads(retry_get(req_url, self.headers))
                host = str(data['allot'])
                # prot = str(data['prot'])
                # tvid = str(data['tvid'])
                # 视频名称
                video_name = str(data['data']['tvName'])
                # 视频大小
                video_size = str(sum(map(int, data['data']['clipsBytes'])))
                # 视频作者
                video_author = str(data['wm_data']['wm_username'])
                # 视频时长
                video_time = str(data['data']['totalDuration'])
                # 视频原地址
                video_url = []
                for su, clip, ck in zip(data['data']['su'], data['data']['clipsURL'], data['data']['ck']):
                    req_url = 'http://' + host + '/?prot=9&prod=flash&pt=1&file=' + clip + '&new=' + su + '&key=' + \
                        ck + '&vid=' + video_id + '&uid=' + str(int(time.time()*1000)) + '&t=' + str(random.random()) + '&rb=1'
                    data = json.loads(retry_get(req_url, self.headers))
                    video_url.append(str(data['url']))
                # 构造url
                req_url = 'http://vstat.v.blog.sohu.com/dostat.do?method=getVideoPlayCount&v=' + video_id
                # 视频观看数
                data = retry_get(req_url, self.headers)
                pattern = re.compile(r'"count":(\d+),', re.M | re.I | re.S)
                video_view = pattern.findall(data)[0]
                # print (video_url)
                return video_id, video_name, video_author, video_size, video_time, video_modify, video_view, video_url
        except Exception as e:
            print ('videoparse.souhu.sh_message(115): ' + str(e))
