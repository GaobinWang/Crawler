#!/usr/bin/python3
#import the necessary packages
import urllib
import time
from urllib import request
from bs4 import BeautifulSoup 
import re
years=["2011","2012","2013","2013","2015"]
months=["01","02","03","04","05","06","07","08","09","10","11","12"]
yyyymm=[i+j for i in years  for j in months]
yyyymm.append("201601")
yyyymm.append("201602")

print("date",",","max_temp",",","min_temp",",","weather",",","wind_dir",",","wind_force")
#url="http://lishi.tianqi.com/hangzhou/201101.html"
for ym in yyyymm:
   url="http://lishi.tianqi.com/hangzhou/"+ym+".html"
   html=urllib.request.urlopen(url).read()
   #html=html.decode("utf-8")
   soup=BeautifulSoup(html)
   a=soup.find("div",{"class":"tqtongji2"})
   b=a.findAll('ul')
   for index in range(1,len(b)):
      c=b[index]
      d=c.findAll('li')
      date=d[0].text
      max_tmp=d[1].text
      min_tmp=d[2].text
      weather=d[3].text
      wind_dir=d[4].text
      wind_force=d[5].text
      print(date,",",max_tmp,",",min_tmp,",",weather,",",wind_dir,",",wind_force)	  
