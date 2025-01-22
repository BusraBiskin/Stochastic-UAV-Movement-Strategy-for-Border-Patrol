#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 19 15:44:03 2023

@author: busrabiskin
"""

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

def Target_Movement(tl, T, l, h):

    T1 = np.zeros(4)
    
    if tl[0] > 0 and tl[0] < l and tl[1] > 0 and tl[1] < h:
        T1 = T
        
    else:
        
        #case: corners
        #upper right corner
        if tl[0] == l and tl[1] == h:
            T1[0] = T[0] + T[3]
            T1[1] = 0
            T1[2] = T[2]
            T1[3] = 0    
        #lower right corner   
        elif tl[0] == l and tl[1] == 0:
            T1[0] = T[0] + T[2]
            T1[1] = 0
            T1[2] = 0
            T1[3] = T[3]    
            
        #case: edges
        #top edge
        elif tl[1] == h and tl[0] != 0 and tl[0] != l:
            T1[0] = T[0] + T[3]
            T1[1] = 0
            T1[2] = T[2]
            T1[3] = 0 
        #right edge
        elif tl[0] == l and tl[1] != h and tl[1] != 0:
           T1 = T 
        #bottom edge
        elif tl[1] == 0 and tl[0] != 0 and tl[0] != l:
            T1[0] = T[0] + T[2]
            T1[1] = 0
            T1[2] = 0
            T1[3] = T[3] 
        
    a = T1[0] + T1[1]
    b = T1[0] + T1[1] + T1[2]
                         
    #real movement starts    
    r = random.uniform(0, 1)
    
    if r < T1[0]:
        tl[0] = tl[0] - 1
    elif r > T1[0] and r < a:
        tl[0] = tl[0] + 1
    elif r > a and r < b:
        tl[1] = tl[1] - 1
    else:
        tl[1] = tl[1] + 1
 
            
    return tl

  