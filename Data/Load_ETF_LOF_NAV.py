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
LOG_PATH = BASE_DIR + '/log/data_update/'
LOG_FILENAME = str(time.strftime('%Y%m%d_%H%M%S', time.localtime(time.time()))) + '_NAV.log'
logging.basicConfig(
    filename=LOG_PATH + LOG_FILENAME,
    level=logging.DEBUG,
    # format="[%(asctime)s] %(name)s:%(levelname)s: %(message)s"
    format="%(levelname)s: %(message)s"
)


def connDB():  # 连接数据库函数
    conn = pymysql.connect(host='localhost', user='root', passwd='66196619', db='data', charset='utf8')
    cur = conn.cursor();
    return (conn, cur);


def exeUpdate(cur, sql):  # 更新语句，可执行update,insert语句
    sta = cur.execute(sql);
    return (sta);


def exeDelete(cur, IDs):  # 删除语句，可批量删除
    for eachID in IDs.split(' '):
        sta = cur.execute('delete from relationTriple where tID =%d' % int(eachID));
    return (sta);


def exeQuery(cur, sql):  # 查询语句
    cur.execute(sql);
    return (cur);


def connClose(conn, cur):  # 关闭所有连接
    cur.close();
    conn.commit();
    conn.close();


def LoadHistory(list):
    conn, cur = connDB()
    page = '1';
    per = '12000';

    edate = time.strftime('%Y-%m-%d', time.localtime(time.time()));

    Historylist = open(list, mode='r', encoding=None, errors=None, newline=None, closefd=True, opener=None)
    symbolList=Historylist.readlines()
    # sdate= '1900-01-01';
    dateinfo = exeQuery(cur, 'select symbol, max(date) FROM data.'+ list + ' group by symbol order by symbol').fetchall()
    maxdate = dict(dateinfo)
    symbolList = tuple(maxdate)

    for k in range(0, len(symbolList)):
        sdate = str(maxdate[symbolList[k]] + datetime.timedelta(days=1))

        if sdate >= edate:
            continue
        url = 'http://fund.eastmoney.com/f10/F10DataApi.aspx?type=lsjz&code=' + symbolList[
            k] + '&page=' + page + '&per=' + per + '&sdate=' + sdate + '&edate=' + edate
        # print(url)
        #       http://fund.eastmoney.com/f10/F10DataApi.aspx?type=lsjz&code=159917&page=1&per=12000
        Temp = urllib.request.urlopen(url).read().decode('utf8', 'ignore')
        soup = BeautifulSoup(Temp, "lxml")
        TempValue = re.sub(r'</?td.*?>', '', str(soup.findAll('td'))).replace('[', '').replace(']', '').replace(' ',
                                                                                                                '').replace(
            '%', '').split(',')

        for i in range(0, len(TempValue) - 1, 7):
            for h in range(i, i + 7):
                if TempValue[h] == '':
                    TempValue[h] = '0'

            istsql = 'insert into ' + list + ' values (\'' + symbolList[k] + '\',\'' + TempValue[i] + '\',' + TempValue[
                1 + i] + ',' + TempValue[2 + i] + ',' + TempValue[3 + i] + ',\'' + TempValue[4 + i] + '\',\'' + \
                     TempValue[5 + i] + '\',\'' + TempValue[6 + i] + '\')'
            logging.info(istsql)
            try:
                conn.cursor().execute(istsql)
            except Exception as e:
                logging.info(e)

    logging.info(
        '''########################################''' + '\n' + list + ' is updated to latest status.' + '\n' + '''########################################''')
    connClose(conn, cur)


LoadHistory('nav_etf')
# LoadHistory('nav_lof')
# LoadHistory('his_classfund')