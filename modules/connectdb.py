import pymysql

def connDB():
    conn=pymysql.connect(host='localhost',user='root',passwd='66196619',db='data',charset='utf8')
    cur=conn.cursor();
    return (conn,cur);

def exeQuery(cur,sql):
    cur.execute(sql);
    return (cur);

def connClose(conn,cur):
    cur.close();
    conn.commit();
    conn.close();