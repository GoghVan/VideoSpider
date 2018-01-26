# -*- coding: utf-8 -*-
import re
from video.src.data import retry_get


class fh_callback:
    def __init__(self,):
        pass

    def __call__(self, url):
        try:
            url_list = self.get_links(url)
            return url_list
        except Exception as e:
            print e

    def get_links(self, web_url):
        links = []
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
                          ' Chrome/61.0.3163.100 Safari/537.36',
        }
        # http://v.ifeng.com/docvlist/8752455-1.js?callback=jsonpCallback
        # 找出视频的Id(str)
        pattern = re.compile(r'http://v.ifeng.com/video_(.*?)\.shtml', re.S | re.I | re.M)
        video_id = pattern.findall(web_url)[0]
        # 构造请求视频原地址url
        req_url = 'http://v.ifeng.com/docvlist/' + video_id + '-1.js?callback=jsonpCallback'
        # 获取data数据(str)
        data = retry_get(req_url, headers)
        if "dataList" in data:
            # 获取相关视频的url
            pattern = re.compile(r'"link":"(.*?)",', re.I | re.M | re.S)
        alllinks = pattern.findall(data)
        for url in alllinks:
            if(url not in links):
                if (url == web_url):
                    pass
                else:
                    links.append(url)
        # print len(links)
        return links


if __name__ == '__main__':
    fenghuang = fh_callback()
    print fenghuang("http://v.ifeng.com/video_8752455.shtml")