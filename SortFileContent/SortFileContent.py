#-*- coding:utf-8 -*- 
'''
Created on Aug 19, 2015

@author: tguo
'''
import os

path = 'D:\\workspace\\sort\\'

filename=os.listdir(path)
print(filename)
for file in filename:
    f = open(path+file,'r')
    content = f.readlines()
    content.sort()
    f.close()    
    f = open(path+file,'w')
    for i in content:
        f.write(i)
    f.close
    