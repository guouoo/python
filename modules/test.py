import tushare as ts
import os
import time
import logging
import numpy
# BASE_DIR = os.path.dirname(__file__)
# LOG_PATH = BASE_DIR +'/'
# LOG_FILENAME = str(time.strftime('%Y%m%d_%H%M%S',time.localtime(time.time()))) + '.log'
logging.basicConfig(
    # filename = LOG_PATH + LOG_FILENAME,
    level=logging.DEBUG,
    # format="[%(asctime)s] %(name)s:%(levelname)s: %(message)s"
    format="%(levelname)s: %(message)s"
)

sdate = '2010-01-01'
enddate = '2011-01-01'
qfqdata = ts.get_k_data('002456', start=sdate, end=enddate);
logging.info(qfqdata)