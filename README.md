VideoSpider
===========

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;此项目是利用python2.7编写爬虫将的视频网站的web_url进行一系列操作，解析其真实视频地址和其视频相关的一些信息，例如视频的名称、ID、观看数、点赞数、评论数等，最后将其视频下载到本地文件夹内，然后将其他的信息保存至mysql数据库中。（目前项目还在开发当中，尽情期待新的内容）<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;那么如何由网站的视频地址找到其视频的真实地址呢？<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;我们一步一步来看O(^_^)O<br>

<h3>数据库</h3>

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;首先先来了解一下这个项目的<strong>数据库操作。</strong><br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;我所使用的是<strong>mysql</strong>数据库，利用<strong>SQLyog</strong>来管理我的数据库。<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;利用SQL语句：<br>

```python
import MYSQLdb
import sys
conn = MYSQLdb.connect('localhost', 'root', 'root', 'video')        // 连接video数据库
try:
  cur = conn.cursor()
  cur.execute("DROP TABLE IF EXISTS rr")
  sql = "CREAT TABLE rr(
    Video_Id varchar(10) NOT NULL,      // Id
    Video_Name varchar(50),             // 名称
    Video_Url varchar(100),             // 真实url
    Video_Author varchar(20),           // 作者
    Video_Time varchar(10),             // 时长
    Video_Size varchar(20),             // 大小
    Video_ViewCount varchar(20),        // 观看数
    Video_CommentCount varchar(20),     // 评论数
    Video_FavCount varchar(20),         // 点赞数
    Video_Web varchar(50),              // web_url
    File_Url varchar(100),              // 本地存放地址
    PRIMARY KEY (Video_Id)              // 设置主键
  )"
  cur.execute(sql)
  cur.close()
  conn.commit()
except:
  conn.rollback()
conn.close()
```

创建出我们所需要的表rr去存放数据。(我是直接利用SQLyog里面可视化建表，方便、靠谱)<br>
(为什么要全部设置为varchar类型呢？因为参数传入数据库的时候比较方便，不用过于担心参数类型。)<br>
(参数类型这个问题是超级头痛，<b>type(xx)</b>这个函数很好用，搞不懂了自己就试一试这个。)<br>
表建好了，接下来就是将获取下来的存放到数据库中。<br>
这个比较简单，编写

```python
  def rr_mysql(url, video_url, video_message, video_url_file):
```

方法，传入web_url、视频真实地址、视频的一些信息、视频的本地存放地址等参数。<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;在方法中先<b>connection</b>连接数据库，接着建立<b>cursor</b>事务，再编写<b>SQL</b>语句，接着用<b>execute</b>实现SQL语句。最后可别忘了关闭事务和连接。<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;有些初学者可能对于传这么多的参数不知道如何下手，这里有一些方法：<br>

