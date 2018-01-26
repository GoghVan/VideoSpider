# -*- coding: utf-8 -*-
import re
import urllib2
import sys
import chardet


class ShCallback:
    def __init__(self, max_urls=10,):
        self.max_urls = max_urls
        self.seed_url = "http://so.tv.sohu.com/list_p11001_p2133_p3_p4_p5_p6_p73_p8_p9_p102_p11_p12_p13.html"

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

    def get_links(self,html):
        """Return a list of links from html
        """
        # a regular expression to extract all links from the webpage
        webpage_regex1 = re.compile(r'href="(.*?)" target="_blank" pb-url=', re.IGNORECASE)
        webpage_regex2 = re.compile(r'<a title="\w+" href="(.*?)">', re.IGNORECASE)
        # http://my.tv.sohu.com/pl/8427173/95196766.shtml
        # list of all links from the webpage
        list1 = webpage_regex1.findall(html)
        list2 = webpage_regex2.findall(html)
        return list1 + list2


if __name__ == "__main__":
    scrape_callback = ShCallback()
    print scrape_callback("http://so.tv.sohu.com/list_p11001_p2133_p3_p4_p5_p6_p73_p8_p9_p102_p11_p12_p13.html")