# -*- coding: utf-8 -*-

import re
import sys
import math
from video.src.data import retry_get

reload(sys)
sys.setdefaultencoding('utf8')


class WangYi(object):
    def __init__(self):
        self.headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/'
                              '61.0.3163.100 Safari/537.36',
            }

    def wy_comment(self, web_url):
        try:
            data = retry_get(web_url, self.headers)
            pattern = re.compile(r'threadCountPath :.*?bbs/.*?/(.*?).js', re.S | re.M | re.I)
            vid = pattern.findall(data)[0].encode('utf8')
            offset = 0
            req_url = 'http://comment.jiankang.163.com/api/v1/products/a2869674571f77b5a0867c3d71db5856/threads/%s' \
                      '/comments/newList?offset=%d&limit=10&showLevelThreshold=70&headLimit=1&tailLimit=2&callback=' \
                      'getData&ibc=newspc' % (vid, offset)
            data = retry_get(req_url, self.headers)
            comment_max = re.search('"newListSize":(.*?)}', data, re.S).group(1)
            content = u''
            x = int(comment_max) % 10
            y = int(math.ceil(int(comment_max) / 10))
            for page in range(0, y+1):
                offset = page
                url = 'http://comment.jiankang.163.com/api/v1/products/a2869674571f77b5a0867c3d71db5856/threads/%s/' \
                      'comments/newList?offset=%d&limit=10&showLevelThreshold=70&headLimit=1&tailLimit=2&callback=' \
                      'getData&ibc=newspc' % (vid, offset)
                data_json = retry_get(url, self.headers)
                comment = re.findall('"content":"(.*?)",', data_json, re.S)
                create_time = re.findall('"createTime":"(.*?)",', data_json, re.S)
                nickname = re.findall('"nickname":"(.*?)",', data_json, re.S)
                vote = re.findall('"vote":(.*?)}', data_json, re.S)
                if page == y:
                    for n in range(0, x):
                        # content = u'%s评论人：%s，评论内容：%s，评论时间：%s，评论点赞数：%s$' \
                        content = u'%s[ %s # %s # %s # %s ]' \
                                  % (content, nickname[n], comment[n], create_time[n], vote[n])
                else:
                    for n in range(0, x+3):
                        # content = u'%s评论人：%s，评论内容：%s，评论时间：%s，评论点赞数：%s$' \
                        content = u'%s[ %s # %s # %s # %s ]' \
                                  % (content, nickname[n], comment[n], create_time[n], vote[n])
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
            print ('messageparse.wangyi.wy_comments(63): ' + str(e))
