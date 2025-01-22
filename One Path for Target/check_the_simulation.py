#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 15:21:14 2024

@author: busrabiskin
"""
import numpy as np
import math
from statistics import mean

from UAV_Movement_Function import UAV_Movement
number_of_runs= 10000000
l=56 
h=61 
max_number_of_steps = 13
radius=2
PoS_matrix = []
M = [0, 0.304, 0, 0.696]


Trials = []
Success = []
    
for j in range(number_of_runs):
            
    #UAV starting location
    u = [5, 0]
    v = [10, 10]
                
    D = 0
    t = 0
                
    while D < 1 and t < max_number_of_steps :
              
        u = UAV_Movement(u, M, l, h)
                 
        t = t + 1
        
        #if(u == v):
        #    D = 1
                
        #find the distance between target's position and UAV  
        geo_dist =  math.dist(u, v)
        
                     
        if  (geo_dist <= radius) :
            D = 1
         
         
                                                                                    
    if D == 1 :
        Success.append(1)
        Trials.append(t)
    else:
        Success.append(0)
        Trials.append(10000)
                
                
if Trials.count(10000) > 0 :
    Trials = list(filter(lambda x: x != 10000, Trials))
                
ET = np.average(Trials)
SD = np.std(Trials)        
NS = sum(Success)
PoS = NS / number_of_runs #proportion of success

    
    