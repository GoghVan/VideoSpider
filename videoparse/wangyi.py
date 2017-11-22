# -*- coding: utf-8 -*-
# @Time    : 2017/11/16 20:23
# @Author  : Gavin

import re
import sys
import json
import urllib
import MySQLdb
import requests
from video.src.log import Log
from contextlib import closing
from video.src.data import retry_get
from video.src.timenow import TimeNow
from video.videocheck.urlcheck import check_url
from video.videodownload.download import DownloadVideo
from video.videocheck.messupdate import update_message

reload(sys)
sys.setdefaultencoding("utf-8")

# http://v.163.com/paike 、http://v.163.com/zixun/ 、 http://v.163.com/jishi/ 仅限这些地址下的分支视频


class WangYi(object):
    def __init__(self):
        self.file_name = "wangyi"
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/'
                          '61.0.3163.100 Safari/537.36',
        }
        self.connect = MySQLdb.connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='1479',
            db='videos',
            charset='utf8',
        )

    def wy_url(self, web_url):
        video_url = ''
        # 从html中找到标准视频的真实下载地址（str)
        # html = requests.get(web_url, headers=header)
        # pattern = re.compile(r'source src="(.*?)"', re.S | re.M | re.I)
        # real_s_url = pattern.findall(html.text)[0].encode('utf8')

        # 构造url，访问服务器，获取xml数据
        html = requests.get(web_url, headers=self.header)
        pattern = re.compile(r'topicid : "(.*?)"', re.S | re.M | re.I)
        cid = pattern.findall(html.text)[0].encode('utf8')  # 获取topicid
        sc = [web_url][0]  # 将url进行list处理
        # 构造url
        req_url = 'http://xml.ws.126.net/video/' + sc[-7] + '/' + sc[-6] + '/' + cid + '_' + sc[-14: -5] + '.xml'  #
        # 获取xml数据
        xml_data = retry_get(req_url, self.header)
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
        html = requests.get(web_url, headers=self.header)
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
        xml_data = retry_get(req_url, self.header)
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
        req_mess = retry_get(mess_url, self.header)
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
        req_mess = retry_get(mess_url, self.header)
        pattern = re.compile(r'"hits":(.*?),', re.M | re.S | re.I)
        # 视频的观看数
        video_view = pattern.findall(req_mess)[0]
        pattern = re.compile(r'"opposecount":(.*?),')
        # 视频的反对数
        video_oppose = pattern.findall(req_mess)[0]
        pattern = re.compile(r'"supportcount":(.*?),')
        # 视频的点赞数
        video_support = pattern.findall(req_mess)[0]

        return video_id, video_name, video_author, video_size, video_time, video_modify, video_view, video_oppose,\
            video_support, video_comment, video_comment_fav, video_comment_against

    def wy_mysql(self, web_url):
        video_url = self.wy_url(web_url)
        video_message = self.wy_message(web_url)
        # 注意文件名要以Unicode形式存储
        download_video = DownloadVideo(video_url, unicode(video_message[1], "utf-8"), self.file_name)
        video_file = download_video.video_download()

        conn = self.connect

        cur = conn.cursor()
        sql = "INSERT INTO wangyi(Video_Id, Video_Name, Video_Author, Video_Size, Video_Time, Video_modify" \
              ", Video_View, Video_Oppose, Video_Support, Video_Comment, Video_Comment_Fav, Video_Comment_Against" \
              ", Video_Web, Video_Url, Video_File) " \
              "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        try:
            cur.execute(sql, (video_message[0], video_message[1], video_message[2], video_message[3], video_message[4],
                              video_message[5], video_message[6], video_message[7], video_message[8],
                              video_message[9], video_message[10], video_message[11], web_url, video_url, video_file))
            conn.commit()
        except Exception as e:
            print ('wangyi.wy_mysql: ' + str(e))
            conn.rollback()
        cur.close()
        conn.close()

    def wy_update(self, web_url):

        video_url = self.wy_url(web_url)
        video_message = self.wy_message(web_url)
        flags = check_url(web_url, video_message, self.file_name, self.connect, video_url)

        flag1 = flags[0]
        flag2 = flags[1]
        flag3 = flags[2]
        lost_url = ''
        check = ''

        conn = self.connect
        if flag1 and flag2 and flag3:
            cur = conn.cursor()
            sql = "SELECT Video_View, Video_Oppose, Video_Support, Video_Comment, Video_Comment_Fav" \
                  ", Video_Comment_Against " \
                  "FROM wangyi " \
                  "WHERE Video_Web=%s AND Video_Name=%s"
            try:
                cur.execute(sql, (web_url, video_message[1]))
                check = cur.fetchone()
                conn.commit()
            except Exception as e:
                print ('wangyi.wy_update.check: ' + str(e))
                conn.rollback()
            cur.close()

            flags = update_message(check, conn, web_url, video_message)
            flag4 = flags[0]
            flag5 = flags[1]
            flag6 = flags[2]
            flag7 = flags[3]
            flag8 = flags[4]
            flag9 = flags[5]

            if flag4 and flag5 and flag6 and flag7 and flag8 and flag9:
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
