'''
Created on Jul 15, 2015

@author: tguo
'''
# import urllib.request
#  
# request = urllib.request.Request("http://www.baidu.com")
# #  response= urllib.request.urlopen("http://pan.baidu.com/s/1sjMFHwD")
# response= urllib.request.urlopen("http://www.baidu.com")
#   
# print(response.read())

# import urllib.request
# 
# request = urllib.request.Request('http://www.xxxxxxxxxxxx.com')

# try:
#     urllib.request.urlopen(request)
# except urllib.request.URLError, e:
#     print(e.reason)

import urllib.request
import http.cookiejar


cookie = http.cookiejar.CookieJar()

handler=urllib.request.HTTPCookieProcessor(cookie)

opener = urllib.request.build_opener(handler)

response = opener.open('http://www.baidu.com')
for item in cookie:
    print ('Name = '+item.name)
    print ('Value = '+item.value)