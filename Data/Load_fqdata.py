import tushare as ts
import time
import datetime
import pymysql
import logging
import os

BASE_DIR = os.path.dirname(__file__)
LOG_PATH = BASE_DIR +'/log/data_update/'
LOG_FILENAME = str(time.strftime('%Y%m%d_%H%M%S',time.localtime(time.time()))) +'_fq'+'.txt'
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

conn, cur = connDB();

def load_fq_daily():

    # 获取日期时间
    dateinfo = exeQuery(cur, 'select symbol, maxdate,mindate FROM data.id_list where source in (\'his_etf\',\'his_stk\',\'his_lof\')  order by symbol').fetchall()

    # dateinfo = exeQuery(cur, 'select symbol, max(date),min(date) FROM data.his_stk_fq where symbol =\'002456\'').fetchall()
    edate = time.strftime('%Y-%m-%d', time.localtime(time.time()))

    # 更新前后复权数据到最新；
    for i in range(0,len(dateinfo)):
        sdate = dateinfo[i][1].isoformat()
        if sdate > edate:
            continue
        try:
            hfqdata = ts.get_k_data(dateinfo[i][0], start=sdate, end=edate, autype='hfq');
        except Exception as e:
            logging.info(e)
        try:
            qfqdata = ts.get_k_data(dateinfo[i][0], start=sdate, end=edate);
        except Exception as e:
            logging.info(e)

        for j in range(0,len(qfqdata)):
            qfqvalue = '(\''
            hfqvalue = ''
            for k in range(0,len(qfqdata.values[j])-2):
                qfqvalue = qfqvalue + ',\'' + str(qfqdata.values[j][k]) + '\''
            qfqvalue = qfqvalue.replace('(\',\'', '(\'')

            for h in range(1, len(qfqdata.values[j])-2):
                hfqvalue = hfqvalue + ',\'' + str(hfqdata.values[j][h]) + '\''
            hfqvalue = hfqvalue.replace('(\',\'', '(\'')

            insertsql = 'insert into data.his_stk_fq (date,openprice_q,closeprice_q,highprice_q,lowprice_q,openprice_h,closeprice_h,highprice_h,lowprice_h,symbol) values ' + qfqvalue +',' +   hfqvalue + ',\'' + hfqdata.values[j][6] + '\');'
            insertsql = insertsql.replace(',,',',')

            try:
                conn.cursor().execute(insertsql)
            except Exception as e:
                logging.info(e)
        conn.commit();
    logging.info(dateinfo[i][0] + ' is loaded into database.')

    connClose(conn, cur)
    logging.info('Loading is finished at ' + str(time.strftime('%Y%m%d_%H%M%S', time.localtime(time.time()))))

def refresh_qfq():
    # 获取日期时间
    dateinfo = exeQuery(cur, 'select symbol, max(date),min(date) FROM data.his_stk_fq group by symbol order by symbol').fetchall()
    # dateinfo = exeQuery(cur, 'select symbol, max(date),min(date) FROM data.his_stk_fq where symbol =\'002456\'').fetchall()
    # 前复权数据历史全刷新
    for i in range(0,len(dateinfo)):
        years = int(int(str(dateinfo[i][1] - dateinfo[i][2]).replace(' days, 0:00:00', '')) / 365) + 1

        for j in range(0, years):
            sdate = dateinfo[i][2] + j * datetime.timedelta(days=365)
            enddate = dateinfo[i][2] + (j + 1) * datetime.timedelta(days=365)
            if sdate > enddate:
                continue
            try:
                qfqdata = ts.get_k_data(dateinfo[i][0], start=str(sdate), end=str(enddate));
            except Exception as e:
                logging.info(e)

            for k in range(0,len(qfqdata)):
                qfqvalue = '(\''
                for h in range(0,len(qfqdata.values[k])-2):
                    qfqvalue = qfqvalue + ',\''+ str(qfqdata.values[k][h]) + '\''
                qfqvalue = qfqvalue.replace('(\',\'','(\'')
                insertsql = 'insert into data.his_stk_fq (date,openprice_q,closeprice_q,highprice_q,lowprice_q,symbol) values ' + qfqvalue + ',\''+ str(qfqdata.values[k][-1])+'\') ON DUPLICATE KEY UPDATE \
                    openprice_q =' + str(qfqdata.values[k][1]) +',' + '\
                    closeprice_q =' + str(qfqdata.values[k][2]) +','+ '\
                    highprice_q =' + str(qfqdata.values[k][3]) +','  + '\
                    lowprice_q =' + str(qfqdata.values[k][4]) +';'  #+ '\
                # logging.info(insertsql)
                try:
                    conn.cursor().execute(insertsql)
                except Exception as e:
                    logging.info(e)
                    logging.info(insertsql)
            conn.commit();

        logging.info(dateinfo[i][0] + ' is refreshed data.')

    connClose(conn, cur)
    logging.info('Loading is finished at ' + str(time.strftime('%Y%m%d_%H%M%S',time.localtime(time.time()))))

# load_fq_daily()
refresh_qfq()