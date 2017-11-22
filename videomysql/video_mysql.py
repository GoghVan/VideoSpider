# -*- coding: utf-8 -*-
# @Time    : 2017/11/20 21:23
# @Author  : Gavin

from video.videodownload.download import DownloadVideo


class VideoMysql(object):
    def __init__(self, web_url, file_name, connect, video_message, video_url):
        self.web_url = web_url
        self.file_name = file_name
        self.connect = connect
        self.video_message = video_message
        self.video_url = video_url

    def sh_mysql(self):
        count = 0
        video_file = ''
        while count < len(self.video_message[7]):
            video_name = self.video_message[1] + '(' + str(count) + ')'
            video_file = DownloadVideo(self.video_message[7][count], unicode(video_name, "utf-8"), self.file_name)\
                .video_download()
            count += 1

        conn = self.connect
        cur = conn.cursor()
        sql = "INSERT INTO souhu(Video_Id, Video_Name, Video_Author, Video_Size, Video_Time, Video_Modify" \
              ", Video_View, Video_Web, Video_Url, Video_File) " \
              "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        try:
            cur.execute(sql, (self.video_message[0], self.video_message[1], self.video_message[2],
                              self.video_message[3], self.video_message[4], self.video_message[5],
                              self.video_message[6], self.web_url, self.video_message[7][count - 1],
                              video_file))
            conn.commit()
        except Exception as e:
            print ('souhu.sh_mysql: ' + str(e))
            conn.rollback()
        cur.close()

    def mg_mysql(self):
        count = 0
        video_file = ''
        conn = self.connect
        while count < len(self.video_message[9]):
            video_name = self.video_message[1] + '(' + str(count) + ')'
            video_file = DownloadVideo(self.video_message[9][count], unicode(video_name, "utf-8"), self.file_name)\
                .video_download()
            count += 1
        cur = conn.cursor()
        sql = "INSERT INTO mangotv(Video_Id, Video_Name, Video_Author, Video_Size, Video_Time, Video_Modify" \
              ", Video_View, Video_Oppose, Video_Support, Video_Web, Video_Url, Video_File) " \
              "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        try:
            cur.execute(sql, (self.video_message[0], self.video_message[1], self.video_message[2],
                              self.video_message[3][count - 1], self.video_message[4], self.video_message[5],
                              self.video_message[6], self.video_message[7], self.video_message[8], self.web_url,
                              self.video_message[9][count - 1], video_file))
            conn.commit()
        except Exception as e:
            print ('mangotv.mg_mysql: ' + str(e))
            conn.rollback()
        cur.close()

    def fh_mysql(self):
        video_file = DownloadVideo(self.video_message[10], unicode(self.video_message[1], "utf-8"), self.file_name)\
            .video_download()

        conn = self.connect
        cur = conn.cursor()
        sql = "INSERT INTO fenghuang(Video_Id, Video_Name, Video_Author, Video_Size, Video_Time, Video_Modify" \
              ", Video_View, Video_Oppose, Video_Support, Video_Comment, Video_Web, Video_Url, Video_File) " \
              "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        try:
            cur.execute(sql, (self.video_message[0], self.video_message[1], self.video_message[2],
                              self.video_message[3], self.video_message[4], self.video_message[5],
                              self.video_message[6], self.video_message[7], self.video_message[8],
                              self.video_message[9], self.web_url, self.video_message[10], video_file))
            conn.commit()
        except Exception as e:
            print ('fenghuang.fh_mysql: ' + str(e))
            conn.rollback()
        cur.close()

    def wy_mysql(self):
        # 注意文件名要以Unicode形式存储
        video_file = DownloadVideo(self.video_url, unicode(self.video_message[1], "utf-8"), self.file_name).\
            video_download()

        conn = self.connect
        cur = conn.cursor()
        sql = "INSERT INTO wangyi(Video_Id, Video_Name, Video_Author, Video_Size, Video_Time, Video_modify" \
              ", Video_View, Video_Oppose, Video_Support, Video_Comment, Video_Comment_Fav, Video_Comment_Against" \
              ", Video_Web, Video_Url, Video_File) " \
              "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        try:
            cur.execute(sql, (self.video_message[0], self.video_message[1], self.video_message[2],
                              self.video_message[3], self.video_message[4], self.video_message[5],
                              self.video_message[6], self.video_message[7], self.video_message[8],
                              self.video_message[9], self.video_message[10], self.video_message[11],
                              self.web_url, self.video_url, video_file))
            conn.commit()
        except Exception as e:
            print ('wangyi.wy_mysql: ' + str(e))
            conn.rollback()
        cur.close()

    def rr_mysql(self):
        video_file = DownloadVideo(self.video_url, unicode(self.video_message[1], "utf-8"), self.file_name).\
            video_download()

        conn = self.connect
        cur = conn.cursor()
        sql = "INSERT INTO renren(Video_Id, Video_Name, Video_Author, Video_Size, Video_Time, " \
            "Video_View, Video_Support, Video_Comment, Video_Web, Video_Url, Video_File) " \
            "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        try:
            cur.execute(sql, (self.video_message[0], self.video_message[1], self.video_message[2],
                              self.video_message[3], self.video_message[4], self.video_message[5],
                              self.video_message[6], self.video_message[7], self.web_url, self.video_url, video_file))
            conn.commit()
        except Exception as e:
            print ('renren.rr_mysql: ' + str(e))
            conn.rollback()
        cur.close()
