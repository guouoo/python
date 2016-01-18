'''
Created on Sep 30, 2015

@author: tguo
'''

# coding=UTF-8
import urllib.request
import time
import datetime
import os
import re
import pymysql 

path ='d:/src/price3/' #下载、处理和导入数据路径

def DownloadPrice(table):
    conn,cur=connDB() 
    
    dateinfo = exeQuery(cur,'select symbol,max(Date) FROM tradeinfo.'+ table +' group by symbol order by symbol').fetchall()
    maxdate=dict(dateinfo)
    symbolList=tuple(maxdate)
    enddate = time.strftime( '%Y%m%d', time.localtime( time.time() ) )

    for k in range(0,len(symbolList)) :
        startdate = str(maxdate[symbolList[k]]+datetime.timedelta(days = 1)).replace('-','')
        # print(symbolList[k] + ' ' + startdate + ' ' + enddate )
        if startdate >= enddate:
            continue
        url = 'http://quotes.money.163.com/service/chddata.html?code=1'+symbolList[k]+'&start='+startdate +'&end='+ enddate
#         print(url)

        local = path + symbolList[k] +'.txt'
        try:
            urllib.request.urlretrieve(url, local)
#             print(symbolList[k] + ' is downloaded.')
        except Exception as e:
            print(e)

    connClose(conn, cur)
    FormatFiles()
    LoadDataToDB(table)
    return


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

def FormatFiles():
    for filename in os.listdir(path):
        stockprice = open(path+filename, mode='r', encoding=None, errors=None, newline=None, closefd=True, opener=None)
        content = stockprice.readlines()
        del content[0]
        for r in range(0,len(content)): 
            content[r] = re.sub('\'','',content[r]).strip()
            list = content[r].split(',') 
            del list[2]
            del list[9:]            
#             for i in range(3,16):
#                 list[i] = formatnumber(list[i])
            line = str(list).replace('[','(').replace(']',')').replace('None','0')
            content[r] = line
        stockprice.close()
         
        stockvalue = open(path+filename, mode='w+', encoding=None, errors=None, newline=None, closefd=True, opener=None)
        for r2 in range(0,len(content)):
            stockvalue.writelines(content[r2]+'\n')
        stockvalue.close()
#         print(filename + ' is formated.')

def LoadDataToDB(table):
    conn,cur=connDB()      
    for filename in os.listdir(path):
        stock = open(path+filename, mode='r', encoding=None, errors=None, newline=None, closefd=True, opener=None)
        hisprice = stock.readlines()
        for j in range(0,len(hisprice)):
            istsql = 'insert into '+ table + ' values '+ hisprice[j]
            try:
                conn.cursor().execute(istsql)
            except Exception as e:
                print(e)
                print(istsql)
        conn.commit();
#         print(filename + ' is loaded into database.')
        stock.close()
        try: 
            os.remove(path + filename)
#             print(filename + ' is deleted.')
        except Exception as e:
            print(e)
     
    connClose(conn, cur)
    print('''########################################''' +'\n' + table + ' is updated to latest status.' +'\n' + '''########################################''')

DownloadPrice('his_idx')                       