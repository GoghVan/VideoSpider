# -*- coding: utf-8 -*-
import MySQLdb
import os
from video.src.log import Log
from video.src.timenow import TimeNow
from video.videourl.renren import RenRen
from video.videourl.wangyi import *


class LostMessage(object):
    def __init__(self, web_url, table, conn):
        self.web_url = web_url
        self.table = table
        self.conn = conn

    def switch(self):
        if 'http://rr.tv/#/video/' in self.web_url:
            r_ren = RenRen()
            r_ren.lost_update(self.web_url)
        if 'http://v.163.com/' in self.web_url:
            w_yi = WangYi()
            w_yi.lost_update(self.web_url)

    def lost_mess(self):

        try:
            cur = self.conn.cursor()
            sql = "SELECT File_Url,Video_Size,Video_Name " \
                  "FROM %s " \
                  "WHERE Video_Web = %s "

            cur.execute(sql, (self.table, self.web_url))
            content = cur.fetchone()
            cur.close()
            self.conn.commit()

            if content:
                if not (os.path.exists(content[0])):
                    mess = TimeNow.get_time() + ' 注意 : [ ' + str(content[2]) + ' ] 信息丢失！'
                    print (mess)
                    Log.log(mess)
                    self.switch()
        except Exception as e:
            self.conn.rollback()
            print (e)