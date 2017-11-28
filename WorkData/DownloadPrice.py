import pymssql
import logging as log
import re
import urllib.request
import requests
from lxml import etree
import os
import gevent
from gevent import monkey, pool; monkey.patch_all()
import time
import xml.dom.minidom

path = 'c:/temp2/'

# BASE_DIR = os.path.dirname(__file__)
LOG_PATH = path +'logs/'
LOG_FILENAME = str(time.strftime('%Y%m%d_%H%M%S',time.localtime(time.time()))) + '.log'
log.basicConfig(
    filename = LOG_PATH + LOG_FILENAME,
    level=log.INFO,
    # format="[%(asctime)s] %(name)s:%(levelname)s: %(message)s"
    format="%(levelname)s: %(message)s"
)


Historylist = open('list2', mode='r', encoding=None, errors=None, newline=None, closefd=True, opener=None)
symbol = Historylist.readlines()

user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = {'user_agent': user_agent}

def DownLoadPrice():
    log.info('-' * 6 + 'Start to download price historical data to xml files...')
    urls={}
    p = pool.Pool(10)
    for i in range(0, len(symbol)):
        urls[symbol[i]]='http://internal-stg-exoi-527127491.us-east-1.elb.amazonaws.com/XOI/Price?Package=HistoricalData&ContentType=MarketPrice&IdType=PerformanceId&Id=' + str(symbol[i].strip())
    threads=[p.spawn(DownLoadPrice, urls[key], key.strip()) for key in urls]
    gevent.joinall(threads)

def DownLoadPrice(url,symbol):
    try:
        request = requests.get(url, allow_redirects=False, timeout=2.0, headers=headers)
        response = request.content
        saveName = path + str(symbol.strip()) + '.xml'
        # content = response.read().decode("utf-8").replace('<OpenPrice>NaN</OpenPrice>','').replace('<HighPrice>NaN</HighPrice>','').replace('<LowPrice>NaN</LowPrice>','').replace('<Volume>NaN</Volume>','')
        content = response.decode("utf-8")  # .replace('>NaN</','></')

        with open(saveName, "wt") as code:
            code.write(content)
            log.info(saveName + ' is dowloaded.')
    except request.status_code as e:
        print(e)

def DownLoadXoiPrice():
    log.info('-' * 6 + 'Start to download price xoi data...')
    openCookies=open(r'cookies.txt','r') # 打开所保存的cookies内容文件
    cookies={} # 初始化cookies字典变量
    periods = ['1968,1969,1970,1971,1972,1973,1974,1975,1976,1977','1978,1979,1980,1981,1982,1983,1984,1985,1986,1987','1988,1989,1990,1991,1992,1993,1994,1995,1996,1997','1998,1999,2000,2001,2002,2003,2004,2005,2006,2007','2008,2009,2010,2011,2012,2013,2014,2015,2016,2017']
    for line in openCookies.read().split(';'):  # 按照字符：进行划分读取
        name, value = line.strip().split('=', 1)  # 其设置为1就会把字符串拆分成2份
        cookies[name] = value  # 为字典cookies添加内容

    for i in range(0,len(symbol)):
        for j in range(0,len(periods)):
            url = 'http://price.xoi.morningstar.com/DataPlatform/DataOutput.aspx?Package=HistoricalData&ContentType=MarketPrice&IdType=PerformanceId&Id=' + str(symbol[i].strip())+ '&Dates=' + periods[j]
            try:
                request=requests.get(url,cookies=cookies)
                response =request.content
                if request.status_code == 404:
                    continue
                saveName = path + 'PriceXOI/'+ str(symbol[i].strip()) + '_' + str(j+1) + '.xml'
                with open(saveName, "wb") as code:
                    code.write(response)

            except request.status_code as e:
                print(e)
        log.info(str(i + 1) + '/' + str(len(symbol)) + ': ' + str(symbol[i].strip())  + ' from XOI is dowloaded.')

def SchemaValidate():
    log.info('-' * 6 + 'Start to get validate xml schema...')
    with open('schema.xsd', 'rb' ) as f:
        schema_root = etree.XML(f.read())

    schema = etree.XMLSchema(schema_root)
    xmlparser = etree.XMLParser(schema=schema)
    for filename in os.listdir(path):
        if 'xml' in filename:
            files = path + filename
            log.info('******Start to check '+ files+ '......')
            with open(files, 'rb') as f:
                try:
                    etree.fromstring(f.read(), xmlparser)
                    log.info(files + ' validates')

                except etree.XMLSchemaError as e:
                    log.info(e)

def CheckEOD():
    log.info('-' * 6 + 'Start to get EOD data...')
    urls={}
    p = pool.Pool(10)
    for i in range(0, len(symbol)):
        urls[symbol[i]]='http://internal-stg-exoi-527127491.us-east-1.elb.amazonaws.com/XOI/Price?Package=Snapshot&ContentType=MarketPerformance&IdType=PerformanceId&Id=' + str(symbol[i].strip())
    threads=[p.spawn(RequestEOD, urls[key], key.strip(),'PriceDetail') for key in urls]
    gevent.joinall(threads)

def RequestEOD(url,symbol,tagName):
    try:
        request = requests.get(url, allow_redirects=False, timeout=2.0, headers=headers)
        response = request.content.decode("utf-8")#.decode("utf-8").replace('\n', '')
        DOMTree = xml.dom.minidom.parseString(response)
        Data = DOMTree.documentElement
        PriceData = Data.getElementsByTagName(tagName)
        EODData = symbol + ':'
        for NodeList in PriceData:
            for DataList in NodeList.childNodes:
                EODData = EODData + DataList.nodeName + '='
                for value in DataList.childNodes:
                    EODData = EODData + value.data + ' '

        log.info(EODData)
    except Exception as e:
        log.info(e)

def CheckPriceCurrencyChange():
    log.info('-' * 6 + 'Start to get price currency history data...')
    urls={}
    p = pool.Pool(10)
    for i in range(0, len(symbol)):
        urls[symbol[i]]='http://internal-stg-exoi-527127491.us-east-1.elb.amazonaws.com/XOI/Price?Package=HistoricalData&ContentType=MarketPriceCurrencyHistory&IdType=PerformanceId&Id=' + str(symbol[i].strip())
    threads=[p.spawn(RequestEOD, urls[key], key.strip(),'MarketPriceCurrencyDetail') for key in urls]
    gevent.joinall(threads)

starttime = time.time()

# DownLoadPrice()
# SchemaValidate()
# DownLoadXoiPrice()
CheckEOD()
# CheckPriceCurrencyChange()
log.info( '-' * 6 + 'End, time cost: ' + str(time.time() - starttime) + 's.')