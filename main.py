# -*- coding: utf-8 -*-
# @Time    : 2017/11/16 20:23
# @Author  : Gavin

import time
import datetime
from video.videoparse.renren import RenRen
from video.videoparse.wangyi import WangYi
from video.videoparse.fenghuang import FengHuang
from video.videoparse.mangotv import MangoTV
from video.videoparse.souhu import SouHu

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
    # 芒果TV
    # url4 = ('https://www.mgtv.com/b/315180/4123811.html', 'https://www.mgtv.com/b/315180/4118954.html',
    #         'https://www.mgtv.com/b/309034/4162625.html', 'https://www.mgtv.com/b/319321/4155793.html',
    #         'https://www.mgtv.com/b/309037/4165708.html', 'https://www.mgtv.com/b/309033/3769262.html',
    #         'https://www.mgtv.com/b/308848/4162604.html', 'https://www.mgtv.com/b/314104/4155515.html',
    #         'https://www.mgtv.com/b/317449/4081602.html', 'https://www.mgtv.com/b/308723/4161865.html',
    #         'https://www.mgtv.com/b/308719/4095140.html', 'https://www.mgtv.com/b/318977/4139048.html',
    #         'https://www.mgtv.com/b/310613/4080053.html', 'https://www.mgtv.com/b/308937/4166436.html',
    #         'https://www.mgtv.com/b/312680/4157863.html', 'https://www.mgtv.com/b/319152/4163376.html',
    #         'https://www.mgtv.com/b/292259/3091699.html', 'https://www.mgtv.com/b/319400/4164530.html',
    #         'https://www.mgtv.com/b/315363/3970832.html', 'https://www.mgtv.com/b/310625/4121054.html',
    #         'https://www.mgtv.com/b/316682/4013541.html', 'https://www.mgtv.com/b/314750/4163296.html',
    #         'https://www.mgtv.com/b/314646/4155536.html', 'https://www.mgtv.com/b/315572/4164325.html',
    #         'https://www.mgtv.com/b/319193/4148752.html', 'https://www.mgtv.com/b/319051/4165850.html',
    #         'https://www.mgtv.com/b/309454/4162039.html', 'https://www.mgtv.com/b/151138/4166865.html',
    #         'https://www.mgtv.com/b/308875/4166319.html', 'https://www.mgtv.com/b/308908/4166429.html',
    #         'https://www.mgtv.com/b/318566/4119663.html', 'https://www.mgtv.com/b/319481/4166103.html',
    #         'https://www.mgtv.com/b/318098/4096537.html', 'https://www.mgtv.com/b/307247/3697251.html',
    #         'https://www.mgtv.com/b/319366/4166863.html', 'https://www.mgtv.com/b/315963/4166450.html',
    #         'https://www.mgtv.com/b/167448/4165899.html', 'https://www.mgtv.com/b/319008/4163069.html',
    #         'https://www.mgtv.com/b/318221/4165211.html', 'https://www.mgtv.com/b/167448/4162785.html',
    #         'https://www.mgtv.com/b/167448/4162776.html', 'https://www.mgtv.com/b/295541/3969491.html',
    #         'https://www.mgtv.com/b/168349/3542701.html', 'https://www.mgtv.com/b/47378/566443.html',
    #         'https://www.mgtv.com/b/105192/2934808.html', 'https://www.mgtv.com/b/299052/3432285.html',
    #         'https://www.mgtv.com/b/301817/4076165.html', 'https://www.mgtv.com/b/314894/4000292.html',
    #         'https://www.mgtv.com/b/315174/4169881.html', 'https://www.mgtv.com/b/167448/4169521.html',
    #         'https://www.mgtv.com/b/168968/3304588.html',)
    # 搜狐视频
    urls5 = ('http://my.tv.sohu.com/pl/9059869/94684875.shtml', 'http://my.tv.sohu.com/pl/9059869/94586313.shtml',
             'http://my.tv.sohu.com/pl/9336861/94727839.shtml', 'http://my.tv.sohu.com/pl/9413585/94439505.shtml',
    #          'http://my.tv.sohu.com/pl/9115681/94619496.shtml', 'http://my.tv.sohu.com/pl/9116786/94756105.shtml',
    #          'http://my.tv.sohu.com/pl/9388352/94664925.shtml', 'http://my.tv.sohu.com/pl/9271813/94803248.shtml',
    #          'http://my.tv.sohu.com/pl/9264256/93977598.shtml', 'https://my.tv.sohu.com/us/312813498/94766453.shtml',
    #          'http://my.tv.sohu.com/us/300966536/94794631.shtml', 'https://tv.sohu.com/20111213/n328893457.shtml',
    #          'https://tv.sohu.com/20171119/n600261860.shtml', 'https://tv.sohu.com/20171106/n600241945.shtml',
             'https://tv.sohu.com/20171106/n600241324.shtml', 'https://tv.sohu.com/20171115/n600254561.shtml',
             'https://tv.sohu.com/20171120/n600262666.shtml', 'http://tv.sohu.com/20170523/n494170295.shtml',)
    #          'https://tv.sohu.com/20150912/n420982178.shtml',)
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
        # 芒果TV
        # for url in url4:
        #     lost_url = MangoTV().mg_update(url)
        #     if lost_url:
        #         MangoTV().mg_mysql(lost_url)
        # 搜狐视频
        for url in urls5:
            lost_url = SouHu().sh_update(url)
            if lost_url:
                SouHu().sh_mysql(lost_url)
        time.sleep(5)
