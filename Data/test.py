# 发送data每日更新情况
# -*- coding: UTF-8 -*-

import time
import os
import pymysql
import logging
import pandas as pd
# import


# BASE_DIR = os.path.dirname(__file__)
# LOG_PATH = BASE_DIR +'/log/data_update/'
# LOG_FILENAME = str(time.strftime('%Y-%m-%d',time.localtime(time.time()))) + '_Updating Status.txt'
logging.basicConfig(
    # filename = LOG_PATH + LOG_FILENAME,
    level=logging.DEBUG,
    # format="[%(asctime)s] %(name)s:%(levelname)s: %(message)s"
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

current_day = time.strftime( '%Y-%m-%d', time.localtime(time.time()))
# logging.info('Current date is: ' + current_day)
conn,cur =connDB()

def latest_record(table):
    query_sql = 'select date, closeprice, chgrate from data.' + table + ' where symbol = \'399300\'  and date between \'2010-01-01\' and \'2017-09-06\' order by date asc '
    try:
        table_data = pd.read_sql_query(query_sql,conn)
        # logging.info(table)
        # logging.info(table_data)
    except Exception as e:
        logging.info(e)
        logging.info(query_sql)
    return table_data

table_list = 'his_idx'

index_data = latest_record(table_list)

connClose(conn, cur)


change_rate = []
hold_rate = [1]
cumulative_rate = [1]
months = [2,11]
for i in range(0,len(index_data)):
    if index_data.iloc[i][0].month in months:
        change_rate.append(index_data.iloc[i][2])
    else:
        change_rate.append('0')

for j in range(1,len(change_rate)):
    rate_temp = cumulative_rate[j-1]*(1+ float(change_rate[j])/100)
    cumulative_rate.append(rate_temp)

    hold_rate_temp = hold_rate[j-1]*(1+ index_data.iloc[j][2]/100)
    hold_rate.append(hold_rate_temp)

index_data.loc[:,'return'] = change_rate
index_data.loc[:,'cumulative'] = cumulative_rate
index_data.loc[:,'holding'] = hold_rate

return_data= index_data.iloc[:,[0,4,5]]
return_data.plot()