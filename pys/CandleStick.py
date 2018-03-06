# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 19:09:09 2018

@author: xiexihao
"""

from pandas import DataFrame, Series
import pandas as pd; import numpy as np
import matplotlib.pyplot as plt
from matplotlib import dates as mdates
from matplotlib import ticker as mticker
from matplotlib.finance import candlestick_ohlc
from matplotlib.dates import DateFormatter, WeekdayLocator, DayLocator, MONDAY,YEARLY
from matplotlib.dates import MonthLocator,MONTHLY
import datetime as dt
import pylab

def candlePlot(seriesData, title = 'a'):
    Date = [date2num(dt) for dt in seriesData.index]
    seriesData.loc[:, 'data_date'] = Date
    
    listData = []
    for i in range(len(seriesData)):
        a = [seriesData.data_date, seriesData.open[i], seriesData.high[i], seriesData.low[i], seriesData.close[i]]
        listData.append(a)
    
    ax = plt.subplot()
    mondays = WeekdayLocator(MONDAY)
    weekFormatter = DateFormatter('%y %b %d')
    ax.xaxis.set_major_locator(mondays)
    ax.xaxis.set_minor_locator(DayLocator())
    ax.xaxis.set_major_formatter(weekFormatter)
    
    candlestick_ohlc(ax, listData, width = 0.7, colorup = 'r', colordown = 'g')
    ax.set_title(title)
    plt.setp(plt.gca().getxticklabels(), rotation = 50, horizontalalignment = 'center')
    return (plt.show())


def drawCandle(dfdata):
    daysreshape = dfdata.reset_index()
    # convert the datetime64 column in the dataframe to 'float days'
    daysreshape['DateTime']=mdates.date2num(daysreshape['DateTime'].astype(dt.date))
    # clean day data for candle view 
    daysreshape.drop('Volume', axis=1, inplace = True)
    daysreshape = daysreshape.reindex(columns=['DateTime','Open','High','Low','Close'])  
    
    Av1 = movingaverage(daysreshape.Close.values, 5)
    Av2 = movingaverage(daysreshape.Close.values, 10)
    SP = len(daysreshape.DateTime.values[MA2-1:])
    fig = plt.figure(facecolor='#07000d',figsize=(15,10))
    
    ax1 = plt.subplot2grid((6,4), (1,0), rowspan=4, colspan=4, axisbg='#07000d')
    candlestick_ohlc(ax1, daysreshape.values[-SP:], width=.6, colorup='#ff1717', colordown='#53c156')
    Label1 = str(5)+' SMA'
    Label2 = str(10)+' SMA'
    
    ax1.plot(daysreshape.DateTime.values[-SP:],Av1[-SP:],'#e1edf9',label=Label1, linewidth=1.5)
    ax1.plot(daysreshape.DateTime.values[-SP:],Av2[-SP:],'#4ee6fd',label=Label2, linewidth=1.5)
    ax1.grid(True, color='w')
    ax1.xaxis.set_major_locator(mticker.MaxNLocator(10))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax1.yaxis.label.set_color("w")
    ax1.spines['bottom'].set_color("#5998ff")
    ax1.spines['top'].set_color("#5998ff")
    ax1.spines['left'].set_color("#5998ff")
    ax1.spines['right'].set_color("#5998ff")
    ax1.tick_params(axis='y', colors='w')
    plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(prune='upper'))
    ax1.tick_params(axis='x', colors='w')
    plt.ylabel('Stock price and Volume')
    plt.show()