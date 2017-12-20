# -*- coding: utf-8 -*-

import re
import sys
import time
import math
from video.src.data import retry_get

reload(sys)
sys.setdefaultencoding('utf8')


class FengHuang(object):
    def __init__(self):
        self.headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
                              ' Chrome/61.0.3163.100 Safari/537.36',
        }

    def fh_message(self, web_url):
        pattern = re.compile(r'http://v.ifeng.com/video_(.*?)\.shtml', re.S | re.I | re.M)
        vid = pattern.findall(web_url)[0]
        req_url = 'http://tv.ifeng.com/h6/' + vid + '/video.json?callback=callback&msg=' + vid + '&rt=js'
        data = retry_get(req_url, self.headers)
        # 获取视频vid
        pattern = re.compile(r'"vid":"(.*?)",', re.I | re.M | re.S)
        cid = pattern.findall(data)[0]
        # 获取key
        pattern = re.compile(r'"skey":"(.*?)",', re.M | re.I | re.S)
        data = retry_get(req_url, self.headers)
        key = pattern.findall(data)
        # 获取评论数
        req_url = 'http://comment.ifeng.com/getv.php?job=3&format=js&docurl=' + cid
        data = retry_get(req_url, self.headers)
        count = 5
        while ("commentJsonVarStr" not in str(data)) and count > 0:
            data = retry_get(req_url, self.headers)
            time.sleep(1)
            count -= 1
        try:
            pattern = re.compile(r'var commentJsonVarStr___=(.*?);', re.M | re.I | re.S)
            video_comment = pattern.findall(data)[0]
        except Exception as e:
            video_comment = '0'
            print ('messageparse.fenghuang.fh_message(45): ' + str(e))
        pagemax = math.ceil(int(video_comment) / 10)
        return pagemax, key, cid, vid

    def fh_comment(self, web_url):
            video_message = self.fh_message(web_url)
            pagemax = video_message[0]
            key = video_message[1]
            cid = video_message[2]
            vid = video_message[3]
            try:
                content = u''
                for page in range(1, int(pagemax)+1):
                    req_url = 'http://comment.ifeng.com/getv.php?job=1&docurl=%s&format=js&skey=%s' \
                              '&pagesize=10&p=%s&callback=video_callbackCommentList' % (cid, key, page)
                    data = retry_get(req_url, self.headers)
                    comment1 = re.findall('"comment_contents":"(.*?)",', data, re.S)
                    create_time = re.findall('"create_time":"(.*?)",', data, re.S)
                    nickname = re.findall('"uname":"(.*?)",', data, re.S)
                    for n in range(0, 10):
                        reg = re.compile('<a href=.*? target="_blank">')
                        comment = reg.sub('', comment1[n].decode('unicode-escape'))
                        # content = u'%s评论人：%s，评论内容：%s，评论时间：%s$' \
                        content = u'%s[ %s # %s # %s ]' \
                                  % (content, nickname[n].decode('unicode-escape'),
                                     comment, create_time[n].decode('unicode-escape'))
                emoji_pattern = re.compile(
                    u"(\ud83d[\ude00-\ude4f])|"  # emoticons
                    u"(\ud83c[\udf00-\uffff])|"  # symbols & pictographs (1 of 2)
                    u"(\ud83d[\u0000-\uddff])|"  # symbols & pictographs (2 of 2)
                    u"(\ud83d[\ude80-\udeff])|"  # transport & map symbols
                    u"(\ud83c[\udde0-\uddff])"  # flags (iOS)
                    "+", flags=re.UNICODE)
                content = str(emoji_pattern.sub(r'', content))
                return content, str(vid)
            except Exception as e:
                print ('messageparse.fenghuang.fh_comments(81): ' + str(e))
