# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 15:32:57 2017

@author: tguo
"""

'''
matplotlib雷达图
'''
import numpy as np
import matplotlib.pyplot as plt


# 雷达图
def plot_radar(labels, data, score):
    '''
    用法：
    >>> labels = np.array(['艺术A','调研I','实际R','常规C','企业E','社会S']) #标签
    >>> data = np.array([1,4,3,6,4,8]) # 数据
    >>> score = 10 # 表明数据是“十分制”。其可选的选项有1分制、5分制、10分制、100分制
        
    >>> plot_radar(labels, data, score) # 画雷达图
    '''
    n = len(labels)
    
    # 转化为十分制！！！
    if score in [5, 10, 100]:
        data = data * 10/score
    elif score == 1:
        data = data * 10
    
    angles = np.linspace(0 + np.pi/2, 2*np.pi + np.pi/2, n, endpoint=False) # 旋转90度，从正上方开始！
    
    data = np.concatenate((data, [data[0]])) # 闭合
    angles = np.concatenate((angles, [angles[0]])) # 闭合
    
    
    fig = plt.figure()
    ax = fig.add_subplot(111, polar=True)# 参数polar，表示极坐标！！
    
    # 自己画grid线（5条环形线）
    for i in [2,4,6,8,10]:
        ax.plot(angles, [i]*(n+1), 'b-',lw=0.5) # 之所以 n +1，是因为要闭合！
    
     # 填充底色
    ax.fill(angles, [10]*(n+1), facecolor='g', alpha=0.5)

    # 自己画grid线（6条半径线）
    for i in range(n):
        ax.plot([angles[i], angles[i]], [0, 10], 'b-',lw=0.5)
        
    
    # 画线
    ax.plot(angles, data, 'bo-', linewidth=2)
    
    # 填充
    #ax.fill(angles, data, facecolor='r', alpha=0.25)
    ax.fill(angles, data, facecolor='r')
    
    
    ax.set_thetagrids(angles * 180/np.pi, labels, fontproperties="SimHei")
    ax.set_title("matplotlib雷达图", va='bottom', fontproperties="SimHei")
    ax.set_rlim(0,10)

    # 下两行去掉所有默认的grid线
    ax.spines['polar'].set_visible(False) # 去掉最外围的黑圈
    ax.grid(False)                        # 去掉中间的黑圈

    # 关闭数值刻度
    ax.set_yticks([])


    plt.show()



# 测试
if __name__ == '__main__':
    
    labels = np.array(['艺术A','调研I','实际R','常规C','企业E','社会S']) #标签
    
    data = np.array([1,4,3,6,4,8]) # 数据
    
    score = 10 # 表明数据是“十分制”。其可选的选项有1分制、5分制、10分制、100分制
    
    
    # 画雷达图
    plot_radar(labels, data, score)