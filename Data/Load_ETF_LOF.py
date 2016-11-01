'''
Created on Nov 23, 2015

@author: tguo
'''


# coding=UTF-8
import urllib.request
import time
import datetime
import re
import pymysql
import logging
from bs4 import BeautifulSoup
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

def LoadHistory(list):
    
    conn,cur=connDB()
    # sdate= '1900-01-01';
    edate= time.strftime('%Y-%m-%d',time.localtime(time.time()));
    
#     Historylist = open(list, mode='r', encoding=None, errors=None, newline=None, closefd=True, opener=None)
#     symbolList=Historylist.readlines()
    
    dateinfo = exeQuery(cur,'select symbol,maxdate FROM data.id_list where source =\''+ list + '\'').fetchall()
    maxdate=dict(dateinfo)
    symbolList=tuple(maxdate)

    for k in range(0,len(symbolList)):
        symbol=symbolList[k]
        sdate = str(maxdate[symbolList[k]]+datetime.timedelta(days = 1))
        if sdate >= edate:
            continue
        if symbolList[k][0] != '5':
            url = 'http://biz.finance.sina.com.cn/stock/flash_hq/kline_data.php?symbol=sz' + symbol + '&begin_date=' + sdate + '&end_date=' + edate
        else:
            url = 'http://biz.finance.sina.com.cn/stock/flash_hq/kline_data.php?symbol=sh' + symbol + '&begin_date=' + sdate + '&end_date=' + edate
        logging.info(url)
            # http://biz.finance.sina.com.cn/stock/flash_hq/kline_data.php?symbol=sz159901&begin_date=20060315&end_date=20161015
        Temp = urllib.request.urlopen(url).read()

        tag = BeautifulSoup(Temp, "xml").findAll("content")
        for j in range(0, len(tag)):
            tradeinfo = str(tag[j]).replace('<content bl="" c="', ',\'').replace('"/>', '\')')
            tradedata = '(\'' + symbol + '\'' + re.sub(r'"..="', '\',\'', tradeinfo)

            istsql = 'insert into ' + list + ' (symbol,closeprice,date,highprice,lowprice,openprice,volume) values ' + tradedata + ';'
            logging.info(istsql)
            try:
                conn.cursor().execute(istsql)
                    #print(istsql)
            except Exception as e:
                print(e)
                print(istsql)
#         print(symbolList[k] + ' : Records from \'' + sdate + '\' to \'' + edate + '\' are inserted into table \'' + list + '\'')
               
#     Historylist.close()
    logging.info('''########################################''' +'\n' + list + ' is updated to latest status.' +'\n' + '''########################################''')
    connClose(conn, cur)

LoadHistory('his_etf')
LoadHistory('his_lof')
#LoadHistory('his_classfund')