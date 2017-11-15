# -*- coding: utf-8 -*-
import re
import sys
import json
import time
import MySQLdb
from video.src.log import Log
from video.src.data import retry_get
from video.src.timenow import TimeNow
from video.videoupdate.urlcheck import check_url
from video.videodownload.download import DownloadVideo
from video.videoupdate.messupdate import update_message

reload(sys)
sys.setdefaultencoding('utf8')


# 由于芒果TV的服务器是电信的，移动网访问会经常报HTTP或connect的相关错误，换到电信网下就好了
class MangoTV(object):
    def __init__(self):
        self.file_name = "mangotv"
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

    def mg_message(self, web_url):
        # 获取视频vid、cid
        try:
            pattern = re.compile(r'/(\d+).html')
            vid = pattern.findall(web_url)[0]
            pattern = re.compile(r'/(\d+)/')
            cid = pattern.findall(web_url)[0]
        except:
            data = retry_get(web_url, self.headers)
            pattern = re.compile(r'vid: (\d+),')
            vid = pattern.findall(data)[0]
            pattern = re.compile(r'cid: (\d+),')
            cid = pattern.findall(data)[0]
        video_id = vid
        # 构造请求url
        req_url = 'https://pcweb.api.mgtv.com/player/video?' + 'video_id=' + vid + '&cid=' + cid
        # 获取数据
        data = retry_get(req_url, self.headers)
        # 将数据python化
        data_json = json.loads(data)
        # 获取视频名称
        try:
            video_author = data_json['data']['info']['title'].encode('utf8')
            video_name = video_author + '-' + data_json['data']['info']['desc'].encode('utf8')
        except:
            try:
                pattern = re.compile(r'"title":"(.*?)",')
                video_author = pattern.findall(data)[0]
                pattern = re.compile(r'"desc":"(.*?)",')
                video_name = video_author + '-' + pattern.findall(data)[0]
            except:
                pattern = re.compile(r'"desc":"(.*?)",')
                video_name = pattern.findall(data)[0]
                video_author = ''
        # 获取视频时长
        try:
            video_modify = data_json['data']['info']['series'].encode('utf8')
        except:
            pattern = re.compile(r'"series":"(.*?)",')
            video_modify = pattern.findall(data)[0]
        # 获取视频长传时间
        try:
            video_time = data_json['data']['info']['duration'].encode('utf8')
        except:
            pattern = re.compile(r'"duration":"(.*?)",')
            video_time = pattern.findall(data)[0]
        # 获取stream_domain
        try:
            stream_domain = data_json['data']['stream_domain'].encode('utf8')
        except:
            pattern = re.compile(r'http://web-disp\d*.titan.mgtv.com')
            stream_domain = pattern.findall(data)
        # 获取stream_url
        try:
            stream_url = []
            stream = data_json['data']['stream']
            for each_stream in stream:
                stream_url.append(each_stream['url'].encode('utf8'))
        except:
            # 获取stream
            pattern = re.compile(r'"stream":\[(.*?)\]', re.S)
            stream = pattern.findall(data)[0]
            # 获取stream_url
            pattern = re.compile(r'"url":"(.*?)"')
            stream_url = pattern.findall(stream)
        # 构造url为获取原视频地址部分参数
        if len(stream_domain) == len(stream_url):
            req_url_para_list = stream_domain[len(stream_domain) - 1] + stream_url[len(stream_url) - 1]
        else:
            req_url_para_list = stream_domain[0] + stream_url[0]
        # 获取原视频url地址相关参数1
        data = retry_get(req_url_para_list, self.headers)
        data_json = json.loads(data)
        try:
            info = data_json['info'].encode('utf8')
        except:
            pattern = re.compile(r'"info":"(.*?)"')
            info = pattern.findall(data)[0]
        # 获取原视频地址参数1
        pattern = re.compile(r'(^http:.*?mp4)')
        para_list_1 = pattern.findall(info)[0]
        # 获取原视频url地址相关参数1集合(不能开myeclipse)
        try:
            data = retry_get(info, self.headers, timeout=30)
        except Exception as e:
            count = 5
            while str(e) == "('Connection aborted.', error(10054, ''))" and count > 0:
                time.sleep(10)
                try:
                    count -= 1
                    data = retry_get(info, self.headers, timeout=30)
                except Exception as e:
                    mess = TimeNow.get_time() + ' ' + str(e)
                    Log.log(mess)
                    print (mess)
        # 获取原视频大小集合
        pattern = re.compile(r'#EXT-MGTV-File-SIZE:(\d+)')
        video_size = pattern.findall(data)
        # 获取原视频地址参数2
        pattern = re.compile(r',([^0-9|A-Z].*?mp4\.ts\?.*?)#', re.S)
        para_list_2 = pattern.findall(data)
        # 获取视频原地址集合
        video_url = []
        for para_list in para_list_2:
            original_url = para_list_1 + '/' + para_list.replace("\n", "")
            video_url.append(original_url)
        # 构造请求url
        req_url = 'https://vc.mgtv.com/v2/dynamicinfo?vid=' + vid
        # 获取数据
        data = retry_get(req_url, self.headers)
        json_data = json.loads(data)
        # 获取视频播放量
        video_view = str(json_data['data']['all'])
        # 获取视频点赞数
        video_support = str(json_data['data']['like'])
        # 获取视频不点赞数
        video_oppose = str(json_data['data']['unlike'])

        return video_id, video_name, video_author, video_size, video_time, video_modify, video_view, video_oppose,\
            video_support, video_url

    def mg_mysql(self, web_url):

        video_message = self.mg_message(web_url)
        count = 0
        video_file = ''
        conn = self.connect
        while count < len(video_message[9]):
            video_name = video_message[1] + '(' + str(count) + ')'
            download_video = DownloadVideo(video_message[9][count], unicode(video_name, "utf-8"), self.file_name)
            video_file = download_video.video_download()
            count += 1
        cur = conn.cursor()
        sql = "INSERT INTO mangotv(Video_Id, Video_Name, Video_Author, Video_Size, Video_Time, Video_Modify" \
              ", Video_View, Video_Oppose, Video_Support, Video_Web, Video_Url, Video_File) " \
              "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        try:
            cur.execute(sql, (video_message[0], video_message[1], video_message[2], video_message[3][count - 1],
                              video_message[4], video_message[5], video_message[6], video_message[7],
                              video_message[8], web_url, video_message[9][count - 1], video_file))
            conn.commit()
        except Exception as e:
            print (e)
            conn.rollback()
        cur.close()
        conn.close()

    def mg_update(self, web_url):

        video_message = self.mg_message(web_url)
        flags = check_url(web_url, video_message, self.file_name, self.connect, " ")

        flag1 = flags[0]
        flag2 = flags[1]
        flag3 = flags[2]
        lost_url = ''
        check = ''

        conn = self.connect
        if flag1 and flag2 and flag3:
            cur = conn.cursor()
            sql = "SELECT Video_View, Video_Oppose, Video_Support " \
                  "FROM mangotv " \
                  "WHERE Video_Web=%s AND Video_Name=%s"
            try:
                cur.execute(sql, (web_url, video_message[1]))
                check = cur.fetchone()
                conn.commit()
            except Exception as e:
                print (e)
                conn.rollback()
            cur.close()

            flags = update_message(check, conn, web_url, video_message)
            flag4 = flags[0]
            flag5 = flags[1]
            flag6 = flags[2]

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
