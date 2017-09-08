'''
Created on Sep 30, 2015

@author: tguo
'''

# coding=UTF-8
import urllib.request
import time
import datetime
import os
import re
import pymysql
import logging

path ='C:/temp/' #下载、处理和导入数据路径

BASE_DIR = os.path.dirname(__file__)
LOG_PATH = BASE_DIR +'/log/data_update/'
LOG_FILENAME = str(time.strftime('%Y%m%d_%H%M%S',time.localtime(time.time()))) + '_idxstk.txt'
logging.basicConfig(
    filename = LOG_PATH + LOG_FILENAME,
    level=logging.DEBUG,
    # format="[%(asctime)s] %(name)s:%(levelname)s: %(message)s"
    format="%(levelname)s: %(message)s"
)

def DownloadPrice(table):
    conn,cur =connDB()
    
    dateinfo = exeQuery(cur,'select symbol,maxdate FROM data.id_list where source = \''+ table +'\'order by symbol').fetchall()
    maxdate = dict(dateinfo)
    symbolList = tuple(maxdate)
    symbolList = sorted(symbolList)
    enddate = time.strftime( '%Y%m%d', time.localtime( time.time() ) )

    for k in range(0,len(symbolList)) :
        startdate = str(maxdate[symbolList[k]]+datetime.timedelta(days = 1)).replace('-','')
        # print(symbolList[k] + ' ' + startdate + ' ' + enddate )
        if startdate >= enddate:
            logging.info(symbolList[k] + ' is ignored as ' +str(startdate))
            continue
        if symbolList[k][0] !='6':
            url = 'http://quotes.money.163.com/service/chddata.html?code=1'+symbolList[k]+'&start='+startdate +'&end='+ enddate
        else:
            url = 'http://quotes.money.163.com/service/chddata.html?code=0' + symbolList[k] + '&start=' + startdate + '&end=' + enddate
        local = path + symbolList[k] +'.txt'
        try:
            urllib.request.urlretrieve(url, local)
            logging.info(symbolList[k] + ' is downloaded: '+ str(startdate) + ' ~ ' + str(enddate))
        except Exception as e:
            logging.info(e)

    connClose(conn, cur)
    FormatFiles()
    LoadDataToDB(table)
    return


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

def FormatFiles():
    for filename in os.listdir(path):
        stockprice = open(path+filename, mode='r', encoding=None, errors=None, newline=None, closefd=True, opener=None)
        content = stockprice.readlines()
        del content[0]
        # try:
        #     del content[0]
        # except Exception as e:
        #     logging.info(e)

        for r in range(0,len(content)): 
            content[r] = re.sub('\'','',content[r]).strip()
            list = content[r].split(',') 
            del list[2]
            del list[6:8]
            del list[7]
            del list[8]
#             for i in range(3,16):
#                 list[i] = formatnumber(list[i])
            line = str(list).replace('[','(').replace(']',')').replace('None','0')
            content[r] = line
        stockprice.close()
         
        stockvalue = open(path+filename, mode='w+', encoding=None, errors=None, newline=None, closefd=True, opener=None)
        for r2 in range(0,len(content)):
            stockvalue.writelines(content[r2]+'\n')
        stockvalue.close()
        logging.info(filename + ' is formated.')

def LoadDataToDB(table):
    conn,cur=connDB()      
    for filename in os.listdir(path):
        stock = open(path+filename, mode='r', encoding=None, errors=None, newline=None, closefd=True, opener=None)
        hisprice = stock.readlines()
        for j in range(0,len(hisprice)):
            istsql = 'insert into '+ table +' (date,symbol,closeprice,highprice,lowprice,openprice,chgrate,volume,marketcap,trademktcap,orders) values '+ hisprice[j]
            try:
                conn.cursor().execute(istsql)
            except Exception as e:
                logging.info(e)
                logging.info(istsql)
        conn.commit();
        logging.info(filename + ' is loaded into database.')
        stock.close()
        try: 
            os.remove(path + filename)
            logging.info(filename + ' is deleted.')
        except Exception as e:
            logging.info(e)
     
    connClose(conn, cur)
    logging.info('''########################################''' +'\n' + table + ' is updated to latest status.' +'\n' + '''########################################''')

DownloadPrice('his_idx')
DownloadPrice('his_stk')
# LoadDataToDB('his_idx')
# FormatFiles()