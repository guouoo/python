
import pymssql
import logging
import re

logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s: %(message)s"
)

# class MSSQL:
#
#     def __init__(self,host,user,pwd,db):
#         self.host = host
#         self.user = user
#         self.pwd = pwd
#         self.db = db
#
#     def __GetConnect(self):
#         if not self.db:
#             raise(NameError,"没有设置数据库信息")
#         self.conn = pymssql.connect(host=self.host,user=self.user,password=self.pwd,database=self.db,charset="utf8")
#         cur = self.conn.cursor()
#         if not cur:
#             raise(NameError,"连接数据库失败")
#         else:
#             return cur
#
#     def ExecQuery(self,sql):
#         """
#         执行查询语句
#         返回的是一个包含tuple的list，list的元素是记录行，tuple的元素是每行记录的字段
#
#         调用示例：
#                 ms = MSSQL(host="localhost",user="sa",pwd="123456",db="PythonWeiboStatistics")
#                 resList = ms.ExecQuery("SELECT id,NickName FROM WeiBoUser")
#                 for (id,NickName) in resList:
#                     print str(id),NickName
#         """
#         cur = self.__GetConnect()
#         cur.execute(sql)
#         resList = cur.fetchall()
#
#         #查询完毕后必须关闭连接
#         self.conn.close()
#         return resList
#
#     def ExecNonQuery(self,sql):
#
#         cur = self.__GetConnect()
#         cur.execute(sql)
#         self.conn.commit()
#         self.conn.close()


def refreshPrice(table):
    Historylist = open('list', mode='r', encoding=None, errors=None, newline=None, closefd=True, opener=None)
    symbol=Historylist.readlines()
    connLive = pymssql.connect(server='geoutputdb601')
    cur = connLive.cursor()

    for raw in symbol:
        ConnSql = 'SELECT * FROM '+ table + ' WHERE ShareClassId =\'' + raw.strip() + '\'' + ' and TradingDate >\'2015-12-31\''
        symbol = raw.strip()
        cur.execute(ConnSql)
        getData=cur.fetchall()
        insertSql = 'INSERT INTO ' + table + ' VALUES '

        for raw in getData:
            insertSql = insertSql + '('
            for i in range(0, len(raw)):
                insertSql = insertSql + "'%s'," % (raw[i])
            insertSql = insertSql + ')'

        reobj = re.compile("000',\)")
        insertSql = reobj.sub('\'),', insertSql)
        reobj3 = re.compile("None")
        insertSql = reobj3.sub('',insertSql)
        reobj4 = re.compile(",\)")
        insertSql = reobj4.sub('),', insertSql)
        reobj2 = re.compile("\'\),$")
        insertSql = reobj2.sub('\');',insertSql)

        connCalc = pymssql.connect(server='gecalcdevdb8002')
        cur2 = connCalc.cursor()
        DelSql = 'DELETE ' + table + ' where ShareClassId =\'' + symbol + '\''  + 'and TradingDate >\'2015-12-31\''
        cur2.execute(DelSql)
        connCalc.commit()

        try:
            cur2.execute(insertSql)
        except Exception as e:
            logging.info(e)
        connCalc.commit()
        logging.info(symbol + '\'s price data are inserted')

    connLive.close()
    connCalc.close()

def refreshRatio(table):
    Historylist = open('list', mode='r', encoding=None, errors=None, newline=None, closefd=True, opener=None)
    symbol=Historylist.readlines()
    connLive = pymssql.connect(server='geoutputdb601')
    cur = connLive.cursor()

    for raw in symbol:
        ConnSql = 'SELECT * FROM '+ table + ' WHERE ShareClassId =\'' + raw.strip() + '\''
        symbol = raw.strip()
        cur.execute(ConnSql)
        getData=cur.fetchall()
        insertSql = 'INSERT INTO ' + table + ' VALUES '

        for raw in getData:
            insertSql = insertSql + '('
            for i in range(0, len(raw)):
                insertSql = insertSql + "'%s'," % (raw[i])
            insertSql = insertSql + ')'

        reobj = re.compile("000',\)")
        insertSql = reobj.sub('\'),', insertSql)
        reobj3 = re.compile("None")
        insertSql = reobj3.sub('',insertSql)
        reobj4 = re.compile(",\)")
        insertSql = reobj4.sub('),', insertSql)
        reobj2 = re.compile("\'\),$")
        insertSql = reobj2.sub('\');',insertSql)

        connCalc = pymssql.connect(server='gecalcdevdb8002')
        cur2 = connCalc.cursor()
        DelSql = 'DELETE ' + table + ' where ShareClassId =\'' + symbol + '\''
        cur2.execute(DelSql)
        connCalc.commit()
        logging.info(insertSql)
        try:
            cur2.execute(insertSql)
        except Exception as e:
            logging.info(e)
        connCalc.commit()
        logging.info(symbol + '\'s HistoricalStockValuationRatios data are inserted')

    connLive.close()
    connCalc.close()

def refreshPriceMultiple(table):
    Historylist = open('list', mode='r', encoding=None, errors=None, newline=None, closefd=True, opener=None)
    symbol=Historylist.readlines()
    connLive = pymssql.connect(server='geoutputdb601')
    cur = connLive.cursor()

    for raw in symbol:
        ConnSql = 'SELECT * FROM '+ table + ' WHERE ShareClassId =\'' + raw.strip() + '\'' + 'and AsOfPriceDate >\'2015-12-31\''
        symbol = raw.strip()
        cur.execute(ConnSql)
        getData=cur.fetchall()
        insertSql = 'INSERT INTO ' + table + ' VALUES '

        for raw in getData:
            insertSql = insertSql + '('
            for i in range(0, len(raw)):
                insertSql = insertSql + "'%s'," % (raw[i])
            insertSql = insertSql + ')'

        reobj = re.compile("000',\)")
        insertSql = reobj.sub('\'),', insertSql)
        reobj3 = re.compile("None")
        insertSql = reobj3.sub('',insertSql)
        reobj4 = re.compile(",\)")
        insertSql = reobj4.sub('),', insertSql)
        reobj2 = re.compile("\'\),$")
        insertSql = reobj2.sub('\');',insertSql)

        connCalc = pymssql.connect(server='gecalcdevdb8002')
        cur2 = connCalc.cursor()
        DelSql = 'DELETE ' + table + ' where ShareClassId =\'' + symbol + '\'' + 'and AsOfPriceDate >\'2015-12-31\''
        cur2.execute(DelSql)
        connCalc.commit()

        try:
            cur2.execute(insertSql)
        except Exception as e:
            logging.info(e)
        connCalc.commit()
        logging.info(symbol + '\'s PriceMultiple data are inserted')

    connLive.close()
    connCalc.close()

def main():

## #返回的是一个包含tuple的list，list的元素是记录行，tuple的元素是每行记录的字段
## ms.ExecNonQuery("insert into WeiBoUser values('2','3')")

    refreshPrice('CentralRawData.dbo.HistoricalRawPrice')
    # refreshRatio('CentralEndData.dbo.HistoricalStockValuationRatios')
    # # refreshPriceMultiple('CentralEndDate.PriceMultiple')

if __name__ == '__main__':
    main()