'''
Created on Dec 10, 2015

@author: tguo
'''
# coding=UTF-8

#倒入支持库文件
import pymysql
import urllib.request
import re
import time
import datetime
import logging
from decimal import Decimal

logging.basicConfig(
    level=logging.DEBUG,
    # format="[%(asctime)s] %(name)s:%(levelname)s: %(message)s"
    format="%(levelname)s: %(message)s"
)

def connDB():
    conn=pymysql.connect(host='localhost',user='root',passwd='6619',db='tradeinfo',charset='utf8')
    cur=conn.cursor();
    return (conn,cur);

def exeQuery(cur,sql):
    cur.execute(sql);
    return (cur);

def exeUpdate(cur,sql):
    sta=cur.execute(sql);
    return(sta);

def connClose(conn,cur):
    cur.close();
    conn.commit();
    conn.close();

conn,cur=connDB()#连接数据库 
universe = ('399102','399004', '399006', '399610', '399008', '399337', '399005', '399300','399330','399001') #定义Universe

#获取Universe内所有指数实时价格
realtimeprice = []
headers = {'User-Agent' : 'Mozilla/10 (compatible; MSIE 1.0; Windows NT 4.0)'}
codes = str(universe).replace('\'','').replace(',',',s_sz').replace('(','').replace(')','').replace(' ','')
url2 = 'http://qt.gtimg.cn/q=s_sz'+ codes
try:
    request = urllib.request.Request(url2,headers = headers)
    response = urllib.request.urlopen(request).read().decode('gbk')
    reobj= re.compile('v_s_sz.*?~.*?~')
    realtemp = reobj.sub('',response).replace('~~";','').replace('\n','~').strip().split('~')
    realtimeprice ={}
    for i in range(0,len(realtemp)-1,6):
        realtimeprice[realtemp[i]] = Decimal(realtemp[i+1])
except Exception as e:
    print(e)

#获取daylist所列回溯日期收盘价
sql1 = 'select Date from tradeinfo.his_idx where symbol = \'399300\' order by date desc limit 20'
exeQuery(cur,sql1)
# sqlcontent = list(np.array(cur.fetchall())
sqlcontent = cur.fetchall()
tempdays = []
daylist=[1,5,20]
for i in daylist:
    tempdays.append(datetime.date.isoformat(sqlcontent[i-1][0]))
days = tuple(tempdays)

sql2 = 'select symbol,Date,closeprice from tradeinfo.his_idx where symbol in '+ str(universe) + ' and Date in ' + str(days) + ' order by date, symbol'
exeQuery(cur,sql2)
sqlcontent2 = cur.fetchall()

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
except Exception as e:
    print(e)

connClose(conn,cur)

#打印标题
size = 25
print('二八趋势轮动策略模型： ' + str(time.strftime( "%Y-%m-%d %H:%M:%S", time.localtime(time.time()))))


#预定义指数与ETF关系，(f-)表示流动性差，(c)表示大成C类型基金
fund = {'399004':'159901 & 150018+150019','399102':'Null','399006':'159915 & 150152+150153','399610':'159909(f-)','399008':'159907(f-) & 270026(c)','399337':'159911(f-)','399005':'159902','399300':'159919 & 510300 & 270010(c)','399001':'159903','399330':'159901 & 150083+150084(f-)'}
fundname = {'399004':'深证100R','399330':'深证100','399300':'沪深300','399001':'深证成指','399005':'中小板指','399008':'中小300','399337':'深证民营','399102':'创业板综','399610':'TMT50','399006':'创业板指'}

#输出计算结果
temp = sorted(days,reverse=True)
temp.reverse()
for i in temp:
    print('-'*(size-10)+ i +'-'*(size+10))
    returntemp =  sorted(dailyreturn[i].items(), key=lambda d: d[1],reverse=True)
    for n in range(0,len(returntemp)):
        if returntemp[n][1] > 0:
            print(str(n+1) + ' .  ' +str(returntemp[n][0]) + ' '
                  + str(fundname[returntemp[n][0]]) +': ' + str(returntemp[n][1]) + '%  >>> '
                  + fund[returntemp[n][0]])
        else:
            print(str(n+1) + ' .  ' +str(returntemp[n][0]) + ' '
                  + fundname[returntemp[n][0]] +': ' + str(returntemp[n][1])  + '%')
