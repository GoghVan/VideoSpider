# -*- coding: utf-8 -*-
import time
import datetime
from video.videourl.rr import RenRen
from video.videodownload.download import DownloadVideo
if __name__ == '__main__':
    urls = ('http://rr.tv/#/video/386036', 'http://rr.tv/#/video/386114',
            'http://rr.tv/#/video/385805', 'http://rr.tv/#/video/386593',
            'http://rr.tv/#/video/392664', 'http://rr.tv/#/video/394883',
            'http://rr.tv/#/video/394815', 'http://rr.tv/#/video/394733',
            'http://rr.tv/#/video/394450', 'http://rr.tv/#/video/394308',
            'http://rr.tv/#/video/395259', 'http://rr.tv/#/video/395139',
            'http://rr.tv/#/video/394894', 'http://rr.tv/#/video/394928',
            'http://rr.tv/#/video/394788', 'http://rr.tv/#/video/394404',
            'http://rr.tv/#/video/394395', 'http://rr.tv/#/video/394938',
            'http://rr.tv/#/video/393274', 'http://rr.tv/#/video/396035',
            'http://rr.tv/#/video/395984', 'http://rr.tv/#/video/395766',)
    startTime = datetime.datetime(2017, 10, 20, 23, 0, 0)
    while datetime.datetime.now() < startTime:
        for url in urls:
            ren_ren = RenRen()
            lost_url = ren_ren.rr_update(url)
            if lost_url:
                video_url = ren_ren.rr_url(url)
                video_message = ren_ren.rr_message(url)
                download_video = DownloadVideo(video_url, video_message)
                video_url_file = download_video.video_download()
                ren_ren.rr_mysql(url, video_url, video_message, video_url_file)
        time.sleep(5)