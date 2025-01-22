# -*- coding: utf-8 -*-
"""
Created on Wed May 18 11:17:39 2022

@author: bb2r20
"""

"Statistics for Probability Vector"
import numpy as np
import random

import copy

from UAV_Movement_Function import UAV_Movement


def Statistics_of_Simulation(X_ref, number_of_runs, ratio, l, h, max_number_of_steps, Dist_Matrix_1,Dist_Matrix_2,Dist_Matrix_3, radius, time_step):
   
    M = copy.deepcopy(X_ref)
  
    Trials = []
    Success = []
     
    for j in range(number_of_runs):
                     
         #target chooses a path, randomly
         path = random.randint(0,2)
         
         if path == 0:
             Dist_Matrix = Dist_Matrix_1
         elif path == 1:
             Dist_Matrix = Dist_Matrix_2
         else:
             Dist_Matrix = Dist_Matrix_3             
            
         #UAV starting location
         u = [0, 0]
            
         D = 0
         t = 0
            
         while D < 1 and t < (Dist_Matrix.shape[1]-1)*ratio :
          
             t += 1
             if t <= time_step:
                M_move = M[0:4]
             else:
                M_move = M[4:8]
                         
             u = UAV_Movement(u, M_move, l, h) #UAV makes a move  
            
             #find the distance between target's position and UAV

             geo_dist = Dist_Matrix[u[1] * (h+1) + u[0], int(t/ratio)]
              
             if  (geo_dist <= radius) :
                 D = 1
                                                                                
         if D == 1:
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
