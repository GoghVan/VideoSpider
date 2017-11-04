# -*- coding: utf-8 -*-
import re
import sys
import json
import MySQLdb
import MySQLdb.cursors
from video.src.log import Log
from video.src.data import retry_post
from video.src.timenow import TimeNow
from video.videoupdate.urlcheck import check_url
from video.videodownload.download import DownloadVideo

reload(sys)
sys.setdefaultencoding('utf8')


class RenRen(object):
    def __init__(self):
        self.file_name = "renren"
        self.header = {
            'clientVersion': '0.1.0',
            'clientType': 'web',
        }   # 添加客户端版本信息
        self.connect = MySQLdb.connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='1479',
            db='videos',
            charset="utf8",
        )

    def rr_url(self, url):

        try:
            # 获取视频的ID
            video_id = re.search(r'[0-9]+', url).group()
            # 调用视频接口
            api_url = 'http://api.rr.tv/v3plus/video/getVideoPlayLinkByVideoId'
            # 发送请求获取数据
            data = {'videoId': video_id}
            req_js = retry_post(api_url, data, self.header)
            # 将JSON数据转换为Python数据
            req_py = json.loads(req_js)
            # 获取视频地址URL
            video_url = req_py["data"]["playLink"]
            return video_url
        except Exception as e:
            print (e)

    def rr_message(self, url):

        try:
            video_id = re.search(r'[0-9]+', url).group()                                                # 获取视频的ID
            api_url = 'http://web.rr.tv/v3plus/video/detail'                                            # 调用信息接口
            data = {'videoId': video_id}
            req_js = retry_post(api_url, data, self.header)   # 发送请求获取数据
            req_py = json.loads(req_js)                                                                 # 将JSON转为Python
            video_name = req_py["data"]["videoDetailView"]["title"]                                     # 获取视频名称
            video_author = req_py["data"]["videoDetailView"]["author"]["nickName"]                      # 获取视频作者
            video_comment = req_py["data"]["videoDetailView"]["commentCount"]                           # 获取视频评论数
            video_support = req_py["data"]["videoDetailView"]["favCount"]                               # 获取视频点赞数
            video_time = req_py["data"]["videoDetailView"]["duration"]                                  # 获取视频时长
            video_view = req_py["data"]["videoDetailView"]["viewCount"]                                 # 获取视频观看次数
            video_size = req_py["data"]["videoDetailView"]["videoFileView"][1]["fileSize"]              # 视频大小
            return video_id, video_name, video_author, video_size, video_time, video_view, video_support, video_comment
        except Exception as e:
            print (e)

    def rr_mysql(self, url):
        video_url = self.rr_url(url)
        video_message = self.rr_message(url)
        download_video = DownloadVideo(video_url, video_message[1], self.file_name)
        video_url_file = download_video.video_download()

        conn = self.connect
        cur = conn.cursor()
        sql = "INSERT INTO renren(Video_Id, Video_Name, Video_Author, Video_Size, Video_Time, " \
            "Video_View, Video_Support, Video_Comment, Video_Web, Video_Url, Video_File) " \
            "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        try:
            cur.execute(sql, (video_message[0], video_message[1], video_message[2], video_message[3],
                        video_message[4], video_message[5], video_message[6], video_message[7], url, video_url,
                        video_url_file))
            conn.commit()
        except Exception as e:
            print (e)
            conn.rollback()
        cur.close()
        conn.close()

    def rr_update(self, url):

        video_url = self.rr_url(url)
        video_message = self.rr_message(url)
        flags = check_url(url, video_message, self.file_name, self.connect, video_url)

        flag1 = flags[0]
        flag2 = flags[1]
        flag3 = flags[2]
        lost_url = ''
        check = ''

        conn = self.connect
        if flag1 and flag2 and flag3:
            cur = conn.cursor()
            sql = "SELECT Video_View,Video_Comment,Video_Support " \
                "FROM renren " \
                "WHERE Video_Web=%s AND Video_Size=%s AND Video_Name=%s"
            try:
                cur.execute(sql, (url, video_message[3], video_message[1]))
                check = cur.fetchone()
                conn.commit()
            except Exception as e:
                print (e)
                conn.rollback()
            cur.close()

            cur = conn.cursor()
            sql = "UPDATE renren " \
                "SET Video_View=%s " \
                "WHERE Video_Web=%s"
            if check[0].encode('utf8') != str(video_message[5]):
                try:
                    cur.execute(sql, (video_message[5], url))
                    conn.commit()
                except Exception as e:
                    print (e)
                    conn.rollback()
                mess = TimeNow.get_time() + " 视频 : [ " + video_message[1].encode('utf8') \
                    + " ] 的Video_View : " \
                    + check[0].encode('utf8') + ", 现在Video_View : " + str(video_message[5])
                print (mess)
                Log.log(mess)
                flag4 = 0
            else:
                flag4 = 1
            cur.close()

            cur = conn.cursor()
            sql = "UPDATE renren " \
                "SET Video_Comment=%s " \
                "WHERE Video_Web=%s"

            if check[1].encode('utf8') != str(video_message[7]):
                try:
                    cur.execute(sql, (video_message[7], url))
                    conn.commit()
                except Exception as e:
                    print (e)
                    conn.rollback()
                mess = TimeNow.get_time() + " 视频 : [ " + video_message[1].encode('utf8') \
                    + " ] 的Video_Comment : " \
                    + check[1].encode('utf8') + ", 现在Video_Comment : " + str(video_message[7])
                print (mess)
                Log.log(mess)
                flag5 = 0
            else:
                flag5 = 1
            cur.close()

            cur = conn.cursor()
            sql = "UPDATE renren " \
                "SET Video_Support=%s " \
                "WHERE Video_Web=%s"

            if check[2].encode('utf8') != str(video_message[6]):
                try:
                    cur.execute(sql, (video_message[6], url))
                    conn.commit()
                except Exception as e:
                    print(e)
                    conn.rollback()
                mess = TimeNow.get_time() + " 视频 : [ " + video_message[1].encode('utf8') \
                    + " ] 的Video_Support : " \
                    + check[2].encode('utf8') + ", 现在Video_Support : " + str(video_message[6])
                print (mess)
                Log.log(mess)
                flag6 = 0
            else:
                flag6 = 1
            cur.close()

            if flag4 and flag5 and flag6:
                mess = TimeNow.get_time() + " 视频 : [ " + video_message[1].encode('utf8') + " ] 没有更新信息。"
                print (mess)
                Log.log(mess)
                conn.close()
        else:
            mess = TimeNow.get_time() + " 注意 : 数据库中没有该视频信息，其url : [ %s ]" % url
            print (mess)
            Log.log(mess)
            lost_url = url
        return lost_url
