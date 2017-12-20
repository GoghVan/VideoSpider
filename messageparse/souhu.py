# -*- coding: utf-8 -*-

import re
import sys
import json
from video.src.data import retry_get

reload(sys)
sys.setdefaultencoding('utf8')


class SouHu(object):
    def __init__(self):
        self.url = 'http://changyan.sohu.com/api/2/topic/load?client_id=cyqyBluaj&topic_url&topic_source_id='
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
                          ' Chrome/61.0.3163.100 Safari/537.36',
        }

    def sh_comment(self, web_url):
        try:
            data = retry_get(web_url, self.headers)
            if re.match(r'http://share.vrs.sohu.com', web_url):
                pattern = re.compile(r'id=(\d+)', re.M | re.I | re.S)
                vid = pattern.findall(web_url)
            else:
                try:
                    pattern = re.compile(r'\Wvid\s*[\:=]\s*[\'"]?(\d+)[\'"]?')
                    vid = pattern.findall(data)[0]
                except:
                    pattern = re.compile(r'var vid=(\d+);')[0]
                    vid = pattern.findall(data)
            url = self.url + str(vid) + '&page_size='
            data = retry_get(url, self.headers)
            value = json.loads(data)
            sum = value['cmt_sum']
            content = u''
            req_url = self.url + str(vid) + '&page_size='+str(sum)
            data = retry_get(req_url, self.headers)
            value = json.loads(data)
            for item in value['comments']:
                nickname = item['passport']['nickname']
                comments = item['content']
                create_time = item['create_time']
                # content = u'%s评论人：%s，评论内容：%s，评论时间：%s$'\
                content = u'%s[ %s # %s # %s ]' \
                          % (content, nickname, comments, create_time)
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
            print ('messageparse.souhu.sh_comments(58): ' + str(e))
