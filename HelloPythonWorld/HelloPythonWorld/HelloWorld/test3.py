# import re;
import decimal
# import time;
# import datetime;
# if(__name__=="__main__"):
#  #today=int(time.strftime("%w"));
# 
#  anyday=datetime.datetime(2012,2,15).strftime("%w");
#  print (anyday)


# a =['a','b']
# b = str(a).replace('[','(').replace(']',')')
# print(a)
# print(b)
# 
# list =['a','aa','aaab','aaaa','cca']
# for str in list:
#     if str.startswith('a'):
#         print ("found it!",str)
 
# test ='[<td>2015-09-10</td>, <td class="tor bold">0.6670</td>, <td class="tor bold">0.6670</td>, <td class="tor bold grn">-1.77%</td>, <td>开放申购</td>, <td>开放赎回</td>, <td class="red unbold"></td>, <td>2015-09-09</td>, <td class="tor bold">0.6790</td>, <td class="tor bold">0.6790</td>, <td class="tor bold red">2.72%</td>, <td>开放申购</td>, <td>开放赎回</td>, <td class="red unbold"></td>, <td>2015-09-08</td>, <td class="tor bold">0.6610</td>, <td class="tor bold">0.6610</td>, <td class="tor bold bck"></td>, <td>开放申购</td>, <td>开放赎回</td>, <td class="red unbold"></td>, <td>2015-09-02</td>, <td class="tor bold">0.6590</td>, <td class="tor bold">0.6590</td>, <td class="tor bold grn">-0.75%</td>, <td>开放申购</td>, <td>开放赎回</td>, <td class="red unbold"></td>, <td>2015-09-01</td>, <td class="tor bold">0.6640</td>, <td class="tor bold">0.6640</td>, <td class="tor bold bck"></td>, <td>开放申购</td>, <td>开放赎回</td>, <td class="red unbold"></td>, <td>2015-08-28</td>, <td class="tor bold">0.6870</td>, <td class="tor bold">0.6870</td>, <td class="tor bold grn">-0.87%</td>, <td>开放申购</td>, <td>开放赎回</td>, <td class="red unbold"></td>, <td>2015-08-27</td>, <td class="tor bold">0.6930</td>, <td class="tor bold">0.6930</td>, <td class="tor bold red">4.37%</td>, <td>开放申购</td>, <td>开放赎回</td>, <td class="red unbold"></td>, <td>2015-08-26</td>, <td class="tor bold">0.6640</td>, <td class="tor bold">0.6640</td>, <td class="tor bold bck">0.00%</td>, <td>开放申购</td>, <td>开放赎回</td>, <td class="red unbold"></td>, <td>2015-08-25</td>, <td class="tor bold">0.6640</td>, <td class="tor bold">0.6640</td>, <td class="tor bold red">0.91%</td>, <td>开放申购</td>, <td>开放赎回</td>, <td class="red unbold"></td>, <td>2015-08-24</td>, <td class="tor bold">0.6580</td>, <td class="tor bold">0.6580</td>, <td class="tor bold grn">-5.32%</td>, <td>开放申购</td>, <td>开放赎回</td>, <td class="red unbold"></td>]'
# LofTemp2 = re.sub(r'</?td.*?>','',test)
# print(LofTemp2) 
# print(LofTemp2.replace('[','').replace(']','').split(','))

import urllib.request
import re
from decimal import Decimal
import numpy


# import time,datetime
# 
# time_original = '17/Sep/2012:11:40:00'
# time_format = datetime.datetime.strptime(time_original, '%d/%b/%Y:%H:%M:%S‘）
# #这里可以 print time_format 或者 直接 time_format 一下看看输出结果，默认存储为datetime格式
# time_format = time_format.strftime('%Y%m%d%H%M%S')
# print (time_format)
# 
# test = {'000345':223}
# print(test.keys())
# 
# list = [1,2,2,3,3,43,4,45,1,1,1,23,3,4,2,12]
# a = max(1,2,3,3,4,5,6,7,2,1,1,0)
# b= [Decimal('999001.435708'), Decimal('1026966.163708'), Decimal('1031533.264708'), Decimal('1040582.194708'), Decimal('1014773.389708'), Decimal('1002730.963708'), Decimal('1022214.493708'), Decimal('1037838.904708'), Decimal('1049225.521708'), Decimal('1072296.085708'), Decimal('1109256.448708')]
# print(b)

# headers = {'User-Agent' : 'Mozilla/12 (compatible; MSIE 1.0; Windows NT 4.0)'}
# codes = '399102'
# url2 = 'http://qt.gtimg.cn/q=s_sz'+codes
# try:            
#     request = urllib.request.Request(url2,headers = headers)
#     response = urllib.request.urlopen(request).read().decode('gbk')
#     reobj= re.compile('v_s_sz.*?~.*?~')
#     realtemp = reobj.sub('',response).replace('~~";','').replace('\n','~').strip().split('~')
#     dictprice ={}
#     for i in range(0,len(realtemp)-1,6):
#         dictprice[realtemp[i]] = Decimal(realtemp[i+1])
#         
# except Exception as e:
#     print(e)
#     
# print(dictprice)
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import pandas as pd
ts = pd.Series(np.random.randn(1000), index=pd.date_range('1/1/2000', periods=1000))
ts = ts.cumsum()
ts.plot()

# list  =[1,2,3,4,5,6,7,8,9,0,1]
# print(numpy.mean(list))
# print(numpy.cov(list))
# print(numpy.std(list))
# print(numpy.median(list))
# 
# arry =[[12,13,10,9,20,7,4,22,15,23],[50,54,48,47,70,20,15,40,35,37]]
# arry2 = [[12,50],[13,54],[10,48],[9,47],[20,70],[7,20],[4,15],[22,40],[15,35],[23,37]]
# print(numpy.cov(arry))
# print(numpy.cov(arry2))



df = pd.DataFrame(np.random.randn(1000, 4), index=ts.index, columns=list('ABCD'))
df = df.cumsum()
plt.figure();  
df.plot();