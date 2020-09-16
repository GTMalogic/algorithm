#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 14 16:10:16 2020

@author: logic
"""
import numpy as np
import random
#提供初始化矩阵
def init(city_loc):
    global city_num,ant_num
    #城市距离矩阵
    city_dis=np.zeros([city_num,city_num],dtype=float)
    for i in range(city_num):
        for j in range(city_num):
            city_dis[i,j]=(((city_loc[i,0]-city_loc[j,0])**2+(city_loc[i,1]-city_loc[j,1])**2))**0.5
            if i==j:
                city_dis[i,i]=0.000001
    #信息素矩阵，记录的是[i,j]i到j这条路径上的信息
    tau=np.zeros([city_num,city_num],dtype=float)
    for i in range(city_num):
        for j in range(city_num):
            tau[i,j]=0.00001
            
    #路径矩阵,记录每只蚂蚁在本次迭代到过哪些地方，不断初始化
    table=np.zeros([ant_num,city_num],dtype=int)
    for i in range(ant_num):
        for j in range(city_num):
            table[i,j]=-1
    return tau,table,city_dis

#第一个阶段，给所有蚂蚁随机选择出发位置
def start():
    global city_num,ant_num
    ant=np.random.randint(0,city_num,ant_num)
    global table
    table[:,0]=ant
 
#该函数用于基于信息素浓度及过往信息,给位于k城的l号蚂蚁选择下一步落脚点
def next_step(k,l):
    global table,city_dis,alpsha,beta,rho,ant_num,city_num
    #先基于轨迹矩阵算出l蚂蚁没去过哪些地方
    unarrived=[]
    for i in range(city_num):
        if i not in table[l,:]:
            unarrived.append(int(i))
    #结合他没去过哪。以及信息素矩阵，计算在k城的他选择下一个城市的概率,probability[i]就是他从k到i的概率,然后进一步提升为概率划分
    #即0.1,0,0.5,0.4-----0.1,0.1,0.6,1
    probability=[0]*city_num
    total=0
    for i in unarrived:
        total=total+(tau[k,i]**alpha)/(city_dis[k,i]**beta)
    for i in unarrived:
        probability[i]=((tau[k,i]**alpha)/(city_dis[k,i]**beta))/total
    probability2=[0]*city_num
    for i in range(city_num):
        probability2[i]=sum(probability[0:i+1])

    #选择去哪
    shaizi=random.random()
    for i in range(city_num):
        if shaizi <= probability2[i]:
            break
    #此时序号i就是下一个去往的城市
    table[l,city_num-len(unarrived)]=i
#该函数用于每一圈迭代后，修改信息素列表
def update_tau():
    global tau,Q,table,ant_num,city_num,rho
    ant_length=[0]*ant_num
    #计算每个蚂蚁行进的总路程
    for k in range(ant_num):
        for i in range(city_num-1):
            ant_length[k]=ant_length[k]+city_dis[table[k,i],table[k,i+1]]
        ant_length[k]=ant_length[k]+city_dis[table[k,city_num-1],table[k,0]]
    #修改每一个位置上的信息素浓度
    for i in range(city_num):
        for j in range(city_num):
            #先整体挥发
            tau[i,j]=(1-rho)*tau[i,j]
            for k in range(ant_num):
                #如果[i,j]这条路k蚂蚁去过，那么才留下信息素,否则不修改信息素矩阵
                if (np.argwhere(table[k,:]==i)-np.argwhere(table[k,:]==j))==-1:
                    tau[i,j]=tau[i,j]+Q/ant_length[k]
                elif np.argwhere(table[k,:]==i)==city_num-1 and np.argwhere(table[k,:]==j)==0:
                    tau[i,j]=tau[i,j]+Q/ant_length[k]                    
#清空上一次迭代
def cleaning():
    global table,ant_num,city_num
    table=np.zeros([ant_num,city_num],dtype=int)
    for i in range(ant_num):
        for j in range(city_num):
            table[i,j]=-1      
def calculate_result():
    global city_num,tau,city_dis
    order=[0]
    i=0
    temp=[]
    #填充路径列表
    while len(order)<=city_num: 
        temp=tau[i,:].copy()
        for j in range(city_num):
            if j in order:
                temp[j]=0
        order.append((temp.tolist()).index(max(temp.tolist())))
        i=order[-1]
    #输出最小距离
    mini_dis=0
    for i in range(city_num-1):
        mini_dis=mini_dis+city_dis[order[i],order[i+1]]
    mini_dis=mini_dis+city_dis[order[city_num-1],order[0]]
    return order,mini_dis
    
if __name__=="__main__":
    #城市最短路线的蚁群算法问题

    #相关参数
    #挥发速度
    rho=0.2
    #信息素、路径信息重要程度
    alpha=2
    beta=2
    #常参数Q
    Q=0.01
    #迭代代数
    it_total=250
    #先是一个城市坐标信息
    #随机创建数据
#    城市、蚁群数量
#    ant_num=20
#    city_num=10
#    city_loc=np.zeros([city_num,2],dtype=float)
#    for i in range(city_num):
#        city_loc[i,0]=random.uniform(1,city_num**2)
#        city_loc[i,1]=random.uniform(1,city_num**2)
    ##用已知数据跑一下
    import pandas as pd
    data=pd.read_table("data.txt",sep=' ')
    data=data.drop(columns="num")
    city_loc=data.values
    city_num=np.shape(city_loc)[0]
    ant_num=10*city_num  
    
    
    #####开始具体计算

    tau,table,city_dis=init(city_loc)
    result=[]
    #每一次迭代
    for it in range(it_total):
        start()
        #每一步
        for l in range(ant_num):
            for i in range(city_num-1):
            #第i步的时候，l蚂蚁在table[l,i]
                next_step(table[l,i],l)
        update_tau()
        #记录最小路线
        order,mini_dis=calculate_result()
        result.append(mini_dis)
        cleaning()
        print(order,mini_dis)
    #####打印一下
    #print(tau)
    print(result,order)
    import matplotlib.pyplot as plt
    plt.plot(np.arange(it_total),result)
    #用的是att48的数据，最优是10628，我这个跑出来是43259

    
    
        
        

                
                
            
            
    
    
    
    
    
    
    
    
    