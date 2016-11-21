import pymysql

def connDB():  # 连接数据库函数
    conn = pymysql.connect(host='localhost', user='root', passwd='66196619', db='data', charset='utf8')
    cur = conn.cursor();
    return (conn, cur);


def exeUpdate(cur, sql):  # 更新语句，可执行update,insert语句
    sta = cur.execute(sql);
    return (sta);

def exeQuery(cur, sql):  # 查询语句
    cur.execute(sql);
    return (cur);


def connClose(conn, cur):  # 关闭所有连接
    cur.close();
    conn.commit();
    conn.close();