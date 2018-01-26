# -*- coding: utf-8 -*-
import re
from video.src.data import retry_get


class mg_callback:
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
        # https://pcweb.api.mgtv.com/variety/showlist?video_id=4165698&callback=jQuery18202789099847652816_1510664574203&_support=10000000&_=1510664574355
        # 找出视频的Id(str)
        pattern = re.compile(r'https://www.mgtv.com/b/\w+/(\w+).html', re.S | re.I | re.M)
        video_id = pattern.findall(web_url)[0]
        # 构造请求视频原地址url
        req_url = 'https://pcweb.api.mgtv.com/variety/showlist?video_id=' + video_id + '&callback=jQuery18202789099847652816_1510664574203'
        # 获取data数据(str)
        data = retry_get(req_url, headers)
        if "data" in data:
            # 获取相关视频的url
            pattern = re.compile(r'"url":"(.*?)",', re.I | re.M | re.S)
        alllinks = pattern.findall(data)
        for link in alllinks:
            flag = re.match(r"/b", link)
            if flag:
                links.append(link)
        return links


if __name__ == '__main__':
    mg = mg_callback()
    print mg("https://www.mgtv.com/b/316387/4165698.html")