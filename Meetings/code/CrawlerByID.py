# -*- coding: utf-8 -*-
"""
Created on Sat Dec 12 19:40:49 2020

@author: Lesile
"""
#%%加载常用Python模块
import sys
import os
import numpy as np
import pandas as pd

from datetime import datetime
from datetime import timedelta

from urllib import request
from bs4 import BeautifulSoup 
from selenium import webdriver
import time
import random
import re
import requests

"""
分页抓取数据
"""

#%%
def RandSleep():
    """
    随机休眠
    
    Example
    =======
    res = RandSleep()
    """
    randnums = random.randint(300,600)
    time.sleep(randnums)
    print("随机休眠%s秒" %(randnums))
    
def parse(soup): # 解析函数，从html中解析数据，返回一个dict
    # 事件详情页分为两部分，简介和表格
    # 简介
    broker = soup.h5.get_text(strip=True) # 机构名称
    title = soup.h3.get_text(strip=True) # 事件标题
    event_type = soup.h3.small.get_text(strip=True)  
    # 事件类型：电话会议，联合调研，路演，主题交流，策略会，培训，展会，其他
    # 早期分类不准，后续还需根据title分类
    time = soup.find('p', 'date').get_text(strip=True) # 事件时间
    import re # 正则库，用于处理时间，从time中提取出日期date '2020/10/26'
    date = re.search('\d{4}[/]\d{2}[/]\d{2}', time).group()
    intro = {
        'broker': broker,
        'title': title,
        'event_type': event_type,
        'date': date}
    # 提取表格部分，配对，不直接提取是为了避免空值造成错位
    table = {}
    for i in range(len(soup.table.find_all('tr'))):
        th = soup.table.find_all('tr')[i].th.get_text(strip=True) # 分别选择第i个tr中的th和td
        td = soup.table.find_all('tr')[i].td.get_text(strip=True)
        table[th] = td
    # 合并intro和table到同一个dict
    data = intro.copy()
    data.update(table)
    return(data)
    
def SimulatedLogin(login_url,username,password):
    """
    模拟登录
    
    Parameter
    ========
    login_url:str
        登录页面的网址
    username:str
        用户名
    password:str
        密码

    Example
    ========
    login_url = r'*******' 
    username = "*******"
    password = '*******'    
    browser = SimulatedLogin(login_url,username,password)
    """
    #建立Phantomjs浏览器对象，括号里是phantomjs.exe在你的电脑上的路径
    #phantomjs下载地址: https://phantomjs.org/download.html
    browser = webdriver.PhantomJS('D:/phantomjs-2.1.1-windows/bin/phantomjs.exe')
    #访问登录页面
    browser.get(login_url)
    #等待一段时间，让js脚本加载完毕
    browser.implicitly_wait(3)  
    #输入用户名
    browser.find_element_by_name('username').send_keys(username)
    browser.find_element_by_name('password').send_keys(password)
    browser.find_element_by_name('btn_submit').click()
    #返回对象
    #RandSleep()
    ###browser.execute_script("return navigator.userAgent")
    return(browser)

def getHeaders(browser):
    Cookies = browser.get_cookies()
    agent = browser.execute_script("return navigator.userAgent")
    REPORT_USERCOOKIE_USERNAME = [i["value"] for i in Cookies if i["name"]=="REPORT_USERCOOKIE_USERNAME"]
    JSESSIONID = [i["value"] for i in Cookies if i["name"]=="JSESSIONID"]
    JREPLICA = [i["value"] for i in Cookies if i["name"]=="JREPLICA"]
    ROUTEID = [i["value"] for i in Cookies if i["name"]=="ROUTEID"]
    REPORT_SESSION_COOKIE = [i["value"] for i in Cookies if i["name"]=="REPORT_SESSION_COOKIE"]
    JSESSIONIDVERSION = [i["value"] for i in Cookies if i["name"]=="JSESSIONIDVERSION"]
    Cookie = "REPORT_USERCOOKIE_USERNAME=%s; JSESSIONID=%s; JREPLICA=%s; ROUTEID=%s; REPORT_SESSION_COOKIE=%s; JSESSIONIDVERSION=%s" %(REPORT_USERCOOKIE_USERNAME[0],JSESSIONID[0],JREPLICA[0],ROUTEID[0],REPORT_SESSION_COOKIE[0],JSESSIONIDVERSION[0])
    headers = {
        'Cookie': Cookie,
        'User-Agent': agent
        }   
    return(headers)
    
