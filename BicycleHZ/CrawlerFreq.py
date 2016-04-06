#!/usr/bin/env python3

#import the necessary packages
import urllib
import time
from urllib import request
from bs4 import BeautifulSoup 
import re
import datetime

url="http://www.ggzxc.cn/"
html=urllib.request.urlopen(url).read()
html=html.decode("utf-8")
soup=BeautifulSoup(html)
a=soup.find("div",{"class":"zyl"})
c=a.find("li",{"class":"zyl2"})
usage=c.text
time=time.strftime('%Y%m%d',time.localtime(time.time() - 24*60*60) )
line=','.join([time]+[usage])
print(line)
