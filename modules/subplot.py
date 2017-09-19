import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import date2num
from mpl_finance import candlestick_ohlc
import tushare as ts

bars = ts.get_h_data('002337', start='2015-01-01', end='2015-01-30')
bars = bars.shift(23, freq='H')
width = 0.4

fig = plt.figure()

ax1 = plt.subplot2grid((4, 4), (0, 0), rowspan=3, colspan=4)
ohlc = zip(bars.index.map(date2num), bars['open'], bars['high'], bars['low'], bars['close'])
candlestick_ohlc(ax1, ohlc, width=width, colorup='#77d879', colordown='#db3f3f')
plt.grid(True)

ax2 = plt.subplot2grid((4, 4), (3, 0), rowspan=1, colspan=4)
ax2.bar(bars.index.map(date2num), bars['volume'] / 10000, width=width, align='center')
plt.grid(True)

ax1.xaxis.set_major_locator(mdates.DayLocator())
ax1.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
ax2.xaxis.set_major_locator(mdates.DayLocator())
ax2.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
for label in ax2.xaxis.get_ticklabels():
    label.set_rotation(60)

ax1.set_title("002337.sz")
ax1.set_ylabel("Price")
ax2.set_ylabel("Volume(ten thousand)")

plt.setp(ax1.get_xticklabels(), visible=False)
plt.setp(ax1.yaxis.get_ticklabels()[0], visible=False)
plt.subplots_adjust(bottom=0.20, top=0.90, hspace=0)
plt.show()
