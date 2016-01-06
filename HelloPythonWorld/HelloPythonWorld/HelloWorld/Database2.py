'''
Created on Dec 9, 2015

@author: tguo
'''
# coding=UTF-8
import pymysql 

def connDB(): #连接数据库函数
    conn=pymysql.connect(host='localhost',user='root',passwd='6619',db='tradeinfo',charset='utf8')
    cur=conn.cursor();
#     cursorclass = pymysql.cursors.DictCursor;
    return (conn,cur);

def connClose(conn,cur):#关闭所有连接
    cur.close();
    conn.commit();
    conn.close();
    
conn,cur=connDB() 
cur.execute('select * from his_pris_stk limit 10')
data = cur.fetchall()  


for row in data:
    print (type(row))
    print (row)
    
connClose(conn, cur)