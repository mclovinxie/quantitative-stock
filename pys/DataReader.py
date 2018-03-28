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


def justTry(dateStr):
    if dbu.DBCon == None:
        dbu.initDBCon()
    
    sql = '''
        SELECT
        	a.stock_code
        	, a.ch_name
        	-- , e.data_date
        	, e.profit_ratio
        	-- , d.data_date
        	, d.profit_ratio
        	-- , c.data_date
        	, c.profit_ratio
        	-- , b.data_date
        	, b.profit_ratio
        	-- , a.data_date
        	, a.profit_ratio
        FROM stock.stock_price_data a
        INNER JOIN stock.stock_price_data b ON
        	b.stock_code = a.stock_code
        	AND b.data_date = DATE_ADD(a.data_date, INTERVAL -1 DAY)
        	AND b.profit_ratio >= 0
        INNER JOIN stock.stock_price_data c ON
        	c.stock_code = b.stock_code
        	AND c.data_date = DATE_ADD(b.data_date, INTERVAL -1 DAY)
        	AND c.profit_ratio >= 0
        INNER JOIN stock.stock_price_data d ON
        	d.stock_code = c.stock_code
        	AND d.data_date = DATE_ADD(c.data_date, INTERVAL -1 DAY)
        	AND d.profit_ratio >= 0
        INNER JOIN stock.stock_price_data e ON
        	e.stock_code = d.stock_code
        	AND e.data_date = DATE_ADD(d.data_date, INTERVAL -1 DAY)
        	AND e.profit_ratio >= 0
        WHERE
        	a.data_date = '%s'
        	AND a.profit_ratio >= 0
        	AND SUBSTR(a.stock_code, 1, 3) <> '000'
        ORDER BY
        	a.stock_code
        ;
    ''' % (dateStr)
    stockdata = pd.DataFrame()
    rawdata = pd.read_sql(sql, dbu.DBCon)
    stockdata = pd.concat([rawdata, stockdata])
    
    dbu.closeDBCon()
    
    return stockdata