# -*- coding: utf-8 -*-
import re
import os
import sys
import json
import urllib
import MySQLdb
import requests
from video.src.log import Log
from contextlib import closing
from video.src.timenow import TimeNow
from video.videodownload.download import DownloadVideo

reload(sys)
sys.setdefaultencoding("utf-8")

# http://v.163.com/paike 、http://v.163.com/zixun/ 、 http://v.163.com/jishi/ 仅限这些地址下的分支视频


class WangYi(object):
    def __init__(self):
        pass

    @staticmethod
    def wy_url(web_url):
        video_url = ''
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/'
                          '61.0.3163.100 Safari/537.36',
        }
        # 从html中找到标准视频的真实下载地址（str)
        # html = requests.get(web_url, headers=header)
        # pattern = re.compile(r'source src="(.*?)"', re.S | re.M | re.I)
        # real_s_url = pattern.findall(html.text)[0].encode('utf8')

        # 构造url，访问服务器，获取xml数据
        html = requests.get(web_url, headers=header)
        pattern = re.compile(r'topicid : "(.*?)"', re.S | re.M | re.I)
        cid = pattern.findall(html.text)[0].encode('utf8')  # 获取topicid
        sc = [web_url][0]  # 将url进行list处理
        # 构造url
        req_url = 'http://xml.ws.126.net/video/' + sc[-7] + '/' + sc[-6] + '/' + cid + '_' + sc[-14: -5] + '.xml'  #
        # 获取xml数据
        xml_data = requests.get(req_url, headers=header).text.encode('utf8')
        pattern = re.compile(r'<flv>(.*?)</flv>', re.S | re.M | re.I)
        flv_url = pattern.findall(xml_data)
        flag1 = 0
        flag2 = 0
        for hd_url in flv_url:
            if '/SHD/' in hd_url:
                video_url = hd_url
                break
            if '/HD/' in hd_url:
                video_url = hd_url
                flag1 = 1
            else:
                flag2 = 0

            if not(flag1 == 1 and flag2 == 0):
                video_url = hd_url
        return video_url

    def wy_message(self, web_url):

        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/'
                          '61.0.3163.100 Safari/537.36',
        }
        html = requests.get(web_url, headers=header)
        video_url = self.wy_url(web_url)
        # 视频大小
        with closing(requests.get(video_url, stream=True)) as size:
            video_size = size.headers['content-length']

        pattern = re.compile(r'<span class="item">(.*?)</span>')
        author = pattern.findall(html.text)
        # 视频作者
        video_author = ''
        flag1 = 0
        flag2 = 0
        for item in author:
            if '来源：' in item:
                video_author = str(item)[9:len(str(item))]
                flag1 = 1
            else:
                flag2 = 0
            if '上传者：' in item:
                video_author = str(item)[12:len(str(item))]
                break
            if not(flag1 == 1 and flag2 == 0):
                video_author = 'author missing'

        pattern = re.compile(r'topicid : "(.*?)"', re.S | re.M | re.I)
        cid = pattern.findall(html.text)[0].encode('utf8')  # 获取topicid
        sc = [web_url][0]  # 将url进行list处理

        # 构造url
        req_url = 'http://xml.ws.126.net/video/' + sc[-7] + '/' + sc[-6] + '/' + cid + '_' + sc[-14: -5] + '.xml'
        # 获取xml数据
        xml_data = requests.get(req_url, headers=header).text.encode('utf8')
        pattern = re.compile(r'<title>(.*?)</title>', re.S | re.M | re.I)
        name = pattern.findall(xml_data)[0]
        # 视频名称
        video_name = urllib.unquote(name)
        pattern = re.compile(r'<totaltime>(.*?)</totaltime>', re.S | re.M | re.I)
        # 视频播放时长
        video_time = pattern.findall(xml_data)[0]
        pattern = re.compile(r'vid : "(.*?)"', re.S | re.M | re.I)
        # 视频id
        video_id = pattern.findall(html.text)[0].encode('utf8')
        pattern = re.compile(r'"productKey" : "(.*?)"', re.S | re.M | re.I)
        product_key = pattern.findall(html.text)[0].encode('utf8')

        try:
            pattern = re.compile(r'"docId" :  "(.*?)"', re.S | re.M | re.I)
            doc_id = pattern.findall(html.text)[0].encode('utf8')
        except:
            pattern = re.compile(r'"docId" : "(.*?)"', re.S | re.M | re.I)
            doc_id = pattern.findall(html.text)[0].encode('utf8')

        # 构造获取视频其他信息的url
        mess_url = 'http://sdk.comment.163.com/api/v1/products/' + product_key + '/threads/' + doc_id
        req_mess = requests.get(mess_url, headers=header).content
        message = json.loads(req_mess)
        # 视频的上传时间
        video_modify = message['modifyTime'].encode('utf8')
        # 视频的评论数
        video_comment = str(message['tcount'])
        # 视频评论的反对数
        video_comment_against = str(message['cmtAgainst'])
        # 视频评论的点赞数
        video_comment_fav = str(message['cmtVote'])

        mess_url = 'http://so.v.163.com/vote/' + video_id + '.js'
        req_mess = requests.get(mess_url, headers=header).content
        pattern = re.compile(r'"hits":(.*?),', re.M | re.S | re.I)
        # 视频的观看数
        video_view = pattern.findall(req_mess)[0]
        pattern = re.compile(r'"opposecount":(.*?),')
        # 视频的反对数
        video_oppose = pattern.findall(req_mess)[0]
        pattern = re.compile(r'"supportcount":(.*?),')
        # 视频的点赞数
        video_support = pattern.findall(req_mess)[0]

        return video_id, video_name, video_author, video_size, video_modify, video_view, video_time, video_oppose,\
            video_support, video_comment_fav, video_comment_against, video_comment

    def wy_mysql(self, web_url):
        video_url = self.wy_url(web_url)
        video_message = self.wy_message(web_url)
        # 注意文件名要以Unicode形式存储
        download_video = DownloadVideo(video_url, unicode(video_message[1], "utf-8"), "wangyi")
        video_file = download_video.video_download()

        conn = MySQLdb.connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='1479',
            db='videos',
            charset='utf8',
        )
        cur = conn.cursor()
        sql = "INSERT INTO wangyi(Video_Id, Video_Name, Video_Author, Video_Size, Video_modify, Video_View" \
              ", Video_Time, Video_Oppose, Video_Support, Video_Comment, Video_Comment_Fav, Video_Comment_Against" \
              ", Video_Web, Video_Url, Video_File) " \
              "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        try:
            cur.execute(sql, (video_message[0], video_message[1], video_message[2], video_message[3], video_message[4],
                              video_message[5], video_message[6], video_message[7], video_message[8],
                              video_message[11], video_message[9], video_message[10], web_url, video_url, video_file))
            cur.close()
            conn.commit()
        except Exception as e:
            conn.rollback()
            print (e)
        conn.close()

    def lost_update(self, web_url):
        video_url = self.wy_url(web_url)
        video_message = self.wy_message(web_url)
        download_video = DownloadVideo(video_url, unicode(video_message[1], "utf-8"), "wangyi")
        video_file = download_video.video_download()

        conn = MySQLdb.connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='1479',
            db='videos',
            charset='utf8',
        )
        cur = conn.cursor()
        sql = "UPDATE wangyi " \
              "SET Video_Id=%s, Video_Name=%s, Video_Author=%s, Video_Size=%s, Video_modify=%s, Video_View=%s" \
              ", Video_Time=%s, Video_Oppose=%s, Video_Support=%s, Video_Comment=%s, Video_Comment_Fav=%s" \
              ", Video_Comment_Against=%s, Video_Url=%s, Video_File=%s " \
              "WHERE Video_Web=%s"
        try:
            cur.execute(sql, (video_message[0], video_message[1], video_message[2], video_message[3], video_message[4],
                              video_message[5], video_message[6], video_message[7], video_message[8],
                              video_message[11], video_message[9], video_message[10], video_url, video_file, web_url))
            cur.close()
            conn.commit()
        except Exception as e:
            conn.rollback()
            print (e)
        conn.close()
        mess = TimeNow.get_time() + ' 注意 : [ ' + video_message[1] + ' ] 信息已补全，请注意查看！'
        print (mess)
        Log.log(mess)

    def lost_mess(self, web_url):
        conn = MySQLdb.connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='1479',
            db='videos',
            charset='utf8',
        )
        try:
            cur = conn.cursor()
            sql = "SELECT Video_File,Video_Size,Video_Name " \
                  "FROM wangyi " \
                  "WHERE Video_Web = %s "

            cur.execute(sql, web_url)
            content = cur.fetchone()
            cur.close()
            conn.commit()

            if content:
                if not (os.path.exists(content[0])):
                    mess = TimeNow.get_time() + ' 注意 : [ ' + str(content[2]) + ' ] 信息丢失！'
                    print (mess)
                    Log.log(mess)
                    self.lost_update(web_url)
        except Exception as e:
            conn.rollback()
            print (e)
        conn.close()

    def wy_check(self, web_url):
        flag1 = 0
        flag2 = 0
        flag3 = 0
        number = 0

        conn = MySQLdb.connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='1479',
            db='videos',
            charset='utf8',
        )

        self.lost_mess(web_url)

        cur = conn.cursor()
        sql = "SELECT COUNT(*) " \
              "FROM wangyi"
        try:
            cur.execute(sql)
            number = cur.fetchone()[0]
            cur.close()
            conn.commit()
        except Exception as e:
            conn.rollback()
            print (e)

        video_message = self.wy_message(web_url)

        cur = conn.cursor()
        sql = "SELECT Video_Web,Video_Size,Video_Name " \
              "FROM wangyi"
        try:
            cur.execute(sql)
            while number:
                results = cur.fetchone()
                if web_url == results[0].encode('utf8'):
                    flag1 = 1
                else:
                    flag1 = 0
                if video_message[3] == results[1].encode('utf8'):
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
            cur.close()
            conn.commit()
        except Exception as e:
            conn.rollback()
            print (e)
        conn.close()
        lost_url = self.wy_update(web_url, flag1, flag2, flag3, video_message)
        return lost_url

    @staticmethod
    def wy_update(web_url, flag1, flag2, flag3, video_message):
        lost_url = ''
        check = ''
        conn = MySQLdb.connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='1479',
            db='videos',
            charset='utf8',
        )
        if flag1 and flag2 and flag3:
            cur = conn.cursor()
            sql = "SELECT Video_View, Video_Oppose, Video_Support, Video_Comment, Video_Comment_Fav" \
                  ", Video_Comment_Against " \
                  "FROM wangyi " \
                  "WHERE Video_Web=%s AND Video_Size=%s AND Video_Name=%s"
            try:
                cur.execute(sql, (web_url, video_message[3], video_message[1]))
                check = cur.fetchone()
                cur.close()
                conn.commit()
            except Exception as e:
                conn.rollback()
                print (e)

            if check[0].encode('utf8') != str(video_message[5]):
                cur = conn.cursor()
                sql = "UPDATE wangyi " \
                      "SET Video_View=%s " \
                      "WHERE Video_Web=%s"
                try:
                    cur.execute(sql, (video_message[5], web_url))
                    cur.close()
                    conn.commit()
                except Exception as e:
                    conn.rollback()
                    print (e)
                mess = TimeNow.get_time() + " 视频 : [ " + video_message[1] + " ] 的Video_View : " \
                    + check[0].encode('utf8') + ", 现在Video_View : " + video_message[5]
                print (mess)
                Log.log(mess)
                flag4 = 0
            else:
                flag4 = 1

            if check[1].encode('utf8') != str(video_message[7]):
                cur = conn.cursor()
                sql = "UPDATE wangyi " \
                      "SET Video_Oppose=%s " \
                      "WHERE Video_Web=%s"
                try:
                    cur.execute(sql, (video_message[7], web_url))
                    cur.close()
                    conn.commit()
                except Exception as e:
                    conn.rollback()
                    print (e)
                mess = TimeNow.get_time() + " 视频 : [ " + video_message[1] + " ] 的Video_Oppose : " \
                    + check[1].encode('utf8') + ", 现在Video_Oppose : " + video_message[7]
                print (mess)
                Log.log(mess)
                flag5 = 0
            else:
                flag5 = 1

            if check[2].encode('utf8') != str(video_message[8]):
                cur = conn.cursor()
                sql = "UPDATE wangyi " \
                      "SET Video_Support=%s " \
                      "WHERE Video_Web=%s"
                try:
                    cur.execute(sql, (video_message[8], web_url))
                    cur.close()
                    conn.commit()
                except Exception as e:
                    conn.rollback()
                    print (e)
                mess = TimeNow.get_time() + " 视频 : [ " + video_message[1] + " ] 的Video_Support : " \
                    + check[2].encode('utf8') + ", 现在Video_Support : " + video_message[8]
                print (mess)
                Log.log(mess)
                flag6 = 0
            else:
                flag6 = 1

            if check[3].encode('utf8') != str(video_message[11]):
                cur = conn.cursor()
                sql = "UPDATE wangyi " \
                      "SET Video_Comment=%s " \
                      "WHERE Video_Web=%s"
                try:
                    cur.execute(sql, (video_message[11], web_url))
                    cur.close()
                    conn.commit()
                except Exception as e:
                    conn.rollback()
                    print (e)
                mess = TimeNow.get_time() + " 视频 : [ " + video_message[1] + " ] 的Video_Comment : " \
                    + check[3].encode('utf8') + ", 现在Video_Comment : " + video_message[11]
                print (mess)
                Log.log(mess)
                flag7 = 0
            else:
                flag7 = 1

            if check[4].encode('utf8') != str(video_message[9]):
                cur = conn.cursor()
                sql = "UPDATE wangyi " \
                      "SET Video_Comment_Fav=%s " \
                      "WHERE Video_Web=%s"
                try:
                    cur.execute(sql, (video_message[9], web_url))
                    cur.close()
                    conn.commit()
                except Exception as e:
                    conn.rollback()
                    print (e)
                mess = TimeNow.get_time() + " 视频 : [ " + video_message[1] + " ] 的Video_Comment_Fav : " \
                    + check[4].encode('utf8') + ", 现在Video_Comment_Fav : " + video_message[9]
                print (mess)
                Log.log(mess)
                flag8 = 0
            else:
                flag8 = 1

            if check[5].encode('utf8') != str(video_message[10]):
                cur = conn.cursor()
                sql = "UPDATE wangyi " \
                      "SET video_comment_against=%s " \
                      "WHERE Video_Web=%s"
                try:
                    cur.execute(sql, (video_message[10], web_url))
                    cur.close()
                    conn.commit()
                except Exception as e:
                    conn.rollback()
                    print (e)
                mess = TimeNow.get_time() + " 视频 : [ " + video_message[1] + " ] 的video_comment_against : " \
                    + check[5].encode('utf8') + ", 现在video_comment_against : " + video_message[10]
                print (mess)
                Log.log(mess)
                flag9 = 0
            else:
                flag9 = 1

            if flag4 and flag5 and flag6 and flag7 and flag8 and flag9:
                mess = TimeNow.get_time() + " 视频 : [ " + video_message[1] + " ] 没有更新信息。"
                print (mess)
                Log.log(mess)
        else:
            mess = TimeNow.get_time() + " 注意 : 数据库中没有该视频信息，其url : [ %s ]" % web_url
            print (mess)
            Log.log(mess)
            lost_url = web_url
        conn.close()
        return lost_url
