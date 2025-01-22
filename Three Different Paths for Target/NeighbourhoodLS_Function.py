#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 18:48:19 2023

@author: busrabiskin
"""

"Neighborhood-Local Search"

import numpy as np

from Statistics_Plural_Function import Statistics_Plural

def NeighbourhoodLS(M, number_of_runs, ratio, l, h, max_number_of_steps, Dist_Matrix_1, Dist_Matrix_2, Dist_Matrix_3,radius):
    
    d = 0.1  
    V1 = np.zeros((8,4))
    
    stop = 1
  
    while stop != 10:
    
        #for P_west, M[1]
        M1_1 = np.zeros(4) 
        M1_1[0] = M[0] + d
        M1_1[1:4] = [x - (d/3) for x in M[1:4]]
        V1[0,] = M1_1
    
        M1_2 = np.zeros(4)
        M1_2[0] = M[0] - d
        M1_2[1:4] = [x + (d/3) for x in M[1:4]]
        V1[1,] = M1_2
    
        #for P_east, M[2]
        M2_1 = np.zeros(4)  
        M2_1[1] = M[1] - d
        M2_1[0] = M[0] + (d/3)
        M2_1[2:4] = [x + (d/3) for x in M[2:4]]
        V1[2,] = M2_1
    
        M2_2 = np.zeros(4)  
        M2_2[1] = M[1] + d
        M2_2[0] = M[0] - (d/3)
        M2_2[2:4] = [x - (d/3) for x in M[2:4]]
        V1[3,] = M2_2
    
        #for P_south, M[3]
        M3_1 = np.zeros(4)  
        M3_1[2] = M[2] - d
        M3_1[0:2] = [x + (d/3) for x in M[0:2]]
        M3_1[3] = M[3] + (d/3)
        V1[4,] = M3_1
    
        M3_2 = np.zeros(4)  
        M3_2[2] = M[2] + d
        M3_2[0:2] = [x - (d/3) for x in M[0:2]]
        M3_2[3] = M[3] - (d/3)
        V1[5,] = M3_2
    
        #for P_north, M[4]
        M4_1 = np.zeros(4)  
        M4_1[3] = M[3] - d
        M4_1[0:3] = [x + (d/3) for x in M[0:3]]
        V1[6,] = M4_1
    
        M4_2 = np.zeros(4)  
        M4_2[3] = M[3] + d
        M4_2[0:3] = [x - (d/3) for x in M[0:3]]
        V1[7,] = M4_2 
        
    
        if np.any(V1 < 0):
            V1 = np.delete(V1, np.where((V1 < 0).any(axis=1)), axis=0)
            
        if len(V1) > 0:
            stop = 10
        else:
            d = d / 2
            
    f = Statistics_Plural(V1, number_of_runs, len(V1)-1, ratio, l, h, max_number_of_steps, Dist_Matrix_1, Dist_Matrix_2, Dist_Matrix_3, radius) 
    f = [row[2] for row in f]        
            
    M1 = V1[np.argmax(f),]
  
  
    return(M1)

  