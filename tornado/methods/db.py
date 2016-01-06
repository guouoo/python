'''
Created on Nov 24, 2015

@author: tguo
'''


# coding=UTF-8

# import MySQLdb
import pymysql 

# conn = MySQLdb.connect(host="localhost", user="root", passwd="6619", db="tradeinfo", port=3306, charset="utf8")    #连接对象
conn = pymysql.connect(host='localhost',user='root',passwd='6619',db='tradeinfo',charset='utf8')
cur = conn.cursor()    #游标对象