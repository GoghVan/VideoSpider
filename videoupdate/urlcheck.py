# -*- coding: utf-8 -*-
from video.videoupdate.lostmess import LostMessage


def check_url(web_url, video_message, file_name, connect, video_url):
    flag1 = 0
    flag2 = 0
    flag3 = 0
    number = 0
    sql1 = sql2 = " "

    if ('http://rr.tv/' in web_url or 'http://www.rr.tv/' in web_url) and file_name == "renren":
        LostMessage(web_url, video_message, file_name, connect, video_url).lost_mess()
        sql1 = "SELECT COUNT(*)" \
            " FROM renren"                                                  # 获取数据库存放的数据量
        sql2 = "SELECT Video_Web,Video_Size,Video_Name" \
            " FROM renren"
    if 'http://v.163.com/' in web_url and file_name == "wangyi":
        LostMessage(web_url, video_message, file_name, connect, video_url).lost_mess()
        sql1 = "SELECT COUNT(*) " \
            "FROM wangyi"
        sql2 = "SELECT Video_Web,Video_Size,Video_Name " \
            "FROM wangyi"
    if 'http://v.ifeng.com/' in web_url and file_name == "fenghuang":
        LostMessage(web_url, video_message, file_name, connect, " ").lost_mess()
        sql1 = "SELECT COUNT(*) " \
            "FROM fenghuang"
        sql2 = "SELECT Video_Web,Video_Size,Video_Name " \
            "FROM fenghuang"

    conn = connect
    cur = conn.cursor()
    try:
        cur.execute(sql1)
        number = cur.fetchone()[0]
        conn.commit()
    except Exception as e:
        print (e)
        conn.rollback()
    cur.close()

    cur = conn.cursor()
    try:
        cur.execute(sql2)
        while number:
            results = cur.fetchone()
            if web_url == results[0].encode('utf8'):
                flag1 = 1
            else:
                flag1 = 0
            if str(video_message[3]) == results[1].encode('utf8'):
                flag2 = 1
            else:
                flag2 = 0
            if video_message[1] == results[2].encode('utf8'):
                flag3 = 1
            else:
                flag3 = 0
            if flag1 and flag2 and flag3:
                break
            number = number - 1
        conn.commit()
    except Exception as e:
        print (e)
        conn.rollback()
    cur.close()
    return flag1, flag2, flag3
