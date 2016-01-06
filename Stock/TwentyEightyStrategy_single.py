'''
Created on Dec 10, 2015

@author: tguo
'''
# coding=UTF-8

#倒入支持库文件
import pymysql
import numpy as np
import time
import urllib.request
import re
from decimal import Decimal

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

#获取已有Return数据
getsql = 'SELECT a.symbol,b.idx_name,\
ret_1day,ret_5days,ret_10days,ret_20days,ret_30days,ret_60days,ret_120days,ret_200days,ret_250days \
FROM tradeinfo.return_idx a left join list_idx b on a.symbol =b.symbol \
where  a.symbol in ' + str(universe) + ' order by ret_20days desc'
exeQuery(cur,getsql)
sqlcontent = np.array(cur.fetchall())


#获取第前20日ClosePrice
getsql2 = 'SELECT a.symbol,b.idx_name,closeprice_20days \
FROM tradeinfo.return_idx a left join list_idx b on a.symbol =b.symbol \
where  a.symbol in ' + str(universe) + ' order by ret_20days desc'
exeQuery(cur,getsql2)
sqlcontent3 = np.array(cur.fetchall())


#获取Universe内所有指数实时价格
headers = {'User-Agent' : 'Mozilla/12 (compatible; MSIE 1.0; Windows NT 4.0)'}
codes = str(universe).replace('\'','').replace(',',',s_sz').replace('(','').replace(')','').replace(' ','')
url2 = 'http://qt.gtimg.cn/q=s_sz'+codes
try:            
    request = urllib.request.Request(url2,headers = headers)
    response = urllib.request.urlopen(request).read().decode('gbk')
    reobj= re.compile('v_s_sz.*?~.*?~')
    realtemp = reobj.sub('',response).replace('~~";','').replace('\n','~').strip().split('~')
    dictprice ={}
    for i in range(0,len(realtemp)-1,6):
        dictprice[realtemp[i]] = Decimal(realtemp[i+1])
except Exception as e:
    print(e)

#打印标题
size = 45
print('*'*100)
print('-'*size+'二八趋势轮动策略模型：  ' + str( time.strftime( "%Y-%m-%d %H:%M:%S", time.localtime( time.time() ) ))  +'-'*size)


#计算实时价格与前20日价格比率
RealPrice=[]
for i in range(0, len(dictprice)):
    ReturnRate = round((dictprice[sqlcontent3[i,0]] - sqlcontent3[i,2])/sqlcontent3[i,2]*100,3)
    RealPrice.append(sqlcontent3[i,0])
    RealPrice.append(sqlcontent3[i,1].strip())
    RealPrice.append(ReturnRate)
temp = np.array(RealPrice).reshape(len(dictprice),3)
Pricedata  = np.array(sorted(temp,key=lambda l:l[2], reverse=True)).reshape(len(dictprice),3)


#输出日历史收益表
sqlcontent1 = sqlcontent[:,[0,1,5]]

print('*'*100)

#预定义指数与ETF关系，(f-)表示流动性差，(c)表示大成C类型基金
fund = {'399004':'159901 & 150018+150019','399102':'Null','399006':'159915 & 150152+150153','399610':'159909(f-)','399008':'159907(f-) & 270026(c)','399337':'159911(f-)','399005':'159902','399300':'159919 & 510300 & 270010(c)','399001':'159903','399330':'159901 & 150083+150084(f-)'}


#输出调仓实时建议
for i in range(0,len(dictprice)):
    if Pricedata[i][2] > 0:

        print(str(i+1) + ' .  ' +str(Pricedata[i,0]).strip()  + ' ' + str(Pricedata[i,1]).strip() +' : '+ str(Pricedata[i,2]).strip() +'%  >>> ' + fund[Pricedata[i,0]].strip())
        
    elif Pricedata[0][2] <= 0:
        print('>>> 负值周期，请空仓等待！建议买入511990，或卖出131810 <<<')
        for i in range(0,len(dictprice)):
            print(str(i+1) + ' .  ' +str(Pricedata[i,0]).strip()  + ' ' + str(Pricedata[i,1]).strip() +' : '+ str(Pricedata[i,2]).strip() +'%')
        break
#         print(str(i+1) + ' .  ' +str(Pricedata[i,0]).strip()  + ' ' + str(Pricedata[i,1]).strip() +' : '+ str(Pricedata[i,2]).strip() +'%  - - - 空仓或卖出 ' + fund[Pricedata[i,0]].strip())
print('-'*100)
