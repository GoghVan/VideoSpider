# -*- coding: utf-8 -*-
import re
import time
import MySQLdb
import requests
from video.src.log import Log
from contextlib import closing
from video.src.data import retry_get
from video.src.timenow import TimeNow
from video.videoupdate.urlcheck import check_url
from video.videodownload.download import DownloadVideo


# 除了VIP、推广、直通车、天天看、星期七、大放送之外都可以下载
class FengHuang(object):
    def __init__(self):
        self.file_name = "fenghuang"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
                          ' Chrome/61.0.3163.100 Safari/537.36',
        }
        self.connect = MySQLdb.connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='1479',
            db='videos',
            charset='utf8',
        )

    def fh_message(self, web_url):
        # 找出视频的Id(str)
        pattern = re.compile(r'http://v.ifeng.com/video_(.*?)\.shtml', re.S | re.I | re.M)
        video_id = pattern.findall(web_url)[0]
        # 构造请求视频原地址url
        req_url = 'http://tv.ifeng.com/h6/' + video_id + '/video.json?callback=callback&msg=' + video_id + '&rt=js'
        # 获取data数据(str)
        data = retry_get(req_url, self.headers)
        if "guid" in data:
            # 获取视频的uid
            pattern = re.compile(r'"guid":"(.*?)",', re.I | re.M | re.S)
        elif "vid" in data:
            # 获取视频的vid
            pattern = re.compile(r'"vid":"(.*?)",', re.I | re.M | re.S)
        cid = pattern.findall(data)[0]

        # 获取video_url(str)
        if "videoPlayUrl" in data:
            pattern = re.compile(r'"videoPlayUrl":"(.*?)",', re.I | re.M | re.S)
        elif "gqSrc" in data:
            pattern = re.compile(r'"gqSrc":"(.*?)",', re.I | re.M | re.S)
        else:
            pattern = re.compile(r'"bqSrc":"(.*?)",', re.I | re.M | re.S)
        video_url = pattern.findall(data)[0]
        # 获取视频的名称(str)
        if "title" in data:
            pattern = re.compile(r'"title":"(.*?)",', re.M | re.I | re.S)
        elif "name" in data:
            pattern = re.compile(r'"name":"(.*?)",', re.M | re.I | re.S)
        video_name = pattern.findall(data)[0]
        if '\u201c' in video_name:
            video_name = video_name.replace('\\u201c', '')
            video_name = video_name.replace('\\u201d', '')
        # 获取视频的上传时间(str)
        pattern = re.compile(r'"createdate":"(.*?)",', re.M | re.I | re.S)
        video_modify = pattern.findall(data)[0]
        # 获取视频的时长(str:s)
        pattern = re.compile(r'"duration":(.*?),', re.M | re.I | re.S)
        video_time = pattern.findall(data)[0]
        # 获取视频作者(str)
        if "mediaName" in data:
            pattern = re.compile(r'"mediaName":"(.*?)"', re.M | re.I | re.S)
        elif "columnName" in data:
            pattern = re.compile(r'"columnName":(.*?)', re.M | re.I | re.S)
        video_author = pattern.findall(data)[0]
        # 获取视频观看数(str)
        req_url = 'http://survey.news.ifeng.com/getaccumulator_weight.php?key=' + cid
        data = retry_get(req_url, self.headers)
        pattern = re.compile(r'{"browse":(.*?)}', re.M | re.I | re.S)
        video_view = pattern.findall(data)[0]
        # 视频点赞数(str)
        req_url = 'http://survey.news.ifeng.com/getaccumulator_ext.php?key=' + cid + 'ding'
        data = retry_get(req_url, self.headers)
        pattern = re.compile(r'{"browse":(.*?)}', re.M | re.I | re.S)
        video_support = pattern.findall(data)[0]
        # 视频不点赞数(str)
        req_url = 'http://survey.news.ifeng.com/getaccumulator_ext.php?key=' + cid + 'cai'
        data = retry_get(req_url, self.headers)
        pattern = re.compile(r'{"browse":(.*?)}', re.M | re.I | re.S)
        video_oppose = pattern.findall(data)[0]
        # 视频评论数(str)
        req_url = 'http://comment.ifeng.com/getv.php?job=3&format=js&docurl=' + cid
        data = retry_get(req_url, self.headers)
        count = 5

        while ("commentJsonVarStr" not in str(data)) and count > 0:
            data = retry_get(req_url, self.headers)
            time.sleep(10)
            count -= 1

        try:
            pattern = re.compile(r'var commentJsonVarStr___=(.*?);', re.M | re.I | re.S)
            video_comment = pattern.findall(data)[0]
        except Exception as e:
            video_comment = '0'
            print (e)
        # 获取视频path(str)
        # data = requests.get(web_url, headers=self.headers).content
        # pattern = re.compile(r'"categoryPath":"(.*?)",', re.M | re.I | re.S)
        # path = pattern.findall(data)[0]
        # 获取视频key(str)
        # pattern = re.compile(r'"skey":"(.*?)",', re.M | re.I | re.S)
        # key = pattern.findall(data)[0]
        # 获取视频大小(str)
        with closing(requests.get(video_url, stream=True)) as size:
            video_size = size.headers['content-length']

        return video_id, video_name, video_author, video_size, video_time, video_modify, video_view, video_oppose,\
            video_support, video_comment, video_url

    def fh_mysql(self, web_url):

        video_message = self.fh_message(web_url)
        download_video = DownloadVideo(video_message[10], unicode(video_message[1], "utf-8"), self.file_name)
        video_file = download_video.video_download()

        conn = self.connect
        cur = conn.cursor()
        sql = "INSERT INTO fenghuang(Video_Id, Video_Name, Video_Author, Video_Size, Video_Time, Video_Modify" \
              ", Video_View, Video_Oppose, Video_Support, Video_Comment, Video_Web, Video_Url, Video_File) " \
              "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        try:
            cur.execute(sql, (video_message[0], video_message[1], video_message[2], video_message[3], video_message[4],
                              video_message[5], video_message[6], video_message[7], video_message[8],
                              video_message[9], web_url, video_message[10], video_file))
            conn.commit()
        except Exception as e:
            print (e)
            conn.rollback()
        cur.close()
        conn.close()

    def fh_update(self, web_url):

        video_message = self.fh_message(web_url)
        flags = check_url(web_url, video_message, self.file_name, self.connect, " ")

        flag1 = flags[0]
        flag2 = flags[1]
        flag3 = flags[2]
        lost_url = ''
        check = ''

        conn = self.connect
        if flag1 and flag2 and flag3:
            cur = conn.cursor()
            sql = "SELECT Video_View, Video_Oppose, Video_Support, Video_Comment " \
                  "FROM fenghuang " \
                  "WHERE Video_Web=%s AND Video_Size=%s AND Video_Name=%s"
            try:
                cur.execute(sql, (web_url, video_message[3], video_message[1]))
                check = cur.fetchone()
                conn.commit()
            except Exception as e:
                print (e)
                conn.rollback()
            cur.close()

            if check[0].encode('utf8') != str(video_message[6]):
                cur = conn.cursor()
                sql = "UPDATE fenghuang " \
                      "SET Video_View=%s " \
                      "WHERE Video_Web=%s"
                try:
                    cur.execute(sql, (video_message[6], web_url))
                    conn.commit()
                except Exception as e:
                    print (e)
                    conn.rollback()
                cur.close()
                mess = TimeNow.get_time() + " 视频 : [ " + video_message[1] + " ] 的Video_View : " \
                    + check[0].encode('utf8') + ", 现在Video_View : " + video_message[6]
                print (mess)
                Log.log(mess)
                flag4 = 0
            else:
                flag4 = 1

            if check[1].encode('utf8') != str(video_message[7]):
                cur = conn.cursor()
                sql = "UPDATE fenghuang " \
                      "SET Video_Oppose=%s " \
                      "WHERE Video_Web=%s"
                try:
                    cur.execute(sql, (video_message[7], web_url))
                    conn.commit()
                except Exception as e:
                    print (e)
                    conn.rollback()
                cur.close()
                mess = TimeNow.get_time() + " 视频 : [ " + video_message[1] + " ] 的Video_Oppose : " \
                    + check[1].encode('utf8') + ", 现在Video_Oppose : " + video_message[7]
                print (mess)
                Log.log(mess)
                flag5 = 0
            else:
                flag5 = 1

            if check[2].encode('utf8') != str(video_message[8]):
                cur = conn.cursor()
                sql = "UPDATE fenghuang " \
                      "SET Video_Support=%s " \
                      "WHERE Video_Web=%s"
                try:
                    cur.execute(sql, (video_message[8], web_url))
                    conn.commit()
                except Exception as e:
                    print (e)
                    conn.rollback()
                cur.close()
                mess = TimeNow.get_time() + " 视频 : [ " + video_message[1] + " ] 的Video_Support : " \
                    + check[2].encode('utf8') + ", 现在Video_Support : " + video_message[8]
                print (mess)
                Log.log(mess)
                flag6 = 0
            else:
                flag6 = 1

            if check[3].encode('utf8') != str(video_message[9]):
                cur = conn.cursor()
                sql = "UPDATE fenghuang " \
                      "SET Video_Comment=%s " \
                      "WHERE Video_Web=%s"
                try:
                    cur.execute(sql, (video_message[9], web_url))
                    conn.commit()
                except Exception as e:
                    print (e)
                    conn.rollback()
                cur.close()
                mess = TimeNow.get_time() + " 视频 : [ " + video_message[1] + " ] 的Video_Comment : " \
                    + check[3].encode('utf8') + ", 现在Video_Comment : " + video_message[9]
                print (mess)
                Log.log(mess)
                flag7 = 0
            else:
                flag7 = 1

            if flag4 and flag5 and flag6 and flag7:
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
