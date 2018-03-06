# -*- coding: utf-8 -*-
"""
Created on Mon Mar  5 16:43:43 2018

@author: xiexihao
"""

import pandas as pd
import DBUtil as dbu

def readStockData(stockcode, sday, eday):
    if dbu.DBCon == None:
        dbu.initDBCon()
    
    sql = "SELECT data_date, open, high, close, low, dill FROM %s.stock_price_data WHERE stock_code = '%s' AND data_date BETWEEN DATE('%s') AND DATE('%s')" % (dbu.DBName, stockcode, sday, eday)
    stockdata = pd.DataFrame()
    rawdata = pd.read_sql(sql, dbu.DBCon)
    stockdata = pd.concat([rawdata, stockdata])
    stockdata = stockdata.sort_index()
    stockdata.index.name = 'data_date'
    #stockdata.drop('amount', axis=1, inplace = True)
    stockdata.columns = ['data_date', 'open', 'high', 'close', 'low', 'volume']
    #stockdata = stockdata[stockdata.index < eday.strftime('%Y-%m-%d')]
    
    dbu.closeDBCon()
    
    return stockdata