# -*- coding: utf-8 -*-
import MySQLdb
from video.src.log import Log
from video.src.timenow import TimeNow


class UpdateVideo(object):
    def __init__(self, web_url, table):
        self.web_url = web_url
        self.table = table

    def rr_update(self):
        global flag1, flag2, flag3, flag4, flag5, flag6, number
        global lost_url
        lost_url = ''
        flag1 = 0
        flag2 = 0
        flag3 = 0
        flag4 = 0
        flag5 = 0
        flag6 = 0
        number = 0

        conn = MySQLdb.connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='1479',
            db='videos',
            charset='utf8',
        )

        self.lost_mess(self.web_url)

        try:
            cur1 = conn.cursor()
            sql1 = "SELECT COUNT(*)" \
                   " FROM %s"                       # 获取数据库存放的数据量
            cur1.execute(sql1, self.table)
            number = cur1.fetchone()[0]             # 数据库的数据量
            cur1.close()
            conn.commit()
        except Exception as e:
            conn.rollback()
            print (e)

        video_message = self.rr_message(self.web_url)

        try:
            cur2 = conn.cursor()
            sql2 = "SELECT Video_Web,Video_Size,Video_Name" \
                   " FROM %s"
            cur2.execute(sql2, self.table)
            while number:
                results = cur2.fetchone()
                if self.web_url.encode('utf8') == results[0].encode('utf8'):
                    flag1 = 1
                else:
                    flag1 = 0
                if str(video_message[6]) == results[1].encode('utf8'):
                    flag2 = 1
                else:
                    flag2 = 0
                if video_message[0].encode('utf8') == results[2].encode('utf8'):
                    flag3 = 1
                else:
                    flag3 = 0
                if flag1 and flag2 and flag3:
                    break
                number = number - 1
            cur2.close()
            conn.commit()
        except Exception as e:
            conn.rollback()
            print (e)

        if flag1 and flag2 and flag3:
            check = ''
            try:
                cur3 = conn.cursor()
                sql3 = "SELECT Video_ViewCount,Video_CommentCount,Video_FavCount " \
                       "FROM %s " \
                       "WHERE Video_Web=%s AND Video_Size=%s AND Video_Name=%s"
                cur3.execute(sql3, (self.table, self.web_url, video_message[6], video_message[0]))
                check = cur3.fetchone()
                cur3.close()
                conn.commit()
            except Exception as e:
                conn.rollback()
                print (e)

            try:
                cur4 = conn.cursor()
                sql4 = "UPDATE %s " \
                       "SET Video_ViewCount=%s " \
                       "WHERE Video_Web=%s"

                if check[0].encode('utf8') != str(video_message[3]):
                    cur4.execute(sql4, (self.table, video_message[3], self.web_url))
                    mess = TimeNow.get_time() + " 视频 : [ " + video_message[0].encode('utf8') + " ] 的Video_ViewCount : " \
                            + check[0].encode('utf8') + ", 现在Video_ViewCount : " + str(video_message[3])
                    print (mess)
                    Log.log(mess)
                    flag4 = 0
                else:
                    flag4 = 1
                cur4.close()
                conn.commit()

                cur5 = conn.cursor()
                sql5 = "UPDATE %s " \
                       "SET Video_CommentCount=%s " \
                       "WHERE Video_Web=%s"

                if check[1].encode('utf8') != str(video_message[4]):
                    cur5.execute(sql5, (self.table, video_message[4], self.web_url))
                    mess = TimeNow.get_time() + " 视频 : [ " + video_message[0].encode('utf8') + " ] 的Video_CommentCount : " \
                            + check[1].encode('utf8') + ", 现在Video_CommentCount : " + str(video_message[4])
                    print (mess)
                    Log.log(mess)
                    flag5 = 0
                else:
                    flag5 = 1
                cur5.close()
                conn.commit()

                cur6 = conn.cursor()
                sql6 = "UPDATE %s " \
                       "SET Video_FavCount=%s " \
                       "WHERE Video_Web=%s"

                if check[2].encode('utf8') != str(video_message[5]):
                    cur6.execute(sql6, (self.table, video_message[5], self.web_url))
                    mess = TimeNow.get_time() + " 视频 : [ " + video_message[0].encode('utf8') + " ] 的Video_FavCount : " \
                            + check[2].encode('utf8') + ", 现在Video_FavCount : " + str(video_message[5])
                    print (mess)
                    Log.log(mess)
                    flag6 = 0
                else:
                    flag6 = 1
                cur6.close()
                conn.commit()

                if flag4 and flag5 and flag6:
                    mess = TimeNow.get_time() + " 视频 : [ " + video_message[0].encode('utf8') + " ] 没有更新信息。"
                    print (mess)
                    Log.log(mess)

            except Exception as e:
                conn.rollback()
                print (e)
        else:
            mess = TimeNow.get_time() + " 注意 : 数据库中没有该视频信息，其url : [ %s ]" % self.web_url
            print (mess)
            Log.log(mess)
            lost_url = self.web_url
        conn.close()
        return lost_url
