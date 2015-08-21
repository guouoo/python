'''
Created on Aug 12, 2015

@author: tguo
'''
'''
Created on Jul 15, 2015
 
@author: tguo
'''

import urllib.request
import re
 
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = { 'User-Agent' : user_agent }
 
for page in range (7099,7100):
    url = 'http://jandan.net/pic/page-' + str(page)
    try:
        request = urllib.request.Request(url,headers = headers)
        response = urllib.request.urlopen(request)
        content = response.read().decode('utf-8 ','ignore')
#       pattern = re.compile('<div.*?class="author">.*?<a.*?</a>.*?<a.*?>(.*?)</a>.*?<div.*?class="content">(.*?)</div>.*?<div.*?class="stats">.*?<span.*?>.*?<i.*?>(.*?)</i>(.*?)</span>',re.S)
        pattern = re.compile('<img src=".*?" /><',re.S)
        items = re.findall(pattern,content)
#         items = re.findall(pattern,items)
        print(items)
        for item in items:              
            item=item.replace('<div class="content">\n\n','')
            item=item.replace('<br/>',' ')
            item=item.replace('</div>','')
            replace_l=re.compile(r'(\n<!--.*?>\n\n)')
            replace_ll=replace_l.sub('',item +'\r')
            print(replace_ll)
#             logfile = open('test.txt','a')
#             logfile.write(replace_ll+'\n')
#             logfile.close()
#         
    except urllib.request.URLError as e:
        if hasattr(e,"code"):
            print (e.code)
        if hasattr(e,"reason"):
            print (e.reason)
