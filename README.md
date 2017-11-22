VideoSpider
===========

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;此项目是利用<strong>python2.7</strong>编写爬虫将的视频网站的web_url进行一系列操作，解析其真实视频地址和其视频相关的一些信息，例如视频的名称、ID、观看数、点赞数、评论数等，最后将其视频下载到本地文件夹内，然后将其他的信息保存至mysql数据库中。（目前项目还在开发当中，尽情期待新的内容）<br>
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
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;按照一般的操作，我们肯定先会<b>右键查看网页源代码</b>：view-source:http://rr.tv/#/video/394450<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;可是.....事实却是只有一些基础的<b>HTML + javascript</b>代码，对于我们这个项目没有多大的帮助。

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;所以我们就要用到抓包利器<b>开发者工具</b>，我用的是<b>Chrome</b>浏览器，快捷键是<b>F12</b>，其他的浏览器一般都可以在设置里面找得到（点击 https://jingyan.baidu.com/article/c843ea0bb9433577921e4a50.html 学习谷歌浏览器开发者工具的基本操作）。
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;获取视频真实地址的第一种方法。刷新后，点击<b>Network</b>，我们可以清楚的看到最上面的<b>时间线</b>中有一条很长的蓝色线段，我们将区间拖动到这条蓝色的线条范围内，下面左边就会被过滤出一个<b>URL</b>,点击这个<b>URL</b>我们可以看到右边的<b>Preview</b>和<b>Response</b>为空的，但是<b>Headers</b>里面就有我们所需要的内容：Request URL:http://qcloud.rrmj.tv/2017/10/14/15b944f6c44541a1979769db41841e23.mp4.f30.mp4?sign=2719acf1b797caa7e631a6ff2d15de0e&t=59e7059d&r=1544495093411242940 ，我们发现里面有<b>.mp4</b>的字符串，我们复制这个<b>URL</b>到浏览器，奇迹出现啦！出现的视频正是我们在网站看到的视频，所以视频的真实地址已经被我们找到，它的获取方式是<b>GET</b>。<br>

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;获取视频真实地址的第二种方法。上面的方法确实可行，但是结合项目本身，我决定还是放弃第一个做法。还是利用<b>开发者工具</b>,刷新后左边出现了很多的数据，整体浏览一遍后我们可以发现在中间偏上的一块区域内出现了两次“<b>getVideoPlayLinkByVideo</b>、<b>detail</b>、<b>list</b>、<b>profile</b>、<b>all</b>、<b>profile</b>”,我们挨个点击发现最前面的数据在<b>Preview</b>中没有显示任何的数据，而后面都会有数据。我们点开<b>etVideoPlayLinkByVideo</b>，发现<b>Preview</b>中有<b>JSON</b>数据，逐级展开后，我们就会惊奇的发现,里面有<b>playLink</b>:http://qcloud.rrmj.tv/2017/10/14/15b944f6c44541a1979769db41841e23.mp4.f30.mp4?sign=237a2538b6310983f1913ad8b687505f&t=59e7288b&r=6224854028442601914 ,我们发现里面有<b>.mp4</b>的字符串，我们复制这个<b>playLink</b>到浏览器，奇迹出现啦！出现的视频正是我们在网站看到的视频，所以视频的真实地址已经被我们找到，在<b>Headers</b>中我们可以看到它的获取方式是向<b>http://web.rr.tv/v3plus/video/getVideoPlayLinkByVideoId</b>发送<b>POST</b>请求。<br>
所以代码可以这样写：
```python
import js
import requests

  headers = {'clientVersion': '0.1.0', 'clientType': 'web',}                                  # 添加客户端版本信息
  video_id = re.search(r'[0-9]+', web_url).group()                                            # 获取视频的ID
  api_url = 'http://api.rr.tv/v3plus/video/getVideoPlayLinkByVideoId'                         # 调用视频接口
  req_js = requests.post(api_url, data={'videoId': video_id}, headers=headers).content        # 发送请求获取数据
  req_py = json.loads(req_js)                                                                 # 将JSON数据转换为Python数据
  video_url = req_py["data"]["playLink"]                                                      # 获取视频真实地址
  print video_url
```

