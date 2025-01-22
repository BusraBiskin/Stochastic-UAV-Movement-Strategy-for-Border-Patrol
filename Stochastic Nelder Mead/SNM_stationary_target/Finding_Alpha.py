#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 15:10:50 2023

@author: busrabiskin
"""
import numpy as np

def Finding_Alpha(X_max, X_cent,n):
    
    p = []
    
    for i in range(n+1):
        p.append(X_cent[i] / (X_cent[i] - X_max[i]))
        
    p = np.array(p)    
    p = p[np.where(p > 0)]
    
    if len(p) > 0:
        alpha_max = min(p)
        alpha = np.random.uniform(0, alpha_max, 1)
    else:
        alpha = np.random.uniform(0, 1, 1)
        
    return(alpha)
  