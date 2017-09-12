# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 15:38:40 2017

@author: tguo
"""
import logging
import talib
import numpy as np
import tushare as ts
from pyecharts import  Line, Kline, Overlap

# BASE_DIR = os.path.dirname(__file__)
# LOG_PATH = BASE_DIR +'/log/data_update/'
# LOG_FILENAME = str(time.strftime('%Y-%m-%d',time.localtime(time.time()))) + '_Updating Status.txt'
logging.basicConfig(
    # filename = LOG_PATH + LOG_FILENAME,
    level=logging.DEBUG,
    # format="[%(asctime)s] %(name)s:%(levelname)s: %(message)s"
    format="%(levelname)s: %(message)s"
)

data = ts.get_k_data('399300', index=True, start='2017-01-01', end='2017-06-31')
ochl = data[['open', 'close', 'high', 'low']]
ochl_tolist = [ochl.ix[i].tolist() for i in range(len(ochl))]
# logging.info(ochl_tolist)

sma_10 = talib.SMA(np.array(data['close']), 10)
sma_30 = talib.SMA(np.array(data['close']), 30)
logging.info(sma_30)

kline = Kline()
kline.add("日K", data['date'], ochl_tolist, is_datazoom_show=True)

line = Line()
line.add('10 日均线', data['date'], sma_10, is_fill=False, line_opacity=0.8, is_smooth=True)
line.add('30 日均线', data['date'], sma_30, is_fill=False, line_opacity=0.8, is_smooth=True)

overlap = Overlap()
overlap.add(kline)
overlap.add(line)
overlap