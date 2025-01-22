#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 18 21:27:13 2023

@author: busrabiskin
"""

# -*- coding: utf-8 -*-
"""
Created on Mon May 16 15:34:02 2022

@author: bb2r20
"""

"UAV Movement Function"

import math
import random
import functools
import numpy as np

def UAV_Movement(u, M, l, h):

    M1 = np.zeros(4)
  
    
    if u[0] > 0 and u[0] < l and u[1] > 0 and u[1] < h:
        
        M1 = M
        
    else:
        #case: corners
        #lower left corner
        if u[0] == 0 and u[1] == 0 :
            M1[0] = 0
            M1[1] = 0.5
            M1[2] = 0
            M1[3] = 0.5
        #upper left corner   
        elif u[0] == 0 and u[1] == h  :
            M1[0] = 0
            M1[1] = 0.5
            M1[2] = 0.5
            M1[3] = 0
        #upper right corner   
        elif u[0] == l and u[1] == h:
            M1[0] = 0.5
            M1[1] = 0
            M1[2] = 0.5
            M1[3] = 0    
        #lower right corner   
        elif u[0] == l and u[1] == 0:
            M1[0] = 0.5
            M1[1] = 0
            M1[2] = 0
            M1[3] = 0.5       
            
        #case: edges
        #left edge
        elif u[0] == 0 and u[1] != 0 and u[1] != h:
            M1[0] = 0
            M1[1] = 1
            M1[2] = 0
            M1[3] = 0
        #top edge
        elif u[1] == h and u[0] != 0 and u[0] != l:
            M1[0] = 0
            M1[1] = 0
            M1[2] = 1
            M1[3] = 0
        #right edge
        elif u[0] == l and u[1] != h and u[1] != 0:
            M1[0] = 1
            M1[1] = 0
            M1[2] = 0 
            M1[3] = 0 
        #bottom edge
        elif u[1] == 0 and u[0] != 0 and u[0] != l:
            M1[0] = 0
            M1[1] = 0
            M1[2] = 0
            M1[3] = 1
        
    a = (M1[0] + M1[1])
    b = (M1[0] + M1[1] + M1[2])
                         
    #real movement starts    
    r = random.uniform(0, 1)
    
    if r < M1[0]:
        u[0] = u[0] - 1
    elif r > M1[0] and r < a:
        u[0] = u[0] + 1
    elif r > a and r < b:
        u[1] = u[1] - 1
    else:
        u[1] = u[1] + 1
 
            
    return u

  