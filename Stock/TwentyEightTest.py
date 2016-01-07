'''
Created on Dec 11, 2015

@author: tguo
'''
# coding=UTF-8
from statdata.connectdb import connDB,exeQuery,connClose
import datetime as dt
import decimal
import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib
# import pandas as pd

universe = ('399004','399300','399337','399610','399008','399006')
start = '2010-11-08'
end = '2014-11-06'
benchmark ='399300'
capital = 1000000
tradecostrate = decimal.Decimal('0.001')
tradecost = 0
frequncy = 1
period = 20
rf = 2.3332

class Account:
    def cash(self,cash):
        self.cash = cash
    def stocks(self,stock):
        self.stocks =  stock
    def cost(self,cost):
        self.cost = cost
    def position(self,position):
        self.position = position
    def total(self,total):
        self.total = total
        
class Benchmark:
    def dailyreturn(self,dailyreturn):
        self.dailyreturn = dailyreturn
    def culreturn(self,culreturn):
        self.culreturn =  culreturn
    def mean(self,mean):
        self.mean = mean
    def var(self,var):
        self.var = var
    def std(self,std):
        self.std = std
    def annualizedreturns(self,annualizedreturns):
        self.annualizedreturns = annualizedreturns
 
def calbenchmark(start,end,symbol):
    conn,cur=connDB()
    getsql = 'select Date, closeprice from his_idx where symbol = \'' + symbol + ' \' and Date > \' '+ start + '\' and Date <=\' ' +end + '\' order by Date asc;'
    exeQuery(cur,getsql)
    records = list(cur)
    temp ={}
    temp1={}
    for i in range(period,len(records)):
        temp[records[i][0]] = round((records[i][1]/records[i-1][1] - 1) * 100,3)  
        temp[records[period][0]] = decimal.Decimal('0.000')
        temp1[records[i][0]] = round((records[i][1]/records[period][1] -1) * 100,3)
    Benchmark.dailyreturn = temp
    Benchmark.culreturn = temp1
    temp2 = list(Benchmark.dailyreturn.values())
    Benchmark.mean = np.mean(temp2)
    Benchmark.var = np.var(temp2)
    Benchmark.std = np.std(temp2)
    Benchmark.annualizedreturns = round((math.pow((records[-1][1]/records[period][1]),250/len(records)) - 1) * 100,2)
    connClose(conn,cur)
     
class Trade:
    def date(self,date):
        self.date = date
    def symbol(self,symbol):
        self.symbol = symbol
    def number(self,number):
        self.number = number
    def price(self,price):
        self.price = price
        
class InfoSeri:
    def culrate(self,culrate):
        self.culrate = culrate
    def rate(self,rate):
        self.rate = rate
    def cov(self,cov):
        self.cov = cov
    def std(self,std):
        self.std = std
    def sharp(self,sharp):
        self.sharp = sharp
    def maxdown(self,maxdown):
        self.maxdown = maxdown
    def mean(self,mean):
        self.mean = mean
    def var(self,var):
        self.var = var  
    def annualizedreturns(self,annualizedreturns):
        self.annualizedreturns = annualizedreturns
    def volatility(self,volatility):
        self.volatility = volatility
    def beta(self,beta):
        self.beta = beta
    def alpha(self,alpha):
        self.beta = alpha                        
                        
def Initialize(account): 
#     account = Account()
    account.cash(capital)
    uni_temp = {}
    for symbol in universe: uni_temp[symbol] = 0
    account.stocks(uni_temp)
    account.cost(tradecost)
    account.position(0)
    
def getPrice(start,end):
    conn,cur=connDB()
    getsql = 'select symbol, Date, closeprice from his_idx where symbol in ' + str(universe) + ' and Date > \' '+ start + '\' and Date <=\' ' +end + '\' order by symbol , Date desc;'
    exeQuery(cur,getsql)
    records = list(cur)
    connClose(conn,cur)
    return records

def operation(opdata):
    opdata = sorted(opdata.items(), key=lambda d: d[1], reverse=True)
    oplist = {}
    for i in opdata: 
        oplist[i[0]] = 0
    if opdata[0][1] > 0:
        oplist[opdata[0][0]] = 1
    return oplist 

