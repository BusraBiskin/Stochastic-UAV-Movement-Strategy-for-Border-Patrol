# -*- coding: utf-8 -*-
"""
Created on Wed May 18 11:17:39 2022

@author: bb2r20
"""

"Statistics for Probability Vector"
import numpy as np
import math
import random

import copy

from UAV_Movement_Function import UAV_Movement


def Statistics_of_Simulation(X_ref, number_of_runs,l, h, max_number_of_steps,radius):
   
    M = copy.deepcopy(X_ref)
    
    Trials = []
    Success = []

    for j in range(number_of_runs):
        
         #UAV starting location
         u = [0, 0]
         v = [5, 5]
            
         D = 0
         t = 0
            
         while D < 1 and t < max_number_of_steps :
          
             u = UAV_Movement(u, M, l, h)
             
             t = t + 1
            
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
    
    result = [ET, SD, PoS]
    result = [10000 if np.isnan(x) else x for x in result]
                        
    return result         
