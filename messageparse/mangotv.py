# -*- coding: utf-8 -*-

import re
import sys
import math
from video.src.data import retry_get

reload(sys)
sys.setdefaultencoding('utf8')


class MangoTV(object):
    def __init__(self):
        self.headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
                              ' Chrome/61.0.3163.100 Safari/537.36',
            }

    def mg_comment(self, web_url):
        page = 1
        try:
            pattern = re.compile(r'/(\d+).html')
            vid = pattern.findall(web_url)[0]
        except:
            data = retry_get(web_url, self.headers)
            pattern = re.compile(r'vid: (\d+),')
            vid = pattern.findall(data)[0]
        req_url = 'https://comment.mgtv.com/video_comment/list/?subject_id=%s&page=%d' % (vid, page)
        data = retry_get(req_url, self.headers)
        comment_max = re.findall('"total_number":(.*?),', data, re.S)[0]
        pagemax = math.ceil(int(comment_max) / 15)
        if pagemax > 100:
            pagemax = 100
        try:
            content = u''
            for page in range(1, int(pagemax)):
                req_url = 'https://comment.mgtv.com/video_comment/list/?callback=jQuery182047769217436073474_15112' \
                            '72601570&_support=10000000&type=hunantv2014&subject_id=%s&page=%d' % (vid, page)
                data = retry_get(req_url, self.headers)
                create_time = re.findall('"create_time":"(.*?)",', data, re.S)
                comment_name = re.findall('"nickname":"(.*?)"}', data, re.S)
                comment_content = re.findall('"content":"(.*?)"', data, re.S)
                for n in range(0, 15):
                    emoji_pattern = re.compile(
                        u"(\ud83d[\ude00-\ude4f])|"  # emoticons
                        u"(\ud83c[\udf00-\uffff])|"  # symbols & pictographs (1 of 2)
                        u"(\ud83d[\u0000-\uddff])|"  # symbols & pictographs (2 of 2)
                        u"(\ud83d[\ude80-\udeff])|"  # transport & map symbols
                        u"(\ud83c[\udde0-\uddff])"  # flags (iOS)
                        "+", flags=re.UNICODE)
                    comment = emoji_pattern.sub(r'', comment_content[n])
                    # content = u'%s评论人 ：%s,评论时间 ：%s,评论内容 ：%s$'\
                    content = u'%s[ %s # %s # %s ]' \
                              % (content, comment_name[n], create_time[n], comment)
            return str(content), str(vid)
        except Exception as e:
            print ('messageparse.mango.mg_comments(57): ' + str(e))
