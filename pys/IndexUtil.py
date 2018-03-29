# -*- coding: utf-8 -*-
"""
Created on Wed Mar 28 19:27:55 2018

@author: xiexihao
"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import DataReader as dr

def smaCal(tsPrice, k):
    Sma = pd.Series(0.0, index = tsPrice.index)
    for i in range(k - 1,len(tsPrice)):
        Sma[i] = sum(tsPrice[(i - k + 1) : (i + 1)]) / k
    return(Sma)

def wmaCal(tsPrice, weight):
   k = len(weight)
   arrWeight = np.array(weight)
   Wma = pd.Series(0.0, index = tsPrice.index)
   for i in range(k - 1,len(tsPrice.index)):
       Wma[i] = sum(arrWeight * tsPrice[(i - k + 1) : (i + 1)])
   return(Wma)

def ewmaCal(tsprice, period = 5, exponential = 0.2):
   Ewma = pd.Series(0.0, index = tsprice.index)
   Ewma[period - 1] = np.mean(tsprice[0 : period])
   for i in range(period, len(tsprice)):
       Ewma[i] = exponential * tsprice[i] + (1 - exponential) * Ewma[i - 1]
   return(Ewma)

def getRollingMean(close, window = 5):
    return close.rolling(window = window).mean()

def indexCal(code):
    data = dr.readStockData(code, '1900-01-01', '2018-03-28')
    data.sort_values('data_date', inplace = True)
    
    data.index = data.data_date
    data.index = pd.to_datetime(data.index, format = '%Y-%m-%d')
    
    #currentDate = dttm.now()
    #delta = datetime.timedelta(days = -90)
    #nDays = currentDate + delta
    #data = data[data['data_date'] > dttm.strptime(nDays.strftime('%Y%m%d'), '%Y%m%d').date()]
    
    close = data.close
    
    indexdata = pd.DataFrame()
    
    if len(close) <= 12:
        return indexdata
    
    dif = ewmaCal(close, 12, 2 / (1 + 12)) - ewmaCal(close, 26, 2 / (1 + 26))
    #dif.tail(n = 3)
    
    dea = ewmaCal(dif, 9, 2 / (1 + 9))
    #dea.tail()
    
    macd = dif - dea
    #macd.tail(n = 3)
    
    #print(macd)
    
    '''
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.subplot(211)
    plt.plot(dif,label="DIF",color='k')
    plt.plot(dea, label="DEA",color='b',linestyle='dashed')
    plt.title("信号线DIF与DEA")
    plt.legend()
    plt.subplot(212)
    plt.bar(left=macd.index,\
            height=macd,\
            label='MACD',color='r')
    plt.legend()
    '''
    
    
    indexdata['ra5'] = close.rolling(window = 5).mean()
    indexdata['ra10'] = close.rolling(window = 10).mean()
    indexdata['ra20'] = close.rolling(window = 20).mean()
    indexdata['ra30'] = close.rolling(window = 30).mean()
    indexdata['dif']= dif
    indexdata['dea']= dea
    indexdata['macd']= macd
    indexdata['data_date'] = macd.index
    indexdata.index = indexdata.data_date
    
    #print(indexdata)
    
    return indexdata

if __name__ == '__main__':
    indexCal('603118')