# -*- coding: utf-8 -*-
"""
Created on Wed May 22 10:07:01 2019

@author: wanggb
"""
#%%加载常用Python模块
import sys
import os
import numpy as np
import pandas as pd
import scipy as sp
import matplotlib.pyplot as plt
from datetime import datetime
from datetime import timedelta
from dateutil.parser import parse
from  scipy.optimize import minimize
from urllib import request
from bs4 import BeautifulSoup 
import json
from selenium import webdriver
import logging
import time
#%% 加载自定义Python函数
path = "D:\\0000MyCodeLibrary"
sys.path.append(path)  
os.chdir(path)
from Functions import *  #常用函数
from SendMailAndMessage import *

#%%设置全局变量
#设置工作路径
path = "D:\\0000Monitor\\MSCIIndexMonitor"
sys.path.append(path)  
os.chdir(path)


#%%
def main():
    try:
        ###定义Log文件
        SetLogFile()
        logging.debug("开始运行程序!")
        ###定义变量
        UserName = 'wanggb@igwfmc.com'
        PassWord = '1234qWER'    
        #登陆页面
        url1 = r'https://login.msci.com/login/login' 
        #跳转页面
        url2 = "https://im.msci.com/app/s/alertNotification/getAlertNotificationData?_dc=1"  
        #建立Phantomjs浏览器对象，括号里是phantomjs.exe在你的电脑上的路径
        browser = webdriver.PhantomJS('D:/phantomjs-1.9.8-windows/phantomjs.exe')
        #访问登录页面
        browser.get(url1)
        #等待一段时间，让js脚本加载完毕
        browser.implicitly_wait(3)   
        #输入用户名
        browser.find_element_by_id('username').send_keys(UserName)
        browser.find_element_by_id('submit').click()
        browser.find_element_by_name('password').send_keys(PassWord)
        browser.find_element_by_id('submit').click()
        ###跳转到目标页面
        browser.implicitly_wait(3)
        browser.get(url2)
        ###
        i = 1
        while browser.title != "":
            print(i,browser.title)
            browser.implicitly_wait(10)
            browser.get(url2)
        
        ###目标页面的解析
        html = browser.page_source
        soup=BeautifulSoup(html)
        Alerts = soup.find("body").text
        Alerts = json.loads(Alerts) #将str转换为列表
        Alerts = pd.DataFrame(Alerts)
        ###数据处理
        Alerts = Alerts.sort_values(by = ["effectiveDate","createdTime"],ascending = False)
        Alerts = Alerts[["createdTime","effectiveDate","eventType","impactType","securityName"]]
        Alerts["createdTime"] = pd.to_datetime(Alerts.createdTime)
        Alerts["effectiveDate"] = pd.to_datetime(Alerts.effectiveDate)
        Alerts["createdTime"] = Alerts.createdTime.apply(lambda x:x.strftime("%Y%m%d %H%M%S"))
        Alerts["createdTime"] = pd.to_datetime(Alerts.createdTime)
        ###事件筛选
        eventTypes = ["Quarterly Index Review"]
        impactTypes = ["Deletion"]
        Alerts = Alerts[(Alerts.eventType.isin(eventTypes)) | (Alerts.impactType.isin(impactTypes))]
        ###日期筛选
        nowday = datetime.now()
        Alerts = Alerts[Alerts.effectiveDate >= nowday] ###生效日位于当前日期之前
        Alerts = Alerts[Alerts.createdTime >= datetime(nowday.year,nowday.month,nowday.day-3)] ###生效日位于当前日期之前
        Alerts = Alerts[["createdTime","effectiveDate","eventType","impactType","securityName"]]
        ThisDate = datetime.now()
        ThisDate = ThisDate.strftime("%Y%m%d")
        NewAlerts = Alerts.loc[Alerts[["effectiveDate","eventType","impactType","securityName"]].drop_duplicates().index]
        NewAlerts = NewAlerts.reset_index(drop = True)
        ###编辑短信内容
        msg_content = ""
        if NewAlerts.shape[0] != 0:
            ###将程序写出到本地
            ThisDate = datetime.now()
            ThisDate = ThisDate.strftime("%Y%m%d%H%M%S")
            filename1 = "NewAlerts" + ThisDate + ".xlsx"
            filename2 = "NewAlerts" + ThisDate + ".html"
            NewAlerts.to_excel("./data/" + filename1)
            NewAlerts.to_html("./mail/" + filename2)
            ###
            impact_type = NewAlerts.impactType.unique()
            event_type = NewAlerts.eventType.unique()
            the_type = set(impact_type) | set(event_type) - set(["Other"])
            the_type = "_".join(the_type) 
            for i in NewAlerts.index:
                print(i)
                the_createdTime = NewAlerts.loc[i,"createdTime"].strftime("%Y-%m-%d %H:%M:%S")
                the_effectiveDate = NewAlerts.loc[i,"effectiveDate"].strftime("%Y-%m-%d")
                the_eventType = NewAlerts.loc[i,"eventType"]
                the_impactType = NewAlerts.loc[i,"impactType"]
                the_securityName = NewAlerts.loc[i,"securityName"]
                the_str = "("+str(i+1)+")" +"信息发布时间:"+the_createdTime+ "   "+"生效时间:"+the_effectiveDate + "   "+ "事件类型:" + the_eventType + "   "+"事件影响:" + the_impactType + "   "+ "受影响的证券:" + the_securityName + "\n"
                msg_content = msg_content + the_str
        else:
            msg_content = "今日无需要关注的调整事项"
            the_type = ""
        ###发送短信
        strEmailContent1 = "【MSCIAlert_" +ThisDate + "_" + "Type:" + the_type +  "】共有"+ str(len(NewAlerts.index))+"个值得关注的通知:\n" + msg_content 
        strEmailContent1 = strEmailContent1[0:400]
        strEmailContent1 = strEmailContent1 + "【详情见MSCI官网】"
        send_msg(content = strEmailContent1, phone_group = "pcf_duty_group")
        #quant_dept_shenzhen
        ###发送邮件
        if NewAlerts.shape[0] != 0:
            f1 = open("./mail/" + filename2)
            table1 = f1.read()
            strEmailTitle = filename1[0:(len(filename1) - 5)]
            strEmailContent = "<h1>MSCI指数调整需要注意的事项</h1>" + table1
            mail_group = "pcf_duty_group"
            MessageType = "email"
            #data = send_mail(strEmailTitle,strEmailContent,mail_group,MessageType)            
        logging.info("程序运行结束:成功!")
    except Exception as e:
        logging.error("程序报错!")
        logging.error(e)
        time.sleep(20)

#%%   
if __name__ == "__main__":
    main()
    
#pcf_duty_group    