# -*- coding: utf-8 -*-
from thread_wy import thread_crawler
from wy_callback import WyCallback
import time


def main():
    scrape_callback = WyCallback()
    max_threads = 8
    max_urls = 40
    seed_url = "http://v.163.com/jishi/V8DLTRECM/index.html"
    thread_crawler(seed_url, scrape_callback=scrape_callback, max_threads=max_threads, timeout=10, max_urls=max_urls)


if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time()
    print '%.2f seconds' % (end-start)
