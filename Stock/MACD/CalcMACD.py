import talib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import copy
import datetime
import numpy as np
import time
from matplotlib.finance import candlestick_ohlc
from matplotlib.dates import date2num
import matplotlib.colors as colors
import matplotlib.finance as finance
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
import matplotlib.font_manager as font_manager
import logging
from matplotlib.dates import DateFormatter, WeekdayLocator,DayLocator, MONDAY


logging.basicConfig(
    level=logging.DEBUG,
    # format="[%(asctime)s] %(name)s:%(levelname)s: %(message)s"
    format="%(levelname)s: %(message)s"
)

# def myMACD(price, fastperiod, slowperiod, signalperiod):
#     ewma12 = pd.ewma(price,span=fastperiod)
#     ewma60 = pd.ewma(price,span=slowperiod)
#     dif = ewma12-ewma60
#     dea = pd.ewma(dif,span=signalperiod)
#     bar = (dif-dea) #有些地方的bar = (dif-dea)*2，但是talib中MACD的计算是bar = (dif-dea)*1
#     return dif,dea,bar

def calcMACD(setting,df):

    macd, signal, hist = talib.MACD(df['close'].values, fastperiod=setting['short'], slowperiod=setting['long'], signalperiod=setting['m'])
    histplus =  copy.deepcopy(hist)
    histsubstract =  copy.deepcopy(hist)
    variationlong =  copy.deepcopy(hist)
    variationshort =  copy.deepcopy(hist)
    for i in range(1,len(hist)):
        if  hist[i-1]*hist[i] < 0 :
            if hist[i-1] <= hist[i]:
                variationlong [i] = (macd[i-1] + macd[i])/2
                variationshort [i] = np.nan
            else:
                variationshort [i] = (macd[i-1] + macd[i])/2
                variationlong [i] = np.nan
        else:
            variationlong [i] = np.nan
            variationshort [i] = np.nan
    return df,macd,signal,hist,variationlong,variationshort

def moving_average(x, n, type='simple'):
    """
    compute an n period moving average.
    type is 'simple' | 'exponential'
    """
    x = np.asarray(x)
    if type == 'simple':
        weights = np.ones(n)
    else:
        weights = np.exp(np.linspace(-1., 0., n))

    weights /= weights.sum()

    a = np.convolve(x, weights, mode='full')[:len(x)]
    a[:n] = a[n]
    return a

def relative_strength(prices, n=14):
    """
    compute the n period relative strength indicator
    http://stockcharts.com/school/doku.php?id=chart_school:glossary_r#relativestrengthindex
    http://www.investopedia.com/terms/r/rsi.asp
    """
    deltas = np.diff(prices)
    seed = deltas[:n+1]
    up = seed[seed >= 0].sum()/n
    down = -seed[seed < 0].sum()/n
    rs = up/down
    rsi = np.zeros_like(prices)
    rsi[:n] = 100. - 100./(1. + rs)

    for i in range(n, len(prices)):
        delta = deltas[i - 1]  # cause the diff is 1 shorter

        if delta > 0:
            upval = delta
            downval = 0.
        else:
            upval = 0.
            downval = -delta

        up = (up*(n - 1) + upval)/n
        down = (down*(n - 1) + downval)/n

        rs = up/down
        rsi[i] = 100. - 100./(1. + rs)

    return rsi

def draw(setting,data):
#初始化图标形状
    plt.rc('axes', grid=True)
    plt.rc('grid', color='0.75', linestyle='-', linewidth=0.5)

    textsize = 10
    left, width = 0.1, 0.8
    rect1 = [left, 0.7, width, 0.2]
    rect2 = [left, 0.3, width, 0.4]
    rect3 = [left, 0.1, width, 0.2]

# 设置图标宽高和背景颜色
    fig = plt.figure(facecolor='white',figsize=[12,8])
    axescolor = '#f6f6f6'  # the axes background color

    ax1 = fig.add_axes(rect1, axisbg=axescolor)  # left, bottom, width, height
    ax2 = fig.add_axes(rect2, axisbg=axescolor, sharex=ax1)
    ax2t = ax2.twinx()
    ax3 = fig.add_axes(rect3, axisbg=axescolor, sharex=ax1)

    temp = np.array(data)
    temp_index = temp[:,0]
    temp_data = np.array(temp[:,1:],dtype='f8')
    df =  pd.DataFrame(temp_data,index=temp_index ,columns = ['open','high','low','close'])

