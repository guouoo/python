import tushare as ts
import time
import pymysql
import logging
import os

BASE_DIR = os.path.dirname(__file__)
LOG_PATH = BASE_DIR +'/log/data_update/'
LOG_FILENAME = str(time.strftime('%Y%m%d_%H%M%S',time.localtime(time.time()))) + '_5m.log'
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


def load5minsdata():
    conn,cur = connDB();
    # files = BASE_DIR + '/'+ file
    # logging.info(files)
    # symbols = open(files, mode='r', encoding=None, errors=None, newline=None, closefd=True,opener=None)
    # content = symbols.readlines()

    searchsql = 'select symbol, max(datetime) from data.his_5mins group by symbol order by symbol;'
    dateinfo = exeQuery(cur,searchsql).fetchall()

    for r in range(0, len(dateinfo)):
        try: # 获取数据
            kdata = ts.get_k_data(dateinfo[r][0], ktype='5');
        except Exception as e:
            logging.info(e)

        for j in range(0,len(kdata)): # 格式调整
            if dateinfo[r][1].strftime("%Y-%m-%d %H:%S:%M")  >=  kdata.values[j][0]:
               # logging.info(dateinfo[r][1].strftime("%Y-%m-%d %H:%S:%M") + ' >= ' + kdata.values[j][0])
               continue
            minsdata = '(\''
            for k in range(0,len(kdata.values[j])):
                 minsdata = minsdata + ',\'' + str(kdata.values[j][k]) + '\''
            minsdata = minsdata.replace('(\',\'','(\'')
            intsql = 'insert into data.his_5mins (datetime,openprice,closeprice,highprice,lowprice,volume,symbol) values ' + minsdata + ');'
            # logging.info(intsql)
            try: # 数据插入
                conn.cursor().execute(intsql)
            except Exception as e:
                logging.info(e)
                # logging.info(intsql)
        conn.commit();
        logging.info(str(dateinfo[r][0]) + ' 5 mins\' data is loaded.');

    connClose(conn, cur);
    logging.info('Loading is finished at ' + str(time.strftime('%Y%m%d_%H%M%S',time.localtime(time.time()))))

load5minsdata()

