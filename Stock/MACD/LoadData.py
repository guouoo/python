# coding=UTF-8

import pymysql


def connDB():
    conn=pymysql.connect(host='localhost',user='root',passwd='6619',db='tradeinfo',charset='utf8')
    cur=conn.cursor()
    return (conn,cur)

def exeQuery(cur,sql):
    cur.execute(sql)
    return (cur)

def connClose(conn,cur):
    cur.close()
    conn.commit()
    conn.close()

def getPrice(universe,start,end):
    conn,cur=connDB()
    sql0 = 'select historytable from tradeinfo.list_all \
           where symbol = \'' + universe + '\''
    temp = list(exeQuery(cur,sql0))

    sql = 'select Date,openprice,highprice,lowprice,closeprice ' \
          'from ' + temp[0][0] +  \
          ' where symbol = \'' + universe + '\' and date >= \'' + start + '\'' \
          ' and date <= \'' + end + '\' order by date asc'

    temp1 = list(exeQuery(cur,sql))
    connClose(conn,cur)
    return temp1

# getPrice('399006','2015-01-01','2016-01-12')