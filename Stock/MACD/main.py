# coding=UTF-8
import logging
from LoadData import getPrice
from CalcMACD import calcMACD

universe = '399006'
start = '2015-01-01'
end = '2016-01-12'
# benchmark ='399300'
capital = 1000000
tradecostrate = 0.001
macd = {'short':12,'long':26,'m':9}

logging.basicConfig(
    level=logging.DEBUG,
    # format="[%(asctime)s] %(name)s:%(levelname)s: %(message)s"
    format="%(levelname)s: %(message)s"
)

if __name__ == "__main__":

    temp = getPrice(universe,start,end)
    logging.debug(temp)
    calcMACD(macd,temp)