```python
// 第一种方法
  sql_1 = "INSERT INTO rr(x1, x2, x3, x4) " \
          "VALUES (%s, %s, %s, %s)"             
   cur.execute(sql, (n1, n2, n3, n4))
// 第二种方法
  sql_1 = "INSERT INTO rr(x1, x2, x3, x4) " \
          "VALUES (%s, %s, %s, %s)" % (n1, n2, n3, n4)            
   cur.execute(sql)
 // 错误方法
   sql_1 = "INSERT INTO rr(x1, x2, x3, x4) " \
           "VALUES (n1, n2, n3, n4)"
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;然后就是关于实时的将视频的动态变化信息存储到数据库中，对于数据库的操作大致没有变化，思路就是通过
<b>SELECT...WHERE...</b>语句查找数据库中关于相同<b>web_url</b>的那一条信息，然后和网上获取下来的数据进行对比，将变化的值通过<b>UPDATE...SET...WHERE...</b>语句进行实时的更新。<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;由于种种可能，例如不小心将文件夹里的视频删除掉了或者数据库的某条信息丢失，我们就要在数据更新的的时候快速发现这个问题，并且解决掉：将缺失的数据、丢失的视频文件补回来。所以解决这个问题的项操作和上面的更新数据方法雷同。数据库中的信息缺失很好解决，就是将没有的数据重新再写回数据库，那么此处有什么难点呢？（确实有，困扰了我几个小时，最后还是将其解决掉了）\\(^.^)/<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;问题就在于如何判断存放这个视频的文件夹中是否缺失了某个视频：彻底丢失或者视频大小不完整。因为程序是在不断地运行中，文件夹中的视频量也是在变化。<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;我的第一个想法就是每次向文件夹中添加一个完整的视频就会使文件夹的size变大，我们在获取视频的时候已经将视频的大小得到了，那么每次下载玩一个视频，将这个文件的大小加上视频的大小，那么可以每次计算文件夹的大小来判断是否缺失视频。但是问题又来了，怎么实时的获取文件夹大小呢？我从网上查了查，找到了利用python获取文件夹的大小的方法：<br>

```python
from os.path import join, getsize

    def file_size(file_url):
        size = 0
        for root, dirs, files in os.walk(file_url):
            size = size + sum([getsize(join(root, name)) for name in files])
        return size
```
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;但是问题又来了，经过我的测试，每次只有当视频已经完全下载后这个大小才会显示正常，并且还不知道如何实时的获取视频流的大小。<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;第二个想法（已经成功）是在第一个想法的基础上更加细致了一些。每次通过某种方法获取到这个视频（已下载的）在文件夹中的大小，与网站中的视频大小进行对比判断是否文件损坏。但是这个前提是必须要判断出来视频（已下载）是否存在于文件夹中。
所以具体思路为：判断视频是否在文件夹中并且视频的大小等于网站上视频的大小，是的话就不做任何事，否的话则重新下载。经过我努力以及细心的在网上查找后发现，可以调用系统函数来实现上述的方法。<br>
```python
import os
from contextlib import closing
video_in_file = os.path.exists(video_in_file_url)         // 判断视频是否在文件夹里，返回TRUE OR FALSE
video_in_file_size = os.path.getsize(video_in_file_url)   // 得到视频在文件夹中的真实大小
```
此外，我们从数据库中获取数据后怎么显示出来呢？看一下这个例子：

```python
  conn = MySQLdb.connect(
       host='localhost', 
       port='3306', 
       user='root,
       passwd='root',
       db='XX',
       charset='utf8',
  )                                         // 连接数据库
  try:
    cur = conn.cursor()                     // 创建事务
    sql = "SELECT * " \
           "FROM XX " \
    cur.execute(sql)                        // 执行sql
    result_1 = cur.fetchone()               //  
    result_2 = cur.fetchmany(n)             // }获取数据
    result_3 = cur.fetchall()               //

    print result_1                          // 打印result_1结果
    
    for raw_2 in result_2:
      print raw_2                           // 打印result_2结果
      
    for raw_3 in result_3:
      print raw_3                           // 打印result_3结果
      
    cur.close()
    conn.commit()
  except:
    conn.rollback()
  conn.close()
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;假设数据库中有很多条的数据，那么利用<b>fetchone()</b>这个函数可以获取所获取数据的第一行，同时如果知道数据库有<b>n</b>条数据的话，可以用

```python
  for i in n:
    result = cur.fetchone()
```
上面这个方法一行一行的获取数据库中的所有数据；而<b>fetchmany(n)</b>可以一次性的获取<b>n</b>条数据，也是需要利用<b>for</b>循环来输出数据；最后<b>fetchall()</b>是一次性获取数据库中的所有数据，同理利用<b>for</b>循环来输出数据。

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;以上就是关于<b>MySQL</b>在这个项目中的一些应用与开发的过程中遇到的一些问题和解决方法。<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;如果对于<b>Python</b>操作<b>MySQL</b>数据库还有疑问的话，可以查阅这个文档：http://www.runoob.com/python/python-mysql.html
<h3>进度条显示ProgressBar</h3>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;因为下载视频的时候一直在等并且控制台也不会显示任何的东西，我们不能实时的看到下载的快慢与过程，这显得就有些让人着急，在结合项目本身，我们需要实时的获取视频流的大小来显示出来。所以我从网上查找了很多的信息，但效果都不是很好，不是我想要的结果，最后终于查到了一个文档：http://blog.csdn.net/supercooly/article/details/51046561<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;但是这个是利用<b>Python3.X</b>的<b>requests</b>模块，我这边用的是<b>Python2.7</b>。所以经过我的尝试与修改终于改为<b>Python2.7</b>可用的版本：

