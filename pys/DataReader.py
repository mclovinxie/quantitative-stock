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


def justTry(dateStr, dayCount):
    if dbu.DBCon == None:
        dbu.initDBCon()
    
    sql = '''
        SELECT
            b.data_date AS data_date    
            , b.stock_code AS stock_code
            , b.ch_name AS ch_name
            , b.last_open AS last_open
            , b.open AS open
            , b.close AS close
            , b.low AS low
            , b.high AS high
            , b.profit AS profit
            , b.profit_ratio AS profit_ratio
        FROM (
            SELECT
               a.stock_code AS stock_code
               , MAX(data_date) AS data_date
            FROM (
                SELECT
                    a.stock_code AS stock_code
                    , a.data_date AS data_date
                    , a.profit_ratio AS profit_ratio
                    , @rownum := @rownum + 1
                    , CASE
                        WHEN @pstock = a.stock_code THEN @rank := @rank + 1
                        ELSE @rank := 1
                      END AS rank
                    , @pstock := a.stock_code
                FROM (
                    SELECT
                        a.stock_code AS stock_code
                        , a.data_date AS data_date
                        , a.profit_ratio AS profit_ratio
                    FROM stock.stock_price_data a
                    INNER JOIN (
                        SELECT
                            @rownum := 0
                            , @pstock := NULL
                            , @rank := 0
                    ) b ON
                        1 = 1
                    WHERE
                        a.data_date <= '%s'
                        AND SUBSTR(a.stock_code, 1, 3) <> '000'
                    ORDER BY
                        a.stock_code ASC
                        , a.data_date DESC
                ) a
            ) a
            WHERE
                a.rank <= %d
            GROUP BY
                a.stock_code
            HAVING
                MIN(a.profit_ratio) >= 0
        ) a
        INNER JOIN stock.stock_price_data b ON
            b.stock_code = a.stock_code
            AND b.data_date = a.data_date
            AND b.open > 0
        ;
    ''' % (dateStr, dayCount)
    stockdata = pd.DataFrame()
    rawdata = pd.read_sql(sql, dbu.DBCon)
    stockdata = pd.concat([rawdata, stockdata])
    
    dbu.closeDBCon()
    
    return stockdata