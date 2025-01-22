# -*- coding: utf-8 -*-
"""
Created on Mon Nov  7 18:08:08 2022

@author: bb2r20
"""

"Creating Distance Matrix"

import numpy as np
from math import sin, cos, sqrt, atan2, radians

def Distance_Matrix(loc_target, loc_UAV, h):

    A = np.zeros(2)
    
    Dist_Matrix = np.zeros(((h+1)*(h+1),loc_target.shape[0]))
    
    for i in range(h+1):
        
        A[0] = (loc_UAV.iloc[0,i]) # UAV latitude
        
        for j in range(h+1):
        
            A[1] = (loc_UAV.iloc[1,j]) # UAV longitude
            
            for k in range(loc_target.shape[0]):
                
               B = loc_target.iloc[k, 0:2] 
               
               R = 6373.0
            
               lat1 = radians(A[0])
               lon1 = radians(A[1])
               lat2 = radians(B[0])
               lon2 = radians(B[1])
            
               dlon = lon2 - lon1
               dlat = lat2 - lat1
            
               a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
               c = 2 * atan2(sqrt(a), sqrt(1 - a))
            
               distance = R * c * 1000
               
               Dist_Matrix[i * (h+1) + j, k] = distance
               
    return Dist_Matrix       