'''
Created on Dec 10, 2015

@author: tguo
'''
# coding=UTF-8

#倒入支持库文件

import datetime
import logging
import tushare as ts

universe = ['399102','399004', '399006', '399610', '399008', '399337', '399005', '399300','399330','399001']

logging.basicConfig(
    level=logging.DEBUG,
    # format="[%(asctime)s] %(name)s:%(levelname)s: %(message)s"
    format="%(levelname)s: %(message)s"
)

#Realtime price
# df = ts.get_realtime_quotes(['399102','399004', '399006', '399610', '399008', '399337', '399005', '399300','399330','399001'])


# df = ts.get_index(universe)
enddate = datetime.datetime.now().strftime("%Y-%m-%d")
startdate =  (datetime.datetime.now() - datetime.timedelta(days = 35)).strftime("%Y-%m-%d")
content2 = {}
for i in universe:
    df = ts.get_h_data(i, index=True, start=startdate,end=enddate)
    temp = df.iloc[[0,4,19], 2:3]
    content2[i] =list(temp.values.flatten())

logging.debug("")
logging.debug(content2)

# #计算Return
# dailyreturn={}
# try:
#     for i in content:
#         tempreturn = {}
#         for k in content[i]:
#             tempreturn[k] = round(100*(realtimeprice[k]/content[i][k] - 1),2)
#         dailyreturn[i] = tempreturn
# except Exception as e:
#     print(e)
#
# connClose(conn,cur)
#
# #打印标题
# size = 25
# print('二八趋势轮动策略模型： ' + time.strftime( "%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
#
#
# #预定义指数与ETF关系，(f-)表示流动性差，(c)表示大成C类型基金
# fund = {'399004':'159901 & 150018+150019','399102':'Null','399006':'159915 & 150152+150153','399610':'159909(f-)','399008':'159907(f-) & 270026(c)','399337':'159911(f-)','399005':'159902','399300':'159919 & 510300 & 270010(c)','399001':'159903','399330':'159901 & 150083+150084(f-)'}
# fundname = {'399004':'深证100R','399330':'深证100','399300':'沪深300','399001':'深证成指','399005':'中小板指','399008':'中小300','399337':'深证民营','399102':'创业板综','399610':'TMT50','399006':'创业板指'}
#
# #输出计算结果
# temp = sorted(days,reverse=True)
# temp.reverse()
# for i in temp:
#     print('-'*(size-10)+ i +'-'*(size+10))
#     returntemp =  sorted(dailyreturn[i].items(), key=lambda d: d[1],reverse=True)
#     for n in range(0,len(returntemp)):
#         if returntemp[n][1] > 0:
#             print(str(n+1) + ' .  ' +str(returntemp[n][0]) + ' '
#                   + str(fundname[returntemp[n][0]]) +': ' + str(returntemp[n][1]) + '%  >>> '
#                   + fund[returntemp[n][0]])
#         else:
#             print(str(n+1) + ' .  ' +str(returntemp[n][0]) + ' '
#                   + fundname[returntemp[n][0]] +': ' + str(returntemp[n][1])  + '%')
