#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 15:10:50 2023

@author: busrabiskin
"""
import numpy as np

def Finding_Alpha(X_max, X_cent,n):
    
    p1 = []
    
    for i in range(n+1):
        p1.append(X_cent[i] / (X_cent[i] - X_max[i]))
        
    p1 = np.array(p1)    
    p1 = p1[np.where(p1 > 0)]
    
    if len(p1) > 0 and any(p1) ==  float('inf'):
        alpha_max = min(p1)
        alpha1 = np.random.uniform(0, alpha_max, 1)
    else:
        alpha1 = np.random.uniform(0, 1, 1)
        
    p2 = []
    
    for i in range(n+1,8):
        p2.append(X_cent[i] / (X_cent[i] - X_max[i]))
        
    p2 = np.array(p2)    
    p2 = p2[np.where(p2 > 0)]
    
    if len(p2) > 0 and any(p1) ==  float('inf'):
        alpha_max = min(p2)
        alpha2 = np.random.uniform(0, alpha_max, 1)
    else:
        alpha2 = np.random.uniform(0, 1, 1)
        
    
        
    return(alpha1,alpha2)
  