'''
Created on Jul 28, 2015

@author: tguo
'''

import pymysql
 
conn = pymysql.connect(user='root', passwd='66196619',
                 host='localhost', db='stock')
cur = conn.cursor()
cur.execute("SET NAMES utf8")
cur.execute("SELECT * FROM stockinfo limit 10")
for r in cur:
#     print("row_number:"+str(cur.rownumber))        
    print("Symbol: "+ r[1] +"\tIPD日期: "+ r[6] +"\t公司名称: "+ r[2]) 

cur.close()    
conn.close() 