这样就可以将视频的真实地址以字符串的形式输出。<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;接着再往下看，会看到有<b>detail</b>，点击<b>detail</b>，在右边的<b>Preview</b>中有<b>JSON</b>数据，逐级展开后，我们最后会在<b>videoDetailView</b>中发现有该视频的信息：<b>author</b>、<b>title</b>、<b>commentCount</b>、<b>favCount</b>、<b>viewCount</b>。在<b>Headers</b>中我们可以看到它的获取方式是向<b>http://web.rr.tv/v3plus/video/detail</b>发送<b>POST</b>请求。<br>
参考上面的代码，变换一下<b>api_url</b>和其对应的<b>pyhon</b>获取<b>JSON</b>中重要信息的代码：
```python
  api_url = 'http://web.rr.tv/v3plus/video/detail'                         # 调用信息接口
```
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;如果对于<b>python</b>操作<b>JSON</b>不太清楚，可以参考文档：http://www.jb51.net/article/73450.htm <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;通过以上的步骤，我们就可以将与视频相关的所有信息获取到了，剩下的就是调用下载函数将视频下载下来，将数据存入数据库。<br>

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;因为项目的增加，之前写的代码的利用性降低了，所以对其中几个地方做了些改变，以至于更好的适应其他的项目。<br>

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<strong>DownloadVideo</strong>文件中牵扯到将不同网站的的视频下载到不同的文件夹中，所以传入<b>video_file</b>这个参数，只要调用下载函数时多传入一个字符串来表明是哪个文件夹，视频就会被下载到不同的文件中，不会被搞混。然后发现这次的视频是<b>.flv</b>文件格式，而不是上次的<b>.mp4</b>文件格式，所以就会出现文件已经下载下来但是播放不了的问题，在这里只需要判断一下视频原下载地址是什么格式的然后对其分配相应格式的后缀名就好了，如下：
```python
  if '.flv' in self.url:
    file_f = '存放文件路径' + '视频名称' + '.flv'
  elif '.mp4' in self.url:
    file_f = '存放文件路径' + '视频名称' + '.mp4'
  else:
    file_f = '存放文件路径' + '视频名称' + '.mp4'
```
（其实下载一个很好的视频播放器，不管是.mp4还是.flv还是等等，都可以随便观看啦，大家可以从网上找找！！）<br>

...接下来我们就切入这次的正题/（￥_￥）\

