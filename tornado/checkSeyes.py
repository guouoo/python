'''
Created on Dec 7, 2015

@author: tguo
'''

# coding=UTF-8

import urllib.request
from bs4 import BeautifulSoup

headers = {'User-Agent' : 'Mozilla/10 (compatible; MSIE 1.0; Windows NT 5.0)'}
url = 'http://www.seyes.cn/vision'
try:            
    request = urllib.request.Request(url,headers = headers)
    response = urllib.request.urlopen(request)
    soup = BeautifulSoup(response, 'html.parser').find('title')
    if '界文 – 视界' in soup:
        print('Connecting is successful.')
    else:
        print('Connecting fails!')
    
except Exception as e:
    print(e)
    print('Connecting fails by error!')