#!/usr/bin/env python3
#import the necessary packages
import urllib
import time
from urllib import request
from bs4 import BeautifulSoup 
import re

print("date",",","max_temp",",","min_temp",",","weather",",","wind_dir",",","wind_force")
#url="http://lishi.tianqi.com/hangzhou/201101.html"
sound_ids=[188175,188204]
for id  in sound_ids:
   url="http://music.163.com/#/song?id="+str(id)
   html=urllib.request.urlopen(url).read()
   #html=html.decode("utf-8")
   soup=BeautifulSoup(html)
   print(soup)
   print("############################")
