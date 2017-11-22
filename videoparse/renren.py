# -*- coding: utf-8 -*-
# @Time    : 2017/11/16 20:23
# @Author  : Gavin

import re
import sys
import json
import MySQLdb
import MySQLdb.cursors
from video.src.log import Log
from video.src.data import retry_post
from video.src.timenow import TimeNow
from video.videocheck.urlcheck import check_url
from video.videocheck.messupdate import update_message
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

    def rr_url(self, web_url):

        try:
            # 获取视频的ID
            video_id = re.search(r'[0-9]+', web_url).group()
            # 调用视频接口
            api_url = 'http://api.rr.tv/v3plus/video/getVideoPlayLinkByVideoId'
            # 发送请求获取数据
            data = {'videoId': video_id}
            req_js = retry_post(api_url, data, self.header)
            # 将JSON数据转换为Python数据
            req_py = json.loads(req_js)
            # 获取视频地址URL
            video_url = str(req_py["data"]["playLink"])
            return video_url
        except Exception as e:
            print ('renren.rr_url: ' + str(e))

    def rr_message(self, web_url):

        try:
            # 获取视频的ID
            video_id = re.search(r'[0-9]+', web_url).group()
            # 调用信息接口
            api_url = 'http://web.rr.tv/v3plus/video/detail'
            data = {'videoId': video_id}
            # 发送请求获取数据
            req_js = retry_post(api_url, data, self.header)
            # 将JSON转为Python
            req_py = json.loads(req_js)
            # 获取视频名称
            video_name = str(req_py["data"]["videoDetailView"]["title"])
            # 获取视频作者
            video_author = str(req_py["data"]["videoDetailView"]["author"]["nickName"])
            # 获取视频评论数
            video_comment = str(req_py["data"]["videoDetailView"]["commentCount"])
            # 获取视频点赞数
            video_support = str(req_py["data"]["videoDetailView"]["favCount"])
            # 获取视频时长
            video_time = str(req_py["data"]["videoDetailView"]["duration"])
            # 获取视频观看次数
            video_view = str(req_py["data"]["videoDetailView"]["viewCount"])
            # 视频大小
            video_size = str(req_py["data"]["videoDetailView"]["videoFileView"][1]["fileSize"])
            return video_id, video_name, video_author, video_size, video_time, video_view, video_support, video_comment
        except Exception as e:
            print ('renren.rr_message: ' + str(e))

    def rr_mysql(self, web_url):
        video_url = self.rr_url(web_url)
        video_message = self.rr_message(web_url)
        video_file = DownloadVideo(video_url, unicode(video_message[1], "utf-8"), self.file_name).video_download()

        conn = self.connect
        cur = conn.cursor()
        sql = "INSERT INTO renren(Video_Id, Video_Name, Video_Author, Video_Size, Video_Time, " \
            "Video_View, Video_Support, Video_Comment, Video_Web, Video_Url, Video_File) " \
            "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        try:
            cur.execute(sql, (video_message[0], video_message[1], video_message[2], video_message[3], video_message[4],
                              video_message[5], video_message[6], video_message[7], web_url, video_url, video_file))
            conn.commit()
        except Exception as e:
            print ('renren.rr_mysql: ' + str(e))
            conn.rollback()
        cur.close()
        conn.close()

    def rr_update(self, web_url):
        video_url = self.rr_url(web_url)
        video_message = self.rr_message(web_url)
        flags = check_url(web_url, video_message, self.file_name, self.connect, video_url)

        flag1 = flags[0]
        flag2 = flags[1]
        flag3 = flags[2]
        lost_url = ''
        check = ''
        conn = self.connect
        if flag1 and flag2 and flag3:

            cur = conn.cursor()
            sql = "SELECT Video_View, Video_Support, Video_Comment " \
                  "FROM renren " \
                  "WHERE Video_Web=%s AND Video_Name=%s"
            try:
                cur.execute(sql, (web_url, video_message[1]))
                check = cur.fetchone()
                conn.commit()
            except Exception as e:
                print ('renren.rr_update.check: ' + str(e))
                conn.rollback()
            cur.close()

            flags = update_message(check, conn, web_url, video_message)
            flag4 = flags[0]
            flag5 = flags[2]
            flag6 = flags[3]

            if flag4 and flag5 and flag6:
                mess = TimeNow.get_time() + " 视频 : [ " + video_message[1] + " ] 没有更新信息。"
                print (mess)
                Log.log(mess)
                conn.close()
        else:
            mess = TimeNow.get_time() + " 注意 : 数据库中没有该视频信息，其url : [ %s ]" % web_url
            print (mess)
            Log.log(mess)
            lost_url = web_url
        return lost_url