def trade(tradedata,oplist):
    holdstock = account.stocks
    for symbol in holdstock:
        if holdstock[symbol] > 0: 
            account.position = symbol
            break
        else:
            account.position = 'NA'
    
    operation = {}
    for symbol in oplist:
        if oplist[symbol] == 1: 
            operation = symbol
            break
        else:
            operation = 'NA'
    stocknumber = 0
    if  account.position == 'NA':
        if operation == 'NA': #空仓继续等待
            account.total = account.cash
            
            Trade.symbol = 'NA'
            Trade.number = 0
            Trade.price =  0
            recordtrade()
            recordaccount()

        else: #空仓全额买入
            stocknumber = int(account.cash/tradedata[operation])
            cost = stocknumber*tradedata[operation]*tradecostrate
            account.cost += cost
            account.cash -= stocknumber*tradedata[operation]
            account.cash -= cost
            account.stocks[operation] = stocknumber
            account.total = account.cash + stocknumber*tradedata[operation]
            
            Trade.symbol = operation
            Trade.number = stocknumber
            Trade.price =  tradedata[operation]
            recordtrade()
            recordaccount()
            
    elif operation == account.position: #满仓持股不变
        account.total = account.cash + account.stocks[account.position]*tradedata[account.position]
        
        Trade.symbol = 'NA'
        Trade.number = 0
        Trade.price =  tradedata[account.position]
        recordtrade()
        recordaccount()
    
    elif operation == 'NA' : #清仓
        stocknumber = account.stocks[account.position]
        cost = stocknumber*tradedata[account.position]*tradecostrate
        account.cost += cost
        account.cash += stocknumber*tradedata[account.position]
        account.cash -= cost
        account.stocks[account.position] = 0
        account.total = account.cash
                            
        Trade.symbol = account.stocks[account.position]
        Trade.number = stocknumber
        Trade.price =  tradedata[account.position]
        recordtrade()
        recordaccount()
    
    else:  #换仓，卖出当前所有，买入标的
        stocknumber = account.stocks[account.position]
        cost = stocknumber*tradedata[account.position]*tradecostrate
        account.cost += cost
        account.cash += stocknumber*tradedata[account.position]
        account.cash -= cost
        account.stocks[account.position] = 0
        account.total = account.cash
        
        Trade.symbol = account.stocks[account.position]
        Trade.number = stocknumber
        Trade.price =  tradedata[account.position]
        recordtrade()

        stocknumber = int(account.cash/tradedata[operation])
        cost = stocknumber*tradedata[operation]*tradecostrate
        account.cost += cost
        account.cash -= stocknumber*tradedata[operation]
        account.cash -= cost
        account.stocks[operation] = stocknumber
        account.position = operation 
        account.total = account.cash + stocknumber*tradedata[operation]
        
        Trade.symbol = operation
        Trade.number = stocknumber
        Trade.price =  tradedata[operation]
        recordtrade()
        recordaccount()

accountinfo = []
tradeinfo = []

def recordaccount():
    accountsnapshot = (Trade.date,account.total,account.cash,account.cost,account.position)
    accountinfo.append(accountsnapshot)
    
def recordtrade():      
    tradeaction = (Trade.date,Trade.symbol,Trade.number,Trade.price)
    tradeinfo.append(tradeaction)
    
def strategygo(start,end):
#获得可用交易数据List
    dbrecords = getPrice(start,end)
    pricedata={}
    tradedate=[]
    for i in range(0,len(dbrecords)):
        temp =  dbrecords[i][0] +'_' + str(dbrecords[i][1])
        pricedata[temp] = dbrecords[i][2]

#获得可用交易日期List
    for j in dbrecords:
        tradedate.append(j[1])
        tradedate=list(set(tradedate))
        tradedate.sort()
         
#按日期进行买卖操作
    for k in range(period,len(tradedate)): 
        opdata={}
        tradedata={}
        for i in universe:
            endpriceidx = i +'_' + str(tradedate[k])
            startpriceidx = i +'_' + str(tradedate[k-period])
            opdata[i] = round((pricedata[endpriceidx]/pricedata[startpriceidx]-1)*100,3)
            tradedata[i] = pricedata[endpriceidx]
        oplist = operation(opdata)
        Trade.date = tradedate[k]
        trade(tradedata,oplist)

