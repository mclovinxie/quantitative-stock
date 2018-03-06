# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 19:00:50 2018

@author: xiexihao
"""

import urllib
import re
import pandas as pd
import os
import time

import DBUtil as dbu

URL = 'http://quote.eastmoney.com/stocklist.html'
DataDir = './../data/crawl/'
DefaultCrawlMode = 'INC'
DefaultStartDate = '20170101'


def getHtml(url):
    html = urllib.request.urlopen(url).read()
    html = html.decode('gbk')
    return html

def getStockCode(html):
    s = r'<li><a target="_blank" href="http://quote.eastmoney.com/\S\S(.*?).html">'
    pat = re.compile(s)
    code = pat.findall(html)
    return code


def store2DB():
    if dbu.DBCon == None:
        dbu.initDBCon()
    cursor = dbu.DBCon.cursor()
    sql = "USE " + dbu.DBName
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
    dbu.DBCon.commit()
    #con.close()


def crawl(mode = DefaultCrawlMode):
    files = os.listdir(DataDir)
    for file in files:
        os.remove(DataDir + file)
    
    crawledCodes = getStockCode(getHtml(URL))
    stockCodeList = []
    
    for code in crawledCodes:
        stockCodeList.append(code)
    
    #stockCodeList = stockCodeList[1000:1010]
    
    currentDate = time.strftime('%Y%m%d', time.localtime(time.time()))
    
    if dbu.DBCon == None:
        dbu.initDBCon()
    
    cursor = dbu.DBCon.cursor()
    
    if mode == 'ALL':
        startDate = DefaultStartDate
        sql = "DROP DATABASE IF EXISTS " + dbu.DBName
        cursor.execute(sql)
        sql = "CREATE DATABASE " + dbu.DBName
        cursor.execute(sql)
        sql = "USE " + dbu.DBName
        cursor.execute(sql)
        sql = "CREATE TABLE stock_price_data (data_date date, stock_code VARCHAR(10), ch_name VARCHAR(10),close float, high float, low float, open float, last_open float, profit float, profit_ratio float, exchange float, dill bigint, dill_amount bigint, market_value bigint, currency_market_value bigint, PRIMARY KEY (data_date, stock_code), INDEX(data_date), INDEX(stock_code))"
        cursor.execute(sql)
    else:
        sql = "USE " + dbu.DBName
        cursor.execute(sql)
        sql = "SELECT MAX(data_date) FROM stock_price_data"
        cursor.execute(sql)
        dt = cursor.fetchone()
        startDate = dt[0].strftime('%Y%m%d')
        if startDate >= currentDate:
            return
    
    for code in stockCodeList:
        print('正在获取股票[%s]数据...' % code)
        time.sleep(0.25)
        url = 'http://quotes.money.163.com/service/chddata.html?code=0' + code + '&start=' + startDate + \
        '&end=' + currentDate + '&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP'
        urllib.request.urlretrieve(url, DataDir + code + '.csv')
    
    store2DB()
    
    dbu.closeDBCon()