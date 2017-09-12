# 发送data每日更新情况
# -*- coding: UTF-8 -*-

import time
import os
import pymysql
import logging
import pandas as pd


BASE_DIR = os.path.dirname(__file__)
LOG_PATH = BASE_DIR +'/log/data_update/'
LOG_FILENAME = str(time.strftime('%Y-%m-%d',time.localtime(time.time()))) + '_Updating Status.txt'
logging.basicConfig(
    filename = LOG_PATH + LOG_FILENAME,
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
logging.info('Current date is: ' + current_day)
conn,cur =connDB()

def latest_record(table):
    query_sql = 'select * from data.' + table + ' order by 2 desc limit 10'
    try:
        table_data = pd.read_sql_query(query_sql,conn)
        logging.info(table)
        logging.info(table_data)
        logging.info('\n')
    except Exception as e:
        logging.info(e)
        logging.info(query_sql)
        logging.info('\n')


table_list = ('his_1min','his_5mins','his_etf','his_lof','his_stk','his_stk_fq','nav_etf','nav_lof')

for i in range(0,len(table_list)):
    latest_record(table_list[i])

connClose(conn, cur)

