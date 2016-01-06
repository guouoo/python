'''
Created on Nov 24, 2015

@author: tguo
'''

import random
# coding=UTF-8
import os
import sys
# print('''This is a multiple testing
# this is a multiple testing
# testing''')
# 
# print('''########################################''' +'\n' + 'table' + ' is updated to latest status.' +'\n' + '''########################################''')
# 
# a=5
# b=a
# print(b)
# print(id(a))
# print(id(b))
# b=6
# print(a)
# print(b)
# print(id(a))
# print(id(b))

# for k in range(0,10000):
#     for i in range(0,random.randint(1,7)):
#         print(str(2005+random.randint(0,11))+',',end='')
#     print('\n')

print(os.sys.path)

print ("path has", len(sys.path), "members")
sys.path.insert(0, "samples")  #将路径插入到path,[0]中

sys.path = []  #删除path中所有路径
import random 

def dump(module):
    print (module, "=>",)
    if module in sys.builtin_module_names:  #查找内建模块是否存在
        print ("<BUILTIN>")
    else:
        module = __import__(module)         #非内建模块输出模块路径
        print (module.__file__)
dump("os")
dump("sys")
# dump("string")
dump("strop")
dump("zlib")
