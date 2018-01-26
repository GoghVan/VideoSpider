# -*- coding: utf-8 -*-
# @Time    : 2017/11/22 8:59
# @Author  : Gavin

import MySQLdb


def messages():
    connect = MySQLdb.connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='Single',
        db='videos',
        charset="utf8",
    )
    file_name = ["renren", "wangyi", "fenghuang", "mangotv", "souhu"]
    return connect, file_name
