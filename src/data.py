# -*- coding: utf-8 -*-
# @Time    : 2017/11/16 20:23
# @Author  : Gavin

import time
import requests
from video.src.log import Log
from video.src.timenow import TimeNow


def retry_get(req_url, headers, count=5, timeout=30):           # 网络差时多次get请求
    try:
        request = requests.get(req_url, headers=headers, timeout=timeout)
        request.raise_for_status()
        data = request.content
    except requests.HTTPError and requests.Timeout as e:
        mess = TimeNow.get_time() + ' ' + 'data.retry_get: ' + str(e)
        Log.log(mess)
        print (mess)
        data = None
        if count > 0:
            count -= 1
            time.sleep(10)
            retry_get(req_url, headers, count-1)
    return data


def retry_post(req_url, data, headers, count=5):           # 网络差时多次post请求
    try:
        request = requests.post(req_url, data=data, headers=headers, timeout=60)
        request.raise_for_status()
        data = request.content
    except requests.HTTPError as e:
        mess = TimeNow.get_time() + ' ' + 'data.retry_post: ' + str(e)
        Log.log(mess)
        print (mess)
        data = None
        if count > 0:
            count -= 1
            time.sleep(10)
            retry_post(req_url, data, headers, count-1)
    return data
