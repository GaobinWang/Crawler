#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 27 21:40:53 2017

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

###寻找返回数据的url
#Step1:用谷歌浏览器打开网址 http://quote.fx678.com/symbol/USD 
#Step2:页面右键单击"检查"
#Step3:点击"Network"选项，寻找返回数据的HTTP请求
#Step4:找到对应的url,即："http://api.q.fx678.com/history.php?symbol=USD&limit=288&resolution=5&codeType=8100&st=0.4970674538241555"
#Step5:网站服务器返回的是json格式的数据，对其进行解析即可获取相应结果
url = "http://api.q.fx678.com/history.php?symbol=USD&limit=288&resolution=5&codeType=8100&st=0.4970674538241555"
html=urllib.request.urlopen(url).read()
html=html.decode("utf-8")
soup=BeautifulSoup(html,"lxml")
data = soup.get_text()
data = json.loads(data)
data.keys() #t代表时间;c o h l 分别代表收盘价、开盘价、最高价、最低价
data['t'] = [datetime.datetime.fromtimestamp(i).strftime("%Y-%m-%d %H:%M:%S")  for i in data['t']]
FinalData = pd.DataFrame(data,index = data['t'])
FinalData = FinalData[['o','h','l','c']]
FinalData.plot()