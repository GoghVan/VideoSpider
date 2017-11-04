# -*- coding: utf-8 -*-
import time
import datetime
from video.videoparse.renren import RenRen
from video.videoparse.wangyi import WangYi
from video.videoparse.fenghuang import FengHuang

if __name__ == '__main__':
    # 人人视频
    # urls1 = ('http://rr.tv/#/video/386036', 'http://rr.tv/#/video/386114',
    #          'http://www.rr.tv/#/video/413765', 'http://www.rr.tv/#/video/419355',
    #          'http://rr.tv/#/video/385805', 'http://rr.tv/#/video/386593',
    #          'http://www.rr.tv/#/video/419317', 'http://www.rr.tv/#/video/419584',
    #          'http://rr.tv/#/video/392664', 'http://rr.tv/#/video/394883',
    #          'http://www.rr.tv/#/video/419386', 'http://www.rr.tv/#/video/419444',
    #          'http://rr.tv/#/video/394815', 'http://rr.tv/#/video/394733',
    #          'http://www.rr.tv/#/video/419530', 'http://www.rr.tv/#/video/419459',
    #          'http://rr.tv/#/video/394450', 'http://rr.tv/#/video/394308',
    #          'http://www.rr.tv/#/video/419715', 'http://www.rr.tv/#/video/419358',
    #          'http://rr.tv/#/video/395259', 'http://rr.tv/#/video/395139',
    #          'http://www.rr.tv/#/video/419653', 'http://www.rr.tv/#/video/419046',
    #          'http://rr.tv/#/video/394894', 'http://rr.tv/#/video/394928',
    #          'http://www.rr.tv/#/video/418125', 'http://www.rr.tv/#/video/418015',
    #          'http://rr.tv/#/video/394788', 'http://rr.tv/#/video/394404',
    #          'http://www.rr.tv/#/video/419772', 'http://www.rr.tv/#/video/419807',
    #          'http://rr.tv/#/video/394395', 'http://rr.tv/#/video/394938',
    #          'http://www.rr.tv/#/video/419804', 'http://www.rr.tv/#/video/419642',
    #          'http://rr.tv/#/video/393274', 'http://rr.tv/#/video/396035',
    #          'http://www.rr.tv/#/video/419881', 'http://www.rr.tv/#/video/419785',
    #          'http://rr.tv/#/video/395984', 'http://rr.tv/#/video/395766',
    #          'http://www.rr.tv/#/video/420407', 'http://www.rr.tv/#/video/420165',)
    # 人人视频
    # urls1 = ('http://rr.tv/#/video/386036', 'http://rr.tv/#/video/386114',)
    # 网易视频
    # urls2 = ('http://v.163.com/zixun/V8GAM8GTF/VBVB9I7AE.html', 'http://v.163.com/paike/VBFGBLNBF/VBHBGAC2L.html',
    #          'http://v.163.com/paike/VBFGBLNBF/VBHDM17C9.html', 'http://v.163.com/jishi/VBKLP54SS/VBKLQOSQM.html')
    # 凤凰视频
    # urls3 = ('http://v.ifeng.com/video_9119714.shtml', 'http://v.ifeng.com/video_9132807.shtml',
    #          'http://v.ifeng.com/video_6227139.shtml', 'http://v.ifeng.com/video_9132821.shtml',
    #          'http://v.ifeng.com/video_9132208.shtml', 'http://v.ifeng.com/video_5595641.shtml',
    #          'http://v.ifeng.com/video_9132179.shtml', 'http://v.ifeng.com/video_9132927.shtml',
    #          'http://v.ifeng.com/video_9132421.shtml', 'http://v.ifeng.com/video_5647509.shtml',
    #          'http://v.ifeng.com/video_6096895.shtml', 'http://v.ifeng.com/video_9131210.shtml',
    #          'http://v.ifeng.com/video_9107672.shtml', 'http://v.ifeng.com/video_9132735.shtml',
    #          'http://v.ifeng.com/video_9132568.shtml', 'http://v.ifeng.com/video_9132014.shtml',
    #          'http://v.ifeng.com/video_9132189.shtml', 'http://v.ifeng.com/video_9132859.shtml',
    #          'http://v.ifeng.com/video_9131685.shtml', 'http://v.ifeng.com/video_9132715.shtml',
    #          'http://v.ifeng.com/video_9132281.shtml', 'http://v.ifeng.com/video_9130360.shtml',)
    # 凤凰视频
    # urls3 = ('http://v.ifeng.com/video_9119714.shtml', 'http://v.ifeng.com/video_9132807.shtml',)
    startTime = datetime.datetime(2017, 11, 30, 0, 0, 0)
    while datetime.datetime.now() < startTime:
        # 人人视频
        # for url in urls1:
        #     lost_url = RenRen().rr_update(url)
        #     if lost_url:
        #         RenRen().rr_mysql(lost_url)
        # 网易视频
        # for url in urls2:
        #     lost_url = WangYi().wy_update(url)
        #     if lost_url:
        #         WangYi().wy_mysql(lost_url)
        # 凤凰视频
        # for url in urls3:
        #     lost_url = FengHuang().fh_update(url)
        #     if lost_url:
        #         FengHuang().fh_mysql(lost_url)
        time.sleep(5)
