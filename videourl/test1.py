# -*- coding: utf-8 -*-
import re
import json
import time
import datetime
import MySQLdb
import requests
import MySQLdb.cursors
from retry import retry
import os
from contextlib import closing
from os.path import join, getsize
import sys

reload(sys)
sys.setdefaultencoding('utf8')

headers = {
    'clientVersion': '0.1.0',
    'clientType': 'web',
}  # 添加客户端版本信息

def rr_url(url):
    try:
        video_Id = re.search(r'[0-9]+', url).group()     #获取视频的ID
        api_url = 'http://api.rr.tv/v3plus/video/getVideoPlayLinkByVideoId'     #调用视频接口
        req_js = requests.post(api_url, data={'videoId': video_Id}, headers=headers).content   #发送请求获取数据
        req_py = json.loads(req_js)     #将JSON数据转换为Python数据
        Video_Url = req_py["data"]["playLink"]     #获取视频地址URL
        return Video_Url
    except Exception as e:
        print e

def rr_message(url):
    try:
        video_Id = re.search(r'[0-9]+', url).group()     # 获取视频的ID
        api_url = 'http://web.rr.tv/v3plus/video/detail'        ##调用信息接口
        req_js = requests.post(api_url, data={'videoId': video_Id}, headers=headers).content        #发送请求获取数据
        req_py = json.loads(req_js)     #将JSON数据转换为Python数据
        Video_Name = req_py["data"]["videoDetailView"]["title"]     #获取视频名称
        Video_Author = req_py["data"]["videoDetailView"]["author"]["nickName"]      #获取视频作者
        Video_CommentCount = req_py["data"]["videoDetailView"]["commentCount"]      #获取视频评论数
        Video_FavCount = req_py["data"]["videoDetailView"]["favCount"]      #获取视频点赞数
        Video_Time = req_py["data"]["videoDetailView"]["duration"]      #获取视频时长
        Video_ViewCount = req_py["data"]["videoDetailView"]["viewCount"]        #获取视频观看次数
        Video_Size = req_py["data"]["videoDetailView"]["videoFileView"][1]["fileSize"]      #视频大小
        return Video_Name, Video_Author, Video_Time, Video_ViewCount, Video_CommentCount, Video_FavCount, Video_Size
    except Exception as e:
        print e

def rr_log(message):                    #日志写入文件
    with open(r'F:\SoftProgram\log/renren.txt', 'a+') as file_mess:
        file_mess.write('\n' + message)

def rr_large(File_Url):                  #实时获取文件的大小
    print 3
    file_size = 0
    for root, dirs, files in os.walk(File_Url):
        file_size = file_size + sum([getsize(join(root, name)) for name in files])
    return file_size

def get_Time():                         #获取当前时间
    Time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    return Time

# print "-->VideoName : " + video_message[0]
# print "-->VideoUrl : " + video_url
# print "-->VideoAuthor : " + video_message[1]
# print "-->VideoTime : " + video_message[2]
# Video_Size = video_message[6] * 0.00000095367
# print "-->VideoSize : " + bytes(round(Video_Size, 2)) + "MB"
# print "-->VideoViewCount : " + bytes(video_message[3])
# print "-->VideoCommentCount : " + bytes(video_message[4])
# print "-->VideoFavCount : " + bytes(video_message[5])
# print "-->VideoFileUrl : " + "F:\SoftProgram\Videos/rr_video/" + video_message[0] + ".mp4"

@retry(tries=5, delay=10)       #下载失败后重新下载
def video_download(num, url, video_message):         #视频下载
    try:
        with closing(requests.get(url, stream=True)) as response:
            chunk_size = 1024
            content_size = int(response.headers['content-length'])
            file_D = 'F:\SoftProgram\Videos\\rr_video/' + video_message[0] + '.mp4'
            if (os.path.exists(file_D) and os.path.getsize(file_D) == content_size):
                print get_Time() + ' ' + video_message[0] + '已存在文件夹中，请注意查看！'
            else:
                progress = ProgressBar(get_Time(), num, video_message[0].encode('utf8'), total=content_size, unit="KB",
                                       chunk_size=chunk_size, run_status="正在下载", fin_status="下载完成")
                with open(file_D, "wb") as file:
                    for data in response.iter_content(chunk_size=chunk_size):
                        file.write(data)
                        progress.refresh(count=len(data))
        return 'F:\SoftProgram\Videos/rr_video/' + video_message[0] + '.mp4'
    except Exception as e:
        print e

