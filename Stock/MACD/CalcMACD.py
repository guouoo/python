import talib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# def myMACD(price, fastperiod, slowperiod, signalperiod):
#     ewma12 = pd.ewma(price,span=fastperiod)
#     ewma60 = pd.ewma(price,span=slowperiod)
#     dif = ewma12-ewma60
#     dea = pd.ewma(dif,span=signalperiod)
#     bar = (dif-dea) #有些地方的bar = (dif-dea)*2，但是talib中MACD的计算是bar = (dif-dea)*1
#     return dif,dea,bar

def calcMACD(setting,data):

# print(dates.sort_values(axis=0, by=['Return_20days'], ascending=False))
    temp = np.array(data)
    temp_index = temp[:,0]
    temp_data = np.array(temp[:,1:],dtype='f8')
    df =  pd.DataFrame(temp_data,index=temp_index ,columns = ['open','high','low','close'])
    macd, signal, hist = talib.MACD(df['close'].values, fastperiod=setting['short'], slowperiod=setting['long'], signalperiod=setting['m'])

    plt.figure(figsize=[12,5])
    plt.plot(df.index,macd,label='DIF',color="red")
    plt.plot(df.index,signal,label='DEA',color="blue")
    plt.axhline(y=0,color='black',linewidth=1.5)
    plt.plot(df.index,hist,label='MACD',color="green")
    plt.bar(df.index,hist, width=0.1,align = 'center',color="green")
    plt.legend(loc='best')
    plt.show()