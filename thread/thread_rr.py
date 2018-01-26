import threading
import time
import urlparse
from video.videoparse.renren import RenRen

from video.videocheck.videoupdate import VideoUpdate

SLEEP_TIME = 1
num = 0


def thread_crawler(seed_url, scrape_callback=None, user_agent='wswp', proxies=None, num_retries=1, max_threads=10, timeout=60,max_urls=3):
    crawl_queue = [seed_url]
    seen = set([seed_url])
    rr = RenRen()
    file_name = "renren"
    global num

    def process_queue():
        global num
        while crawl_queue:
            try:
                url = crawl_queue.pop()
            except IndexError:
                break
            else:
                VideoUpdate(url).rr_update()
                if scrape_callback:
                    if num < max_urls:
                        try:
                            links = scrape_callback(url) or []
                        except Exception as e:
                            print 'Error in callback for: {}: {}'.format(url, e)
                        else:
                            for link in links:
                                link = normalize(seed_url, link)
                                print link
                                if link not in seen:
                                    if mutex.acquire():
                                        num = num + 1
                                        mutex.release()
                                    if num == max_urls:
                                        break
                                    seen.add(link)
                                    crawl_queue.append(link)
                                    # print crawl_queue

    threads = []
    mutex = threading.Lock()
    while crawl_queue or threads:
        if mutex.acquire():
            if num == max_urls:
                break
            mutex.release()
        for t in threads:
            if not t.is_alive():
                threads.remove(t)
        while len(threads) < max_threads and crawl_queue:
            if mutex.acquire():
                if num == max_urls:
                    break
                mutex.release()
            t = threading.Thread(target=process_queue, )
            t.setDaemon(True)
            t.start()
            threads.append(t)
    for t in threads:
        t.join()
    time.sleep(SLEEP_TIME)


def normalize(seed_url, id):
    str1 = '#/video/'
    link, _ = urlparse.urldefrag(seed_url)
    return urlparse.urljoin(link, str1 + str(id))

