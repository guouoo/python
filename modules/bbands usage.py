# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 15:16:17 2017

@author: tguo
"""
import pandas as pd
import numpy as np
import talib as ta
import logging
import pymysql
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, WeekdayLocator, DayLocator, MONDAY,YEARLY,date2num
from mpl_finance import candlestick_ohlc  as candlestick


import numpy as np

logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s: %(message)s"
)

def connDB(): #连接数据库函数
    conn=pymysql.connect(host='localhost',user='root',passwd='66196619',db='data',charset='utf8')
    cur=conn.cursor();
    return (conn,cur);

def exeQuery(cur,sql):#查询语句
    cur.execute(sql);
    return (cur);

def connClose(conn,cur):#关闭所有连接
    cur.close();
    conn.commit();
    conn.close();
    
conn,cur =connDB()
query_sql = 'select date, openprice_q,highprice_q,lowprice_q,closeprice_q from data.his_stk_fq where symbol = \'002456\'  and date between \'2017-03-01\' and \'2017-10-11\' order by date asc '
try:
    table_data = pd.read_sql_query(query_sql,conn)
except Exception as e:
    print(e)


connClose(conn, cur)

sma_5 = ta.SMA(np.array(table_data['closeprice_q']), 5)
sma_20 = ta.SMA(np.array(table_data['closeprice_q']), 20)

np_data = np.array(table_data)
for i in range(0,len(np_data)):
    np_data[i][0] = date2num(np_data[i][0])
    # np_data[i][1:5] =

closeprice = np.array([float(x) for x in np_data[:,4]])
upperband, middleband, lowerband = ta.BBANDS(closeprice, timeperiod=5, nbdevup=2, nbdevdn=2, matype=0)

fig, ax = plt.subplots()
fig.subplots_adjust(bottom=0.2)
# 设置X轴刻度为日期时间
ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
plt.xticks(rotation=45)
plt.yticks()
candlestick(ax,np_data,width=0.8,colorup='r',colordown='green')
# plt.plot(np_data[:,0], sma_5,'r-', lw = 1 ,label='MA_5pyderd')
# plt.plot(np_data[:,0], sma_20,'b-',lw = 1 ,label='MA_20d')
plt.plot(np_data[:,0], upperband,'k-', lw = 0.8 )
plt.plot(np_data[:,0], middleband,'c-',lw = 1)
plt.plot(np_data[:,0], lowerband,'k-',lw = 0.8 )
plt.grid(True)
plt.show()
#
#
# seri