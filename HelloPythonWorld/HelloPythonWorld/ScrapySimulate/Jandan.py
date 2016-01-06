'''
Created on Jul 15, 2015
 
@author: tguo
'''

import urllib.request
import re
import random
from bs4 import BeautifulSoup
 
# user_agent = 'Mozilla/14.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)'
# headers = { 'User-Agent' : user_agent }
# Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)
# IE8 on Windows Vista 
# Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Trident/4.0) 
# IE8 on Windows Vista
# Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0) 
# IE8 on Windows 7
# Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)
# 64-bit IE on 64-bit Windows 7:
# Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Win64; x64; Trident/4.0) 
# 32-bit IE on 64-bit Windows 7:
# Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0)
 
for page in range (6999,8000):
    
    user_agent = 'Mozilla/'+str(random.randint(0,9))+'.'+str(random.randint(0,9))+' (compatible; MSIE 1.0; Windows NT 5.0)'
    headers = { 'User-Agent' : user_agent }
    url = 'http://jandan.net/pic/page-' + str(page)
    try:            
        request = urllib.request.Request(url,headers = headers)
        response = urllib.request.urlopen(request)
        soup = BeautifulSoup(response, 'html.parser')

        for link in soup.find_all('img'):
#             print(link)
            logfile = open('path.txt','a')
            if re.search('^(?!.*thumbnail).*(gif|jpg)',link.get('src')):
#               print(link.get('src'))
                logfile.write(str(page)+','+link.get('src')+'\n')
            if link.get('org_src') is not None:
#                print(link.get('org_src'))     
                 logfile.write(str(page)+','+link.get('org_src')+'\n')          
            logfile.close()
         
    except urllib.request.URLError as e:
        if hasattr(e,"code"):
            print (e.code)
        if hasattr(e,"reason"):
            print (e.reason)
            print(page)
            break
