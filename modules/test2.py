# -*- coding: utf-8 -*-
"""
Created on Mon Sep 25 16:18:10 2017

@author: tguo
"""
stk_order = {}
num_shares = 0 
stock_return = {'t1': 1.0111,'t2':0.998,'t3':1.0234}
stock_return = sorted(stock_return.items(), key=lambda items:items[1],reverse=True)
for i in range(0,len(stock_return)):
    if stock_return[i][1] >= stock_return[0][1] :
        stk_order[str(stock_return[i][0])] = 1
    else:
        stk_order[str(stock_return[i][0])] = -1
        
for key in stk_order:
    print(key)
    print(type(key))