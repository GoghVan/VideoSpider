# -*- coding: utf-8 -*-
# @Time    : 2017/11/16 20:23
# @Author  : Gavin

from video.src.log import Log
from video.src.timenow import TimeNow


def update_message(check, connect, web_url, video_message):
    sql1 = sql2 = sql3 = sql4 = sql5 = sql6 = ''
    point = 0
    if 'http://rr.tv/' in web_url or 'http://www.rr.tv/' in web_url:
        point = 1
        sql1 = "UPDATE renren " \
               "SET Video_View=%s " \
               "WHERE Video_Web=%s"
        sql2 = "UPDATE renren " \
               "SET Video_Support=%s " \
               "WHERE Video_Web=%s"
        sql4 = "UPDATE renren " \
               "SET Video_Comment=%s " \
               "WHERE Video_Web=%s"

    if 'http://v.163.com/' in web_url:
        point = 2
        sql1 = "UPDATE wangyi " \
               "SET Video_View=%s " \
               "WHERE Video_Web=%s"
        sql2 = "UPDATE wangyi " \
               "SET Video_Support=%s " \
               "WHERE Video_Web=%s"
        sql3 = "UPDATE wangyi " \
               "SET Video_Oppose=%s " \
               "WHERE Video_Web=%s"
        sql4 = "UPDATE wangyi " \
               "SET Video_Comment=%s " \
               "WHERE Video_Web=%s"
        sql5 = "UPDATE wangyi " \
               "SET Video_Comment_Fav=%s " \
               "WHERE Video_Web=%s"
        sql6 = "UPDATE wangyi " \
               "SET video_comment_against=%s " \
               "WHERE Video_Web=%s"

    if 'http://v.ifeng.com/' in web_url:
        point = 3
        sql1 = "UPDATE fenghuang " \
               "SET Video_View=%s " \
               "WHERE Video_Web=%s"
        sql2 = "UPDATE fenghuang " \
               "SET Video_Support=%s " \
               "WHERE Video_Web=%s"
        sql3 = "UPDATE fenghuang " \
               "SET Video_Oppose=%s " \
               "WHERE Video_Web=%s"
        sql4 = "UPDATE fenghuang " \
               "SET Video_Comment=%s " \
               "WHERE Video_Web=%s"

    if 'https://www.mgtv.com' in web_url:
        point = 4
        sql1 = "UPDATE mangotv " \
               "SET Video_View=%s " \
               "WHERE Video_Web=%s"
        sql2 = "UPDATE mangotv " \
               "SET Video_Support=%s " \
               "WHERE Video_Web=%s"
        sql3 = "UPDATE mangotv " \
               "SET Video_Oppose=%s " \
               "WHERE Video_Web=%s"

    if 'http://my.tv.sohu.com/' in web_url or 'https://my.tv.sohu.com/' in web_url \
            or 'https://tv.sohu.com/' in web_url or 'http://tv.sohu.com/' in web_url:
        point = 5
        sql1 = "UPDATE souhu " \
               "SET Video_View=%s " \
               "WHERE Video_Web=%s"

    conn = connect
    # 视频观看数
    cur = conn.cursor()
    if (point == 1 or point == 2 or point == 3 or point == 4 or point == 5) \
        and ((point != 1 and check[0].encode('utf8') != str(video_message[6]))
             or (point == 1 and check[0].encode('utf8') != str(video_message[5]))):
        try:
            if point == 1:
                cur.execute(sql1, (video_message[5], web_url))
            else:
                cur.execute(sql1, (video_message[6], web_url))
            conn.commit()
        except Exception as e:
            print ('messupdate.update_message.video_view: ' + str(e))
            conn.rollback()
        if point == 1:
            mess = TimeNow.get_time() + " 视频 : [ " + video_message[1] + " ] 的Video_View : " \
                + check[0].encode('utf8') + ", 现在Video_View : " + str(video_message[5])
        else:
            mess = TimeNow.get_time() + " 视频 : [ " + video_message[1] + " ] 的Video_View : " \
                + check[0].encode('utf8') + ", 现在Video_View : " + str(video_message[6])
        print (mess)
        Log.log(mess)
        flag4 = 0
    else:
        flag4 = 1
    cur.close()

    # 视频不点赞数
    cur = conn.cursor()
    if (point == 2 or point == 3 or point == 4) and check[1].encode('utf8') != str(video_message[7]):
        try:
            cur.execute(sql3, (video_message[7], web_url))
            conn.commit()
        except Exception as e:
            print ('messupdate.update_message.video_oppose: ' + str(e))
            conn.rollback()
        mess = TimeNow.get_time() + " 视频 : [ " + video_message[1] + " ] 的Video_Oppose : " \
            + check[1].encode('utf8') + ", 现在Video_Oppose : " + video_message[7]
        print (mess)
        Log.log(mess)
        flag5 = 0
    else:
        flag5 = 1
    cur.close()

    # 视频点赞数
    cur = conn.cursor()
    if (point == 1 or point == 2 or point == 3 or point == 4) \
        and (point != 1 and check[2].encode('utf8') != str(video_message[8])
             or (point == 1 and check[1].encode('utf8') != str(video_message[6]))):
        try:
            if point == 1:
                cur.execute(sql2, (video_message[6], web_url))
            else:
                cur.execute(sql2, (video_message[8], web_url))
            conn.commit()
        except Exception as e:
            print ('messupdate.update_message.video_support: ' + str(e))
            conn.rollback()
        if point == 1:
            mess = TimeNow.get_time() + " 视频 : [ " + video_message[1] + " ] 的Video_Support : " \
                   + check[1].encode('utf8') + ", 现在Video_Support : " + str(video_message[6])
        else:
            mess = TimeNow.get_time() + " 视频 : [ " + video_message[1] + " ] 的Video_Support : " \
                + check[2].encode('utf8') + ", 现在Video_Support : " + str(video_message[8])
        print (mess)
        Log.log(mess)
        flag6 = 0
    else:
        flag6 = 1
    cur.close()

    # 视频评论数
    cur = conn.cursor()
    if (point == 1 or point == 2 or point == 3) \
        and (point != 1 and check[3].encode('utf8') != str(video_message[9])
             or (point == 1 and check[2].encode('utf8') != str(video_message[7]))):
        try:
            if point == 1:
                cur.execute(sql4, (video_message[7], web_url))
            else:
                cur.execute(sql4, (video_message[9], web_url))
            conn.commit()
        except Exception as e:
            print ('messupdate.update_message.video_comment: ' + str(e))
            conn.rollback()
        if point == 1:
            mess = TimeNow.get_time() + " 视频 : [ " + video_message[1] + " ] 的Video_Comment : " \
                   + check[2].encode('utf8') + ", 现在Video_Comment : " + str(video_message[7])
        else:
            mess = TimeNow.get_time() + " 视频 : [ " + video_message[1] + " ] 的Video_Comment : " \
                + check[3].encode('utf8') + ", 现在Video_Comment : " + str(video_message[9])
        print (mess)
        Log.log(mess)
        flag7 = 0
    else:
        flag7 = 1
    cur.close()

    # 视频评论点赞数
    cur = conn.cursor()
    if point == 2 and check[4].encode('utf8') != str(video_message[10]):
        try:
            cur.execute(sql5, (video_message[10], web_url))
            conn.commit()
        except Exception as e:
            print ('messupdate.update_message.video_comment_fav: ' + str(e))
            conn.rollback()
        mess = TimeNow.get_time() + " 视频 : [ " + video_message[1] + " ] 的Video_Comment_Fav : " \
            + check[4].encode('utf8') + ", 现在Video_Comment_Fav : " + video_message[10]
        print (mess)
        Log.log(mess)
        flag8 = 0
    else:
        flag8 = 1
    cur.close()

    # 视频评论不点赞数
    cur = conn.cursor()
    if point == 2 and check[5].encode('utf8') != str(video_message[11]):
        try:
            cur.execute(sql6, (video_message[11], web_url))
            conn.commit()
        except Exception as e:
            print ('messupdate.update_message.video_comment_against: ' + str(e))
            conn.rollback()
        mess = TimeNow.get_time() + " 视频 : [ " + video_message[1] + " ] 的video_comment_against : " \
            + check[5].encode('utf8') + ", 现在video_comment_against : " + video_message[11]
        print (mess)
        Log.log(mess)
        flag9 = 0
    else:
        flag9 = 1
    cur.close()
    return flag4, flag5, flag6, flag7, flag8, flag9
