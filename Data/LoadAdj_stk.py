import DBConnect
import logging
import os
import tushare as ts
import time

# BASE_DIR = os.path.dirname(__file__)
# LOG_PATH = BASE_DIR + '/log/data_update/'
# LOG_FILENAME = str(time.strftime('%Y%m%d_%H%M%S', time.localtime(time.time()))) + '_NAV.log'
logging.basicConfig(
    # filename=LOG_PATH + LOG_FILENAME,
    level=logging.DEBUG,
    # format="[%(asctime)s] %(name)s:%(levelname)s: %(message)s"
    format="%(levelname)s: %(message)s"
)

df = ts.get_k_data('002456',start='2012-10-01', end='2013-10-31', autype='qfq')

conn, cur = connDB()


logging.info(df)

