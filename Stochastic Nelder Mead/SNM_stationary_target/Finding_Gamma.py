#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 16:05:56 2023

@author: busrabiskin
"""

import numpy as np

def Finding_Gamma(X_ref, X_cent, n):
    
    p = []
    
    for i in range(n+1):
        p.append(X_cent[i]/(X_ref[i]-X_cent[i]))
        
    p = np.array(p)
    p = p[np.where(p > 0)]
    
    if len(p) > 0:
        gamma_max = min(p)
        gamma = np.random.uniform(1, gamma_max, 1)
    else:
        gamma = np.random.uniform(1, 2, 1)
        
    return(gamma)
        
        