'''
Created on Dec 9, 2015

@author: tguo
'''

# coding=UTF-8

import mysql
from mysql import connector
from collections import namedtuple

def generate_namedtuple(cur):
    from collections import namedtuple
    fieldnames = [d[0].lower() for d in cur.description]
    Record = namedtuple('Record', fieldnames)
    rows = cur.fetchall()    
    if not rows:return
    else:
        return map(Record._make, rows)
            
def generate_dicts(cur):
    fieldnames = [d[0].lower() for d in cur.description]
    while True:
        rows = cur.fetchmany()
        if not rows: return
        for row in rows:
            yield dict(zip(fieldnames, row))

if __name__ == '__main__':
    user = 'root'
    pwd = '6619'
    host = '127.0.0.1'
    db = 'tradeinfo'
    cnx = mysql.connector.connect(user=user, password=pwd, host=host,database=db)
    print(cnx)
    cur = cnx.cursor()
    print(cur)

    cur.execute("SELECT *  FROM his_pris_stk\
                 limit 100")
    sqlcontent = cur.fetchall()
    print(sqlcontent)
    print(generate_dicts(cur))
    for r in generate_dicts(cur):
        print(r['name'], r['closeprice'])

#     cur.execute("SELECT *  FROM his_pris_stk\
#                  limit 100")

    print("-----------------------------")

#     for k in generate_namedtuple(cur):
#         print(k.name, k.population)

    cur.close()
    cnx.close()