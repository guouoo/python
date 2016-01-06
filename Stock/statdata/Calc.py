'''
Created on Dec 4, 2015

@author: tguo
'''
# coding=UTF-8

from statdata.connectdb import connDB,exeQuery,connClose,exeUpdate
import numpy as np
from numpy import *
import pandas as pd


def annualreturn(sdate,edate,symbol):
    conn,cur=connDB()
    if len(symbol) == 6:
        symbollist = '(\'' +  str(symbol) +'\')'
    else:
        symbollist = str(symbol)
#     print(len(symbol))
    getsql ='select * from list_all where symbol in '  + symbollist + ' order by symbol'
#     print(getsql)
    exeQuery(cur,getsql)
    sqlcontent = np.array(cur.fetchall())
    content = sqlcontent[:,0:3]
#     print(content)
    recorddate = '(\'' + str(sdate) + '\',\'' + str(edate) + '\')'

    content3 = list()
    for i in range(sqlcontent.shape[0]):
        if sqlcontent[i][1] in ('Stock','Index') :
            readsql = 'select Date,closeprice from ' + sqlcontent[i][3] + ' where symbol = \'' + sqlcontent[i][0] + '\' and date in ' + recorddate + ' order by date asc;' 

        elif sqlcontent[i][1] in ('ETF','LOF','classfund') :
            readsql = 'select Date,CulNav from ' + sqlcontent[i][3] + ' where symbol = \'' + sqlcontent[i][0] + '\' and date in ' + recorddate + ' order by date asc;'
        
        try:
            exeQuery(cur,readsql)
            content2=list(cur.fetchall())
            returnrate = round((content2[1][1] - content2[0][1])/content2[0][1]*100,3) 
            content3.append(content2[0][0])
            content3.append(content2[0][1])
            content3.append(content2[1][0])
            content3.append(content2[1][1])
            content3.append(returnrate)
            content3.append(sqlcontent[i][0])

        except Exception as e:
            print(e)
            print(sqlcontent[i][0])
    content4 = array(content3)
    content4.resize((sqlcontent.shape[0],6))
    finalContent = hstack((content,content4))

    title = ['Symbol','Type','Name','StartDate','StartPrice','CloseDate','ClosePrice','ReturnRate','Symbol']    
    dates = pd.DataFrame(finalContent,index=None,columns = title) 
    
#     print(dates)
    print(dates.sort_values(axis=0, by=['ReturnRate'], ascending=False))
    connClose(conn, cur)
    return 

universe = ('399102','399006','399610','399008','399337','399005','399300',)

# universe =('399003','399107','399108','399106','399305','399707','399300','399004','399311','399312','399315','399316','399705','399706','399351','399810','399811','399945','399910','399967','399934','399702','399960','399946','399911','399969','399935','399703','399962','399922','399948','399913','399978','399936','399812','399963','399925','399950','399914','399983','399937','399905','399964','399930','399952','399915','399989','399965','399931','399320','399957','399917','399995','399943','399907','399966','399933','399701','399958','399919','399982','399317','399318','399352','399353','399101','399901','399005','399324','399100','399333','399904','399356','399975','399355','399358','399927','399813','399926','399938','399939','399953','399361','399362','399337','399363','399339','399359','399335','399346','399348','399367','399007','399368','399344','399373','399374','399375','399376','399377','399370','399993','399371','399008','399602','399604','399606','399006','399977','399102','399378','399608','399610','399971','399994','399611','399612','399615','399616','399618','399619','399620','399621','399622','399973','399623','399626','399627','399624','399625','399959','399629','399630','399631','399009','399010','399011','399628','399635','399632','399633','399634','399636','399637','399638','399380','399383','399384','399386','399387','399306','399388','399379','399390','399806','399808','399976','399992')    
annualreturn('2010-11-08','2015-12-09',universe)
