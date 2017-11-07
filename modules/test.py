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

fd = ts.Bond()
df = fd.BondCoupon(ticker='000001', field='secShortName,perValueDate,refRatePer,coupon')
logging.info(fd)
logging.info(df)