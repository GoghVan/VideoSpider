# -*- coding: utf-8 -*-
import re
import os
import sys
import json
import MySQLdb
import requests
import MySQLdb.cursors
from video.src.log import Log
from video.src.timenow import TimeNow
from video.videodownload.download import DownloadVideo

reload(sys)
sys.setdefaultencoding('utf8')


class RenRen(object):
    def __init__(self):
        pass

    @staticmethod
    def rr_url(url):
        headers = {
            'clientVersion': '0.1.0',
            'clientType': 'web',
        }                                                                                           # 添加客户端版本信息

        try:
            video_id = re.search(r'[0-9]+', url).group()                                       #获取视频的ID
            api_url = 'http://api.rr.tv/v3plus/video/getVideoPlayLinkByVideoId'                     #调用视频接口
            req_js = requests.post(api_url, data={'videoId': video_id}, headers=headers).content    #发送请求获取数据
            req_py = json.loads(req_js)                                                             #将JSON数据转换为Python数据
            video_url = req_py["data"]["playLink"]                                                  #获取视频地址URL
            return video_url
        except Exception as e:
            print (e)

    @staticmethod
    def rr_message(url):
        headers = {
            'clientVersion': '0.1.0',
            'clientType': 'web',
        }  # 添加客户端版本信息

        try:
            video_id = re.search(r'[0-9]+', url).group()                                           # 获取视频的ID
            api_url = 'http://web.rr.tv/v3plus/video/detail'                                            #调用信息接口
            req_js = requests.post(api_url, data={'videoId': video_id}, headers=headers).content        #发送请求获取数据
            req_py = json.loads(req_js)                                                                 #将JSON数据转换为Python数据
            video_name = req_py["data"]["videoDetailView"]["title"]                                     #获取视频名称
            video_author = req_py["data"]["videoDetailView"]["author"]["nickName"]                      #获取视频作者
            video_comment_count = req_py["data"]["videoDetailView"]["commentCount"]                     #获取视频评论数
            video_fav_count = req_py["data"]["videoDetailView"]["favCount"]                             #获取视频点赞数
            video_time = req_py["data"]["videoDetailView"]["duration"]                                  #获取视频时长
            video_view_count = req_py["data"]["videoDetailView"]["viewCount"]                           #获取视频观看次数
            video_size = req_py["data"]["videoDetailView"]["videoFileView"][1]["fileSize"]              #视频大小
            return video_name, video_author, video_time, video_view_count, video_comment_count, \
                   video_fav_count, video_size, video_id
        except Exception as e:
            print (e)

    def lost_update(self, url):

        video_url = self.rr_url(url)
        video_message = self.rr_message(url)
        download_video = DownloadVideo(video_url, video_message)
        video_url_file = download_video.video_download()

        conn = MySQLdb.connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='1479',
            db='videos',
            charset="utf8",
        )

        try:
            cur = conn.cursor()
            sql = "UPDATE test " \
                  "SET Video_Id=%s,Video_Name=%s,Video_Url=%s,Video_Author=%s,Video_Time=%s,Video_Size=%s," \
                  "Video_ViewCount=%s,Video_CommentCount=%s,Video_FavCount=%s,File_Url=%s " \
                  "WHERE Video_Web=%s"
            cur.execute(sql, (video_message[7], video_message[0], video_url, video_message[1],
                              video_message[2],video_message[6], video_message[3], video_message[4],
                              video_message[5], video_url_file, url))
            cur.close()
            conn.commit()
        except Exception as e:
            conn.rollback()
            print (e)
        mess = TimeNow.get_time() + ' 注意 : [ ' + video_message[0].encode('utf8') + ' ] 信息已补全，请注意查看！'
        print (mess)
        Log.log(mess)

    @staticmethod
    def rr_mysql(url, video_url, video_message, video_url_file):

        if video_url:
            conn = MySQLdb.connect(
                host='localhost',
                port=3306,
                user='root',
                passwd='1479',
                db='videos',
                charset="utf8",
            )
            cur = conn.cursor()
            sql = "INSERT INTO test(Video_Id, Video_Name, Video_Url, Video_Author, Video_Time, Video_Size, " \
                  "Video_ViewCount, Video_CommentCount, Video_FavCount, Video_Web, File_Url) " \
                  "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            try:
                cur.execute(sql, (video_message[7], video_message[0], video_url, video_message[1], video_message[2],
                                  video_message[6], video_message[3], video_message[4], video_message[5], url,
                                  video_url_file))
                cur.close()
                conn.commit()
            except Exception as e:
                conn.rollback()
                print (e)
            conn.close()

    def lost_mess(self, url):
        conn = MySQLdb.connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='1479',
            db='videos',
            charset='utf8',
        )

        try:
            cur_one = conn.cursor()
            sql_one = "SELECT File_Url,Video_Size,Video_Name " \
                      "FROM test " \
                      "WHERE Video_Web = %s "

            cur_one.execute(sql_one, url)
            content_one = cur_one.fetchone()
            cur_one.close()
            conn.commit()

            if content_one:
                if not (os.path.exists(content_one[0])):
                    mess = TimeNow.get_time() + ' 注意 : [ ' + str(content_one[2]) + ' ] 信息丢失！'
                    print (mess)
                    Log.log(mess)
                    self.lost_update(url)

        except Exception as e:
            conn.rollback()
            print (e)

        conn.close()

    def rr_update(self, url):
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

        self.lost_mess(url)

        try:
            cur1 = conn.cursor()
            sql1 = "SELECT COUNT(*)" \
                   " FROM test"                       # 获取数据库存放的数据量
            cur1.execute(sql1)
            number = cur1.fetchone()[0]             # 数据库的数据量
            cur1.close()
            conn.commit()
        except Exception as e:
            conn.rollback()
            print (e)

        video_message = self.rr_message(url)

        try:
            cur2 = conn.cursor()
            sql2 = "SELECT Video_Web,Video_Size,Video_Name" \
                   " FROM test"
            cur2.execute(sql2)
            while number:
                results = cur2.fetchone()
                if url.encode('utf8') == results[0].encode('utf8'):
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

            try:
                cur3 = conn.cursor()
                sql3 = "SELECT Video_ViewCount,Video_CommentCount,Video_FavCount " \
                       "FROM test " \
                       "WHERE Video_Web=%s AND Video_Size=%s AND Video_Name=%s"
                cur3.execute(sql3, (url, video_message[6], video_message[0]))
                check = cur3.fetchone()
                cur3.close()
                conn.commit()
            except Exception as e:
                conn.rollback()
                print (e)

            try:
                cur4 = conn.cursor()
                sql4 = "UPDATE test " \
                       "SET Video_ViewCount=%s " \
                       "WHERE Video_Web=%s"

                if check[0].encode('utf8') != str(video_message[3]):
                    cur4.execute(sql4, (video_message[3], url))
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
                sql5 = "UPDATE test " \
                       "SET Video_CommentCount=%s " \
                       "WHERE Video_Web=%s"

                if check[1].encode('utf8') != str(video_message[4]):
                    cur5.execute(sql5, (video_message[4], url))
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
                sql6 = "UPDATE test " \
                       "SET Video_FavCount=%s " \
                       "WHERE Video_Web=%s"

                if check[2].encode('utf8') != str(video_message[5]):
                    cur6.execute(sql6, (video_message[5], url))
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
            mess = TimeNow.get_time() + " 注意 : 数据库中没有该视频信息，其url : [ %s ]" % url
            print (mess)
            Log.log(mess)
            lost_url = url
        conn.close()
        return lost_url
