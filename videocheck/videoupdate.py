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
from video.videomysql.video_mysql import VideoMysql
from video.videocheck.messupdate import update_message
from video.videocheck.commentupdate import CommentUpdate


class VideoUpdate(object):
    def __init__(self, web_url):
        self.web_url = web_url

    def rr_update(self):
        video_url = RenRen().rr_url(self.web_url)
        video_message = RenRen().rr_message(self.web_url)
        flags = check_url(self.web_url, video_message, messages()[1][0], messages()[0], video_url)

        flag1 = flags[0]
        flag2 = flags[1]
        flag3 = flags[2]
        check = ''
        conn = messages()[0]
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
                print ('videocheck.renren.rr_update.check(43): ' + str(e))
                conn.rollback()
            cur.close()
            flags = update_message(check, conn, self.web_url, video_message)
            flag4 = flags[0]
            flag5 = flags[2]
            flag6 = flags[3]

            if flag4 and flag5 and flag6:
                flag = CommentUpdate().rr_update(messages()[0], self.web_url, video_message[1])
                if flag:
                    mess = TimeNow.get_time() + " 视频 : [ " + video_message[1] + " ] 没有更新信息。"
                    print (mess)
                    Log.log(mess)
                    conn.close()
            else:
                CommentUpdate().rr_update(messages()[0], self.web_url, video_message[1])
        else:
            mess = TimeNow.get_time() + " 注意 : 数据库中没有该视频信息，其url : [ %s ]" % self.web_url
            print (mess)
            Log.log(mess)
            try:
                VideoMysql(self.web_url, messages()[1][0], messages()[0], video_message, video_url).rr_mysql()
                CommentUpdate().rr_update(messages()[0], self.web_url, video_message[1])
            except Exception as e:
                print ("videocheck.videoupdate.rr_update.rr_mysql(68): " + str(e))

    def wy_update(self):
        video_url = WangYi().wy_url(self.web_url)
        video_message = WangYi().wy_message(self.web_url)
        flags = check_url(self.web_url, video_message, messages()[1][1], messages()[0], video_url)

        flag1 = flags[0]
        flag2 = flags[1]
        flag3 = flags[2]
        check = ''

        conn = messages()[0]
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
                print ('videocheck.wangyi.wy_update.check(92): ' + str(e))
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
                flag = CommentUpdate().wy_update(messages()[0], self.web_url, video_message[1])
                if flag:
                    mess = TimeNow.get_time() + " 视频 : [ " + video_message[1] + " ] 没有更新信息。"
                    print (mess)
                    Log.log(mess)
                    conn.close()
        else:
            mess = TimeNow.get_time() + " 注意 : 数据库中没有该视频信息，其url : [ %s ]" % self.web_url
            print (mess)
            Log.log(mess)
            try:
                VideoMysql(self.web_url, messages()[1][1], messages()[0], video_message, video_url).wy_mysql()
                CommentUpdate().wy_update(messages()[0], self.web_url, video_message[1])
            except Exception as e:
                print ("videocheck.videoupdate.wy_update.wy_mysql(119): " + str(e))

    def fh_update(self):
        video_message = FengHuang().fh_message(self.web_url)
        flags = check_url(self.web_url, video_message, messages()[1][2], messages()[0], " ")

        flag1 = flags[0]
        flag2 = flags[1]
        flag3 = flags[2]
        check = ''

        conn = messages()[0]
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
                print ('videocheck.fenghuang.fh_update(141): ' + str(e))
                conn.rollback()
            cur.close()

            flags = update_message(check, conn, self.web_url, video_message)
            flag4 = flags[0]
            flag5 = flags[1]
            flag6 = flags[2]
            flag7 = flags[3]

            if flag4 and flag5 and flag6 and flag7:
                flag = CommentUpdate().fh_update(messages()[0], self.web_url, video_message[1])
                if flag:
                    mess = TimeNow.get_time() + " 视频 : [ " + video_message[1] + " ] 没有更新信息。"
                    print (mess)
                    Log.log(mess)
                    conn.close()
        else:
            mess = TimeNow.get_time() + " 注意 : 数据库中没有该视频信息，其url : [ %s ]" % self.web_url
            print (mess)
            Log.log(mess)
            try:
                VideoMysql(self.web_url, messages()[1][2], messages()[0], video_message, '').fh_mysql()
                CommentUpdate().fh_update(messages()[0], self.web_url, video_message[1])
            except Exception as e:
                print ("videocheck.videoupdate.fh_update.fh_mysql(166): " + str(e))

    def mg_update(self):
        video_message = MangoTV().mg_message(self.web_url)
        flags = check_url(self.web_url, video_message, messages()[1][3], messages()[0], " ")

        flag1 = flags[0]
        flag2 = flags[1]
        flag3 = flags[2]
        check = ''

        conn = messages()[0]
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
                print ('videocheck.mangotv.mg_update(188): ' + str(e))
                conn.rollback()
            cur.close()

            flags = update_message(check, conn, self.web_url, video_message)
            flag4 = flags[0]
            flag5 = flags[1]
            flag6 = flags[2]

            if flag4 and flag5 and flag6:
                flag = CommentUpdate().mg_update(messages()[0], self.web_url, video_message[1])
                if flag:
                    mess = TimeNow.get_time() + " 视频 : [ " + video_message[1] + " ] 没有更新信息。"
                    print (mess)
                    Log.log(mess)
                    conn.close()
        else:
            mess = TimeNow.get_time() + " 注意 : 数据库中没有该视频信息，其url : [ %s ]" % self.web_url
            print (mess)
            Log.log(mess)
            try:
                VideoMysql(self.web_url, messages()[1][3], messages()[0], video_message, '').mg_mysql()
                CommentUpdate().mg_update(messages()[0], self.web_url, video_message[1])
            except Exception as e:
                print ("videocheck.videoupdate.mg_update.mg_mysql(212): " + str(e))

    def sh_update(self):
        video_message = SouHu().sh_message(self.web_url)
        flags = check_url(self.web_url, video_message, messages()[1][4], messages()[0], " ")

        flag1 = flags[0]
        flag2 = flags[1]
        flag3 = flags[2]
        check = ''

        conn = messages()[0]
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
                print ('videocheck.souhu.sh_update.check(234): ' + str(e))
                conn.rollback()
            cur.close()

            flags = update_message(check, conn, self.web_url, video_message)
            flag4 = flags[0]

            if flag4:
                flag = CommentUpdate().sh_update(messages()[0], self.web_url, video_message[1])
                if flag:
                    mess = TimeNow.get_time() + " 视频 : [ " + video_message[1] + " ] 没有更新信息。"
                    print (mess)
                    Log.log(mess)
                    conn.close()
        else:
            mess = TimeNow.get_time() + " 注意 : 数据库中没有该视频信息，其url : [ %s ]" % self.web_url
            print (mess)
            Log.log(mess)
            try:
                VideoMysql(self.web_url, messages()[1][4], messages()[0], video_message, '').sh_mysql()
                CommentUpdate().sh_update(messages()[0], self.web_url, video_message[1])
            except Exception as e:
                print ("videocheck.videoupdate.sh_update.sh_mysql(256): " + str(e))
