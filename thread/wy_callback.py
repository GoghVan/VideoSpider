# -*- coding: utf-8 -*-
import re
import urllib2
import sys
import chardet


class WyCallback:
    def __init__(self, max_urls=10,):
        self.max_urls = max_urls
        self.seed_url = "http://v.163.com/jishi/V8DLTRECM/VAPPQC6E9.html"

    def __call__(self, url):
        try:
            html = self.download(url)
            url_list = self.get_links(html)
            return url_list
        except Exception as e:
            print e

    def download(self, url, num_retries=2):
        # print 'Downloading:', url
        try:
            request = urllib2.Request(url)
            content = urllib2.urlopen(request).read()
            typeEncode = sys.getfilesystemencoding()  ##系统默认编码
            infoencode = chardet.detect(content).get('encoding', 'utf-8')  ##通过第3方模块来自动提取网页的编码
            html = content.decode(infoencode, 'ignore').encode(typeEncode)  ##先转换成unicode编码，然后转换系统编码输出
        except urllib2.URLError as e:
            print 'Download error:', e.reason
            html = None
            if num_retries > 0:
                if hasattr(e, 'code') and 500 <= e.code < 600:
                    html = self.download(url, num_retries - 1)
        return html

    def get_links(self, html):

        webpage_regex = re.compile('<a href="(.*?)"', re.IGNORECASE)
        list = webpage_regex.findall(html)
        list2 = []
        for link in list:
            if re.match("/jishi/", link):
                if link not in list2:
                    list2.append(link)
        return list2


if __name__ == "__main__":
    scrape_callback = WyCallback()
    print scrape_callback("http://v.163.com/jishi/V8DLTRECM/index.html")
