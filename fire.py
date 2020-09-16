#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 15:52:07 2020

@author: logic
"""
def cal_dis(city_loc):
    global city_num
    #城市距离矩阵
    city_dis=np.zeros([city_num,city_num],dtype=float)
    for i in range(city_num):
        for j in range(city_num):
            city_dis[i,j]=(((city_loc[i,0]-city_loc[j,0])**2+(city_loc[i,1]-city_loc[j,1])**2))**0.5
            if i==j:
                city_dis[i,i]=0.000001
    return city_dis
#生成初始随机路线
def randompath():
    global city_num
    randompath=(np.random.permutation(np.arange(city_num))).tolist()
    randompath.append(randompath[0])
    return randompath
#计算路线之间长度
def compare(path1,path2):   
    global city_dis         
    pathlength1=0
    pathlength2=0
    global city_num
    for i in range(city_num):
        pathlength1=pathlength1+city_dis[path1[i],path1[i+1]]
        pathlength2=pathlength2+city_dis[path2[i],path2[i+1]]
    return pathlength1,pathlength2

#计算选择路线
def cal_prob(path1,path2,t):
    pathlength1,pathlength2=compare(path1,path2)
#   新解更优一定取，新解不优看概率取
    if pathlength1>=pathlength2:
        return path2
    else:
        prob=math.e**(-(pathlength2-pathlength1)/t)
        shaizi=random.random()
        if shaizi<prob:
            return path2
        else:
            return path1
#二变换法，基于path1生成新path2
def generate(path1):
    path2=path1.copy()
    a=random.randint(0,len(path1)-1)       
    b=random.randint(0,len(path1)-1)
    while a==b:
        b=random.randint(0,len(path1)-1)
    temp=path2[a]
    path2[a]=path2[b]
    path2[b]=temp
    return path2
         
#每代改变温度
def change_temp(t,it):
    global q
    return t*q

if __name__=="__main__":
    import numpy as np
    import math
    import random
#    city_num=10
#    city_loc=np.zeros([city_num,2],dtype=float)
#    for i in range(city_num):
#        city_loc[i,0]=random.uniform(1,city_num**2)
#        city_loc[i,1]=random.uniform(1,city_num**2)
    ###用已知数据跑一下
    import pandas as pd
    data=pd.read_table("data.txt",sep=' ')
    data=data.drop(columns="num")
    city_loc=data.values
    city_num=np.shape(city_loc)[0]

    
    #定义相关参数
    t0=1e5
    tend=1e-10
    #降温代数
    it_total=500
    q=0.95
    #每代迭代次数
    change=1000
    
    ####开始计算
    city_dis=cal_dis(city_loc)
    t=t0
    record=[]
    temp_record=[]
    path1=randompath()
    for it in range(it_total):
        for c in range(change):
            path2=generate(path1)
            path1=cal_prob(path1,path2,t)
        t=change_temp(t,it)
        temp_record.append(t)
        pathlength1,pathlength2=compare(path1,path2)
        record.append(pathlength1)
        #打印每一代的最优解
        print(it,pathlength1)
    #打印
    final_path=path1
    print(final_path)
    print(pathlength1)
    import matplotlib.pyplot as plt
    plt.plot(np.arange(it_total),record)
    plt.show()
    plt.plot(np.arange(it_total),temp_record)
    #最优解是10628,我这个36460
    #这个算法如何调整好的退火温度方程很关键，如果温度下降慢了，可能不收敛，如果温度下降的够快，又无法探索到足够好的解
    #除此之外，调整方法还可以是减少代数，增加每一代的探索次数但是我这样也只搞到了335966
    
        
            
            
    
    