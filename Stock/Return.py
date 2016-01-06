'''
Created on Nov 26, 2015

@author: tguo
'''
# coding=UTF-8

from statdata.connectdb import connDB,exeQuery,connClose,exeUpdate
import datetime
# import logging
import time
# import os

def pricereturn():
    conn,cur=connDB() 
    getsql1= 'select symbol,name from list_all where type = \'Index\' order by symbol;'  
    exeQuery(cur,getsql1)
    symboldetail=dict(cur)
    symbollist=tuple(symboldetail)
       
    for symbol in symbollist:
        pricedata = dayreturn(symbol)
        pricedata.insert(0,symbol)
        pricedata.append(time.strftime("%Y-%m-%d %X", time.localtime()))
        insertdata = str(pricedata).replace('[','(').replace(']',')')
        insertsql = 'delete from return_idx where symbol=\'' + symbol + '\' ;' + ' insert into return_idx values ' + insertdata +';'
#         print(insertsql)
        try:             
            exeUpdate(cur,insertsql)
        except Exception as e:
            print(e)
            print(insertsql)
    print('Return data is updated to latest records.')
    connClose(conn, cur)
    return


def dayreturn(symbol):
    conn,cur=connDB()
    getsql = 'select Date, closeprice from his_idx where symbol =\'' + symbol+ '\''  + ' order by Date desc limit 251'
#     print(getsql)
    exeQuery(cur,getsql)
    records = list(cur)
#     print(records)
    pricedata = []
    pricedata.append(datetime.datetime.strftime(records[0][0],'%Y-%m-%d')) 
    pricedata.append(float(records[0][1]))
    returndays=[1,5,10,15,20,30,60,120,200,250]
#     print(symbol)
    for i in returndays:
        if i < len(records):
            pricedata.append(datetime.datetime.strftime(records[i][0],'%Y-%m-%d')) 
            pricedata.append(float(records[i][1])) 
            pricedata.append(float(round((records[0][1]-records[i][1])/records[i][1]*100,3)))
        else:
            pricedata.append(datetime.datetime.strftime(records[-1][0],'%Y-%m-%d'))
            pricedata.append(float(records[-1][1]))  
            pricedata.append(float(round((records[0][1]-records[-1][1])/records[-1][1]*100,3)))
#     print(pricedata)   
    connClose(conn,cur)
    return pricedata

pricereturn()

# print(os.sys.path)


