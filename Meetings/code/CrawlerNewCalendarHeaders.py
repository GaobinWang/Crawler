# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 22:39:50 2020

@author: Lesile


头文件的方式抓取新页面

"""
#%%加载常用Python模块
import sys
import os
import numpy as np
import pandas as pd

from datetime import datetime
from datetime import timedelta

import requests
from urllib import request
from bs4 import BeautifulSoup 
from selenium import webdriver
import time

import re
import requests

#%%
def CrawlerData(date):
    """
    Example
    ==========
    date = "20201202"
    data = CrawlerData(date)
    """
    headers = {
        'Cookie': 'REPORT_USERCOOKIE_USERNAME=wanggb%40igwfmc.com; JSESSIONID=e8039165d82329cf0b62fb0ff798; JREPLICA=instance234; ROUTEID=.4; REPORT_SESSION_COOKIE=UZFefbU5f93VYQrav6jACpTPY1w%2Fd4Lr9cXrftqYBOzeL4oVZCPtqqWGdrM%2BEEi8r21oiIQds5Ar%0A%2BwiA2ZfqyQ%3D%3D; JSESSIONIDVERSION=2f:28',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'
        }    
    headers = {
        'Cookie': 'REPORT_USERCOOKIE_USERNAME=zengl%40invescogreatwall.com; JSESSIONID=674d3cc4a46c2523d1afc14deaa7; JREPLICA=instance235; ROUTEID=.3; REPORT_SESSION_COOKIE=%2BMvPVCRCEbqZM9De8ialM7uPwqxGhD%2BAO%2BudqFTYDUCRYFUL0N1WOPrt2RtvCb9ur21oiIQds5Ar%0A%2BwiA2ZfqyQ%3D%3D; JSESSIONIDVERSION=2f:80',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'
        }   
    url = 'https://igwfmc.kanzhiqiu.com/calendar/events.htm?newweb=true&pageSize=-1&page=1&sort=a.begindate&asc=true&showAll=true&stocks=&search=&type=&ipt_start={}&location='.format(date)
    url = r'https://www.kanzhiqiu.com/calendar/events.htm?type=&ipt_start={}&location_select=&location=&stocks=&search='.format(date)
    result = requests.get(url, headers=headers)
    time.sleep(random.random())
    the_text = result.text
    soup = BeautifulSoup(the_text, 'lxml') 
    meetinglist = soup.find_all(name= 'div', attrs= {'class': 'calendarList clearfix'})
    final_res = []
    for events in meetinglist:
        thetradingday = events["id"]
        thetradingday = thetradingday[-8:]
        ###
        eventslist = events.find_all(name= 'div', attrs= {'class': 'meetingDetailList clearfix'})
        for event in eventslist:
            print(event)
            thetype = event.find(name = "p",attrs= {'class': 'type clearfix'}).text
            thetype = thetype.replace("\n","")
            theclock = event.find(name = "p",attrs= {'class': 'clock'}).text
            the_theme = event.find(name = "p",attrs= {'class': 'theme'}).text
            the_theme = the_theme.replace(" ","")
            the_theme = the_theme.replace("\n","")
            the_themes = the_theme.split("\r\r")
            if len(the_themes)>=2:
                the_theme1 = the_themes[0]
                the_stockcode = the_themes[1]
            else:
                the_theme1 = the_themes[0]
                the_stockcode = ""
            the_theme2= the_theme1.split("**")
            the_broker = the_theme2[0]
            theurl = event.find(name = "p",attrs= {'class': 'theme'}).a["href"]
            theurl = "https://igwfmc.kanzhiqiu.com/calendar/"+ theurl
            #汇总结果
            res = [thetradingday,theclock,thetype,the_theme1,the_broker,the_stockcode,theurl]
            final_res.append(res)
    result = pd.DataFrame(final_res,columns = ["TradingDay","Time","Type","Themes","Broker","StockCode","URL"])
    return(result)
#%%
def func(x):
    if len(x)==6:
        y = "A"
    elif len(x)==5:
        y = "H"
    else:
        y=""
    return(y)
#%%
    
path = "C:\\Users\\Lesile\\Desktop\\DrawData\\result"
os.chdir(path)

result = pd.DataFrame()
DateList = pd.date_range(start="20191101",end="20201201",freq="M")
for i in range(len(DateList)):
    tradingday = DateList[i]
    date = tradingday.strftime("%Y%m%d")
    print(i,date)
    data = getDataFromXN(date)
    time.sleep(random.random()) # 模拟人工浏览
    time.sleep(3)
    filename = date + ".csv"
    data.to_csv(filename,index = False)
    result = pd.concat([result,data])

result = result.drop_duplicates(subset = "URL")
result["StockCode"] = result.StockCode.apply(lambda x:x.replace("\r",""))
result["Market"] = result.StockCode.apply(lambda x:func(x))
result.to_csv("result.csv",index=False)   

dat1 = result[result.Market == "A"]
dat2 = result[result.Market == "H"]

dat1.groupby("StockCode").size().sort_index()
dat2.groupby("StockCode").size().sort_index()
"""
H 221
A 1364
7647
7647条数据,覆盖1364只A股,221只港股
近1年调研数据20191201_20201201(7647条数据,覆盖1364只A股,221只港股)
"""
