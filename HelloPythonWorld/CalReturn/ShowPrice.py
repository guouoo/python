'''
Created on Jul 28, 2015

@author: tguo
'''

import pymysql
 
conn = pymysql.connect(user='root', passwd='66196619',
                 host='localhost', db='stock')
cur = conn.cursor()
cur.execute("SET NAMES utf8")

symbol =  input('请输入股票代码: ')

query = ("select b.LegalName,a.TradingDate,a.OpenPrice, a.ClosePrice,a.DayHigh,a.DayLow,a.Volume from stockprice a left join stockinfo b on a.ShareClassId=b.ShareClassId WHERE b.Symbol='%s' order by TradingDate desc limit 10" % symbol)

cur.execute(query)

if cur.execute(query) == 0:
    print("很抱歉，查询不到以下股票代码的记录： %s。" % symbol)
else: 
    for r in cur:
#     print("row_number:"+str(cur.rownumber))        
        print(str(r[0])+"\tTradingDate: "+ str(r[1]) +"\tOpenPrice: "+ str(r[2])+"\tClosePrice: "+ str(r[3])+"\tDayHigh: "+ str(r[4])+"\tDayLow: "+ str(r[5])+"\tVolume: "+ str(r[6])) 

cur.close()    
conn.close() 

