__author__ = 'Jun Guo'
'''
Created on Jul 16, 2015

@author: tguo
'''
import urllib.request
import re
import time

class QSBK:
    def __init__(self):
        self.pageIndex=1
        self.user_agent ='Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        self.headers ={'User-Agent' : 'user_agent' }
        self.stories =[]
        self.enable =False
    
    def getPage(self,pageIndex):
        try:
            url= 'http://www.qiushibaike.com/hot/page/' + str(pageIndex)
            request = urllib.request (url,headers = self.headers)
            response = urllib.urlopen(request)
            pageCode = response.read().decode('utf-8')
            return pageCode
        
        except urllib.URLError as e:
            if hasattr(e,'reason'):
                print(u'Connect fails as', e.reason)
                return None
    
    def getPageItems(self,pageIndex):
        pageCode = self.getPage(pageIndex)
        if not pageCode:
            print('Page loading fails')
            return None
        pattern = re.compile('<div.*?class="author.*?>.*?<a.*?</a>.*?<a.*?>(.*?)</a>.*?<div.*?class'+
                         '="content".*?title="(.*?)">(.*?)</div>(.*?)<div class="stats.*?class="number">(.*?)</i>', re.S)
        items = re.findall(pattern,pageCode)
        for item in items:
            for item in items:
                haveImg = re.search("img",item[3])
                if not haveImg:
                    pageStories.append([item[0].strip(),item[1].strip(),item[2].strip(),item[4].strip()])
        return pageStories
            
    def loadPage(self):
        if self.enable == True:
            if len(self.stories) < 2:
                pageStories = self.getPageItems(self.pageIndex)
                if pageStories:
                    self.stories.append(pageStories)
                    self.pageIndex +=1
                    
    def getOneStory(self,pageStories,page):
        for story in pageStories:
            input = raw_input()
            self.loadPage()
            if input == 'Q':
                self.enable=False
                return
            print(page,story[0],story[1],story[2],story[3])
    
    def start(self):
        print('Loading... Enter for a new one and press Q to exit')    
        self.enable=True
        self.loadPage()
        nowPage =0
        while self.enable:
            if len(self.stories) > 0:
                pageStories =self.stories[0]
                nowPage += 1
                del self.stories[0]
                self.getOneStory(pageStories, nowPage)

spider = QSBK()
spider.start()    