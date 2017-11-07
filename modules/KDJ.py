import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import date2num
from mpl_finance import candlestick_ohlc
import tushare as ts
import talib as ta

bars = ts.get_h_data('002456', start='2017-01-01', end='2017-10-12')
bars= bars.sort_index(axis=0, level=None, ascending=True)
bars = bars.shift(23, freq='H')
width = 0.5 # K线柱体宽度

fig = plt.figure()

# 子图1,3/4空间
ax1 = plt.subplot2grid((4, 4), (0, 0), rowspan=3, colspan=4)
ohlc = zip(bars.index.map(date2num), bars['open'], bars['high'], bars['low'], bars['close'])
candlestick_ohlc(ax1, ohlc, width=width, colorup='#db3f3f', colordown='#77d879')
plt.grid(True)

# 计算KDJ数据，加入矩阵
bars['slowk'], bars['slowd'] = ta.STOCH(bars['high'].values,
                                        bars['low'].values,
                                        bars['close'].values,
                                        fastk_period=5,
                                        slowk_period=3,
                                        slowk_matype=0,
                                        slowd_period=3,
                                        slowd_matype=0)

bars['jvalue'] = 3*bars['slowk']-2*bars['slowd']
tempcol = bars['jvalue'].replace([bars['jvalue'][bars['jvalue']>100].values],100).replace([bars['jvalue'][bars['jvalue']<0].values],0)
bars = bars.replace(bars['jvalue'].values,tempcol)

# 子图2,1/4空间
ax2 = plt.subplot2grid((4, 4), (3, 0), rowspan=1, colspan=4)
# ax2 =ax1.twinx() # 两图重叠
ax2.plot(bars.index.map(date2num), bars.slowk, '-', color='b',lw=0.8)
ax2.plot(bars.index.map(date2num), bars.slowd, '-', color='y',lw=0.8)
ax2.plot(bars.index.map(date2num), bars.jvalue, '-', color='r',lw=0.8)
ax2.plot(bars.index.map(date2num), [80]*len(bars), '-', color='m',lw=1)
ax2.plot(bars.index.map(date2num), [20]*len(bars), '-', color='m',lw=1)
# ax2.bar(bars.index.map(date2num), bars['volume'] / 10000, width=width, align='center')
plt.grid(True)

ax1.xaxis.set_major_locator(mdates.WeekdayLocator())
ax1.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
# ax1.xaxis.set_major_formatter(mdates.AutoDateFormatter("%Y-%m-%d"))
ax2.xaxis.set_major_locator(mdates.WeekdayLocator())
ax2.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
# ax2.xaxis.set_major_formatter(mdates.AutoDateFormatter("%Y-%m-%d"))
for label in ax2.xaxis.get_ticklabels():
    label.set_rotation(60)

ax1.set_ylabel("Price")
ax2.set_ylabel("KDJ")

plt.setp(ax1.get_xticklabels(), visible=False)
plt.setp(ax1.yaxis.get_ticklabels()[0], visible=False)
plt.subplots_adjust(bottom=0.15, top=0.85, hspace=0)
plt.show()
