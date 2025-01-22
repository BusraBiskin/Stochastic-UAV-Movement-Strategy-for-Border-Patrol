#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 22 20:58:53 2022

@author: busrabiskin
"""

import math as m
from scipy.optimize import minimize 

def Global_Search(V,n):
    
     def delta(x):
        rbf_global = 0
        for i in range(n):
            sub_sum = 0
            for j in range(4):
                sub_sum = sub_sum + (x[j] - V[i,j]) ** 2
            if sub_sum == 0:
                sub_sum = sub_sum
            else:
                rbf_global = rbf_global + (1 / m.sqrt(sub_sum))
        return rbf_global
    
     #defining constraints
    
     #sum of probabilities should equal to 1
     def constraint1(x):
        sum_x = 1
        for i in range(4):
            sum_x = sum_x - x[i]
        return sum_x
    
     #bounds on probabilities
     bs = (0.001, 1.0)
     bnds = (bs, bs, bs, bs)
    
     #starting solution, x0
     x0 = [0.25, 0.25, 0.25, 0.25]  
        
     #minimizing delta function
     cons1 = {'type': 'eq','fun':constraint1}
     cons = [cons1]
     
     sol = minimize(delta, x0, method = 'SLSQP', bounds = bnds, constraints = cons)
     
     X = sol.x
     
     return X
     