def CrawlerDataByID(theid,headers):
    """
    Example
    ==========
    headers = {
        'Cookie': 'REPORT_USERCOOKIE_USERNAME=wanggb%40igwfmc.com; JSESSIONID=674d3cc4a46c2523d1afc14deaa7; JREPLICA=instance234; ROUTEID=.4; REPORT_SESSION_COOKIE=UZFefbU5f93VYQrav6jACpTPY1w%2Fd4Lr9cXrftqYBOzeL4oVZCPtqqWGdrM%2BEEi8r21oiIQds5Ar%0A%2BwiA2ZfqyQ%3D%3D; JSESSIONIDVERSION=2f:28',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'
        }    
    headers = {
        'Cookie': 'REPORT_USERCOOKIE_USERNAME=zengl%40invescogreatwall.com; JSESSIONID=674d3cc4a46c2523d1afc14deaa7; JREPLICA=instance235; ROUTEID=.3; REPORT_SESSION_COOKIE=%2BMvPVCRCEbqZM9De8ialM7uPwqxGhD%2BAO%2BudqFTYDUCRYFUL0N1WOPrt2RtvCb9ur21oiIQds5Ar%0A%2BwiA2ZfqyQ%3D%3D; JSESSIONIDVERSION=2f:1047',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'
        }   

    date = "20201202"
    data = CrawlerData(date)
    """
    #url = 'https://igwfmc.kanzhiqiu.com/calendar/events.htm?newweb=true&pageSize=-1&page=1&sort=a.begindate&asc=true&showAll=true&stocks=&search=&type=&ipt_start={}&location='.format(date)
    #url = r'https://www.kanzhiqiu.com/calendar/events.htm?type=&ipt_start={}&location_select=&location=&stocks=&search='.format(date)
    url = "https://www.kanzhiqiu.com/calendar/event.htm?id=" + theid
    result = requests.get(url, headers = headers)
    time.sleep(1)
    the_text = result.text
    soup = BeautifulSoup(the_text, 'lxml') 
    try:
        res = parse(soup)
        ###
        data = pd.DataFrame(data = res,index = [0])
    except:
        print(theid ,"Error!!!!!!!!!!!!!!!1")
        data = pd.DataFrame(data = [theid],columns = ["theid"])
    ###数据写出到本地
    filename = theid + ".csv"
    data.to_csv(filename,index = False)
    return(data)
#%%
path = r"E:\Github\Crawler\Meetings"
filename = os.path.join(path,"老页面抓取结果20201212.xlsx")
Data = pd.read_excel(filename)
print("1111111111111")
#%%
path = r"E:\Github\Crawler\Meetings"
filename = os.path.join(path,"PrivateData.xlsx")
PrivateData = pd.read_excel(filename)

i = 2
username = PrivateData.UserName.iloc[i]
password = PrivateData.Password.iloc[i]
login_url = PrivateData.LoginUrl.iloc[i]
dataurl = PrivateData.DataUrl.iloc[i]
browser = SimulatedLogin(login_url,username,password)
headers = getHeaders(browser)
"""
headers = {
    'Cookie': 'REPORT_USERCOOKIE_USERNAME=wanggb%40igwfmc.com; JSESSIONID=9fed56ea250710a70f4754b81188; JREPLICA=instance235; ROUTEID=.3; REPORT_SESSION_COOKIE=OUkruy%2FEdbE8JtL8w3vJLj8Ok3bw2y26BY1qctxg%2B%2BEnfUj7blDOJvBsDFc71krhr21oiIQds5Ar%0A%2BwiA2ZfqyQ%3D%3D; JSESSIONIDVERSION=2f:72',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'
    }   
"""
print("FFFFFFFFFFFFFF")
#%%
path = r"E:\Github\Crawler\Meetings\databyid"
os.chdir(path)
##读取已经抓取的ID
FileList = os.listdir(path)
CrawleredIDs = [int(i.split(".")[0]) for i in FileList]

##需要抓取的界面
startid = 0
endid = 10000
result = pd.DataFrame()
idlist = [i for i in range(startid,endid+1)]
idlist = list(set(idlist) - set(CrawleredIDs))
    
i = 0
while len(idlist)>=1:
    i = i+1
    ###查询
    FileList = os.listdir(path)
    CrawleredIDs = [int(i.split(".")[0]) for i in FileList]
    idlist = list(set(idlist) - set(CrawleredIDs))
    ###
    theid = random.choice(idlist)
    #idlist = list(set(idlist) - set([theid]))
    theid = str(theid)
    theurl = "https://www.kanzhiqiu.com/calendar/event.htm?id=" + theid
    print("剩余个数:%s  ;循环次数: %s; 当前URL: %s ; " %(len(idlist),i,theurl))
    data = CrawlerDataByID(theid,headers)
    RandSleep()
    randnums = random.randint(120,240)
    time.sleep(randnums)
#%%
"""
path = r"E:\Github\Crawler\Meetings\databyid"
filelist = os.listdir(path)
result = pd.DataFrame()
for i in range(len(filelist)):
    filename = filelist[i]
    filepath = os.path.join(path,filename)
    data = pd.read_csv(filepath)
    print(i,filepath,data.shape[0])
    result = pd.concat([result,data])
    
#result2 = result.drop_duplicates(subset = "URL")
path = r"E:\Github\Crawler\Meetings"
filename = "老页面抓取结果ByID20201212.xlsx"
filepath = os.path.join(path,filename)
result.to_excel(filepath)
"""