import tushare as ts
import time
import datetime
import logging
import os
from src.DBConnect import connDB,exeQuery,connClose,exeUpdate

BASE_DIR = os.path.dirname(__file__)
LOG_PATH = BASE_DIR +'/log/data_update/'
LOG_FILENAME = str(time.strftime('%Y%m%d_%H%M%S',time.localtime(time.time()))) + '_qfq.log'
logging.basicConfig(
    filename = LOG_PATH + LOG_FILENAME,
    level=logging.DEBUG,
    # format="[%(asctime)s] %(name)s:%(levelname)s: %(message)s"
    format="%(levelname)s: %(message)s"
)
#
# a = ts.get_k_data('000005', ktype='D', autype='qfq', start='1994-01-05', end='1996-07-10');
# print(a)

def LoadStockHistory():
    conn, cur = connDB()
    dateinfo = exeQuery(cur, 'select symbol , mindate, maxdate FROM data.id_list where source = "his_stk"').fetchall()

    for k in range(0,len(dateinfo)):
        conn, cur = connDB()
        years = int(int(str(dateinfo[k][2] - dateinfo[k][1]).replace(' days, 0:00:00', '')) / 365) + 1
        for i in range(0,years):
            sdate=dateinfo[k][1] + i*datetime.timedelta(days=365)
            edate=dateinfo[k][1] + (i+1)*datetime.timedelta(days=365)
            if sdate >  dateinfo[k][2]:
                continue
            try:
                pricedata = ts.get_k_data(dateinfo[k][0], ktype='D', autype='qfq', start=sdate, end=edate);
            except Exception as e:
                logging.info(e)

            for h in range(0,len(pricedata)):
                values = str(pricedata.values[h]).replace('\' \'','\', \'').replace('[','').replace(']',');')
                insql = 'insert into data.his_stk_qfq (date,open,close,high,low,volume,symbol) values (' + values
                # logging.info(insql)
                try:
                    conn.cursor().execute(insql)
                except Exception as e:
                    logging.info(e)

        conn.commit()
        logging.info(str(dateinfo[k][0]) + ' is inserted' )
    connClose(conn, cur)


LoadStockHistory();