# -*- coding: utf-8 -*-


from thread_rr import thread_crawler
from rr_callback import rr_callback
import time


def main():
    scrape_callback = rr_callback()
    max_threads = 4
    max_urls = 25
    seed_url = 'http://rr.tv/#/video/386036'
    thread_crawler(seed_url, scrape_callback=scrape_callback, max_threads=max_threads, timeout=10, max_urls=max_urls)


if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time()
    print '%.2f seconds' % (end-start)
