#!/usr/bin/python3

###import the necessary packages
#import pymysql
import trace
import urllib
import time
from urllib import request
from bs4 import BeautifulSoup 
import re
import datetime
#print("datetime1",",","datetime2",",","sound_id",",","sound_name",",","sound_length",",","played_times",",","sound_url",",","up_user_name",",","up_user_id",",","up_user_url",",","up_time",",","share,like",",","comment",",","channel_name",",","channel_id",",","channel_url")
#asdfas
#mysql_table_name="20160226_finaltest"
log_file_name="LogEcho.txt"
#conn=pymysql.connect(host='localhost',user='root',passwd='dmc123',db='echo_crawler',charset='utf8')
#cur=conn.cursor()

###define some functions to cleandata
def cleandata1(a):
   a=a.replace(',','M')
   a=a.replace('，','M')
   a=a.replace('"','M')
   a=a.replace('(','M')
   a=a.replace(')','M') 
   a=a.replace('{','M')
   a=a.replace('}','M')
   a=a.replace('[','M')
   a=a.replace(']','M')
   a=a.replace('<','M')
   a=a.replace('>','M')
   a=a.replace('/','M')
   a=a.replace('\\','M')
   a=a.replace(';','M')
   a=a.replace(':','M')
   a=a.replace('\'','M')
   a=a.replace('?','M')
   a=a.replace('&','M')
   a=a.replace('$','M')
   a=a.replace('#','M')
   a=a.replace('=','M')
   a=a.replace('~','M')
   a=a.replace('。','M')
   a=a.replace('.','M')
   a=a.replace('*','M')
   a=a.replace('\n','M')
   a=a.replace('\r','M')
   a=a.replace('\t','M')
   return a

#处理播放量、点赞数、评论数不规则的情况   
def cleandata2(a):
   if '万' in a:
      pattern=re.compile(r"\d*\.*\d*")
      match=pattern.match(a)
      result=match.group()
      return int(float(result)*10000)
   elif a==' ':
      return a
   else:
      return int(a)

#处理上传时间不规则的情况	  
def cleandata3(a):
   a=a.replace('上传','')
   year=time.strftime("%Y",time.localtime(time.time()))
   month=time.strftime("%m",time.localtime(time.time()))
   day=time.strftime("%d",time.localtime(time.time()))
   if '秒前' in a or '分钟前' in a or '小时前' in a:
      a=time.strftime('%Y-%m-%d',time.localtime(time.time())) 
   elif '天前' in a:
      pattern=re.compile(r"\d*")
      match=pattern.match(a)
      result=match.group()
      a=year+"-"+month+"-"+str(int(day)-int(result))
   else:
      a=a
   return a
 
#start
m=1
n=1500000
error_list=[]
for sound_id  in range(m,n):
   try:
      url="http://www.app-echo.com/sound/"+str(sound_id)
      #cur=conn.cursor()
      html=urllib.request.urlopen(url).read()
      html=html.decode("utf-8")
      soup=BeautifulSoup(html)
      a=soup.find("div",{"class":"title fl"})
      test=str(type(a))
      if  test=="<class 'NoneType'>":
         continue
      sound_name=a.find('h1').text
      sound_name=cleandata1(str(sound_name))
      test2=a.find("span",{"class":"voice-length"})
      test2=str(type(test2))
      if  test2=="<class 'NoneType'>":
         continue   #专为700842设置
      sound_length=a.find("span",{"class":"voice-length"}).text
      played_times=a.find("span",{"class":"played"}).find("b").text
      played_times=cleandata2(str(played_times))
      sound_url="www.app-echo.com/sound/"+str(sound_id)
      d=soup.find("div",{"class":"category fr"})
      channel_name=d.find("a").text
      channel_name=cleandata1(str(channel_name))
      channel_id=d.find("a")["href"]
      channel_id=channel_id.replace("/channel/","")
      channel_url="www.app-echo.com"+d.find("a")["href"]
      c=soup.find("div",{"class":"user-and-time"})
      up_user=c.find("a",{"class":"user-name"}).text
      up_user_name=cleandata1(str(up_user))
      up_user_id=c.find("a",{"class":"user-name"})["href"]
      up_user_id=up_user_id.replace("/user/","")
      up_user_url="www.app-echo.com"+c.find("a",{"class":"user-name"})["href"]
      up_time=c.find("time",{"class","upload-time"}).text
      up_time=cleandata3(str(up_time))
      b=soup.find("div",{"class":"ui-status voice-status fr cf"})
      share=b.find("span",{"class":"share"}).text
      share=cleandata2(str(share))
      like=b.find("span",{"class":"like"}).text
      like=cleandata2(str(like))
      comment=b.find("span",{"class":"comment"}).text
      comment=cleandata2(str(comment))
      datetime1=time.strftime('%Y-%m-%d',time.localtime(time.time()))
      datetime2=time.strftime('%H:%M:%S',time.localtime(time.time()))
      print(datetime1,",",datetime2,",",sound_id,",",sound_name,",",sound_length,",",played_times,",",sound_url,",",up_user_name,",",up_user_id,",",up_user_url,",",up_time,",",share,",",like,",",comment,",",channel_name,",",channel_id,",",channel_url)
      #dataone=(datetime1,datetime2,sound_id,sound_name,sound_length,played_times,sound_url,up_user_name,up_user_id,up_user_url,up_time,share,like,comment,channel_name,channel_id,channel_url)
      #print(dataone)
      #sqli="insert into "+mysql_table_name+"  values(%s,%s,%s,%s,%s,%s,%s,%s ,%s,%s,%s,%s ,%s,%s,%s,%s ,%s)"
      #cur.execute(sqli,dataone)
      #print(sound_id,",",sound_name,",",sound_name2,",",sound_length,",",played_times,",",played_times2,",",up_user,",",up_user_url,",",up_time,",",up_time2,",",share,",",like,",",comment,",",channel_name,",",channel_url)
      #cur.close()
      #conn.commit()
   except:
      error_list.append(sound_id)
      f=open(log_file_name,"a")
      datetime1=time.strftime('%Y-%m-%d',time.localtime(time.time()))
      datetime2=time.strftime('%H:%M:%S',time.localtime(time.time()))
      f.write("###"+"error sound_id:"+str(sound_id)+"###"+"error_time"+datetime1+" "+datetime2+'\n')
      f.write(error_list)
      traceback.print_exc(file=f)
      f.flush()
      f.close()

#conn.close()


