# -*- coding: utf-8 -*-
"""
Created on Mon May 16 13:41:25 2022

@author: bb2r20
"""

"Statistics for Plural Probability Vectors"

import numpy as np
import math
import time
import random
import copy

from UAV_Movement_Function import UAV_Movement
#from GeoDistance import Geo_Dist


def Statistics_Plural(V, number_of_runs, n,l, h, max_number_of_steps,radius):
    
    ET = []
    SD = []
    PoS = []
   
    result = np.zeros((n+1,3))

#loop for n starting solutions

    for i in range(n+1):
    
        
        Trials = []
        Success = []
      
       
        M = copy.deepcopy(V[i,])
    
        start_time = time.time()
        
        for j in range(number_of_runs):
                
            #UAV starting location
            u = [0, 0]
            v = [5, 5]
            
            D = 0
            t = 0
            
            while D < 1 and t < max_number_of_steps :
                         
                u = UAV_Movement(u, M, l, h) #UAV makes a move
                
                t = t + 1 # time step is increased by one
                
                #find the distance between target's position and UAV  
                geo_dist = math.dist(u, v)
                    
                if  (geo_dist <= radius) :
                    D = 1
                                                                                
            if D == 1 :
                Success.append(1)
                Trials.append(t)
            else:
                Success.append(0)
                Trials.append(10000)
            
        print("--- %s seconds ---" % (time.time() - start_time))    
                
        if Trials.count(10000) > 0 :
            Trials = list(filter(lambda x: x != 10000, Trials))

      
        ET.append(np.average(Trials)) 
        SD.append(np.std(Trials)) 
        NS = sum(Success)
        PoS.append((NS / number_of_runs))  #proportion of success
    
        result[i,]=(ET[i], SD[i], PoS[i])
        result = np.where(np.isnan(result), 10000, result)
    
                        
    return result                 
                

                