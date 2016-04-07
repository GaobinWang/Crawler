#!/usr/bin/env python3

import trace
import urllib
import time
from urllib import request
from bs4 import BeautifulSoup 
import re
import datetime

log_file_name="Log.txt"

#url="http://lishi.tianqi.com/hangzhou/201101.html"
sound_ids=[36025962,34057518,32924132]
n1=50000000
n2=1000000000
sound_ids=range(n1,n2)
#sound_ids=[n1+1]
for sound_id  in sound_ids:
   try:
      url="http://music.163.com/song?id="+str(sound_id)
      html=urllib.request.urlopen(url).read()
      html=html.decode("utf-8")
      soup=BeautifulSoup(html)
      d=soup.find("em",{"class":"f-ff2"})
      d=str(type(d))
      if  d=="<class 'NoneType'>":
         continue
      sound_name=soup.find("em",{"class":"f-ff2"}).text
      print(sound_name)
      temp1=soup.findAll("p",{"class":"des s-fc4"})[0]
      print(temp1)
      singer_url="http://music.163.com/#"+str(temp1.find("a",{"class":"s-fc7"})["href"])
      singer=temp1.find("a",{"class":"s-fc7"}).text
      temp2=soup.findAll("p",{"class":"des s-fc4"})[1]
      channel_url="http://music.163.com/#"+str(temp2.find("a",{"class":"s-fc7"})["href"])
      channel=temp2.find("a",{"class":"s-fc7"}).text
      comments=soup.find("span",{"id":"cnt_comment_count"}).text
      print(sound_id,",",sound_name,",",singer,",",singer_url,",",channel,",",channel_url,",",comments)
   except:
      #eror_list.append(sound_id)
      f=open(log_file_name,"a")
      datetime1=time.strftime('%Y-%m-%d',time.localtime(time.time()))
      datetime2=time.strftime('%H:%M:%S',time.localtime(time.time()))
      f.write("###"+"error sound_id:"+str(sound_id)+"###"+"error_time"+datetime1+" "+datetime2)
      traceback.print_exc(file=f)
      f.flush()
      f.close()

