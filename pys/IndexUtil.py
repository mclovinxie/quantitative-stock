# -*- coding: utf-8 -*-
"""
Created on Wed Mar 28 19:27:55 2018

@author: xiexihao
"""

import datetime

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime as dttm

import DataReader as dr

def smaCal(tsPrice,k):
    Sma=pd.Series(0.0,index=tsPrice.index)
    for i in range(k-1,len(tsPrice)):
        Sma[i]=sum(tsPrice[(i-k+1):(i+1)])/k
    return(Sma)

def wmaCal(tsPrice,weight):
   k=len(weight)
   arrWeight=np.array(weight)
   Wma=pd.Series(0.0,index=tsPrice.index)
   for i in range(k-1,len(tsPrice.index)):
       Wma[i]=sum(arrWeight*tsPrice[(i-k+1):(i+1)])
   return(Wma)

def ewmaCal(tsprice,period=5,exponential=0.2):
   Ewma=pd.Series(0.0,index=tsprice.index)
   Ewma[period-1]=np.mean(tsprice[0:period])
   for i in range(period,len(tsprice)):
       Ewma[i]=exponential*tsprice[i]+(1-exponential)*Ewma[i-1]
   return(Ewma)

def getMACD(code):
    data = dr.readStockData(code, '2000-01-01', '2018-03-28')
    data.sort_values('data_date', inplace = True)
    
    data.index = data.data_date
    data.index = pd.to_datetime(data.index, format = '%Y-%m-%d')
    
    #currentDate = dttm.now()
    #delta = datetime.timedelta(days = -90)
    #nDays = currentDate + delta
    #data = data[data['data_date'] > dttm.strptime(nDays.strftime('%Y%m%d'), '%Y%m%d').date()]
    
    close = data.close
    
    dif = ewmaCal(close, 12, 2 / (1 + 12)) - ewmaCal(close, 26, 2 / (1 + 26))
    #dif.tail(n = 3)
    
    dea = ewmaCal(dif, 9, 2 / (1 + 9))
    #dea.tail()
    
    macd = dif - dea
    #macd.tail(n = 3)
    
    print(macd)
    
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.subplot(211)
    plt.plot(dif,label="DIF",color='k')
    plt.plot(dea, label="DEA",color='b',linestyle='dashed')
    plt.title("信号线DIF与DEA")
    plt.legend()
    plt.subplot(212)
    plt.bar(left=macd.index,\
            height=macd,\
            label='macd',color='r')
    plt.legend()
    
    macddata=pd.DataFrame()
    macddata['DIF']= dif
    macddata['DEA']= dea
    macddata['MACD']= macd

if __name__ == '__main__':
    getMACD('603118')