<h3>网易视频</h3>
<b>网易视频包含的种类繁多，所以我只挑了其中3部分来做，包括：http://v.163.com/paike 、 http://v.163.com/zixun 、http://v.163.com/jishi </b>，大家可以将以上三个分支下的视频下载下来。<br>

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;打开其中一个视频：http://v.163.com/paike/VBFGBLNBF/VBHBGAC2L.html <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;其实很多网页视频的url都还是蛮规整的0（！_ ！）0<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;先来介绍最最简单的一个获取视频原下载地址的方法：鼠标右键点击<b>检查网页源代码</b>，大致浏览一下网页的<b>html</b>发现其实代码挺乱的，大量的<b><script></script></b>标签嵌套在<b>html</b>中，但这对于我们我们有好处，仔细的再浏览一遍发现有很多有用的<b>JSON</b>文件，类似于：
```python
  var _param = {
    pltype : 6,
    videoadv : 'http://v.163.com/special/008547FN/vo_zixun.xml',
    openSub : false,
    width : '100%',
    height : '100%'
  };
```
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;所以我们很快的发现了带有<b><video></video></b>的标签，其中就有我们想要的视频原地址：
```html
  <source src="http://flv.bn.netease.com/videolib3/1603/16/aUzmv6975/SD/aUzmv6975-mobile.mp4" type="video/mp4">
```
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;将其复制到浏览器地址栏中，回车你就会惊奇的发现出现了下载对话框，点击确认，你就会将视频下载到本地。所以这段的代码可以利用<b>正则表达式</b>来获取地址：
```python
  html = requests.get(web_url)
  pattern = re.compile(r'source src="(.*?)"', re.S | re.M | re.I)
  real_s_url = pattern.findall(html.text)[0].encode('utf8')
```
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;但是，我肯定不会这样做滴，原因有三：首先下载下来的视频是标准视频，很多视频都会有高清和超高清视频，我们当自然要下载质量高的视频了；其二如果哪天人家看着直接放出视频原地址不顺眼，将该隐藏的隐藏掉，那就不好玩了，找也找不到了；其三牵扯到视频相关信息的下载。所以我们还是一步一步来吧。<br>
<br>
<strong>视频原地址</strong><br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;通过<b>开发者工具</b>，我们挨个的找取以<b>.js</b>或<b>.xml</b>结尾的请求url，发现带有<b>1000_VBHBGAC2L.xm</b>的这个url中有我们想要的东西：在<b><flv></flv></b>中就是我们要找的视频原地址，一共有6个，分别在<b><flvUrl></flvUrl>、<hdUrl></hdUrl>、<shdUrl></shdUrl></b>中，这三种标签分别代表视频为：标清、高清、超高清。（flv和flv4对我们没有很大的影响，所以可以归纳为三个url）
我们要做的就是将这里面对应的视频清晰度最好的地址获取到。
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;这段文件的请求<b>url</b>为：http://xml.ws.126.net/video/2/L/1000_VBHBGAC2L.xml ，打开多个视频我们可以看到其中有些部分是不会改变的：<b>http://xml.ws.126.net/video/</b>和<b>.xml</b>。所以我们要做就是<b>构造</b>这类请求的<b>url</b>。
通过观察我们可以发现<b>2</b>和<b>L</b>是<b>VBHBGAC2L</b>的最后两个字母，而<b>_VBHBGAC2L</b>前面的<b>1000</b>,我们可以在网页源代码中找得到：<b>topicId='1000'</b>。所以我们可以通过以上的分析得到下面这段代码（我们将<b>VBHBGAC2L</b>作为<b>id</b>）：
```python
  html = requests.get(web_url, headers=header)
  pattern = re.compile(r'topicid : "(.*?)"', re.S | re.M | re.I)
  cid = pattern.findall(html.text)[0].encode('utf8')  # 获取topicid
  id = [web_url][0]  # 将url进行list处理获取id
  # 构造url
  req_url = 'http://xml.ws.126.net/video/' + id[-7] + '/' + id[-6] + '/' + cid + '_' + id[-14: -5] + '.xml'
```
然后通过<b>GET</b>请求访问这个<b>req_url</b>得到<b>xml</b>文件，进行解析，得到清晰度较高的视频地址。<br>
<br>
<strong>视频信息</strong><br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;接着再通过<b>开发者工具</b>，找到了<b>http://sdk.comment.163.com/api/v1/products/a2869674571f77b5a0867c3d71db5856/threads/BHBGAC2L008535RB?ibc=jssdk&callback=tool1002321329669789156_1509093181749&_=1509093181750</b>这个<b>url</b>,它所返回的数据正是要找的大部分视频信息。要获取这个信息的办法还是构造请求的<b>url</b>,但是发现这个url很长，url中还包含着很多的参数，再怎么查找发现其他的包里面没有关于其参数的信息。所以我们要想办法去简化其<b>url</b>。经过测试发现，将<b>?ibc=jssdk&callback=tool1002321329669789156_1509093181749&_=1509093181750</b>这些参数去掉我们还是可以访问到这个文件。所以我们只需要构造类似于<b>http://sdk.comment.163.com/api/v1/products/a2869674571f77b5a0867c3d71db5856/threads/BHBGAC2L008535RB</b>的<b>url</b>。经过多次试验，发现其中<b>http://sdk.comment.163.com/api/v1/products/</b>和<b>/threads/</b>不会改变。我们只需要获取到<b>a2869674571f77b5a0867c3d71db5856</b>和<b>BHBGAC2L008535RB</b>就可以了。结合之前的思路，我们很快在网页源代码中发现了其参数：<b>"docId" :  "BHBGAC2L008535RB"</b>和<b>"productKey" : "a2869674571f77b5a0867c3d71db5856"</b>。所以我们可以通过以上的分析得到下面这段代码：
```python
  pattern = re.compile(r'"productKey" : "(.*?)"', re.S | re.M | re.I)
  product_key = pattern.findall(html.text)[0].encode('utf8')
  try:
      pattern = re.compile(r'"docId" :  "(.*?)"', re.S | re.M | re.I)
      doc_id = pattern.findall(html.text)[0].encode('utf8')
  except:
      doc_id = pattern.findall(html.text)[0].encode('utf8')
  mess_url = 'http://sdk.comment.163.com/api/v1/products/' + product_key + '/threads/' + doc_id
```
然后通过<b>GET</b>请求访问这个<b>mess_url</b>得到<b>JSON</b>文件，进行解析，得到其中关于视频的信息。（还有其他的信息的获取方法类似与上面所说）<br>
<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;最后就是将获取的内容全部存入数据库中，然后进行更新操作，这部分的内容和前面的类似，就不在这里赘述了。
<b></b>

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;因为项目数量的增加，发现不同项目中的类似代码冗余量太大，一方面解析模块代码量过于庞大，另一方面程序运行容易出问题。所以对以上问题作出了修改：<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;（1）由于长时间运行代码，在不断地向目的服务器发送<b>url</b>，请求数据的时候可能会由于对方服务器访问量过多或者本机的网络太差，一次请求不能获得我们所需要的数据（404或者页面丢失），我们需要多次的请求，所以在<b>src</b>模块中加入<b>retey_get</b>/<b>retry_post</b>：当返回的状态码错误时自动的再次请求。<br>
```python
  def retry_get(req_url, headers, count=5):           # 网络差时多次get请求
      try:
          request = requests.get(req_url, headers=headers, timeout=60)
          request.raise_for_status()
          data = request.content
      except requests.HTTPError as e:
          data = None
          if count > 0:
              count -= 1
              time.sleep(10)
              retry_get(req_url, headers, count-1)
      return data
```
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;（2）将<b>lost_update</b>从各个解析模块中提出，进行整合放入一个<b>lostupdate</b>模块中，在模块内对不同的需求进行不同的任务分配。<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;（3）将<b>lost_mess</b>从各个解析模块中提出，进行整合放入一个<b>lostmess</b>模块中，在模块内对不同的需求进行不同的任务分配。<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;（4）将<b>ckeck_url</b>从各个解析模块中提出，进行整合放入一个<b>urlcheck</b>模块中，在模块内对不同的需求进行不同的任务分配。<br>
（更改后的调用与之前的一样）<br>
  <br>
  
  <h3>凤凰视频</h3>
  <b>凤凰视频包含的种类繁多，除了直通车、天天看、星期7、大放送四个模块，其余都可以下载。</b><br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;打开其中一个视频：http://v.ifeng.com/video_9119714.shtml <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;这个网页视频的url都还是蛮规整的0（！_ ！）0<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;观察网页，我们可以获取到的信息有：视频名称、视频上传时间、视频播放时长、视频的观看量、视频的点赞数、视频的不点赞数、视频的评论数等等。<br>
  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;右键点击<b></b>网页查看源代码，仔细浏览后发现唯一可能有用的信息：
