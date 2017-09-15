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

return_order = {'510880.XSHG': 1.012,'510500.XSHG': 1.002,'513500.XSHG': 1.035,'513100.XSHG':0.998}
# stock_order  = sorted(return_order.items(),key=lambda item:item[1])
# order  = stock_order[-1]
keys = list(return_order.keys())[0]
logging.info(keys)
# stocks = '159901.XSHE'
# logging.info(stocks)
# stocks = ['510880.XSHG','510500.XSHG','513500.XSHG','513100.XSHG','159901.XSHE','510160.XSHG','510900.XSHG']
# for stock in stocks:
#     logging.info(stock)