def rr_mysql(url, video_url, video_message, video_url_file):

    if video_url:
        Video_Name = video_message[0]
        Video_Author = video_message[1]
        Video_Time = video_message[2]
        Video_ViewCount = video_message[3]
        Video_CommentCount = video_message[4]
        Video_FavCount = video_message[5]
        Video_Size = video_message[6]
        File_Url = video_url_file
        Video_Web = url
        Video_Url = video_url

        conn = MySQLdb.connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='1479',
            db='videos',
            charset="utf8",
        )
        cur = conn.cursor()
        sql = "INSERT INTO test(Video_Name, Video_Url, Video_Author, Video_Time, Video_Size, " \
              "Video_ViewCount, Video_CommentCount, Video_FavCount, Video_Web, File_Url) " \
              "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        try:
            cur.execute(sql, (Video_Name, Video_Url, Video_Author, Video_Time, Video_Size, Video_ViewCount,
                              Video_CommentCount, Video_FavCount, Video_Web, File_Url))
            cur.close()
            conn.commit()
        except Exception as e:
            conn.rollback()
            print e
        conn.close()

flag1 = 0
flag2 = 0
flag3 = 0
flag4 = 0
flag5 = 0
flag6 = 0

def rr_axay(url):
    global flag1, flag2, flag3, flag4, flag5, flag6
    global lost_url
    lost_url = ''
    flag1 = 0
    flag2 = 0
    flag3 = 0
    flag4 = 0
    flag5 = 0
    flag6 = 0

    conn = MySQLdb.connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='1479',
        db='videos',
        charset='utf8',
    )
    try:
        cur1 = conn.cursor()
        sql1 = "SELECT COUNT(*)" \
               " FROM test"         # 获取数据库存放的数据量
        cur1.execute(sql1)
        number = cur1.fetchone()[0]             # 数据库的数据量
        cur1.close()
        conn.commit()
    except Exception as e:
        conn.rollback()
        print e

    video_message = rr_message(url)

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
        print e

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
            print e

        try:
            cur4 = conn.cursor()
            sql4 = "UPDATE test " \
                   "SET Video_ViewCount=%s " \
                   "WHERE Video_Web=%s"

            if check[0].encode('utf8') != str(video_message[3]):
                cur4.execute(sql4, (video_message[3], url))
                mess = get_Time() + " 视频 : [" + video_message[0].encode('utf8') + "] 的Video_ViewCount : " \
                        + check[0].encode('utf8') + ", 现在Video_ViewCount : " + str(video_message[3])
                print mess
                rr_log(mess)
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
                mess = get_Time() + " 视频 : [" + video_message[0].encode('utf8') + "] 的Video_CommentCount : " \
                        + check[1].encode('utf8') + ", 现在Video_CommentCount : " + str(video_message[4])
                print mess
                rr_log(mess)
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
                mess = get_Time() + " 视频 : [" + video_message[0].encode('utf8') + "] 的Video_FavCount : " \
                        + check[2].encode('utf8') + ", 现在Video_FavCount : " + str(video_message[5])
                print mess
                rr_log(mess)
                flag6 = 0
            else:
                flag6 = 1
            cur6.close()
            conn.commit()

            if flag4 and flag5 and flag6:
                mess = get_Time() + " 视频 : [" + video_message[0].encode('utf8') + "] 没有更新信息。"
                print mess
                rr_log(mess)

        except Exception as e:
            conn.rollback()
            print e
    else:
        mess = get_Time() + " 数据库中没有该视频信息，其url : %s" %url
        print mess
        rr_log(mess)
        lost_url = url
    conn.close()
    return lost_url

class ProgressBar(object):              #进度显示条
    def __init__(self, Time, num, title, count=0.0, run_status=None, fin_status=None, total=100.0, unit='',
                 sep='/', chunk_size=1.0):
        super(ProgressBar, self).__init__()
        self.info = "%s <%s> [%s] %s %.2f %s %s %.2f %s"
        self.Time = Time
        self.num = num
        self.title = title
        self.total = total
        self.count = count
        self.chunk_size = chunk_size
        self.status = run_status or ""
        self.fin_status = fin_status or " " * len(self.statue)
        self.unit = unit
        self.seq = sep

    def __get_info(self):
        # 【名称】状态 进度 单位 分割线 总数 单位
        _info = self.info % (self.Time, self.num, self.title, self.status, self.count / self.chunk_size, self.unit, self.seq,
                             self.total / self.chunk_size, self.unit)
        return _info

    def refresh(self, count=1, status=None):
        self.count += count
        self.status = status or self.status
        sys.stdout.write('\r')
        sys.stdout.write(self.__get_info())
        sys.stdout.flush()
        if self.count >= self.total:
            self.status = status or self.fin_status
            sys.stdout.write('\r')
            sys.stdout.write(self.__get_info())
            sys.stdout.write('\n')
            rr_log(self.__get_info())


urls = ('http://rr.tv/#/video/386036', 'http://rr.tv/#/video/386114')

startTime = datetime.datetime(2017, 10, 15, 23, 0, 0)
num = 1
while datetime.datetime.now() < startTime:
    for url in urls:
        lost_url = rr_axay(url)
        if lost_url:
            video_url = rr_url(url)
            video_message = rr_message(url)
            video_url_file = video_download(num, video_url, video_message)
            rr_mysql(url, video_url, video_message, video_url_file)
            num = num + 1
        time.sleep(5)
    time.sleep(5)
