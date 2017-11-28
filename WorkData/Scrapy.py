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
import pymssql
import logging as log
import re
import http.cookiejar as cookielib
import xml.dom.minidom
import requests
from lxml import etree
import os

import gevent
from gevent import monkey, pool; monkey.patch_all()
import time
from xml.dom.minidom import parse
import xml.dom.minidom



log.basicConfig(
    level=log.DEBUG,
    format="%(levelname)s: %(message)s"
)

starttime = time.time()

log.info(starttime)