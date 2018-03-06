# -*- coding: utf-8 -*-
"""
Created on Mon Mar  5 16:45:59 2018

@author: xiexihao
"""

import pymysql

DBName = 'stock'
DBCon = None

def initDBCon():
    ip = 'localhost'
    usr = 'root'
    pwd = 'xxh@WE10018164'
    charset = 'utf8'
    
    global DBCon
    DBCon = pymysql.connect(ip, usr, pwd, charset = charset)


def closeDBCon():
    global DBCon
    if DBCon != None:
        try:
            DBCon.close()
        except:
            print('数据库关闭失败')
    
    DBCon = None