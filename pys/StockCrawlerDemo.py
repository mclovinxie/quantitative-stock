# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 19:35:33 2018

@author: xiexihao
"""

import pandas as pd
import matplotlib.pyplot as plt
import datetime

from datetime import datetime as dttm

import Crawler as crwl
import CandleStick as cndl
import DataReader as dr

def describeStock(code):
    #data = pd.read_csv(DataDir + code + '.csv', encoding = 'gbk')
    #if dbu.DBCon == None:
    #    dbu.initDBCon()
    #sql = "SELECT * FROM %s.stock_price_data WHERE stock_code = '%s'" % (dbu.DBName, code)
    #data = pd.read_sql(sql, dbu.DBCon)
    #dbu.closeDBCon()
    data = dr.readStockData(code, '2017-09-30', '2018-03-05')
   
    data.sort_values('data_date', inplace = True)
    
    data.index = data.data_date
    data.index = pd.to_datetime(data.index, format = '%Y-%m-%d')
    
    #date = pd.Series([pd.to_datetime(str)] for str in data.data_date)
    #data.index = date
    currentDate = dttm.now()
    delta = datetime.timedelta(days = -90)
    nDays = currentDate + delta
    data = data[data['data_date'] > dttm.strptime(nDays.strftime('%Y%m%d'), '%Y%m%d').date()]
    
    print(data.head(5))
    
    open = data.open
    close = data.close
    low = data.low
    high = data.high
    
    #plt.plot(data.data_date, low)
    #plt.plot(data.data_date, high)
    
    ma = 10
    #rolling_mean = pd.rolling_mean(close, ma)
    rolling_mean_10 = close.rolling(window = ma).mean()
    plt.plot(data.data_date, rolling_mean_10)
    
    ma = 5
    rolling_mean_5 = close.rolling(window = ma).mean()
    plt.plot(data.data_date, rolling_mean_5)
    
    #cndl.candlePlot(data, title = 'K line')
    cndl.drawCandle(data)


if __name__ == '__main__':
    toCrawl = True
    crawlMode = 'INC'
    
    if toCrawl:
        crwl.crawl(crawlMode)
    else:
        #describeStock('600313')
        tmpdata = dr.justTry()
        print(tmpdata)
