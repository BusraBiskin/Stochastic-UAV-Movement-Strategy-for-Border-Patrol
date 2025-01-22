# -*- coding: utf-8 -*-
"""
Created on Mon May 16 13:41:25 2022

@author: bb2r20
"""

"Statistics for Plural Probability Vectors"

import numpy as np
import copy
import time
import random

from UAV_Movement_Function import UAV_Movement
#from GeoDistance import Geo_Dist


def Statistics_Plural(V, number_of_runs, n, ratio, l, h, Dist_Matrix_1, Dist_Matrix_2, Dist_Matrix_3, radius):
    
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
            
           
            #target chooses a path, randomly
            path = random.randint(0,2)
            
            if path == 0:
                Dist_Matrix = Dist_Matrix_1
        
            elif path == 1:
                Dist_Matrix = Dist_Matrix_2
            else:
                Dist_Matrix = Dist_Matrix_3
            
            #target starting location
            #v = loc_target.iloc[0,0:2]
            
            #UAV starting location
            u1 = [0, 0]
            u2 = [56, 61]
            #u_c = np.zeros(2) #location in real map
            
            D1 = 0
            D2 = 0
            t = 0
            
            M1 = M[0:4]
            M2 = M[4:8]
            
            while D1 < 1 and D2 < 1 and t < (Dist_Matrix.shape[1]-1)*ratio :
                
                "Signal Part"
                if t == 30 and (path == 0 or path == 1): 
                    
                 
                    geo_dist1 = Dist_Matrix[u1[1] * (h+1) + u1[0], int(t/ratio)]
                    geo_dist2 = Dist_Matrix[u2[1] * (h+1) + u2[0], int(t/ratio)]
                  
                    t += max(int(geo_dist1/10), int(geo_dist2/10))
                
                    u1 = [48, 26]
                    u2 = [48, 26]
                
                u1 = UAV_Movement(u1, M1, l, h)
                u2 = UAV_Movement(u2, M2, l, h)
                t = t + 1
                
                geo_dist1 = Dist_Matrix[u1[1] * (h+1) + u1[0], int(t/ratio) ]
                    
                if  (geo_dist1 <= radius) :
                    D1 = 1
                  
        
                geo_dist2 = Dist_Matrix[u2[1] * (h+1) + u2[0], int(t/ratio) ]
                    
                if  (geo_dist2 <= radius) :
                    D2 = 1       
                                                                                
            if D1 == 1 or D2 == 1:
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
                

                