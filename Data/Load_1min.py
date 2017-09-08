import time
import pymysql
import logging
import os
import urllib.request

BASE_DIR = os.path.dirname(__file__)
LOG_PATH = BASE_DIR +'/log/data_update/'
LOG_FILENAME = str(time.strftime('%Y%m%d_%H%M%S',time.localtime(time.time()))) + '_1m.log'
logging.basicConfig(
    filename = LOG_PATH + LOG_FILENAME,
    level=logging.DEBUG,
    # format="[%(asctime)s] %(name)s:%(levelname)s: %(message)s"
    format="%(levelname)s: %(message)s"
)

logging.info('Loading is start at ' + str(time.strftime('%Y%m%d_%H%M%S',time.localtime(time.time()))) )

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


def load1mindata():
    conn, cur = connDB();

    # symbols = open(files, mode='r', encoding=None, errors=None, newline=None, closefd=True,opener=None)
    # symbolList = symbols.readlines()

    searchsql = 'select symbol from data.his_1min group by symbol order by symbol;' ;
    timeinfo = exeQuery(cur,searchsql).fetchall()

    for i in range(0,len(timeinfo)):
        if str(timeinfo[i][0]).startswith('6'):
            symbol = 'sh' + str(timeinfo[i][0])
        elif str(timeinfo[i][0]).startswith('5'):
            symbol = 'sh' + str(timeinfo[i][0])
        elif str(timeinfo[i][0]).startswith('1'):
            symbol = 'sz' + str(timeinfo[i][0])
        elif str(timeinfo[i][0]).startswith('0'):
            symbol = 'sz' + str(timeinfo[i][0])
        else:
            symbol = 'sz' + str(timeinfo[i][0])
        urls = 'http://data.gtimg.cn/flashdata/hushen/minute/' + symbol +'.js?'
        # urls = 'http://data.gtimg.cn/flashdata/hushen/minute/sz002456.js?'
        # logging.info(urls)
        headers = {'User-Agent': 'Mozilla/10 (compatible; MSIE 1.0; Windows NT 4.0)'}
        try:
            request = urllib.request.Request(urls,headers = headers)
            response = str(urllib.request.urlopen(request).read()).replace('\\n','') .replace('\\\\\\',',').split(',')
            del response[0]
            del response[-1]
        except Exception as e:
            logging.info(e)
            logging.info(symbol)

        volumeGap = 0
        for j in range(1,len(response)):
            tempRsp = str(response[j]).split(' ')

            datetimeStr = response[0][5:] + tempRsp[0]
            temptime = time.strptime(datetimeStr,'%y%m%d%H%M')
            datetime = time.strftime('%Y-%m-%d %H:%M:%S',temptime)

            minsPrice = tempRsp[1]
            minsVolume = int(tempRsp[2]) - volumeGap
            volumeGap = int(tempRsp[2])


            insertSql =  'insert into data.his_1min values(\'' + str(timeinfo[i][0])  + '\',\'' + datetime + '\',\''  + minsPrice + '\',\'' + str(minsVolume) + '\');'
            try: # 数据插入
                conn.cursor().execute(insertSql)
            except Exception as e:
                logging.info(e)
                # logging.info(insertSql)
        conn.commit();
        logging.info(str(timeinfo[i][0]) + ' 1 mins\' data is loaded.');

    connClose(conn, cur);
    logging.info('Loading is finished at ' + str(time.strftime('%Y%m%d_%H%M%S', time.localtime(time.time()))))


load1mindata();