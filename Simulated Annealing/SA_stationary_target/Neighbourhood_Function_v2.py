#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  3 13:00:25 2023

@author: busrabiskin
"""

"Neighborhood Search v2"

import numpy as np
import random

def Neighbourhood(M):
    
    d = 0.1   
    stop = 1
    
    n = random.randint(0,7)
  
    while stop != 10:
        
        if n == 0:
            #for P_west, M[1]
            M1 = np.zeros(4) 
            M1[0] = M[0] + d
            M1[1:4] = [x - (d/3) for x in M[1:4]]
            
        elif n == 1:    
            M1 = np.zeros(4)
            M1[0] = M[0] - d
            M1[1:4] = [x + (d/3) for x in M[1:4]]
            
        elif n == 2:    
            #for P_east, M[2]
            M1= np.zeros(4)  
            M1[1] = M[1] - d
            M1[0] = M[0] + (d/3)
            M1[2:4] = [x + (d/3) for x in M[2:4]]
            
        elif n == 3:    
            M1 = np.zeros(4)  
            M1[1] = M[1] + d
            M1[0] = M[0] - (d/3)
            M1[2:4] = [x - (d/3) for x in M[2:4]]
            
        elif n == 4:    
            #for P_south, M[3]
            M1 = np.zeros(4)  
            M1[2] = M[2] - d
            M1[0:2] = [x + (d/3) for x in M[0:2]]
            M1[3] = M[3] + (d/3)
            
        elif n == 5:
            M1 = np.zeros(4)  
            M1[2] = M[2] + d
            M1[0:2] = [x - (d/3) for x in M[0:2]]
            M1[3] = M[3] - (d/3)
        
        elif n == 6:
            #for P_north, M[4]
            M1 = np.zeros(4)  
            M1[3] = M[3] - d
            M1[0:3] = [x + (d/3) for x in M[0:3]]
        else:    
            M1 = np.zeros(4)  
            M1[3] = M[3] + d
            M1[0:3] = [x - (d/3) for x in M[0:3]] 
            
        if np.any(M1 < 0):
           d = d / 2
            
        else:
            stop = 10
             
    return(M1)

  