'''
Created on Dec 10, 2015

@author: tguo
'''
# coding=UTF-8

#导入支持库文件
import pymysql
import urllib.request
import re
import time
import datetime
import logging
from decimal import Decimal
import sys
from termcolor import colored, cprint

logging.basicConfig(
    level=logging.DEBUG,
    # format="[%(asctime)s] %(name)s:%(levelname)s: %(message)s"
    format="%(levelname)s: %(message)s"
)

class Message:
    def info(self,info):
        self.info = info

def connDB():
    conn=pymysql.connect(host='localhost',user='root',passwd='66196619',db='data',charset='utf8')
    cur=conn.cursor();
    return (conn,cur);

def exeQuery(cur,sql):
    cur.execute(sql);
    return (cur);

def connClose(conn,cur):
    cur.close();
    conn.commit();
    conn.close();

conn,cur=connDB()#连接数据库 
universe = ('510500','159901','159919','159902','159937','518880','510500','511010','159915','159905','159903','510900') #定义Universe
# universe = ('510880','510500','513500','513100','159901','510160','510900') #定义Universe

#获取Universe内所有指数实时价格
realtimeprice = []
headers = {'User-Agent' : 'Mozilla/10 (compatible; MSIE 1.0; Windows NT 4.0)'}
codes = str(universe).replace('\'','').replace(', 1',',s_sz1').replace(', 5',',s_sh5').replace('(','').replace(')','')
url2 = 'http://qt.gtimg.cn/q=s_sh'+ codes

try:
    request = urllib.request.Request(url2,headers = headers)
    response = urllib.request.urlopen(request).read().decode('gbk')
    reobj= re.compile('v_s_s.*?~.*?~')
    realtemp = reobj.sub('',response).replace('~~";','').replace('\n','~').strip().split('~')
    # logging.info(realtemp)
    realtimeprice ={}
    realtimechg={}
    for i in range(0,len(realtemp)-1,6):
        realtimeprice[realtemp[i]] = Decimal(realtemp[i+1])
        realtimechg[realtemp[i]] = Decimal(realtemp[i+3])
except Exception as e:
    print(e)


#获取daylist所列回溯日期收盘价
sql1 = 'select date from data.his_idx where symbol = \'399300\' order by date desc limit 22'
exeQuery(cur,sql1)
sqlcontent = cur.fetchall()
# logging.info(sqlcontent)

tempdays = []
daylist=[8,9,10,20]
for i in daylist:
    tempdays.append(datetime.date.isoformat(sqlcontent[i-1][0]))
days = tuple(tempdays)

sql2 = 'select symbol,date,closeprice from data.his_etf where symbol in '+ str(universe) + ' and date in ' + str(days) + ' order by date, symbol'
exeQuery(cur,sql2)
sqlcontent2 = cur.fetchall()

sql3 = 'select symbol,name from data.id_list where symbol in '+ str(universe)
exeQuery(cur,sql3)
sqlcontent3 = dict(cur.fetchall())

#格式化为以日期为key值得嵌套字典格式
content={}
for i in days:
    dailyprice = {}
    for k in sqlcontent2:
        if i == datetime.date.isoformat(k[1]):
            dailyprice[k[0]] = k[2]
    content[i] = dailyprice

#计算Return
dailyreturn={}
try:
    for i in content:
        tempreturn = {}
        for k in content[i]:
            tempreturn[k] = round(100*(realtimeprice[k]/content[i][k] - 1),2)
        dailyreturn[i] = tempreturn
        # logging.info(dailyreturn[i])
except Exception as e:
    print(e)

# logging.info(dailyreturn)

connClose(conn,cur)

#打印标题
Message.info = ''
size = 25
title = '二八趋势轮动策略模型： ' + str(time.strftime( "%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
print(title)
Message.info += title +'\n'

#预定义指数与ETF关系


temp = sorted(days,reverse=True)
temp.reverse()

day5 = dailyreturn[temp[-1]]
temp.pop()

#输出计算结果
for i in temp:
    lines = '-'*(size-10)+ i +'-'*(size+10)
    Message.info  += lines + '\n'
    print(lines)
    returntemp =  sorted(dailyreturn[i].items(), key=lambda d: d[1],reverse=True)

    for n in range(0,len(returntemp)):
        temp = str(n + 1) + ' .  ' + str(returntemp[n][0]) + ' '+ str(sqlcontent3[returntemp[n][0]])+ ': ' + str(returntemp[n][1]) + '%'
        temp2 =  ' | D: '+str(realtimechg[returntemp[n][0]]) + '%'
        temp3 =  ' | W: '+str(day5[returntemp[n][0]]) + '%'

        if returntemp[n][1] > 0:
            cprint(temp,'green',end="")
        else:
            cprint(temp,'white',end="")

        if realtimechg[returntemp[n][0]] <= -3:
            cprint(temp2, 'red',end="")
        else:
            cprint(temp2, 'white',end="")

        if day5[returntemp[n][0]] <= -5:
            cprint(temp3, 'red')
        else:
            cprint(temp3, 'white')

        Message.info += temp + '\n'

