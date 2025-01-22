# -*- coding: utf-8 -*-
"""
Created on Mon May 16 13:41:25 2022

@author: bb2r20
"""

"Statistics for Plural Probability Vectors"

import numpy as np
import random

import copy

from UAV_Movement_Function import UAV_Movement
#from GeoDistance import Geo_Dist


def Statistics_Plural(V, number_of_runs, n, ratio, l, h, max_number_of_steps,Dist_Matrix_1, Dist_Matrix_2, Dist_Matrix_3, radius):
    
    ET = []
    SD = []
    PoS = []
   
    result = np.zeros((n+1,3))

#loop for n starting solutions

    for i in range(n+1):
    
        
        Trials = []
        Success = []
      
       
        M = copy.deepcopy(V[i,])
        
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
            
            while D < 1 and t < (Dist_Matrix.shape[1]-1)*ratio:

                u = UAV_Movement(u, M, l, h) #UAV makes a move
                t += 1 # time step is increased by one
                                
                #find the distance between target's position and UAV  
                geo_dist = Dist_Matrix[u[1] * (h+1) + u[0], int(t/ratio)]
                    
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

      
        ET.append(np.average(Trials)) 
        SD.append(np.std(Trials)) 
        NS = sum(Success)
        PoS.append((NS / number_of_runs))  #proportion of success
    
        result[i,]=(ET[i], SD[i], PoS[i])
        result = np.where(np.isnan(result), 10000, result)
    
                        
    return result                 
                

                