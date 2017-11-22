# -*- coding: utf-8 -*-
# @Time    : 2017/11/21 22:18
# @Author  : Gavin

from video.src.log import Log
from video.src.timenow import TimeNow
from video.src.message import messages
from video.videoparse.souhu import SouHu
from video.videoparse.renren import RenRen
from video.videoparse.wangyi import WangYi
from video.videoparse.mangotv import MangoTV
from video.videocheck.urlcheck import check_url
from video.videoparse.fenghuang import FengHuang
from video.videocheck.messupdate import update_message


class VideoUpdate(object):
    def __init__(self, web_url):
        self.web_url = web_url
        self.connect = messages()[0]
        self.file_name = messages()[1]

    def rr_update(self):
        video_url = RenRen().rr_url(self.web_url)
        video_message = RenRen().rr_message(self.web_url)
        flags = check_url(self.web_url, video_message, self.file_name[0], self.connect, video_url)

        flag1 = flags[0]
        flag2 = flags[1]
        flag3 = flags[2]
        check = ''
        conn = self.connect
        if flag1 and flag2 and flag3:
            cur = conn.cursor()
            sql = "SELECT Video_View, Video_Support, Video_Comment " \
                  "FROM renren " \
                  "WHERE Video_Web=%s AND Video_Name=%s"
            try:
                cur.execute(sql, (self.web_url, video_message[1]))
                check = cur.fetchone()
                conn.commit()
            except Exception as e:
                print ('renren.rr_update.check: ' + str(e))
                conn.rollback()
            cur.close()
            flags = update_message(check, conn, self.web_url, video_message)
            flag4 = flags[0]
            flag5 = flags[2]
            flag6 = flags[3]

            if flag4 and flag5 and flag6:
                mess = TimeNow.get_time() + " 视频 : [ " + video_message[1] + " ] 没有更新信息。"
                print (mess)
                Log.log(mess)
                conn.close()
        else:
            mess = TimeNow.get_time() + " 注意 : 数据库中没有该视频信息，其url : [ %s ]" % self.web_url
            print (mess)
            Log.log(mess)

    def wy_update(self):
        video_url = WangYi().wy_url(self.web_url)
        video_message = WangYi().wy_message(self.web_url)
        flags = check_url(self.web_url, video_message, self.file_name[1], self.connect, video_url)

        flag1 = flags[0]
        flag2 = flags[1]
        flag3 = flags[2]
        check = ''

        conn = self.connect
        if flag1 and flag2 and flag3:
            cur = conn.cursor()
            sql = "SELECT Video_View, Video_Oppose, Video_Support, Video_Comment, Video_Comment_Fav" \
                  ", Video_Comment_Against " \
                  "FROM wangyi " \
                  "WHERE Video_Web=%s AND Video_Name=%s"
            try:
                cur.execute(sql, (self.web_url, video_message[1]))
                check = cur.fetchone()
                conn.commit()
            except Exception as e:
                print ('wangyi.wy_update.check: ' + str(e))
                conn.rollback()
            cur.close()

            flags = update_message(check, conn, self.web_url, video_message)
            flag4 = flags[0]
            flag5 = flags[1]
            flag6 = flags[2]
            flag7 = flags[3]
            flag8 = flags[4]
            flag9 = flags[5]

            if flag4 and flag5 and flag6 and flag7 and flag8 and flag9:
                mess = TimeNow.get_time() + " 视频 : [ " + video_message[1] + " ] 没有更新信息。"
                print (mess)
                Log.log(mess)
                conn.close()
        else:
            mess = TimeNow.get_time() + " 注意 : 数据库中没有该视频信息，其url : [ %s ]" % self.web_url
            print (mess)
            Log.log(mess)

    def fh_update(self):

        video_message = FengHuang().fh_message(self.web_url)
        flags = check_url(self.web_url, video_message, self.file_name[2], self.connect, " ")

        flag1 = flags[0]
        flag2 = flags[1]
        flag3 = flags[2]
        check = ''

        conn = self.connect
        if flag1 and flag2 and flag3:
            cur = conn.cursor()
            sql = "SELECT Video_View, Video_Oppose, Video_Support, Video_Comment " \
                  "FROM fenghuang " \
                  "WHERE Video_Web=%s AND Video_Name=%s"
            try:
                cur.execute(sql, (self.web_url, video_message[1]))
                check = cur.fetchone()
                conn.commit()
            except Exception as e:
                print ('fenghuang.fh_update: ' + str(e))
                conn.rollback()
            cur.close()

            flags = update_message(check, conn, self.web_url, video_message)
            flag4 = flags[0]
            flag5 = flags[1]
            flag6 = flags[2]
            flag7 = flags[3]

            if flag4 and flag5 and flag6 and flag7:
                mess = TimeNow.get_time() + " 视频 : [ " + video_message[1] + " ] 没有更新信息。"
                print (mess)
                Log.log(mess)
                conn.close()
        else:
            mess = TimeNow.get_time() + " 注意 : 数据库中没有该视频信息，其url : [ %s ]" % self.web_url
            print (mess)
            Log.log(mess)

    def mg_update(self):
        video_message = MangoTV().mg_message(self.web_url)
        flags = check_url(self.web_url, video_message, self.file_name[3], self.connect, " ")

        flag1 = flags[0]
        flag2 = flags[1]
        flag3 = flags[2]
        check = ''

        conn = self.connect
        if flag1 and flag2 and flag3:
            cur = conn.cursor()
            sql = "SELECT Video_View, Video_Oppose, Video_Support " \
                  "FROM mangotv " \
                  "WHERE Video_Web=%s AND Video_Name=%s"
            try:
                cur.execute(sql, (self.web_url, video_message[1]))
                check = cur.fetchone()
                conn.commit()
            except Exception as e:
                print ('mangotv.mg_update: ' + str(e))
                conn.rollback()
            cur.close()

            flags = update_message(check, conn, self.web_url, video_message)
            flag4 = flags[0]
            flag5 = flags[1]
            flag6 = flags[2]

            if flag4 and flag5 and flag6:
                mess = TimeNow.get_time() + " 视频 : [ " + video_message[1] + " ] 没有更新信息。"
                print (mess)
                Log.log(mess)
                conn.close()
        else:
            mess = TimeNow.get_time() + " 注意 : 数据库中没有该视频信息，其url : [ %s ]" % self.web_url
            print (mess)
            Log.log(mess)

    def sh_update(self):
        video_message = SouHu().sh_message(self.web_url)
        flags = check_url(self.web_url, video_message, self.file_name[4], self.connect, " ")

        flag1 = flags[0]
        flag2 = flags[1]
        flag3 = flags[2]
        check = ''

        conn = self.connect
        if flag1 and flag2 and flag3:
            cur = conn.cursor()
            sql = "SELECT Video_View " \
                  "FROM souhu " \
                  "WHERE Video_Web=%s AND Video_Name=%s"
            try:
                cur.execute(sql, (self.web_url, video_message[1]))
                check = cur.fetchone()
                conn.commit()
            except Exception as e:
                print ('souhu.sh_update.check: ' + str(e))
                conn.rollback()
            cur.close()

            flags = update_message(check, conn, self.web_url, video_message)
            flag4 = flags[0]

            if flag4:
                mess = TimeNow.get_time() + " 视频 : [ " + video_message[1] + " ] 没有更新信息。"
                print (mess)
                Log.log(mess)
                conn.close()
        else:
            mess = TimeNow.get_time() + " 注意 : 数据库中没有该视频信息，其url : [ %s ]" % self.web_url
            print (mess)
            Log.log(mess)
