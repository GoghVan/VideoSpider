VideoSpider
===========
（目前项目还在开发当中，尽情期待新的内容）<br>
此项目是利用python2.7编写爬虫将的视频网站的web_url进行一系列操作，解析其真实视频地址和其视频相关的一些信息，<br>
例如视频的名称、ID、观看数、点赞数、评论数等，最后将其视频下载到本地文件夹内，然后将其他的信息保存至mysql数 <br>
据库中。<br>
那么如何由网站的视频地址找到其视频的真实地址呢？<br>
我们一步一步来看O(^_^)O<br>
<br>
首先先来了解一下基本的<strong>数据库操作</strong><br>
我所使用的是<strong>mysql</strong>数据库，利用<strong>SQLyog</strong>来管理我的数据库。<br>
利用SQL语句：<br>
```python
import MYSQLdb
import sys
conn = MYSQLdb.connect('localhost', 'root', 'root', 'test')        //连接test数据库
try:
  cur = conn.cursor()
  cur.execute("DROP TABLE IF EXISTS rr")
  sql = "CREAT TABLE rr(
    Video_Id varchar(10) NOT NULL,      //Id
    Video_Name varchar(50),             //名称
    Video_Url varchar(100),             //真实url
    Video_Author varchar(20),           //作者
    Video_Time varchar(10),             //时长
    Video_Size varchar(20),             //大小
    Video_ViewCount varchar(20),        //观看数
    Video_CommentCount varchar(20),     //评论数
    Video_FavCount varchar(20),         //点赞数
    Video_Web varchar(50),              //web_url
    File_Url varchar(100),              //本地存放地址
    PRIMARY KEY (Video_Id)              //设置主键
  )"
  cur.execute(sql)
  cur.close()
  conn.commit()
except:
  conn.rollback()
conn.close()
```
创建出我们所需要的表

<h3>人人视频</h3>
首先打开人人视频的网站 http://www.rr.tv/#/<br>
虽然网站给人的印象比较简答，但其内容还算广泛，也没有多余的广告.......<br>
接着随便打开一个视频,例如其web_url：http://rr.tv/#/video/394450<br>
按照一般的操作，我们肯定先会<strong>右键查看网页源代码</strong><br>
可是.....确实这样：<br>