```python
 <script>
        var videoinfo = {
            "id":"9119714",
            "vid": "56ca21e4-59df-49ab-8afa-bb38317a13cd",
            "name": "贾玲爆笑上演多版本“来自星星的你” 还是东北女神最传情",
            "duration": "572",
            "url": "http://v.ifeng.com/video_9119714.shtml",
            "skey":"746F26",
            "videoLargePoster": "http://p1.ifengimg.com/a/2017_44/3ce23a9f6783667.jpg",
            "playerName":"vFreePlayer",  
            "mUrl":"http://v.ifeng.com/dyn/m/video/9119714/index.shtml",
            "categoryId":"57-60",
            "mediaId":"764981",
            "adtype":"5",
            "categoryPath":"variety",
            "danmaku": "",
            "columnName":"开心大米粒",
            "CPId": '166',
            "keywords": '百变大咖秀 贾玲 何炅',
            "createdate": '2017-11-01 20:55:02'
        };
    </script>
```
信息量不全，所以我们暂且先放弃从源代码中获取信息的方式。<br>
<strong>视频信息+原地址</strong>（这次两个内容是连在一起的，所以一并介绍）<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;接着再通过<b>开发者工具</b>，找到了<b>http://tv.ifeng.com/h6/9119714/video.json?callback=callback&msg=9119714&rt=js&param=play&_=1509805191192</b>这个<b>url</b>，其<b>Preview</b>中有我们想要获取的部分信息，包括视频的原地址。经过简化后发现<b>http://tv.ifeng.com/h6/9119714/video.json?callback=callback&msg=9119714&rt=js</b>也可以访问到我们所想问的数据(json)：
 ```python
 {
    "preview": {
        "path": "http://p0.ifengimg.com/pmop/2017/11/01/70006145-b563-40f6-bad2-cc974bd09e5a.jpg",
        "sub_width": 128,
        "time_span": 6,
        "sub_height": 72,
        "width": 1280,
        "sub_picture_number": 95,
        "picture_number": 1,
        "height": 720
    },
    "videoLargePoster": "http://p1.ifengimg.com/a/2017_44/3ce23a9f6783667.jpg",
    "cpId": "166",
    "createdate": "2017-11-01 20:55:02",
    "bqSrc": "http://ips.ifeng.com/video19.ifeng.com/video09/2017/11/01/12610851-102-009-205616.mp4",
    "mediaId": 764981,
    "title": "贾玲爆笑上演多版本“来自星星的你” 还是东北女神最传情",
    "url": "http://v.ifeng.com/video_9119714.shtml",
    "videoPlayUrl": "http://ips.ifeng.com/video19.ifeng.com/video09/2017/11/01/12610851-102-009-205616.mp4",
    "vid": "56ca21e4-59df-49ab-8afa-bb38317a13cd",
    "duration": 572,
    "posterUrl": "http://p1.ifengimg.com/a/2017_44/3ce23a9f6783667.jpg",
    "anchor": [],
    "CPId": "166",
    "aspect": "16:9",
    "name": "贾玲爆笑上演多版本“来自星星的你” 还是东北女神最传情",
    "guid": "56ca21e4-59df-49ab-8afa-bb38317a13cd",
    "gqSrc": "http://ips.ifeng.com/video19.ifeng.com/video09/2017/11/01/12610851-102-009-205616.mp4",
    "id": 9119714,
    "keyword": "百变大咖秀 贾玲 何炅",
    "categoryId": "57-60",
    "mediaName": "开心大米粒",
    "columnName": "开心大米粒"
}
 ```
 其中<b></b>"createdate"是视频的上传时间，<b>"bqSrc"</b>、<b>"videoPlayUrl"</b>、<b>"gqSrc"</b>为视频的原地址（就目前测试来看下载下来的视频没有什么区别），<b>"title"</b>为视频的名称，<b>"mediaName"</b>、<b>"columnName"</b>为视频上传者（只有极少数不一样），<b>"vid"</b>、<b>"guid"</b>为重要的参数（两者都一样），之后要用的到。<br>
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;所以接下里的任务就是如何构造此请求<b>url</b>。经过测试发现只有<b>msg=9119714</b>中的参数和前面的<b>id</b>在变化，其实两者是同一个东西，所以只要获取到<b>web_url</b>中的<b>id</b>，拼接到其中即可：
 ```python
 
  pattern = re.compile(r'http://v.ifeng.com/video_(.*?)\.shtml', re.S | re.I | re.M)
  video_id = pattern.findall(web_url)[0]
  req_url = 'http://tv.ifeng.com/h6/' + video_id + '/video.json?callback=callback&msg=' + video_id + '&rt=js'
```
进行访问时一定要加头部<b>（headers）</b>，之后对其进行解析获取信息就好。
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;但是还是有一些信息没有获取到：视频的播放量、点赞数、不点赞数、评论量。通过逐一排查后，我们发现
分别在一下几个<b>url</b>中（逐一对应）：<br>
<b>http://survey.news.ifeng.com/getaccumulator_weight.php?format=js&serverid=2&key=56ca21e4-59df-49ab-8afa-bb38317a13cd&callback=f15f8766f6240</b>、<br>
<b>http://survey.news.ifeng.com/getaccumulator_ext.php?callback=jQuery17107289447875246187_1509805190738&key=56ca21e4-59df-49ab-8afa-bb38317a13cdding&format=js&serverid=1&var=ding</b>、<br>
<b>http://survey.news.ifeng.com/getaccumulator_ext.php?callback=jQuery17107289447875246187_1509805190739&key=56ca21e4-59df-49ab-8afa-bb38317a13cdcai&format=js&serverid=1&var=cai</b>、<br>
<b>http://comment.ifeng.com/getv.php?callback=jQuery17107289447875246187_1509805190737&job=3&format=js&docurl=56ca21e4-59df-49ab-8afa-bb38317a13cd</b>。由于其<b>url</b>太过于复杂，所以首先还是先进性简化，简化后为（逐一对应）：<br>
<b>http://survey.news.ifeng.com/getaccumulator_weight.php?format=js&key=56ca21e4-59df-49ab-8afa-bb38317a13cd</b>、<br><b>http://survey.news.ifeng.com/getaccumulator_ext.php?key=56ca21e4-59df-49ab-8afa-bb38317a13cdding</b>、<br><b>http://survey.news.ifeng.com/getaccumulator_ext.php?key=56ca21e4-59df-49ab-8afa-bb38317a13cdcai</b>、<br><b>http://comment.ifeng.com/getv.php?docurl=56ca21e4-59df-49ab-8afa-bb38317a13cd</b>。其中每一个对应的<b>key</b>都是相同的，即前面所获取到的<b>"vid"</b>与<b>"guid"</b>，所以讲其拼接到其中即可：
```python
  # 获取视频观看数(str)
  req_url = 'http://survey.news.ifeng.com/getaccumulator_weight.php?key=' + vid
  # 视频点赞数(str)
  req_url = 'http://survey.news.ifeng.com/getaccumulator_ext.php?key=' + vid + 'ding'
  # 视频不点赞数(str)
  req_url = 'http://survey.news.ifeng.com/getaccumulator_ext.php?key=' + vid + 'cai'
  # 视频评论数(str)
  req_url = 'http://comment.ifeng.com/getv.php?job=3&format=js&docurl=' + vid
```
同理进行访问时一定要加头部<b>（headers）</b>，之后对其进行解析获取信息就好。
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;最后就是将获取的内容全部存入数据库中，然后进行更新操作，这部分的内容和前面的类似，就不在这里赘述了。

