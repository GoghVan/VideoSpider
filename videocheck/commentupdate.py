# -* coding: utf-8 -*-
from video.src.log import Log
from video.src.timenow import TimeNow
from video.messageparse.renren import RenRen
from video.messageparse.mangotv import MangoTV
from video.messageparse.fenghuang import FengHuang
from video.messageparse.wangyi import WangYi
from video.messageparse.souhu import SouHu


# 调用下载视频评论函数，将单个视频评论获取下来，然后连接数据库，与数据库中对应的评论进行字符串对比，
# 如果如果数据库中的评论字符串中没有此字符串，那就执行增加操作，将
# 该字符串存入数据库的那个字符串中（执行更行操作）。
class CommentUpdate(object):
    def __init__(self):
        pass

    @staticmethod
    def rr_update(conn, web_url, video_name):
        # 人人视频
        result = ''
        message = RenRen().rr_comment(web_url)
        vid = message[1]
        content = message[0]
        cur = conn.cursor()
        sql1 = "SELECT vid FROM rr"
        try:
            cur.execute(sql1)
            result = cur.fetchall()
            conn.commit()
        except Exception as e:
            print ('videocheck.commentupdate.update.rr(32): ' + str(e))
            conn.rollback()
        cur.close()
        if (vid.encode('utf8'),) in result:

            cur = conn.cursor()
            sql1 = "SELECT content FROM rr WHERE vid = %s"
            try:
                cur.execute(sql1, vid)
                result = cur.fetchone()
                conn.commit()
            except Exception as e:
                print ('videocheck.commentupdate.update.rr(44): ' + str(e))
                conn.rollback()
            cur.close()

            if len(content) == 0 and result == None:
                return 1
            elif len(content) != 0 and result == None:
                cur = conn.cursor()
                sql = "UPDATE rr SET content = %s WHERE vid = %s"
                try:
                    cur.execute(sql, (content, vid))
                    conn.commit()
                except Exception as e:
                    print ('videocheck.commentupdate.update.rr(57): ' + str(e))
                    conn.rollback()
                cur.close()
                mess = TimeNow.get_time() + " 视频 : [ " + video_name + " ] 评论更新完毕。"
                print (mess)
                Log.log(mess)
                return 0
            elif content in result[0].encode('utf8'):
                cur = conn.cursor()
                sql = "UPDATE rr SET content = %s WHERE vid = %s"
                try:
                    cur.execute(sql, (content, vid))
                    conn.commit()
                except Exception as e:
                    print ('videocheck.commentupdate.update.rr(71): ' + str(e))
                    conn.rollback()
                cur.close()
                mess = TimeNow.get_time() + " 视频 : [ " + video_name + " ] 评论更新完毕。"
                print (mess)
                Log.log(mess)
                return 0
        else:
            cur = conn.cursor()
            sql = "INSERT INTO rr(vid,content) VALUES (%s,%s)"
            try:
                cur.execute(sql, (vid, content))
                conn.commit()
            except Exception as e:
                print ('videocheck.commentupdate.update.rr(85): ' + str(e))
                conn.rollback()
            cur.close()
            mess = TimeNow.get_time() + " 视频 : [ " + video_name + " ] 评论已插入数据库。"
            print (mess)
            Log.log(mess)

    @staticmethod
    def mg_update(conn, web_url, video_name):
        #  芒果TV
        result = ''
        message = MangoTV().mg_comment(web_url)
        vid = message[1]
        content = message[0]
        cur = conn.cursor()
        sql1 = "SELECT vid FROM mg"
        try:
            cur.execute(sql1)
            result = cur.fetchall()
            conn.commit()
        except Exception as e:
            print ('videocheck.commentupdate.update.mg(106): ' + str(e))
            conn.rollback()
        cur.close()

        if (vid.encode('utf8'),) in result:

            cur = conn.cursor()
            sql1 = "SELECT content FROM mg WHERE vid = %s"
            try:
                cur.execute(sql1, vid)
                result = cur.fetchone()
                conn.commit()
            except Exception as e:
                print ('videocheck.commentupdate.update.mg(119): ' + str(e))
                conn.rollback()
            cur.close()

            if len(content) == 0 and result == None:
                return 1
            elif len(content) != 0 and result == None:
                cur = conn.cursor()
                sql = "UPDATE mg SET content = %s WHERE vid = %s"
                try:
                    cur.execute(sql, (content, vid))
                    conn.commit()
                except Exception as e:
                    print ('videocheck.commentupdate.update.mg(132): '+str(e))
                    conn.rollback()
                cur.close()
                mess = TimeNow.get_time() + " 视频 : [ " + video_name + " ] 评论更新完毕。"
                print (mess)
                Log.log(mess)
                return 0
            elif content in result[0].encode('utf8'):
                cur = conn.cursor()
                sql = "UPDATE mg SET content = %s WHERE vid = %s"
                try:
                    cur.execute(sql, (content, vid))
                    conn.commit()
                except Exception as e:
                    print ('videocheck.commentupdate.update.mg(146): '+str(e))
                    conn.rollback()
                cur.close()
                mess = TimeNow.get_time() + " 视频 : [ " + video_name + " ] 评论更新完毕。"
                print (mess)
                Log.log(mess)
                return 0
        else:
            cur = conn.cursor()
            sql = "INSERT INTO mg(vid,content) VALUES (%s,%s)"
            try:
                cur.execute(sql, (vid, content))
                conn.commit()
            except Exception as e:
                print ('videocheck.commentupdate.update.mg(160): ' + str(e))
                conn.rollback()
            cur.close()
            mess = TimeNow.get_time() + " 视频 : [ " + video_name + " ] 评论已插入数据库。"
            print (mess)
            Log.log(mess)

    @staticmethod
    def wy_update(conn, web_url, video_name):
        # 网易视频
        result = ''
        message = WangYi().wy_comment(web_url)
        vid = message[1]
        content = message[0]
        cur = conn.cursor()
        sql1 = "SELECT vid FROM wy"
        try:
            cur.execute(sql1)
            result = cur.fetchall()
            conn.commit()
        except Exception as e:
            print ('videocheck.commentupdate.update.wy(181): ' + str(e))
            conn.rollback()
        cur.close()
        if (vid.encode('utf8'),) in result:

            cur = conn.cursor()
            sql1 = "SELECT content FROM wy WHERE vid = %s"
            try:
                cur.execute(sql1, vid)
                result = cur.fetchone()
                conn.commit()
            except Exception as e:
                print ('videocheck.commentupdate.update.wy(193): ' + str(e))
                conn.rollback()
            cur.close()

            if len(content) == 0 and result == None:
                return 1
            elif len(content) != 0 and result == None:
                cur = conn.cursor()
                sql = "UPDATE wy SET content = %s WHERE vid = %s"
                try:
                    cur.execute(sql, (content, vid))
                    conn.commit()
                except Exception as e:
                    print ('videocheckcommentupdate.update.wy(206): '+str(e))
                    conn.rollback()
                cur.close()
                mess = TimeNow.get_time() + " 视频 : [ " + video_name + " ] 评论更新完毕。"
                print (mess)
                Log.log(mess)
                return 0
            elif content in result[0].encode('utf8'):
                cur = conn.cursor()
                sql = "UPDATE wy SET content = %s WHERE vid = %s"
                try:
                    cur.execute(sql, (content, vid))
                    conn.commit()
                except Exception as e:
                    print ('videocheck.commentupdate.update.wy(220): '+str(e))
                    conn.rollback()
                cur.close()
                mess = TimeNow.get_time() + " 视频 : [ " + video_name + " ] 评论更新完毕。"
                print (mess)
                Log.log(mess)
                return 0
        else:
            cur = conn.cursor()
            sql = "INSERT INTO wy(vid,content) VALUES (%s,%s)"
            try:
                cur.execute(sql, (vid, content))
                conn.commit()
            except Exception as e:
                print ('videocheck.commentupdate.update.wy(234): ' + str(e))
                conn.rollback()
            cur.close()
            mess = TimeNow.get_time() + " 视频 : [ " + video_name + " ] 评论已插入数据库。"
            print (mess)
            Log.log(mess)

    @staticmethod
    def fh_update(conn, web_url, video_name):
        # 凤凰视频
        result = ''
        message = FengHuang().fh_comment(web_url)
        vid = message[1]
        content = message[0]
        cur = conn.cursor()
        sql1 = "SELECT vid FROM fh"
        try:
            cur.execute(sql1)
            result = cur.fetchall()
            conn.commit()
        except Exception as e:
            print ('videocheck.commentupdate.update.fh(255): ' + str(e))
            conn.rollback()
        cur.close()
        if (vid.encode('utf8'),) in result:

            cur = conn.cursor()
            sql1 = "SELECT content FROM rr WHERE vid = %s"
            try:
                cur.execute(sql1, vid)
                result = cur.fetchone()
                conn.commit()
            except Exception as e:
                print ('videocheck.commentupdate.update.fh(267): ' + str(e))
                conn.rollback()
            cur.close()

            if len(content) == 0 and result == None:
                return 1
            elif len(content) != 0 and result == None:
                cur = conn.cursor()
                sql = "UPDATE fh SET content = %s WHERE vid = %s"
                try:
                    cur.execute(sql, (content, vid))
                    conn.commit()
                except Exception as e:
                    print ('videocheck.commentupdate.update.fh(280): ' + str(e))
                    conn.rollback()
                cur.close()
                mess = TimeNow.get_time() + " 视频 : [ " + video_name + " ] 评论更新完毕。"
                print (mess)
                Log.log(mess)
                return 0
            elif content in result[0].encode('utf8'):
                cur = conn.cursor()
                sql = "UPDATE fh SET content = %s WHERE vid = %s"
                try:
                    cur.execute(sql, (content, vid))
                    conn.commit()
                except Exception as e:
                    print ('videocheck.commentupdate.update.fh(294): ' + str(e))
                    conn.rollback()
                cur.close()
                mess = TimeNow.get_time() + " 视频 : [ " + video_name + " ] 评论更新完毕。"
                print (mess)
                Log.log(mess)
                return 0
        else:
            cur = conn.cursor()
            sql = "INSERT INTO fh(vid,content) VALUES (%s,%s)"
            try:
                cur.execute(sql, (vid, content))
                conn.commit()
            except Exception as e:
                print ('videocheck.commentupdate.update.fh(308): ' + str(e))
                conn.rollback()
            cur.close()
            mess = TimeNow.get_time() + " 视频 : [ " + video_name + " ] 评论已插入数据库。"
            print (mess)
            Log.log(mess)

    @staticmethod
    def sh_update(conn, web_url, video_name):
        # 搜狐视频
        result = ''
        message = SouHu().sh_comment(web_url)
        vid = message[1]
        content = message[0]
        cur = conn.cursor()
        sql1 = "SELECT vid FROM sh"
        try:
            cur.execute(sql1)
            result = cur.fetchall()
            conn.commit()
        except Exception as e:
            print ('videocheck.commentupdate.update.sh(329): ' + str(e))
        cur.close()
        if (vid.encode('utf8'),) in result:

            cur = conn.cursor()
            sql1 = "SELECT content FROM rr WHERE vid = %s"
            try:
                cur.execute(sql1, vid)
                result = cur.fetchone()
                conn.commit()
            except Exception as e:
                print ('videocheck.commentupdate.update.sh(340): ' + str(e))
                conn.rollback()
            cur.close()

            if len(content) == 0 and result == None:
                return 1
            elif len(content) != 0 and result == None:
                cur = conn.cursor()
                sql = "UPDATE sh SET content = %s WHERE vid = %s"
                try:
                    cur.execute(sql, (content, vid))
                    conn.commit()
                except Exception as e:
                    print ('videocheck.commentupdate.update.sh(353): ' + str(e))
                    conn.rollback()
                cur.close()
                mess = TimeNow.get_time() + " 视频 : [ " + video_name + " ] 评论更新完毕。"
                print (mess)
                Log.log(mess)
                return 0
            elif content in result[0].encode('utf8'):
                cur = conn.cursor()
                sql = "UPDATE sh SET content = %s WHERE vid = %s"
                try:
                    cur.execute(sql, (content, vid))
                    conn.commit()
                except Exception as e:
                    print ('videocheck.commentupdate.update.sh(367): ' + str(e))
                    conn.rollback()
                cur.close()
                mess = TimeNow.get_time() + " 视频 : [ " + video_name + " ] 评论更新完毕。"
                print (mess)
                Log.log(mess)
                return 0
        else:
            cur = conn.cursor()
            sql = "INSERT INTO sh(vid,content) VALUES (%s,%s)"
            try:
                cur.execute(sql, (vid, content))
                conn.commit()
            except Exception as e:
                print ('videocheck.commentupdate.update.sh(381): ' + str(e))
                conn.rollback()
            cur.close()
            mess = TimeNow.get_time() + " 视频 : [ " + video_name + " ] 评论已插入数据库。"
            print (mess)
            Log.log(mess)
