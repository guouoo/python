'''
Created on Sep 4, 2015

@author: tguo
'''

# coding=UTF-8
import re
import urllib.request
import random

print('Downloading is started...')
 
pathfile = open('D:\src\path.txt', mode='r', encoding=None, errors=None, newline=None, closefd=True, opener=None)
 
urls=pathfile.readlines()


for url in urls:
    try:
        filename = re.sub('http.*/','',url).replace('?','a').replace('.jpg','').replace('.gif','')
        filetype = re.sub('http.*\.','',url)
        filename = filename.strip()
        filetype = filetype.strip()
        num = str(random.sample(range(1,99),1)).replace('[','').replace(']','')
        local = 'D:\\src\\pics\\'+filename+'_'+ num + '.'+ filetype
        local = local.strip()
#         print(local)
        urllib.request.urlretrieve(url, local)
        print(local + ' S.')
    except:
        print(local + '      F.')
    
pathfile.close()
