VideoSpider
===========
（目前项目还在开发当中，尽情期待新的内容）<br>
此项目是利用python2.7编写爬虫将的视频网站的web_url进行一系列操作，解析其真实视频地址和其视频相关的一些信息，<br>
例如视频的名称、ID、观看数、点赞数、评论数等，最后将其视频下载到本地文件夹内，然后将其他的信息保存至mysql数 <br>
据库中。<br>
那么如何由网站的视频地址找到其视频的真实地址呢？<br>
我们一步一步来看O(^_^)O<br>
<br>
<h3>数据库</h3>
首先先来了解一下基本的<strong>数据库操作</strong><br>
我所使用的是<strong>mysql</strong>数据库，利用<strong>SQLyog</strong>来管理我的数据库。<br>
利用SQL语句：<br>
```python
import MYSQLdb
import sys
conn = MYSQLdb.connect('localhost', 'root', 'root', 'video')        //连接video数据库
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
创建出我们所需要的表rr去存放数据。(我是直接利用SQLyog里面可视化建表，方便、靠谱)<br>
(为什么要全部设置为varchar类型呢？因为参数传入数据库的时候比较方便，不用过于担心参数类型)<br>
(参数类型这个问题是超级头痛，<b>type(xx)</b>这个函数很好用，搞不懂了自己就试一试这个。)<br>
表建好了，接下来就是将获取下来的存放到数据库中。<br>
这个比较简单，编写
```python
def rr_mysql(url, video_url, video_message, video_url_file):
```
方法，传入web_url、视频真实地址、视频的一些信息、视频的本地存放地址等参数。<br>
在方法中先<b>connection</b>连接数据库，接着建立<b>cursor</>事务，再编写<b>SQL</b>语句，<br>
接着用<b>execute</b>实现SQL语句。最后可别忘了关闭事务和连接。<br>
有些初学者可能对于传这么多的参数不知道如何下手，这里有一些方法：<br>
```python
//第一种方法
sql_1 = "INSERT INTO rr(Video_Id, Video_Name, Video_Url, Video_Author, Video_Time, Video_Size, " \
                  "Video_ViewCount, Video_CommentCount, Video_FavCount, Video_Web, File_Url) " \
                  "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"             
 cur.execute(sql, (video_message[7], video_message[0], video_url, video_message[1], video_message[2],
                   video_message[6], video_message[3], video_message[4], video_message[5], url,
                   video_url_file))
//第二种方法
sql_1 = "INSERT INTO rr(Video_Id, Video_Name, Video_Url, Video_Author, Video_Time, Video_Size, " \
                  "Video_ViewCount, Video_CommentCount, Video_FavCount, Video_Web, File_Url) " \
                  "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" % (video_message[7], video_message[0],
                  video_url, video_message[1], video_message[2],video_message[6], video_message[3], 
                  video_message[4], video_message[5], url,video_url_file)             
 cur.execute(sql)
 //错误方法
 sql_1 = "INSERT INTO rr(Video_Id, Video_Name, Video_Url, Video_Author, Video_Time, Video_Size, " \
                  "Video_ViewCount, Video_CommentCount, Video_FavCount, Video_Web, File_Url) " \
                  "VALUES (video_message[7], video_message[0],video_url, video_message[1], 
                  video_message[2],video_message[6], video_message[3], video_message[4], 
                  video_message[5], url,video_url_file)"
```


<h3>人人视频</h3>
首先打开人人视频的网站 http://www.rr.tv/#/<br>
虽然网站给人的印象比较简答，但其内容还算广泛，也没有多余的广告.......<br>
接着随便打开一个视频,例如其web_url：http://rr.tv/#/video/394450<br>
按照一般的操作，我们肯定先会<strong>右键查看网页源代码</strong><br>
可是.....确实这样：<br>