def getreturn(accountinfo):
    temp = {}
    temp[accountinfo[0][0]] = float(round((accountinfo[0][1]/capital - 1)*100,3))
    for k in range(1,len(accountinfo)):
        temp[accountinfo[k][0]] = float(round((accountinfo[k][1]/accountinfo[k-1][1] - 1)*100,3))
    InfoSeri.rate = temp
    
    dailyreturn = list(InfoSeri.rate.values())    
    InfoSeri.mean = np.mean(dailyreturn)
    InfoSeri.var = np.var(dailyreturn)
    InfoSeri.std = np.std(dailyreturn)

    temp ={}
    for k in accountinfo:
        temp[k[0]] = round((k[1]/capital-1)*100 ,3)
    InfoSeri.culrate = temp
        
    InfoSeri.annualizedreturns = round((math.pow((accountinfo[-1][1]/capital),250/len(accountinfo)) - 1) * 100,2)
    
    temp3 = []
    temp4 = []
    covdata = []
    for j in InfoSeri.rate:
        temp3.append(float(InfoSeri.rate[j]))
        temp4.append(float(Benchmark.dailyreturn[j]))
    covdata.append(temp3)
    covdata.append(temp4)
    temp6 = np.cov(covdata)
    InfoSeri.cov = temp6[0][1]
    
    InfoSeri.beta = InfoSeri.cov/float(Benchmark.var)
        
    temp = []
    accountvalues = []
    for k in range(0,len(accountinfo)):
        accountvalues.append(accountinfo[k][1])  
   
    for i in range(1,len(accountinfo)):
        temp1 = accountvalues[0:i]
        temp.append(round((1-accountinfo[i][1]/max(temp1))*100,2))
    InfoSeri.maxdown = max(temp)
    
    temp5 = 0
    for i in InfoSeri.rate:
        temp5 += math.pow((InfoSeri.rate[i] - InfoSeri.mean)/100,2)
    InfoSeri.volatility = math.pow(temp5/(len(InfoSeri.rate)-1),0.5)*100

    InfoSeri.sharp = (InfoSeri.annualizedreturns-rf)/InfoSeri.volatility
    
    InfoSeri.alpha = InfoSeri.annualizedreturns - rf - InfoSeri.beta*(Benchmark.annualizedreturns - rf) 

def formatdrw(dnary):
    temp = [(k,dnary[k]) for k in sorted(dnary.keys())] 
    temp1 = []
    for i in temp:
        temp1.append(i[1]) 
    return temp1

def drw():
    font = matplotlib.font_manager.FontProperties(fname=r"c:\windows\fonts\msyh.ttf", size=13)
    x = sorted(list(InfoSeri.culrate)) 
    days = int(len(x)*0.2)    
    portfolio = formatdrw(InfoSeri.culrate)
    bench = formatdrw(Benchmark.culreturn)  
    plt.figure(figsize=(12,6.75))
    portfolioline, = plt.plot(x,portfolio,label="$Portfolio$",color="red",linewidth=2,linestyle='-')
    benchline,  = plt.plot(x,bench,label="$Benchmark$",color="blue",linewidth=2,linestyle='-')
    noteslabel =  '年化收益：' + str(InfoSeri.annualizedreturns) +'%    ' + '最大回撤：'+ str(InfoSeri.maxdown) +'%    '+ '基准年化：'+ str(Benchmark.annualizedreturns) +'%    '+ '收益波动：'+ str(round(InfoSeri.volatility,2)) +'%    '
    noteslabel2 = '夏普比率：'+ str(round(InfoSeri.sharp,2))+ '    阿尔法：'+ str(round(InfoSeri.alpha,2))+ '    贝塔：'+ str(round(InfoSeri.beta,2))
#     plt.xlabel("$Date$",fontsize='large')    
    plt.title("$Cumulative  Return(\%)$",fontsize='large')
#     plt.title(u'累计收益率(%)', fontproperties=font)
    plt.ylabel("$Return Rate(\%)$",fontsize='large')
    maxtemp = 25 * (int(max(max(InfoSeri.culrate.values()),max(Benchmark.culreturn.values()))/25)+2)
    mintemp = 25 * (int(min(min(InfoSeri.culrate.values()),min(Benchmark.culreturn.values()))/25)-1)
    plt.text(min(x)+dt.timedelta(days=days), maxtemp*0.7, noteslabel,fontproperties=font, ha='left', va='top')
    plt.text(min(x)+dt.timedelta(days=days), maxtemp*0.6, noteslabel2,fontproperties=font, ha='left', va='top')
    plt.ylim(mintemp,maxtemp)
    plt.legend(handles=[portfolioline,benchline], loc=2,borderaxespad=0.)
    plt.show()

def savedata():
    
    pass
    
if __name__ == "__main__":
    account = Account()
    Initialize(account)
    calbenchmark(start,end,benchmark)
    strategygo(start,end)
    getreturn(accountinfo)
    drw()
#     print(accountinfo)
#     savedata()
