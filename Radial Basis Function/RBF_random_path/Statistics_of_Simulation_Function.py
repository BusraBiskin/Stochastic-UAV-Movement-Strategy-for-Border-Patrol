# -*- coding: utf-8 -*-
"""
Created on Wed May 18 11:17:39 2022

@author: bb2r20
"""

"Statistics for Probability Vector"
import numpy as np
import pandas as pd
import random
import math

import copy

from UAV_Movement_Function import UAV_Movement
from Target_Movement_Function import Target_Movement


def Statistics_of_Simulation(X_ref, T, number_of_runs, ratio, l, h, max_number_of_steps):
   
    M = copy.deepcopy(X_ref) 
    
    Trials = []
    Success = []
    signal = [28,30]

    for j in range(number_of_runs):
               
         #UAV starting location
         u = [0, 0]
         
         #target starting location
         tl = [l, random.randint(0, h)] 
            
         D = 0  #shows if UAV detected the target
         t = 0  #counts time step
            
         while D < 1 and t < max_number_of_steps and tl[0] != 0 :
           
             "Signal Part"
             if math.dist(tl,signal) < 2: 
                 
                 geo_dist = math.dist(tl,u)
                 t += int(geo_dist)
                 
                 if int(geo_dist > ratio):
                     for i in range(int(geo_dist / ratio)):
                         tl = Target_Movement(tl, T, l, h)                
                         
                 u = [28,30]
                 M_new = M[4:8]
                                  
             else:
                 M_new = M[0:4]
        
             u = UAV_Movement(u, M_new, l, h) #UAV makes a new move
             
             if t%10 == 0:
                 tl = Target_Movement(tl, T, l, h)
                 
             t = t + 1
        
             #find the distance between target's position and UAV  
             geo_dist = math.dist(tl,u)
                 
             if  (geo_dist <= 2) : #if it is in UAV's search coverage
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
    
    result = [ET, SD, PoS]
    result = [10000 if np.isnan(x) else x for x in result]
                        
    return result         
