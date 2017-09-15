#导入支持库文件
import logging as log
from modules.connectdb import *
from modules.k_patterns import *
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, WeekdayLocator, DayLocator, MONDAY,YEARLY,date2num
from mpl_finance import candlestick_ohlc as candle_stick
import numpy as np
import talib as ta

# log格式设定
log.basicConfig(
    level=log.DEBUG,
    # format="[%(asctime)s] %(name)s:%(levelname)s: %(message)s"
    format="%(levelname)s: %(message)s"
)

stk_code ='002456'
s_date = '2017-01-01'
e_date = '2017-09-12'

# 获取复权数据
conn,cur=connDB() # 连接数据库
query_sql = 'select date, openprice_q,highprice_q,lowprice_q,closeprice_q from data.his_stk_fq where symbol = \'' + stk_code + '\' and date between \'' + s_date + '\' and \'' + e_date + '\' order by date asc;'
table_data = pd.read_sql_query(query_sql,conn)
connClose(conn, cur)

# 计算移动平均线
sma_5 = ta.SMA(np.array(table_data['closeprice_q']), 5)
sma_20 = ta.SMA(np.array(table_data['closeprice_q']), 20)

# 蜡烛图数据处理
np_data = np.array(table_data)
for i in range(0,len(np_data)):
    np_data[i][0] = date2num(np_data[i][0])

# 布林线数据处理和计算
# closeprice = np.array([float(x) for x in np_data[:,4]])
# upperband, middleband, lowerband = ta.BBANDS(closeprice, timeperiod=5, nbdevup=2, nbdevdn=2, matype=0)

# W%R的计算
wr_n = [2,5,10]
wr_data = table_data.date
for n in wr_n:
    wr_high = np.array(table_data['highprice_q'])
    wr_low = np.array(table_data['lowprice_q'])
    wr_close = np.array(table_data['closeprice_q'])
    calc_willr = 100 + ta.WILLR(wr_high,wr_low,wr_close, timeperiod=n)
    s1 = pd.Series(calc_willr,index = wr_data.index,name='wr_' + str(n))
    wr_data = pd.concat([wr_data,s1], axis=1).round(1)

# RSI的计算
rsi_n = wr_n
rsi_data = table_data.date
for n in wr_n:
    rsi_real = np.array(table_data['closeprice_q'])
    calc_rsi = ta.RSI(rsi_real,timeperiod = n)
    s2 = pd.Series(calc_rsi,index = rsi_data.index,name='rsi_' + str(n))
    rsi_data = pd.concat([rsi_data,s2], axis=1).round(1)

# fig, ax = plt.subplots()
# fig.subplots_adjust(bottom=0.2)
# # 设置X轴刻度为日期时间
# ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
# plt.xticks(rotation=45)
# plt.yticks()
# candle_stick(ax,np_data,width=0.6,colorup='r',colordown='green')
# plt.plot(np_data[:,0], sma_5,'b-', lw = 0.7 ,label='MA_5d')
# plt.plot(np_data[:,0], sma_20,'y-',lw = 0.7 ,label='MA_20d')
# # plt.plot(np_data[:,0], upperband,'k-', lw = 0.8 )
# # plt.plot(np_data[:,0], middleband,'c-',lw = 1)
# # plt.plot(np_data[:,0], lowerband,'k-',lw = 0.8 )
# plt.grid( linestyle='-.', linewidth=0.5)

# K线模式识别
k_open = np.array(table_data['openprice_q'])
k_high = np.array(table_data['highprice_q'])
k_low = np.array(table_data['lowprice_q'])
k_close = np.array(table_data['closeprice_q'])
# 函数名：CDL2CROWS 两只乌鸦
# 简介：三日K线模式，第一天长阳，第二天高开收阴，第三天再次高开继续收阴，收盘比前一日收盘价低，预示股价下跌。

res = ta.CDL2CROWS(k_open,k_high,k_low,k_close)



