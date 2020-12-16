# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 22:39:50 2020

@author: Lesile

模拟登录抓取老页面
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
#%%
def RandSleep():
    """
    随机休眠
    
    Example
    =======
    res = RandSleep()
    """
    randnums = random.randint(3,10)
    time.sleep(randnums)
    print("随机休眠%s秒" %(randnums))

def GeneratePath(path,pathname):
    """
    Example
    =======
    path = r"E:\Github\Crawler\Meetings\data"
    pathname = "20201211"
    GeneratePath(path,pathname)
    """
    filepath = os.path.join(path,pathname)
    if os.path.exists(filepath) == False:
        os.mkdir(filepath)
    os.chdir(filepath)
    
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
    RandSleep()
    return(browser)


def CrawlerDataFromBrowser(login_url,username,password,date,dataurl):
    """
    从页面抓取数据
    
    Parameter
    =========

    Example
    ========
    date = "20200101"
    data = CrawlerDataFromBrowser(login_url,username,password,date,dataurl)
    """
    browser = SimulatedLogin(login_url,username,password)
    ###跳转到目标页面
    url = dataurl
    browser.implicitly_wait(3)
    browser.get(url)
    ###选择日期并跳转到相关界面
    browser.find_element_by_name('ipt_start').clear()  #清楚原有日期
    browser.find_element_by_name('ipt_start').send_keys(date)  #设置新的查询日期
    #<button type="submit" class="btn btn-primary">查询</button>
    #class属性是比较特殊的一个，属性值可以有多个，中间是用空格隔开的
    #browser.find_element_by_class_name("btn btn-primary").submit()  #使用class_name会报错
    #browser.find_element_by_class_name("btn-primary").submit()      #第一种解决办法：class值取其中之一
    #browser.find_element_by_class_name("btn").submit()          #第一种解决办法：class值取其中之一
    #browser.find_element_by_css_selector(".btn.btn-primary").submit()          #第二种解决办法：使用css.selector，每个class值前面加.
    browser.find_element_by_class_name("btn-primary").click()  #点击查询
    ###保存当前界面的截图
    time.sleep(5)
    RandSleep()
    filename = date + "_Pic.png"
    browser.save_screenshot(filename)
    ###解析当前界面
    html = browser.page_source
    soup = BeautifulSoup(html, 'lxml') 
    meetinglist = soup.find_all(name= 'dl', attrs= {'class': 'data-row'})
    final_res = []
    for i in range(len(meetinglist)):
        print(i)
        event = meetinglist[i]
        ###解析title,样例如下：<a href="event.htm?id=26193" title="2019-12-25 14:37:18.0">国泰君安**联合调研**中国银行</a>
        title = event.find("span",{"class":"title"})
        theurl = "https://www.kanzhiqiu.com/calendar/" + title.find("a")["href"] # url        
        theupdatetime = title.find("a")["title"] #上传时间
        title = title.text 
        titletmp = title.split("**")
        if len(titletmp)==3:
            thebroker = titletmp[0]        
            thetype = titletmp[1]        
            thetitle = titletmp[2]
        elif len(titletmp)==2:
            thebroker = titletmp[0]        
            thetype = titletmp[1]        
            thetitle = np.nan            
        elif len(titletmp)==1:
            thebroker = titletmp[0]        
            thetype = np.nan        
            thetitle = np.nan  
        else:
            thebroker =  np.nan      
            thetype = np.nan        
            thetitle = np.nan  
        ###解析date,样例如下:<span class="date">开始和结束：2020/01/06</span>
        startdate_enddate = event.find(name = "span", attrs= {'class': 'date'}).text
        startdate_enddate = startdate_enddate.replace("开始和结束：","")
        startdate_enddatetmp = startdate_enddate.split("-")
        if len(startdate_enddatetmp)==2:
            thestartdate = startdate_enddatetmp[0]  #开始时间
            theenddate = startdate_enddatetmp[1]    #结束时间
        else:
            thestartdate = startdate_enddatetmp[0]
            theenddate = np.nan         
        ###提取个股代码和名称
        stock_str = event.find("b",{"class":"stock"})
        try:
            stock = stock_str.text
            nums = re.sub("\D", "", stock) #数字
            nonums = re.sub("\d", "", stock) #非数字(汉字和英文)
            strs = ''.join(re.findall(r'[A-Za-z]', stock)) #提取英文
            if len(strs)>1:
                stockcode = strs  #股票代码
                stockname = nonums.replace(stockcode,"")  #股票名称
            else:
                stockcode = nums  #股票代码
                stockname = nonums  #股票名称                
        except:
            stockcode = np.nan
            stockname =np.nan
        ###
        res = [thestartdate,theenddate,theupdatetime,stockcode,stockname,thebroker,thetype,thetitle,theurl,title,stock_str]
        #res = [thetradingday,theclock,thetype,the_theme1,the_broker,the_stockcode,theurl]
        final_res.append(res) 
    TheColNames = ["StartDate","EndDate","UpdateDate","StockCode","StockName","Broker","Type","Title","URL","title_str","stock_str"]
    result = pd.DataFrame(final_res,columns = TheColNames)
    result["StartDate"] = pd.to_datetime(result.StartDate)
    result["EndDate"] = pd.to_datetime(result.EndDate)
    result["UpdateDate"] = pd.to_datetime(result.UpdateDate)
    browser.quit()
    return(result)
#%%
path = r"E:\Github\Crawler\Meetings"
filename = os.path.join(path,"PrivateData.xlsx")
PrivateData = pd.read_excel(filename)
path = r"E:\Github\Crawler\Meetings\data"
i = 1
username = PrivateData.UserName.iloc[i]
password = PrivateData.Password.iloc[i]
login_url = PrivateData.LoginUrl.iloc[i]
dataurl = PrivateData.DataUrl.iloc[i]

tradingday = datetime.now()
date = tradingday.strftime("%Y%m%d")
date = "20201214"
GeneratePath(path,date)
data = CrawlerDataFromBrowser(login_url,username,password,date,dataurl)
filename = date + ".csv"
data.to_csv(filename,index = False)
#%%
"""
startdate = "20200412"
enddate = "20201212"
result = pd.DataFrame()
DateList = pd.date_range(start=startdate,end= enddate ,freq="W")
for i in range(len(DateList)):
    tradingday = DateList[i]
    date = tradingday.strftime("%Y%m%d")
    print(i,date)
    ###创建目录
    GeneratePath(path,date)
    ###
    data = CrawlerDataFromBrowser(login_url,username,password,date,dataurl)
    ###数据写出到本地
    filename = date + ".csv"
    data.to_csv(filename,index = False)
"""