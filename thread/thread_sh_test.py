# -*- coding: utf-8 -*-
from thread_sh import thread_crawler
from sh_callback import ShCallback
import time


def main():
    scrape_callback = ShCallback()
    max_threads = 8
    max_urls = 40
    seed_url = "http://so.tv.sohu.com/list_p11001_p2133_p3_p4_p5_p6_p73_p8_p9_p102_p11_p12_p13.html"
    thread_crawler(seed_url, scrape_callback=scrape_callback, max_threads=max_threads, timeout=10, max_urls=max_urls)


if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time()
    print '%.2f seconds' % (end-start)
