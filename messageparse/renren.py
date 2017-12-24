# -*- coding: utf-8 -*-

import re
import sys
import json
import math
import requests

reload(sys)
sys.setdefaultencoding('utf8')


class RenRen(object):
    def __init__(self):
        self.headers = {
            'clientVersion': '0.1.0',
            'clientType': 'web',
        }

    def rr_get(self, comment, req_py, vid):
        comment_author = req_py['data']['results'][comment]['author']['nickName']
        comment_content = req_py['data']['results'][comment]['content']
        comment_time = req_py['data']['results'][comment]['createTimeStr']
        comment_like = req_py['data']['results'][comment]['likeCount']
        return vid, comment_author, comment_content, comment_time, comment_like

    def rr_comment(self, web_url):
        try:
            content1 = u''
            page = 1
            vid = re.search(r'[0-9]+', web_url).group()
            api_url = 'http://web.rr.tv/v3plus/comment/list'
            req_js = requests.post(api_url, data={'videoId': vid, 'page': page}, headers=self.headers).content
            req_py = json.loads(req_js)
            comment_count = req_py['data']['total']
            x = int(comment_count % 10)
            y = int(math.ceil(comment_count / 10))
            for page in range(1, y + 1):
                req_js = requests.post(api_url, data={'videoId': vid, 'page': page}, headers=self.headers).content
                req_py = json.loads(req_js)
                if page == y:
                    for Comment in range(0, 10):
                        comment_message = self.rr_get(Comment, req_py, vid)
                        # content1 = u'%s[评论人：%s<->评论内容：%s<->评论时间：%s<->评论点赞数：%s$] '\
                        content1 = u'%s[ %s # %s # %s # %s ] ' \
                                   % (content1, comment_message[1], comment_message[2],
                                      comment_message[3], comment_message[4])
                else:
                    for Comment in range(0, x):
                        comment_message = self.rr_get(Comment, req_py, vid)
                        # content1 = u'%s[评论人：%s<->评论内容：%s<->评论时间：%s<->评论点赞数：%s$] '\
                        content1 = u'%s[ %s # %s # %s # %s ] ' \
                                   % (content1, comment_message[1], comment_message[2],
                                      comment_message[3], comment_message[4])
            emoji_pattern = re.compile(
                u"(\ud83d[\ude00-\ude4f])|"  # emoticons
                u"(\ud83c[\udf00-\uffff])|"  # symbols & pictographs (1 of 2)
                u"(\ud83d[\u0000-\uddff])|"  # symbols & pictographs (2 of 2)
                u"(\ud83d[\ude80-\udeff])|"  # transport & map symbols
                u"(\ud83c[\udde0-\uddff])"  # flags (iOS)
                "+", flags=re.UNICODE)
            content = str(emoji_pattern.sub(r'', content1))
            return content, str(vid)
        except Exception as e:
            print ('messageparse.renren.rr_comments(65): ' + str(e))