```python
import sys
    ....//以上内容和原文当中类似，改变相应参数即可
    def refresh(self, count=1, status=None):              //在控制台显示下载进度
        self.count += count
        self.status = status or self.status
        sys.stdout.write('\r')                            //
        sys.stdout.write(self.__get_info())               // }利用sys.studout.write()/flush()
        sys.stdout.flush()                                //
        if self.count >= self.total:
            self.status = status or self.fin_status
            sys.stdout.write('\r')
            sys.stdout.write(self.__get_info())
            sys.stdout.write('\n')

```

<h3>with....as...小语法</h3>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;再介绍一个很好用的语法：<b>with....as...</b>。它的作用是什么呢？来看一下这两个例子就明白了！

```python
//example one
  file = open('log.txt', 'w')
  file.write('I am a text!')
  file.close()
  
//example two
  with open('log.txt') as file:
    file.write('I am a text!')

```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;上述俩个例子都可以实现将<b>'I am a text!'</b>存放到已建好的文件<b>log.txt</b>中，但是第一个事例是先将文件打开<b>open</b>，再写入内容<b>write</b>，最后再关闭<b>close</b>。而第二个实例利用<b>with....as...</b>语句就可以直接实现打开文件和关闭文件的功能，这样大大减少了因代码繁多而忘记写<b>close</b>的问题。<br>
<br>
...接下来我们就切入正题/（￥_￥）\

<h3>人人视频</h3>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;打开人人视频的网站 http://www.rr.tv/#/<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;虽然网站给人的印象比较简答，但其内容还算广泛，也没有多余的广告.......<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;随便打开一个视频,例如其web_url：http://rr.tv/#/video/394450<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;按照一般的操作，我们肯定先会<strong>右键查看网页源代码</strong>：view-source:http://rr.tv/#/video/394450<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;可是.....事实却是只有一些基础的<b>HTML + javascript</b>代码，对于我们这个项目没有多大的帮助。

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;所以我们就要用到抓包利器<b>开发者工具</b>，我用的是<b>Chrome</b>浏览器，快捷键是<b>F12</b>，其他的浏览器一般都可以在设置里面找得到（点击 https://jingyan.baidu.com/article/c843ea0bb9433577921e4a50.html 学习谷歌浏览器开发者工具的基本操作）。
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;获取视频真实地址的第一种方法。刷新后，点击<b>Network</b>，我们可以清楚的看到最上面的<b>时间线</b>中有一条很长的蓝色线段，我们将区间拖动到这条蓝色的线条范围内，下面左边就会被过滤出一个<b>URL</b>,点击这个<b>URL</b>我们可以看到右边的<b>Preview</b>和<b>Response</b>为空的，但是<b>Header</b>里面就有我们所需要的内容：<b>Request URL</b>:<b>http://qcloud.rrmj.tv/2017/10/14/15b944f6c44541a1979769db41841e23.mp4.f30.mp4?sign=2719acf1b797caa7e631a6ff2d15de0e&t=59e7059d&r=1544495093411242940</b>，我们发现里面有<b>.mp4</b>的字符串，我们复制这个<b>URL</b>到浏览器，奇迹出现啦！出现的视频正是我们在网站看到的视频，所以视频的真实地址已经被我们找到，它的获取方式是<b>GET</b>。















