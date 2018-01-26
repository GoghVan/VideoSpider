# -*- coding: utf-8 -*-
# @Time    : 2017/11/16 20:23
# @Author  : Gavin

import os
from video.src.log import Log
from video.src.timenow import TimeNow
from video.videomysql.video_mysql import VideoMysql
from video.videocheck.lostupadte import lost_update


class LostMessage(object):
    def __init__(self, web_url, video_message, file_name, connect, video_url):
        self.web_url = web_url
        self.video_message = video_message
        self.file_name = file_name
        self.connect = connect
        self.video_url = video_url

    def download(self, flag):
        mess = TimeNow.get_time() + " 注意 : 数据库中没有该视频信息，其url : [ %s ]" % self.web_url
        print (mess)
        Log.log(mess)
        if flag == "renren" == self.file_name:
            VideoMysql(self.web_url, self.file_name, self.connect, self.video_message, self.video_url).rr_mysql()
        if flag == "wangyi" == self.file_name:
            VideoMysql(self.web_url, self.file_name, self.connect, self.video_message, self.video_url).wy_mysql()
        if flag == "fenghuang" == self.file_name:
            VideoMysql(self.web_url, self.file_name, self.connect, self.video_message, self.video_url).fh_mysql()
        if flag == "mangotv" == self.file_name:
            VideoMysql(self.web_url, self.file_name, self.connect, self.video_message, self.video_url).mg_mysql()
        if flag == "souhu" == self.file_name:
            VideoMysql(self.web_url, self.file_name, self.connect, self.video_message, self.video_url).sh_mysql()

    def switch(self, flag):
        if flag == "renren" == self.file_name:
            lost_update(self.web_url, self.video_message, self.file_name, self.connect, self.video_url)
        if flag == "wangyi" == self.file_name:
            lost_update(self.web_url, self.video_message, self.file_name, self.connect, self.video_url)
        if flag == "fenghuang" == self.file_name:
            lost_update(self.web_url, self.video_message, self.file_name, self.connect)
        if flag == "mangotv" == self.file_name:
            lost_update(self.web_url, self.video_message, self.file_name, self.connect)
        if flag == "souhu" == self.file_name:
            lost_update(self.web_url, self.video_message, self.file_name, self.connect)

    def lost_mess(self):
        conn = self.connect
        cur = conn.cursor()
        sql = flag = " "
        if ('http://rr.tv/' in self.web_url or 'http://www.rr.tv/' in self.web_url) and self.file_name == "renren":
            flag = self.file_name
            sql = "SELECT Video_File,Video_Size,Video_Name " \
                  "FROM renren " \
                  "WHERE Video_Web = %s "
        if 'http://v.163.com/' in self.web_url and self.file_name == "wangyi":
            flag = self.file_name
            sql = "SELECT Video_File,Video_Size,Video_Name " \
                  "FROM wangyi " \
                  "WHERE Video_Web = %s "
        if 'http://v.ifeng.com/' in self.web_url and self.file_name == "fenghuang":
            flag = self.file_name
            sql = "SELECT Video_File,Video_Size,Video_Name " \
                  "FROM fenghuang " \
                  "WHERE Video_Web = %s "
        if 'https://www.mgtv.com' in self.web_url and self.file_name == "mangotv":
            flag = self.file_name
            sql = "SELECT Video_File,Video_Size,Video_Name " \
                  "FROM mangotv " \
                  "WHERE Video_Web = %s "
        if ('http://my.tv.sohu.com/' in self.web_url or 'https://my.tv.sohu.com/' in self.web_url
            or 'https://tv.sohu.com/' in self.web_url or 'http://tv.sohu.com/' in self.web_url) \
                and self.file_name == "souhu":
            flag = self.file_name
            sql = "SELECT Video_File,Video_Size,Video_Name " \
                  "FROM souhu " \
                  "WHERE Video_Web = %s "

        try:
            cur.execute(sql, self.web_url)
            content = cur.fetchone()
            conn.commit()
            cur.close()
            if content:
                if not (os.path.exists(content[0])):
                    mess = TimeNow.get_time() + ' 注意 : [ ' + str(content[2]) + ' ] 信息丢失！'
                    print (mess)
                    Log.log(mess)
                    self.switch(flag)
            # else:
            #     self.download(flag)
        except Exception as e:
            print ('videocheck.lostmess.lost_mess(93): ' + str(e))
            conn.rollback()
            cur.close()
