'''
Created on Dec 31, 2015

@author: tguo
'''

# coding=UTF-8


dict = [{'id':'4','name':'b'},{'id':'6','name':'c'}, {'id':'3','name':'a'},{'id':'1','name':'g'},{'id':'8','name':'f'}]  
  
dict.sort(lambda x,y: cmp(x['id'], y['id']))    
dict = sorted(dict, key=lambda x:x['id'])  

print(dict)