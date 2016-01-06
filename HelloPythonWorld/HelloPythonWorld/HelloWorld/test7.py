'''
Created on Dec 28, 2015

@author: tguo
'''


# coding=UTF-8

import datetime as dt
import time
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib 

# x = [dt.date(2015, 7, 10),dt.date(2015,8, 10), dt.date(2015, 9, 10),  dt.date(2015, 10, 10)]
# y = [1, 3, 2, 5]
# fig, ax = plt.subplots()
# ax.plot_date(x, y, linestyle='-')
# ax.annotate('Test', (mdates.date2num(x[1]), y[1]), xytext=(20, 15), textcoords='offset points', arrowprops=dict(arrowstyle='-|>'))
# fig.autofmt_xdate()


# text(0.1, 0.9,'matplotlib', ha='center', va='center', transform=ax.transAxes)

plt.axis([0, 20, 0, 20])

t = "This is a really long string that I'd rather have wrapped so that"
#     plt.text(4, 1, t, ha='left', rotation=15)
#     plt.text(5, 3.5, t, ha='right', rotation=-15)
plt.text(5, 5, t, fontsize=11, ha='center', va='top')
#     plt.text(3, 0, t, family='serif', style='italic', ha='right')
#     plt.title("This is a really long title that I want to have wrapped so it"\
#              " does not go outside the figure boundaries", ha='center')

    # Now make the text auto-wrap...
# fig.canvas.mpl_connect('draw_event', on_draw)


# legend.fontsize
 
plt.legend()
plt.show()