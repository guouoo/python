# coding=UTF-8
import logging
import datetime
from LoadData import getPrice
import CalcMACD as calc

universe = '399006'
start = '2015-05-01'
end = datetime.datetime.now().strftime("%Y-%m-%d")
# benchmark ='399300'
capital = 1000000
tradecostrate = 0.001
macd = {'short':13,'long':26,'m':9}

logging.basicConfig(
    level=logging.DEBUG,
    # format="[%(asctime)s] %(name)s:%(levelname)s: %(message)s"
    format="%(levelname)s: %(message)s"
)

if __name__ == "__main__":
    temp = getPrice(universe,start,end)
    calc.draw(macd,temp)
    # ,,hist,, = calc.calcMACD(macd,temp)
    # print(hist)