#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 27 21:41:58 2017

@author: wanggb
"""


#import the necessary packages
import pandas as pd
import urllib
import time
from urllib import request
from bs4 import BeautifulSoup 
import re
import datetime
import json

###寻找API
#注意：以上请求返回的是页面呈现出来的数据的结果，我们需要找到网站的API，然后定时获取数据
url = "http://api.q.fx678.com/quotes.php?exchName=WH&symbol=USD"
html=urllib.request.urlopen(url).read()
html=html.decode("utf-8")
soup=BeautifulSoup(html,"lxml")
data = soup.get_text()
data = json.loads(data)
#解析json
TheDatetime = datetime.datetime.fromtimestamp(int(data['t'][0])).strftime("%Y-%m-%d %H:%M:%S")
b = data['b'][0]
o = data['o'][0]
h = data['h'][0]
l = data['l'][0]
c = data['c'][0]
p = data['p'][0]
se = data['se'][0]
result = [TheDatetime,b,o,h,l,c,p,se]
print(result)
#t代表时间
#o h l c 分别代表开盘价、最高价、最低价、收盘价
#b 和 se其中一个应该是当前价格，你设置一个定时任务，每分钟抓取一次数据，即可获得你想要的结果
