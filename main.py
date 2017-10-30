# -*- coding: utf-8 -*-
import time
import datetime
from video.videourl.renren import RenRen
from video.videourl.wangyi import WangYi
from video.videodownload.download import DownloadVideo


if __name__ == '__main__':
    # 人人视频
    urls1 = ('http://rr.tv/#/video/386036', 'http://rr.tv/#/video/386114',
             'http://www.rr.tv/#/video/413765', 'http://www.rr.tv/#/video/419355',
             'http://rr.tv/#/video/385805', 'http://rr.tv/#/video/386593',
             'http://www.rr.tv/#/video/419317', 'http://www.rr.tv/#/video/419584',
             'http://rr.tv/#/video/392664', 'http://rr.tv/#/video/394883',
             'http://www.rr.tv/#/video/419386', 'http://www.rr.tv/#/video/419444',
             'http://rr.tv/#/video/394815', 'http://rr.tv/#/video/394733',
             'http://www.rr.tv/#/video/419530', 'http://www.rr.tv/#/video/419459',
             'http://rr.tv/#/video/394450', 'http://rr.tv/#/video/394308',
             'http://www.rr.tv/#/video/419715', 'http://www.rr.tv/#/video/419358',
             'http://rr.tv/#/video/395259', 'http://rr.tv/#/video/395139',
             'http://www.rr.tv/#/video/419653', 'http://www.rr.tv/#/video/419046',
             'http://rr.tv/#/video/394894', 'http://rr.tv/#/video/394928',
             'http://www.rr.tv/#/video/418125', 'http://www.rr.tv/#/video/418015',
             'http://rr.tv/#/video/394788', 'http://rr.tv/#/video/394404',
             'http://www.rr.tv/#/video/419772', 'http://www.rr.tv/#/video/419807',
             'http://rr.tv/#/video/394395', 'http://rr.tv/#/video/394938',
             'http://www.rr.tv/#/video/419804', 'http://www.rr.tv/#/video/419642',
             'http://rr.tv/#/video/393274', 'http://rr.tv/#/video/396035',
             'http://www.rr.tv/#/video/419881', 'http://www.rr.tv/#/video/419785',
             'http://rr.tv/#/video/395984', 'http://rr.tv/#/video/395766',
             'http://www.rr.tv/#/video/420407', 'http://www.rr.tv/#/video/420165',)
    # 人人视频
    # urls1 = ('http://rr.tv/#/video/386036', 'http://rr.tv/#/video/386114',
    #          'http://rr.tv/#/video/385805', 'http://rr.tv/#/video/386593',)
    # 网易视频
    # urls2 = ('http://v.163.com/zixun/V8GAM8GTF/VBVB9I7AE.html', 'http://v.163.com/paike/VBFGBLNBF/VBHBGAC2L.html',
    #          'http://v.163.com/paike/VBFGBLNBF/VBHDM17C9.html', 'http://v.163.com/jishi/VBKLP54SS/VBKLQOSQM.html')
    startTime = datetime.datetime(2017, 10, 30, 0, 0, 0)
    while datetime.datetime.now() < startTime:
        # 人人视频
        for url in urls1:
            ren_ren = RenRen()
            lost_url = ren_ren.rr_check(url)
            if lost_url:
                ren_ren.rr_mysql(lost_url)
        # 网易视频
        # for url in urls2:
        #     wang_yi = WangYi()
        #     lost_url = wang_yi.wy_check(url)
        #     if lost_url:
        #         wang_yi.wy_mysql(lost_url)
        time.sleep(5)
