import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import date2num
import talib as ta
import logging as log
from modules.connectdb import *
import pandas as pd
from matplotlib.dates import DateFormatter, WeekdayLocator, DayLocator, MONDAY,YEARLY,date2num
import numpy as np

# log格式设定
log.basicConfig(
    level=log.DEBUG,
    # format="[%(asctime)s] %(name)s:%(levelname)s: %(message)s"
    format="%(levelname)s: %(message)s"
)

stk_code ='002456'
s_date = '2016-01-01'
e_date = '2017-12-31'

# 获取复权数据
conn,cur=connDB() # 连接数据库
query_sql = 'select date, openprice_q,highprice_q,lowprice_q,closeprice_q from data.his_stk_fq where symbol = \'' + stk_code + '\' and date between \'' + s_date + '\' and \'' + e_date + '\' order by date asc;'
price_data = pd.read_sql_query(query_sql,conn)
connClose(conn, cur)


# 计算KDJ数据，加入矩阵
price_data['slowk'], price_data['slowd'] = ta.STOCH(price_data['highprice_q'].values,
                                        price_data['lowprice_q'].values,
                                        price_data['closeprice_q'].values,
                                        fastk_period=5,
                                        slowk_period=3,
                                        slowk_matype=0,
                                        slowd_period=3,
                                        slowd_matype=0)

price_data['jvalue'] = 3*price_data['slowk']-2*price_data['slowd']
tempcol = price_data['jvalue'].replace([price_data['jvalue'][price_data['jvalue']>100].values],100).replace([price_data['jvalue'][price_data['jvalue']<0].values],0)
price_data = price_data.replace(price_data['jvalue'].values,tempcol)

## 买卖条件判断
ops = []
ops.append(0)
for i in range(1,len(price_data)):
    # if price_data['jvalue'][i] > price_data['slowk'][i] and price_data['slowk'][i] > price_data['slowd'][i] and price_data['slowk'][i-1] < 20 and price_data['slowk'][i] > 20:
    #     ops.append(1)
    # elif price_data['jvalue'][i] < price_data['slowk'][i] and price_data['slowk'][i] < price_data['slowd'][i] and price_data['slowk'][i] < 80 and price_data['slowk'][i-1] > 80:
    #     ops.append(-1)
    # else:
    #     ops.append(0)
    if price_data['slowk'][i] > price_data['slowd'][i] and price_data['slowk'][i-1] < price_data['slowd'][i-1]:
        ops.append(1)
    elif price_data['slowk'][i] < price_data['slowd'][i] and price_data['slowk'][i-1] > price_data['slowd'][i-1]:
        ops.append(-1)
    else:
        ops.append(0)
price_data['ops'] = ops

#
#
# # def ATR(price_data):
# atr_high = 0
# ops_t = []
# ops_t.append(0)
# atr_value = ta.ATR(price_data['highprice_q'].values, price_data['lowprice_q'].values, price_data['closeprice_q'].values, timeperiod=14)
# atr_value = np.nan_to_num(atr_value)
#
# for i in range(1,len(price_data)):
#     if price_data['ops'][i-1] == 1:
#         atr_high = max(price_data['highprice_q'][i], atr_high)
#         if (atr_high - 3 * atr_value[i]) > price_data['closeprice_q'][i]:
#             ops_t.append(-1)
#         else:
#             ops_t.append(0)
#     else:
#         ops_t.append(0)
# price_data['ops_t'] = ops_t
# price_data = price_data.replace(price_data['ops'].values, price_data['ops_t'] + price_data['ops'])
#
#     # return price_data

# price_data = ATR(price_data)

## 计算Return
daily_ret = []
daily_ret.append(0)
daily_cul_ret = []
daily_cul_ret.append(1)
for i in range(1,len(price_data)):
    temp_ret = (price_data['closeprice_q'][i] -price_data['closeprice_q'][i-1])/price_data['closeprice_q'][i-1]
    daily_ret.append(temp_ret)
    daily_cul_ret.append(daily_cul_ret[i-1]*(1+temp_ret))
price_data['daily_ret'] = daily_ret
price_data['daily_cul_ret'] = daily_cul_ret

## 计算买卖每日Return和累积Return
ops_ret = []
ops_ret.append(0)
cul_ret = []
cul_ret.append(1)
status = 0
for i in range(1,len(price_data)):
    if status  == 0 and price_data['ops'][i-1] == 1:
        temp_ops_ret = price_data['daily_ret'][i]
        status = 1
    elif status  == 1 and price_data['ops'][i-1] == 0:
        temp_ops_ret = price_data['daily_ret'][i]
    elif status  == 1 and price_data['ops'][i-1] == -1:
        temp_ops_ret = price_data['daily_ret'][i]
        status = 0
    else:
        temp_ops_ret = 0
    temp_cul_ret = cul_ret[i-1]*(1+temp_ops_ret)
    ops_ret.append(temp_ops_ret)
    cul_ret.append(temp_cul_ret)
price_data['ops_ret'] = ops_ret
price_data['cul_ret'] = cul_ret


# 作图
fig, ax = plt.subplots()
fig.subplots_adjust(bottom=0.2)
# 设置X轴刻度为日期时间
ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
plt.xticks(rotation=45)
plt.yticks()

plt.plot(price_data.date, price_data.daily_cul_ret,'k-',color='r', lw = 0.8 )
# plt.plot(np_data[:,0], middleband,'c-',lw = 1)
plt.plot(price_data.date, price_data.cul_ret,'k-',color='b',lw = 0.8 )
plt.grid(True)
plt.show()