# -*- coding: utf-8 -*-
"""
Created on Fri Nov 11 21:56:59 2016

@author: TH
Q1
.
"""

import random
import statistics

def coinToss():
    flip = random.randint(0, 1)
    if flip == 0:
        return 0
    else:
        return 1
        
#print(coinToss())
trial1 = []
trial2 = []
trial3 = []
trial4 = []
trial5 = []
trial6 = []
trial7 = []
trial8 = []
trial9 = []
trial10 = []

sum_v_1 = 0
sum_v_rand = 0
sum_v_min = 0

def random_toss():
    for i in range(1000):
        trial1.append(coinToss())
        trial2.append(coinToss())
        trial3.append(coinToss())
        trial4.append(coinToss())
        trial5.append(coinToss())
        trial6.append(coinToss())
        trial7.append(coinToss())
        trial8.append(coinToss())
        trial9.append(coinToss())
        trial10.append(coinToss())

def average(k):
    return (trial1[k]+trial2[k]+trial3[k]+trial4[k]+trial5[k]+trial6[k]+trial7[k]+trial8[k]+trial9[k]+trial10[k])/10
rotate_time = 10000
for exp in range(rotate_time):
    if exp % 1000 == 0:
        print(exp)
    # Clean trials
    trial1 = []
    trial2 = []
    trial3 = []
    trial4 = []
    trial5 = []
    trial6 = []
    trial7 = []
    trial8 = []
    trial9 = []
    trial10 = []
    random_toss()
    average_all = []
    for j in range(1000):
        average_all.append(average(j))
    
    #print(trial1[random.randint(1, 1000)])
    
    v_1 = average_all[0]
    v_rand = (trial1[random.randint(0, 999)]+trial2[random.randint(0, 999)]+trial3[random.randint(0, 999)]+trial4[random.randint(0, 999)]+trial5[random.randint(0, 999)]+trial6[random.randint(0, 999)]+trial7[random.randint(0, 999)]+trial8[random.randint(0, 999)]+trial9[random.randint(0, 999)]+trial10[random.randint(0, 999)])/10  
    v_min = min(average_all)
    sum_v_1 += v_1
    sum_v_rand += v_rand
    sum_v_min += v_min
    print(v_1, v_rand, v_min) 
print(sum_v_1/rotate_time, sum_v_rand/rotate_time, sum_v_min/rotate_time)