import pymssql

a = pymssql.connect(server='geoutputdb601')
cur = a.cursor()
cur.execute("select top 10 * from CentralRawData.dbo.HistoricalRawPrice")
resList = cur.fetchall()
print(resList)