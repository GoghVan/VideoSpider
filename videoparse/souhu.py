# -*- coding: utf-8 -*-
# @Time    : 2017/11/16 20:23
# @Author  : Gavin

import re
import sys
import time
import json
import random
import MySQLdb
from video.src.data import retry_get
from video.src.timenow import TimeNow
from video.src.log import Log
from video.videocheck.urlcheck import check_url
from video.videocheck.messupdate import update_message
from video.videodownload.download import DownloadVideo

reload(sys)
sys.setdefaultencoding('utf8')


class SouHu(object):

    def __init__(self):
        self.file_name = "souhu"
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

    def sh_message(self, web_url):
        data = retry_get(web_url, self.headers)
        # 获取视频vid(video_id)
        if re.match(r'http://share.vrs.sohu.com', web_url):
            pattern = re.compile(r'id=(\d+)', re.M | re.I | re.S)
            video_id = pattern.findall(web_url)
        else:
            try:
                pattern = re.compile(r'\Wvid\s*[\:=]\s*[\'"]?(\d+)[\'"]?')
                video_id = pattern.findall(data)[0]
            except:
                pattern = re.compile(r'var vid=(\d+);')[0]
                video_id = pattern.findall(data)
        if '/n' in web_url:
            req_url = 'http://hot.vrs.sohu.com/vrs_flash.action?vid=%s' % video_id
            data = json.loads(retry_get(req_url, self.headers))
            for qtyp in ["oriVid", "superVid", "highVid", "norVid", "relativeId"]:
                if 'data' in data:
                    hqvid = data['data'][qtyp]
                else:
                    hqvid = data[qtyp]
                if hqvid != 0 and hqvid != video_id:
                    req_url = 'http://hot.vrs.sohu.com/vrs_flash.action?vid=%s' % hqvid
                    data = json.loads(retry_get(req_url, self.headers))
                    if not 'allot' in data:
                        continue
                    break
            # 一些参数
            host = data['allot']
            # prot = data['prot']
            # tvid = data['tvid']
            # 视频名称
            video_name = str(data['data']['tvName'])
            # 视频大小
            video_size = str(sum(data['data']['clipsBytes']))
            # 视频作者
            video_author = str(data['keyword'])
            # 视频上传时间
            video_modify = str(data['tv_application_time'])
            # 视频时长
            video_time = str(data['data']['totalDuration'])
            # 获取视频原url
            video_url = []
            for su, clip, ck in zip(data['data']['su'], data['data']['clipsURL'], data['data']['ck']):
                req_url = 'http://' + host + '/?prot=9&prod=flash&pt=1&file=' + clip + '&new=' + su + '&key=' + \
                    ck + '&vid=' + video_id + '&uid=' + str(int(time.time()*1000)) + '&t=' + str(random.random()) + '&rb=1'
                data = json.loads(retry_get(req_url, self.headers))
                video_url.append(str(data['url']))
            # 构造url
            req_url = 'https://count.vrs.sohu.com/count/queryext.action?vids=%s&callback=playCountVrs' % video_id
            # 视频观看数
            data = retry_get(req_url, self.headers)
            pattern = re.compile(r'"total":(\d+),', re.M | re.I | re.S)
            video_view = pattern.findall(data)[0]
            return video_id, video_name, video_author, video_size, video_time, video_modify, video_view, video_url
        else:
            # 视频上传时间
            pattern = re.compile(r',uploadTime: \'(.*?)\'', re.M | re.I | re.S)
            video_modify = pattern.findall(data)[0]
            # # 构造url
            req_url = "http://my.tv.sohu.com/play/videonew.do?vid=%s&referer=http://my.tv.sohu.com" % video_id
            # 一些参数
            data = json.loads(retry_get(req_url, self.headers))
            host = str(data['allot'])
            # prot = str(data['prot'])
            # tvid = str(data['tvid'])
            # 视频名称
            video_name = str(data['data']['tvName'])
            # 视频大小
            video_size = str(sum(map(int, data['data']['clipsBytes'])))
            # 视频作者
            video_author = str(data['wm_data']['wm_username'])
            # 视频时长
            video_time = str(data['data']['totalDuration'])
            # 视频原地址
            video_url = []
            for su, clip, ck in zip(data['data']['su'], data['data']['clipsURL'], data['data']['ck']):
                req_url = 'http://' + host + '/?prot=9&prod=flash&pt=1&file=' + clip + '&new=' + su + '&key=' + \
                    ck + '&vid=' + video_id + '&uid=' + str(int(time.time()*1000)) + '&t=' + str(random.random()) + '&rb=1'
                data = json.loads(retry_get(req_url, self.headers))
                video_url.append(str(data['url']))
            # 构造url
            req_url = 'http://vstat.v.blog.sohu.com/dostat.do?method=getVideoPlayCount&v=' + video_id
            # 视频观看数
            data = retry_get(req_url, self.headers)
            pattern = re.compile(r'"count":(\d+),', re.M | re.I | re.S)
            video_view = pattern.findall(data)[0]

            return video_id, video_name, video_author, video_size, video_time, video_modify, video_view, video_url

    def sh_mysql(self, web_url):
        video_message = self.sh_message(web_url)
        count = 0
        video_file = ''
        while count < len(video_message[7]):
            video_name = video_message[1] + '(' + str(count) + ')'
            video_file = DownloadVideo(video_message[7][count], unicode(video_name, "utf-8"), self.file_name)\
                .video_download()
            count += 1

        conn = self.connect
        cur = conn.cursor()
        sql = "INSERT INTO souhu(Video_Id, Video_Name, Video_Author, Video_Size, Video_Time, Video_Modify" \
              ", Video_View, Video_Web, Video_Url, Video_File) " \
              "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        try:
            cur.execute(sql, (video_message[0], video_message[1], video_message[2], video_message[3], video_message[4],
                              video_message[5], video_message[6], web_url, video_message[7][count - 1], video_file))
            conn.commit()
        except Exception as e:
            print ('souhu.sh_mysql: ' + str(e))
            conn.rollback()
        cur.close()
        conn.close()

    def sh_update(self, web_url):
        video_message = self.sh_message(web_url)
        flags = check_url(web_url, video_message, self.file_name, self.connect, " ")

        flag1 = flags[0]
        flag2 = flags[1]
        flag3 = flags[2]
        lost_url = ''
        check = ''

        conn = self.connect
        if flag1 and flag2 and flag3:
            cur = conn.cursor()
            sql = "SELECT Video_View " \
                  "FROM souhu " \
                  "WHERE Video_Web=%s AND Video_Name=%s"
            try:
                cur.execute(sql, (web_url, video_message[1]))
                check = cur.fetchone()
                conn.commit()
            except Exception as e:
                print ('souhu.sh_update.check: ' + str(e))
                conn.rollback()
            cur.close()

            flags = update_message(check, conn, web_url, video_message)
            flag4 = flags[0]

            if flag4:
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
