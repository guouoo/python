'''
Created on Nov 23, 2015

@author: tguo
'''
# For ETF/LOF/ClassFund

# coding=UTF-8
import urllib.request
import time
import datetime
import re
import pymysql 
from bs4 import BeautifulSoup

def connDB(): #连接数据库函数
    conn=pymysql.connect(host='localhost',user='root',passwd='6619',db='tradeinfo',charset='utf8')
    cur=conn.cursor();
    return (conn,cur);

def exeUpdate(cur,sql):#更新语句，可执行update,insert语句
    sta=cur.execute(sql);
    return(sta);

def exeDelete(cur,IDs): #删除语句，可批量删除
    for eachID in IDs.split(' '):
        sta=cur.execute('delete from relationTriple where tID =%d'% int(eachID));
    return (sta);

def exeQuery(cur,sql):#查询语句
    cur.execute(sql);
    return (cur);

def connClose(conn,cur):#关闭所有连接
    cur.close();
    conn.commit();
    conn.close();
    


def LoadHistory(list):
    
    conn,cur=connDB() 
    page = '1';
    per = '12000';
    sdate= '1900-01-01';
    edate= time.strftime('%Y-%m-%d',time.localtime(time.time()));
    
    Historylist = open('PreLoadList', mode='r', encoding=None, errors=None, newline=None, closefd=True, opener=None)
    symbolList=Historylist.readlines()
    
#     dateinfo = exeQuery(cur,'select symbol,max(Date) FROM tradeinfo.' + list +' group by symbol order by symbol').fetchall()
#     maxdate=dict(dateinfo)
#     symbolList=tuple(maxdate)
    
    for k in range(0,len(symbolList)):
#         sdate = str(maxdate[symbolList[k]]+datetime.timedelta(days = 1))
        if sdate >= edate:
            continue
        symbol =symbolList[k].strip()
        url = 'http://fund.eastmoney.com/f10/F10DataApi.aspx?type=lsjz&code='+symbol+'&page='+page+'&per='+per+'&sdate='+sdate+'&edate='+ edate
        print(url)
        
        Temp = urllib.request.urlopen(url).read().decode('gbk ','ignore')
        soup = BeautifulSoup(Temp,"lxml")
        TempValue = re.sub(r'</?td.*?>','',str(soup.findAll('td'))).replace('[','').replace(']','').replace(' ','').replace('%','').split(',')
         
        for i in range(0,len(TempValue)-1,7):
            for h in range(i,i+7):
                if TempValue[h] == '':
                    TempValue[h] = '0'
            values2= TempValue[i:7+i]
                                            
            istsql = 'insert into '+ list +' values (\'' + symbolList[k] +'\',\'' + TempValue[i] +'\','+ TempValue[1+i] + ','+ TempValue[2+i] + ',' +TempValue[3+i] + ',\'' + TempValue[4+i]+'\',\'' + TempValue[5+i]+'\',\'' + TempValue[6+i]+'\')'
            try:
                conn.cursor().execute(istsql)
#                 print(istsql)
            except Exception as e:
                print(e)
                print(istsql)
        print(symbol + ' : Records from \'' + sdate + '\' to \'' + edate + '\' are inserted into table \'' + list + '\'')
               
    Historylist.close()
    print('''########################################''' +'\n' + list + ' is updated to latest status.' +'\n' + '''########################################''')
    connClose(conn, cur)

LoadHistory('his_pris_stk')