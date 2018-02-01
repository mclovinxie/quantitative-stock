# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 19:35:33 2018

@author: xiexihao
"""

import urllib
import re
import pandas as pd
import pymysql
import os
import sys
import matplotlib.pyplot as plt
import numpy as np
import time

from dateutil import parser


URL = 'http://quote.eastmoney.com/stocklist.html'
DataDir = './../data/crawl/'
DefaultCrawlMode = 'INC'
DefaultStartDate = '20170101'
DBName = 'stock'
DBCon = None

def getHtml(url):
    html = urllib.request.urlopen(url).read()
    html = html.decode('gbk')
    return html

def getStockCode(html):
    s = r'<li><a target="_blank" href="http://quote.eastmoney.com/\S\S(.*?).html">'
    pat = re.compile(s)
    code = pat.findall(html)
    return code

def initDBCon():
    ip = 'localhost'
    usr = 'root'
    pwd = 'xxh@WE10018164'
    charset = 'utf8'
    
    global DBCon
    DBCon = pymysql.connect(ip, usr, pwd, charset = charset)

def closeDBCon():
    if DBCon != None:
        try:
            DBCon.close()
        except:
            print('数据库关闭失败')

def describeStock(code):
    data = pd.read_csv(DataDir + code + '.csv', encoding = 'gbk')
    print(data.head(5))
    
    data.sort_values('日期', inplace = True)
    
    data = data[data['日期'] > '2017-10-01']
    date = pd.Series([pd.to_datetime(str)] for str in data.日期)
    data.index = date
    
    open = data.开盘价
    close = data.收盘价
    low = data.最低价
    high = data.最高价
    
    plt.plot(date, low)
    plt.plot(date, high)
    
    ma = 30
    #rolling_mean = pd.rolling_mean(close, ma)
    rolling_mean = close.rolling(window = ma).mean()
    plt.plot(date, rolling_mean)



def store2DB():
    if DBCon == None:
        initDBCon()
    cursor = DBCon.cursor()
    sql = "USE " + DBName
    cursor.execute(sql)
    
    files = os.listdir(DataDir)
    for file in files:
        data = pd.read_csv(DataDir + file, encoding = 'gbk')
        
        print('正在存储stock_%s'% file[0:6])
        length = len(data)
        for i in range(0, length):
            record = tuple(data.loc[i])
            #插入数据语句
            try:
                sql = "INSERT INTO stock_price_data (data_date, stock_code, ch_name, close, high, low, open, last_open, profit, profit_ratio, exchange, \
                dill, dill_amount, market_value, currency_market_value) values ('%s',%s','%s',%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" % record
                #获取的表中数据很乱，包含缺失值、Nnone、none等，插入数据库需要处理成空值
                sql = sql.replace('nan','null').replace('None','null').replace('none','null') 
                cursor.execute(sql)
            except:
                #如果以上插入过程出错，跳过这条数据记录，继续往下进行
                break
    
    #关闭游标，提交，关闭数据库连接
    cursor.close()
    DBCon.commit()
    #con.close()


def crawl(mode = DefaultCrawlMode):
    files = os.listdir(DataDir)
    for file in files:
        os.remove(DataDir + file)
    
    crawledCodes = getStockCode(getHtml(URL))
    stockCodeList = []
    
    for code in crawledCodes:
        stockCodeList.append(code)
    
    stockCodeList = stockCodeList[1000:1010]
    
    currentDate = time.strftime('%Y%m%d', time.localtime(time.time()))
    
    if DBCon == None:
        initDBCon()
    
    cursor = DBCon.cursor()
    
    if mode == 'ALL':
        startDate = DefaultStartDate
        sql = "DROP DATABASE IF EXISTS " + DBName
        cursor.execute(sql)
        sql = "CREATE DATABASE " + DBName
        cursor.execute(sql)
        sql = "USE " + DBName
        cursor.execute(sql)
        sql = "CREATE TABLE stock_price_data (data_date date, stock_code VARCHAR(10), ch_name VARCHAR(10),close float, high float, low float, open float, last_open float, profit float, profit_ratio float, exchange float, dill bigint, dill_amount bigint, market_value bigint, currency_market_value bigint, PRIMARY KEY (data_date, stock_code))"
        cursor.execute(sql)
    else:
        sql = "USE " + DBName
        cursor.execute(sql)
        sql = "SELECT MAX(data_date) FROM stock_price_data"
        cursor.execute(sql)
        dt = cursor.fetchone()
        startDate = dt[0].strftime('%Y%m%d')
        if startDate >= currentDate:
            return
    
    for code in stockCodeList:
        print('正在获取股票[%s]数据...' % code)
        url = 'http://quotes.money.163.com/service/chddata.html?code=0' + code + '&start=' + startDate + \
        '&end=' + currentDate + '&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP'
        urllib.request.urlretrieve(url, DataDir + code + '.csv')
    
    store2DB()



if __name__ == '__main__':
    toCrawl = True
    crawlMode = 'INC'
    
    initDBCon()
    
    if toCrawl:
        crawl(crawlMode)
    else:
        describeStock('600790')
    
    closeDBCon()
