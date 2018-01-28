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

URL = 'http://quote.eastmoney.com/stocklist.html'
DataDir = './../data/'

def getHtml(url):
    html = urllib.request.urlopen(url).read()
    html = html.decode('gbk')
    return html

def getStockCode(html):
    s = r'<li><a target="_blank" href="http://quote.eastmoney.com/\S\S(.*?).html">'
    pat = re.compile(s)
    code = pat.findall(html)
    return code

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

def crawl():
    crawledCodes = getStockCode(getHtml(URL))
    stockCodeList = []
    
    for code in crawledCodes:
        stockCodeList.append(code)
    
    stockCodeList = stockCodeList[1000:1001]
    
    for code in stockCodeList:
        print('正在获取股票[%s]数据...' % code)
        url = 'http://quotes.money.163.com/service/chddata.html?code=0' + code + \
        '&end=20180126&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP'
        urllib.request.urlretrieve(url, DataDir + code + '.csv')

def store2DB():
    ip = 'localhost'
    usr = 'root'
    pwd = 'xxh@WE10018164'
    charset = 'utf8'
    db = 'stock'
    
    db = pymysql.connect(ip, usr, pwd, charset = charset)
    cursor = db.cursor()
    cursor.execute("DROP DATABASE stock;")
    cursor.execute("CREATE DATABASE stock;")
    cursor.execute("USE stock;")
    
    files = os.listdir(DataDir)
    for file in files:
        data = pd.read_csv(DataDir + file, encoding = 'gbk')
        sql = "create table stock_%s" % file[0:6] + "(data_date date, stock_code VARCHAR(10), " + "ch_name VARCHAR(10),\
                       close float, high float, low float, open float, last_open float, profit float, \
                       profit_ratio float, exchange float, dill bigint, dill_amount bigint, market_value bigint, currency_market_value bigint)"
        try:
            cursor.execute(sql)
        except:
            print('数据表已存在！')
        
        print('正在存储stock_%s'% file[0:6])
        length = len(data)
        for i in range(0, length):
            record = tuple(data.loc[i])
            #插入数据语句
            try:
                sql = "insert into stock_%s" % file[0:6] + "(data_date, stock_code, ch_name, close, high, low, open, last_open, profit, profit_ratio, exchange, \
                dill, dill_amount, market_value, currency_market_value) values ('%s',%s','%s',%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" % record
                #获取的表中数据很乱，包含缺失值、Nnone、none等，插入数据库需要处理成空值
                sql = sql.replace('nan','null').replace('None','null').replace('none','null') 
                cursor.execute(sql)
            except:
                #如果以上插入过程出错，跳过这条数据记录，继续往下进行
                break
    
    #关闭游标，提交，关闭数据库连接
    cursor.close()
    db.commit()
    db.close()


if __name__ == '__main__':
    toCrawl = False
    if toCrawl:
        crawl()
        store2DB()
    else:
        describeStock('600790')
