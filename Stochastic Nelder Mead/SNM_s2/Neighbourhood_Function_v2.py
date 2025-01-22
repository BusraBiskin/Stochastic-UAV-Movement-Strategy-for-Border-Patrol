#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 12:37:54 2023

@author: busrabiskin
"""

import numpy as np
import random

def Neighbourhood(M, number_of_runs, ratio, l, h, max_number_of_steps, Dist_Matrix_1, Dist_Matrix_2, Dist_Matrix_3,radius):
    
    d = 0.1
    stop = 1
    
    b = random.randint(0,1)
    
    n = random.randint(0,7)
    
    if b == 0:
        
        M1 = np.zeros(8)
        M1[4:8] = M[4:8]
        
        while stop != 10:
            
            if n == 0: 
            	 M1[0] = M[0] + d
            	 M1[1:4] = [x - (d/3) for x in M[1:4]]
                 
            elif n == 1:
                 M1[0] = M[0] - d
                 M1[1:4] = [x + (d/3) for x in M[1:4]]
                 
            elif n == 2:
                 M1[1] = M[1] - d
                 M1[0] = M[0] + (d/3)
                 M1[2:4] = [x + (d/3) for x in M[2:4]]
            
            elif n == 3:    
                 M1[1] = M[1] + d
                 M1[0] = M[0] - (d/3)
                 M1[2:4] = [x - (d/3) for x in M[2:4]]
            
            elif n == 4:     
                 M1[2] = M[2] - d
                 M1[0:2] = [x + (d/3) for x in M[0:2]]
                 M1[3] = M[3] + (d/3)
            
            elif n == 5:
                 M1[2] = M[2] + d
                 M1[0:2] = [x - (d/3) for x in M[0:2]]
                 M1[3] = M[3] - (d/3)
        
            elif n == 6:
                 M1[3] = M[3] - d
                 M1[0:3] = [x + (d/3) for x in M[0:3]]
                
            else:    
                 M1[3] = M[3] + d
                 M1[0:3] = [x - (d/3) for x in M[0:3]]
            
            if np.any(M1 < 0):
                d = d / 2
            
            else:
                stop = 10
                
    else:
        
        M1 = np.zeros(8)
        M1[0:4] = M[0:4]
        
        while stop != 10:
            
              if n == 0:
                  M1[4] = M[4] + d
                  M1[5:8] = [x - (d/3) for x in M[5:8]]
                 
              elif n == 1:
                  M1[4] = M[4] - d
                  M1[5:8] = [x + (d/3) for x in M[5:8]]
                                   
              elif n == 2: 
                  M1[5] = M[5] - d
                  M1[4] = M[4] + (d/3)
                  M1[6:8] = [x + (d/3) for x in M[6:8]]
            
              elif n == 3:    
                  M1[5] = M[5] + d
                  M1[4] = M[4] - (d/3)
                  M1[6:8] = [x - (d/3) for x in M[6:8]]
            
              elif n == 4:    
                  M1[6] = M[6] - d
                  M1[4:6] = [x + (d/3) for x in M[4:6]]
                  M1[7] = M[7] + (d/3)
            
              elif n == 5: 
                  M1[6] = M[6] + d
                  M1[4:6] = [x - (d/3) for x in M[4:6]]
                  M1[7] = M[7] - (d/3)
        
              elif n == 6: 
                  M1[7] = M[7] - d
                  M1[4:7] = [x + (d/3) for x in M[4:7]]
                
              else:    
                  M1[7] = M[7] + d
                  M1[4:7] = [x - (d/3) for x in M[4:7]]
            
              if np.any(M1 < 0):
                  d = d / 2
            
              else:
                  stop = 10
                  
    return (M1)
        
