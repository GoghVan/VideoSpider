# -*- coding: utf-8 -*-
import time
import datetime
from video.videourl.rr import RenRen
from video.videourl.wangyi import WangYi
from video.videodownload.download import DownloadVideo


if __name__ == '__main__':
    # 人人视频
    # urls1 = ('http://rr.tv/#/video/386036', 'http://rr.tv/#/video/386114',
    #         'http://rr.tv/#/video/385805', 'http://rr.tv/#/video/386593',
    #         'http://rr.tv/#/video/392664', 'http://rr.tv/#/video/394883',
    #         'http://rr.tv/#/video/394815', 'http://rr.tv/#/video/394733',
    #         'http://rr.tv/#/video/394450', 'http://rr.tv/#/video/394308',
    #         'http://rr.tv/#/video/395259', 'http://rr.tv/#/video/395139',
    #         'http://rr.tv/#/video/394894', 'http://rr.tv/#/video/394928',
    #         'http://rr.tv/#/video/394788', 'http://rr.tv/#/video/394404',
    #         'http://rr.tv/#/video/394395', 'http://rr.tv/#/video/394938',
    #         'http://rr.tv/#/video/393274', 'http://rr.tv/#/video/396035',
    #         'http://rr.tv/#/video/395984', 'http://rr.tv/#/video/395766',)

    # 网易视频
    urls2 = ('http://v.163.com/zixun/V8GAM8GTF/VBVB9I7AE.html', 'http://v.163.com/paike/VBFGBLNBF/VBHBGAC2L.html',
             'http://v.163.com/paike/VBFGBLNBF/VBHDM17C9.html', 'http://v.163.com/jishi/VBKLP54SS/VBKLQOSQM.html')
    startTime = datetime.datetime(2017, 10, 30, 0, 0, 0)
    while datetime.datetime.now() < startTime:
        # 人人视频
        # for url in urls1:
        #     ren_ren = RenRen()
        #     lost_url = ren_ren.rr_update(url)
        #     if lost_url:
        #         video_url = ren_ren.rr_url(url)
        #         video_message = ren_ren.rr_message(url)
        #         download_video = DownloadVideo(video_url, video_message[0], "renren")
        #         video_url_file = download_video.video_download()
        #         ren_ren.rr_mysql(url, video_url, video_message, video_url_file)
        # 网易视频
        for url in urls2:
            wang_yi = WangYi()
            lost_url = wang_yi.wang_yi_check(url)
            if lost_url:
                wang_yi.wy_mysql(lost_url)
        time.sleep(5)