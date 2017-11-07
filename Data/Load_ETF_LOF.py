'''
Created on Nov 23, 2015

@author: tguo
'''


# coding=UTF-8
import tushare as ts
import time
import datetime
import pymysql
import logging
import os

BASE_DIR = os.path.dirname(__file__)
LOG_PATH = BASE_DIR +'/log/data_update/'
LOG_FILENAME = str(time.strftime('%Y%m%d_%H%M%S',time.localtime(time.time()))) + '.log'
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

def exeUpdate(cur,sql):#更新语句，可执行update,insert语句
    sta=cur.execute(sql);
    return(sta);

def exeDelete(cur,IDs): #删除语句，可批量删除
    for eachID in IDs.split(' '):
        sta=cur.execute('delete from relationTriple where tID =%d'% int(eachID));
    return (sta);

def exeQuery(cur,sql):#查询语句
    cur.execute(sql);
    return (cur);

def connClose(conn,cur):#关闭所有连接
    cur.close();
    conn.commit();
    conn.close();


def LoadStockHistory(list):
    conn, cur = connDB();
    dateinfo = exeQuery(cur, 'select symbol , maxdate FROM data.id_list where source = \''+ list + '\'').fetchall()
    # edate = time.strftime('%Y-%m-%d', time.localtime(time.time()));
    edate = datetime.date.today();

    for k in range(0,len(dateinfo)):
        conn, cur = connDB()
        sdate=dateinfo[k][1]

        if sdate >  edate:
           continue
        try:
            pricedata = ts.get_k_data(dateinfo[k][0], ktype='D', start=str(sdate), end=str(edate));
        except Exception as e:
            logging.info(e)

        for h in range(0,len(pricedata)):
            daily_data = '(\''
            for k in range(0,len(pricedata.values[h])):
                daily_data = daily_data + ',\'' + str(pricedata.values[h][k]) + '\''
            daily_data = daily_data.replace('(\',\'','(\'')
            insql = 'insert into ' + list + ' (date,openprice,closeprice,highprice,lowprice,volume,symbol) values ' + daily_data + ');'
            # logging.info(insql)
            try:
                conn.cursor().execute(insql)
            except Exception as e:
                logging.info(e)

        conn.commit()
        logging.info(str(dateinfo[k][0]) + ' is inserted' )
    connClose(conn, cur)

LoadStockHistory('his_etf')
LoadStockHistory('his_lof')