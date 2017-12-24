# -* coding: utf-8 -*-
import MySQLdb
from video.messageparse.renren import RenRen
from video.messageparse.mangotv import MangoTV
from video.messageparse.fenghuang import FengHuang
from video.messageparse.souhu import SouHu
from video.messageparse.wangyi import WangYi


# 没有用到
class MessageMysql(object):
    connect = MySQLdb.connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='1479',
        db='video',
        charset="utf8",
    )

    def sh_mysql(self, web_url):
        message = SouHu().sh_comment(web_url)
        vid = message[1]
        content = message[0]
        conn = self.connect
        cur = conn.cursor()
        sql = "INSERT INTO sh(vid,content)" \
              "VALUES (%s,%s)"
        try:
            cur.execute(sql, (vid, content))
            cur.close()
            conn.commit()
        except Exception as e:
            conn.rollback()
            print ('sohu.sh_mysql.comment:'+str(e))
        conn.close()

    def mg_mysql(self, web_url):
        conn = self.connect
        message = MangoTV().mg_comment(web_url)
        vid = message[1]
        content = message[0]
        cur = conn.cursor()
        sql = "INSERT INTO mg(vid,content)" \
              "VALUES (%s,%s)"
        try:
            cur.execute(sql, (vid, content))
            conn.commit()
        except Exception as e:
            print ('mangotv.mg_mysql.comment: ' + str(e))
        cur.close()

    def fh_mysql(self, web_url):
        message = FengHuang().fh_comment(web_url)
        vid = message[1]
        content = message[0]
        conn = self.connect
        cur = conn.cursor()
        sql = "INSERT INTO fh(vid, content)" \
              "VALUES (%s, %s)"
        try:
            cur.execute(sql, (vid, content))
            cur.close()
            conn.commit()
        except Exception as e:
            print ('fenghuangtv.mg_mysql.comment: ' + str(e))
            conn.rollback()
        conn.close()

    def wy_mysql(self, web_url):
        message = WangYi().wy_comment(web_url)
        vid = message[1]
        content = message[0]
        conn = self.connect
        cur = conn.cursor()
        sql = "INSERT INTO wy(vid, content)" \
              "VALUES (%s, %s)"
        try:
            cur.execute(sql, (vid, content))
            cur.close()
            conn.commit()
        except Exception as e:
            print ('wangyitv.mg_mysql.comment: ' + str(e))
            conn.rollback()
        conn.close()

    def rr_mysql(self, web_url):
        conn = self.connect
        message = RenRen().rr_comment(web_url)
        content = message[0]
        vid = message[1]
        cur = conn.cursor()
        sql = "INSERT INTO rr(vid,content)" \
              "VALUES (%s,%s)"
        cur.execute(sql, (vid, content))
        cur.close()
        conn.commit()
