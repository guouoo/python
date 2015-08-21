'''
Created on Jul 24, 2015

@author: tguo
'''
#this example can download the data in finance.yahoo and put in our computers  
  
import os
import urllib.request
  
ticker = '000651.SZ'           #the Ticker Symbol  
date1 = ( 1900, 1, 1 )    #begining time  
date2 = ( 2015, 11, 11 )  #ending time  
  
  
d1 = (date1[1]-1, date1[2], date1[0])  
      
d2 = (date2[1]-1, date2[2], date2[0])  
  
g='d'  
  
urlFmt = 'http://table.finance.yahoo.com/table.csv?a=%d&b=%d&c=%d&d=%d&e=%d&f=%d&s=%s&y=0&g=%s&ignore=.csv'  
url =  urlFmt % (d1[0], d1[1], d1[2],  
                     d2[0], d2[1], d2[2], ticker, g)  #the url of historical data  
print (url)
  
path = 'D:'
file_name = '\\ticker.csv'                #file name  
dest_dir = os.path.join(path,file_name)   #located file  
print ( dest_dir)
urllib.request.urlretrieve(url,dest_dir)        #download the data and put in located file