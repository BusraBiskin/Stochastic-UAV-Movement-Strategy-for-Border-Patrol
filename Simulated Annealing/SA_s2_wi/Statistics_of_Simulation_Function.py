# -*- coding: utf-8 -*-
"""
Created on Wed May 18 11:17:39 2022

@author: bb2r20
"""

"Statistics for Probability Vector"
import numpy as np
import pandas as pd
import random

import copy

from UAV_Movement_Function import UAV_Movement
#from GeoDistance import Geo_Dist


def Statistics_of_Simulation(X_ref, number_of_runs, ratio, l, h, max_number_of_steps, Dist_Matrix_1,Dist_Matrix_2,Dist_Matrix_3, radius):
   
    M = copy.deepcopy(X_ref)
    
    Trials = []
    Success = []
    path_choise = []

    
    for j in range(number_of_runs):
                
         #target chooses a path, randomly
         path = random.randint(0,2)
         path_choise.append(path)
         
         if path == 0:
             Dist_Matrix = Dist_Matrix_1
         elif path == 1:
             Dist_Matrix = Dist_Matrix_2
         else:
             Dist_Matrix = Dist_Matrix_3
               
            
         #UAV starting location
         u = [0, 0]
            
         D = 0  #shows if UAV detected the target
         t = 0  #counts time step
            
         while D < 1 and t < max_number_of_steps :
             
             "Signal Part"
             if t == 30 and (path == 0 or path == 1): 
                 
                 geo_dist = Dist_Matrix[u[1] * (h+1) + u[0], int(t/ratio)]
                 t += int(geo_dist/10)
                 
                 u = [48,26]
             
             if t <= 30:  #until n steps of move, UAV uses first set of probabilities
                 M_new = M[0:4]
             else:
                 M_new = M[4:8]  #after n steps of move, UAV changes set of probabilities

             u = UAV_Movement(u, M_new, l, h)
             t = t + 1
             
             #checking if UAV detected the target
             if D == 0:
                
                 #find the distance between target's position and UAV  
                 geo_dist = Dist_Matrix[ u[1] * (h+1) + u[0], int(t/ratio) ]
                 
                 if  (geo_dist <= radius) : #if it is in UAV's search coverage
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
    
    result = [ET, SD, PoS, path_choise.count(0),path_choise.count(1),path_choise.count(2)]
    result = [10000 if np.isnan(x) else x for x in result]
                        
    return result         
