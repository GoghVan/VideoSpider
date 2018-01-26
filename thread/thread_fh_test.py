# -*- coding: utf-8 -*-


from thread_fh import thread_crawler
from fh_callback import fh_callback
import time


def main():
    scrape_callback = fh_callback()
    max_threads = 4
    max_urls = 25
    seed_url = 'http://v.ifeng.com/video_8752455.shtml'
    thread_crawler(seed_url, scrape_callback=scrape_callback, max_threads=max_threads, timeout=10, max_urls=max_urls)


if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time()
    print '%.2f seconds' % (end-start)
