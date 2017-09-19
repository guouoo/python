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

# K线模式识别
k_open = np.array(table_data['openprice_q'])
k_high = np.array(table_data['highprice_q'])
k_low = np.array(table_data['lowprice_q'])
k_close = np.array(table_data['closeprice_q'])

# 函数名：CDL2CROWS 两只乌鸦
res = ta.CDL2CROWS(k_open,k_high,k_low,k_close)