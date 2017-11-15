# -*- coding: utf-8 -*-
import os
from video.src.log import Log
from video.src.timenow import TimeNow
from video.videoupdate.lostupadte import lost_update


class LostMessage(object):
    def __init__(self, web_url, video_message, file_name, conn, video_url):
        self.web_url = web_url
        self.video_message = video_message
        self.file_name = file_name
        self.conn = conn
        self.video_url = video_url

    def switch(self, flag):
        if flag == "renren" == self.file_name:
            lost_update(self.web_url, self.video_message, self.file_name, self.conn, self.video_url)
        if flag == "wangyi" == self.file_name:
            lost_update(self.web_url, self.video_message, self.file_name, self.conn, self.video_url)
        if flag == "fenghuang" == self.file_name:
            lost_update(self.web_url, self.video_message, self.file_name, self.conn)
        if flag == "mangotv" == self.file_name:
            lost_update(self.web_url, self.video_message, self.file_name, self.conn)

    def lost_mess(self):
        conn = self.conn
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
        except Exception as e:
            print (e)
            conn.rollback()
            cur.close()