# RSI计算
    prices = df['close'].values
    rsi = relative_strength(prices)
    fillcolor = 'darkgoldenrod'

# 绘制RSI线
    ax1.plot(df.index, rsi, color=fillcolor)
    ax1.axhline(70, color=fillcolor)
    ax1.axhline(30, color=fillcolor)
    ax1.axhline(50, color='pink')
    ax1.fill_between(df.index, rsi, 70, where=(rsi >= 70), facecolor=fillcolor, edgecolor=fillcolor)
    ax1.fill_between(df.index, rsi, 30, where=(rsi <= 30), facecolor=fillcolor, edgecolor=fillcolor)
    ax1.text(0.8, 0.9, '>70 = overbought', va='top', transform=ax1.transAxes, fontsize=textsize)
    ax1.text(0.8, 0.1, '<30 = oversold', transform=ax1.transAxes, fontsize=textsize)
    ax1.set_ylim(0, 100)
    ax1.set_yticks([30, 70])
    ax1.text(0.025, 0.95, 'RSI (14)', va='top', transform=ax1.transAxes, fontsize=textsize)
    # ax1.set_title('Daily Statistics')

# 绘制移动平均5/10/20/30天
    ma5 = moving_average(prices, 5, type='simple')
    ma10 = moving_average(prices, 10, type='simple')
    ma20 = moving_average(prices, 20, type='simple')
    ma30 = moving_average(prices, 30, type='simple')
    # volume = (r.close*r.volume)/1e6  # dollar volume in millions
    # vmax = volume.max()
    # poly = ax2t.fill_between(r.date, volume, 0, label='Volume', facecolor=fillcolor, edgecolor=fillcolor)
    # ax2t.set_ylim(0, 5*vmax)
    # ax2t.set_yticks([])
    linema5, = ax2.plot(df.index, ma5, color='red', lw=1, label='MA_5')
    linema10, = ax2.plot(df.index, ma10, color='brown', lw=0.5, label='MA_10')
    linema20, = ax2.plot(df.index, ma20, color='blue', lw=1, label='MA_20')
    linema30, = ax2.plot(df.index, ma30, color='black', lw=0.8, label='MA_30')
    # t4 = ax2.text(0.3, 0.9, s, transform=ax2.transAxes, fontsize=textsize)
    props = font_manager.FontProperties(size=10)
    leg = ax2.legend(loc='upper left', shadow=True, fancybox=True, prop=props)
    leg.get_frame().set_alpha(0.7)


# 绘制蜡烛图
    df2 = []
    for i in data:
        temp = list(i)
        temp[0] = datetime.date.toordinal(i[0])
        df2.append(temp)

    candlestick_ohlc(ax2, df2,width=0.8,colorup = 'red' ,colordown ='green', alpha=1)


# MACD计算
    df,macd,signal,hist,variationlong,variationshort = calcMACD(setting,df)

# 绘制MACD线
    ax3.plot(df.index,macd,label='DIF',color="red")
    ax3.plot(df.index,signal,label='DEA',color="blue")
    ax3.axhline(y=0,color='black',linewidth=1.5)
    ax3.plot(df.index,hist,label='MACD',color="black")
    ax3.fill_between(df.index, hist, 0, where=(hist >= 0), facecolor='red', edgecolor='red')
    ax3.fill_between(df.index, hist, 0, where=(hist < 0), facecolor='green', edgecolor='green')
    ax3.scatter(df.index,variationlong, marker='o',c='r',s = 50,label='Long',)
    ax3.scatter(df.index,variationshort, marker='*',c='black',s = 80 ,label='Short', )
    leg = ax3.legend(loc='lower left', shadow=True, fancybox=True, prop=props)
    leg.get_frame().set_alpha(0.7)
    ax3.text(0.025, 0.95, 'MACD (%d,%d,%d)' % (setting['short'], setting['long'], setting['m']), va='top', transform=ax3.transAxes, fontsize=textsize)
    ax3.set_xlim(df.index[0],df.index[-1]+datetime.timedelta(1))

# 处理横坐标，只显示底部一条
    for ax in ax1, ax2, ax2t, ax3:
        if ax != ax3:
            for label in ax.get_xticklabels():
                label.set_visible(False)
        else:
            for label in ax.get_xticklabels():
                label.set_rotation(30)
                label.set_horizontalalignment('right')
        ax.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')


    plt.show()