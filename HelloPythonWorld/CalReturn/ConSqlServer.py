'''
Created on Jul 23, 2015

@author: tguo
'''
import pymssql


class MSSQL:



    def __init__(self,host,user,pwd,db):
        self.host = 'geproddb62'
        self.user = 'MSDOMAIN1\tguo'
        self.pwd =' ggstar\'6619'
        self.db = 'CentralRawData'

    def __GetConnect(self):

        if not self.db:
            raise(NameError,"No setting info for database")
        self.conn = pymssql.connect(host=self.host,user=self.user,password=self.pwd,database=self.db,charset="utf8")
        cur = self.conn.cursor()
        if not cur:
            raise(NameError,"Connecting fails.")
        else:
            return cur

    def ExecQuery(self,sql):
        """
                ms = MSSQL(host="localhost",user="sa",pwd="123456",db="PythonWeiboStatistics")
                resList = ms.ExecQuery("SELECT id,NickName FROM WeiBoUser")
                for (id,NickName) in resList:
                    print str(id),NickName
        """
        cur = self.__GetConnect()
        cur.execute(sql)
        resList = cur.fetchall()

        self.conn.close()
        return resList

    def ExecNonQuery(self,sql):
        """
            cur = self.__GetConnect()
            cur.execute(sql)
            self.conn.commit()
            self.conn.close()
        """
        cur = self.__GetConnect()
        cur.execute(sql)
        self.conn.commit()
        self.conn.close()

'''
def main():
## ms = MSSQL(host="localhost",user="sa",pwd="123456",db="PythonWeiboStatistics")
## ms.ExecNonQuery("insert into WeiBoUser values('2','3')")

    ms = MSSQL(host="localhost",user="sa",pwd="123456",db="PythonWeiboStatistics")
    resList = ms.ExecQuery("SELECT id,weibocontent FROM WeiBo")
    for (id,weibocontent) in resList:
        print (str(weibocontent).decode("utf8"))
'''
if __name__ == '__main__':
    main()