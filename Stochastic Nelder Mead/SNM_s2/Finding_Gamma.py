#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 16:05:56 2023

@author: busrabiskin
"""

import numpy as np

def Finding_Gamma(X_ref, X_cent, n):
    
    p1 = []
    
    for i in range(n+1):
        p1.append(X_cent[i]/(X_ref[i]-X_cent[i]))
        
    p1 = np.array(p1)
    p1 = p1[np.where(p1 > 0)]
    
    if len(p1) > 0:
        gamma_max = min(p1)
        gamma1 = np.random.uniform(1, gamma_max, 1)
    else:
        gamma1 = np.random.uniform(1, 2, 1)
    
    p2 = []
    
    for i in range(n+1,8):
        p2.append(X_cent[i]/(X_ref[i]-X_cent[i]))
        
    p2 = np.array(p2)
    p2 = p2[np.where(p2 > 0)]
    
    if len(p2) > 0:
        gamma_max = min(p2)
        gamma2 = np.random.uniform(1, gamma_max, 1)
    else:
        gamma2 = np.random.uniform(1, 2, 1)
        
    return(gamma1, gamma2)
        
        