<h3>芒果TV</h3>
<b>下载前须知：该视频网页web_url的格式必须为https://www.mgtv.com/b/cid/vid.html , 其中cid为6位数字，vid为7位数字！！！</b><br>
芒果TV是湖南广播电视台旗下唯一互联网视频平台，独家提供湖南卫视所有栏目高清视频直播点播，并为用户提供各类热门电影、电视剧、综艺、动漫、音乐、娱乐等内容。由湖南快乐阳光互动娱乐传媒有限公司（简称“快乐阳光”）负责具体运营。系湖南广播电视台全力发展网络视频业务的唯一新媒体机构。----百度百科<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;之前一直想爬取芒果TV的视频，经过几度的查找和测试，发现芒果TV的视频原地址种类很多，可能由于前期准备工作没有做好，所以放弃掉了。之后的偶然来了一些灵感，我就沿着之前的方法继续找了下去，最终还是被我找到了。\\(O_O)/<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;接下来我们就一步一步的来看（有点绕，不过很有趣！）<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;老办法，利用开发者工具，刷新视频页面，当视频加载到一半后暂停视频，转到开发者工具中，在左上角的输入框中输入<strong>video</strong>，它会自动的筛选出含有<strong>video</strong>的url。我们可以发现有几行是带有<strong>mp4.ts</strong>字段的，将其复制到浏览器地址栏，点击回车我们可以发现出来的就是该视频，不过只是一部分。所以将其余类似的url复制到地址栏，我们就会得到完整的视频。所以我们就可以大致推断出该视频网站的视频是分段存储的。<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;仔细观察视频原地址url发现此url很复杂，所需要的参数非常的多，即使你找遍所有的js包也不可能找全所有的参数，但是唯一有用的一点就是这个url的格式，我们之后会用得到。<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;因为视频的原地址是在是不好构造，那么就先来找到关于视频信息的url。通过仔细查找后发现：https://pcweb.api.mgtv.com/player/video?video_id=4153263&cid=167299&keepPlay=0&vid=&watchTime=0&\_support=10000000, 这是一个json格式的文件，里面有很多有用的信息。简化后变为：https://pcweb.api.mgtv.com/player/video?video_id=4153263&cid=167299。 在<b>info</b>中有关于视频的名称、时长、上传日期等。最最令人惊喜的是我们第一眼就可以看到有：标清、高清、超清的字段。很多人的第一感觉是：喔喔，终于找到了视频的原地址。但是当逐级展开后才发现，这里面的<b>url</b>只有一半，并且里面没有<b>mp4</b>或是<b>flv</b>的字段，这就令人很恼火。我之前的想法是拼凑到其它的<b>url</b>后是不是可以获得一些东西。经过多次尝试发现好像没有什么卵用。知道这次我突然发现在<b>stream</b>下面还有一个<b>stream_domain</b>标签，展开后里面也是有三个<b>url</b>，并且是完整的，将其复制到地址栏并访问后发现毛也没有。但是something hit me！就在不经意间我突然想到之前没有将上面缺失的<b>url</b>和下面这个<b>url</b>拼凑到一起去访问，不试不知道，一试吓一跳，还果真跳出来了点数据。还是json数据，那就更有用了。回到前面，仔细观察你会发现在<b>stream</b>中有三个缺失<b>url</b>，在下面的<b>stream_domain</b>有三个完整的<b>url</b>，经过几次尝试，发现以下规律：<b>stream</b>中<b>0</b>中的<b>url</b>只能与<b>stream_domain</b>中<b>0</b>中的<b>url</b>相结合，并且访问后会出现想要的数据，如果不按以上套路的话，之后的数据会出现差错。接着我们访问https://web-disp.titan.mgtv.com/vod.do?pm=yTDK6Bwlnfm5mniUXWM_xheXsHJy9ovX86dePBwXVxUbBQeBryHvwZ~LUUvHXAXROsTMsdWnfpbJ3lZCjqUCwdiI0_CJO6Pd2ZtY7zVbRT~owCHcFbdzVaEBIldRQ4kSyj7kcr~quvbGJARwntQcFBvDY~zqWkQZwgPDfvOBZdDLFXWP8Hid1uMTV9PuA1F3flDMUYLNsxIeTzJ~3qTqzlOwUmY-&fid=363B4D5D6ACE4B4EC42D69C10AF4726E&arange=0&gsid=164acb88-2301-4d64-af3c-c67b922111ca， 后发现<b>info</b>标签中有<b>MP4</b>字段，且其格式为<b>.m3u8</b>格式的（m3u8不知道的话网上搜一搜）完整url：http://202.109.167.175/c1/2017/10/30_0/47EF3DBB09BD495F5945834205F098D2_20171030_1_1_256_mp4/23270BB618347E98C7237180E54B1A73.m3u8?arange=0&pm=Q22CEwhDc4ERhxMu8vqX_goZwoHgJzf9NNpAFgnaky48OlgH~6yJpExVAhRFjzLDPH_wOgbhwVyMP5UgcJdpVKhe5syenJ2WMyZk81oOxftPW6lQ4GKaXkKVL1rtk0RyfFAr6lCYh_mKrCWWXl~PE9GyCc3UYwPB2Sdxs_qnANmk8RqYaLbJpNBanjbXB6Khq6ke5kJ3rwlAXUYLBZ1KBrs~K0NlpfYuEq0hUHG54GmR5G11IRMi~bGqSjP2vAvJGi5Qhz35kTXno1sUO4ccPBaQ98Zl9QDlbS_1PatCd~I2MqUp0RE8u0bv9A4JWqEYK4vw_lU1QZN3l_3u08Rr1TpPAsHB~SGq4Isr8KltDU0N67gjqXs_XIv1~qX1y0MD7l2KAY7ZJCyLf3Xz，  很多人又很兴奋了：终于终于找到了！！快速的将其粘贴到地址栏并访问，还真是有东西可以下载下来，下载下来后突然傻眼，怎么看不了？exc me？看看其属性大小，实在是小的可怜，那当然是下错了。所以我们换一种思路，不通过地址栏去访问，我们通过编写一段代码去访问或者利用现有的软件去访问，看看能不能获取一些有用的数据。我是用的<b>Postman</b>（大家可以在网上下载，很好用，教程网上都有的！）。通过<b>postman</b>访问后发现，出来了很多的数据，不清楚是什么格式的，但是确实非常有用。仔细观察后发现，隔几行就会有一些很长很长的字符串，其中带有很多的参数，并且在每一个长字符串的上两行都会有<b>#EXT-MGTV-File-SIZE</b>字段，后面会标有数字，一般都是万以上的数字。我们之前说过里的视频是分段存储的，其实到这里我们就已经恍然大悟了，这里的每段长字符串其实是分段视频每段的参数，上面的<b>SIZE</b>字段所对应的数字是这段视频的大小。<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;前面还说过<b>某个url</b>的格式很重要。对，就是抓包抓出来可以在网页上观看的<b>url</b>。通过对比后我们发现在<b>_mp4/</b>的后面出现的那一大串东西很像上面的那串很长的字符串，我们经过替换粘贴到地址栏并访问后发现并不能得到视频。那么问题出在哪呢？要怎么解决呢？时间证明：实践才是最好的老师。我发现<b>http://202.109.167.175/c1/2017/10/30_0/47EF3DBB09BD495F5945834205F098D2_20171030_1_1_256_mp4 </b>和<b>http://pcvideows.titan.mgtv.com/c1/2017/10/30_0/47EF3DBB09BD495F5945834205F098D2_20171030_1_1_256_mp4 </b>很相似，我何不将那段长字符串粘贴到http://202.109.167.175/c1/2017/10/30_0/47EF3DBB09BD495F5945834205F098D2_20171030_1_1_256_mp4 后面呢，经过测试，最终获得成功。通过构造所得到的url是原视频的地址。然后将所得到的长字符串挨个更换，我们发现就可以获得完整的视频。（以上对应的是标清，通过同样的方法可以获得高清和超清，代码提供的是超清）。<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;接着找到了https://vc.mgtv.com/v2/dynamicinfo?callback=jQuery182012115295195808984_1510472757793&_support=10000000&vid=4153263&_=1510472758501 ， 简化后https://vc.mgtv.com/v2/dynamicinfo?vid=4153263，同样可以得到相同的内容。里面有关于视频的播放量、点赞数、不点赞数。<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;在后面的代码编写和测试过程中可能你会发现是不是的就会报代码错误（例如：<b>Connection aborted.', error(10054, '')</b>），但是通过软件或者浏览器就正确，但是有时候就会发现都不好使了，这是怎么回事呢？观察<b>http://202.109.167.175/c1/2017/10/30_0/47EF3DBB09BD495F5945834205F098D2_20171030_1_1_256_mp4</b> 我们们可以发现，其中有个<b>202.109.167.175 </b>IP字段，上网查了后发现这是一个江西省吉安市的电信IP号，极有可能芒果TV是用的此服务器，所以通过移动宽带去访问的过程中移动与电信之间的“桥”经常断，所易导致代码一直报错，或者视频一直下载不下来。要彻底解决这个问题，那就尽可能在电信网下工作。<br><br>

以上纯属个人兴趣爱好，欢迎多多提意见，如有冒犯，尽请谅解，不喜勿喷！












