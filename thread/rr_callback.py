# -*- coding: utf-8 -*-
import json
import re
import requests


class rr_callback:
    def __init__(self, max_urls=10,):
        self.max_urls = max_urls
        self.seed_url = "http://www.rr.tv/#/video/394883"

    def __call__(self,url):
        headers = {
            'clientVersion': '0.1.0',
            'clientType': 'web',
        }  # 添加客户端版本信息
        try:
            video_Id = re.search(r'[0-9]+', url).group()  # 获取视频的ID
            api_url = 'http://web.rr.tv/v3plus/video/detail'  # 调用信息接口
            req_js = requests.post(api_url, data={'videoId': video_Id}, headers=headers).content  # 发送请求获取数据
            req_py = json.loads(req_js)  # 将JSON数据转换为Python数据
            url_list = []
            for index in range(len(req_py["data"]["recommendVideoList"])):
                video_id = req_py["data"]["recommendVideoList"][index]["id"]
                url_list.append(video_id)
                if len(url_list) == self.max_urls:
                    break
            return url_list

        except Exception as e:
            print e


if __name__ == "__main__":
    scrape_callback = rr_callback()
    print scrape_callback()
