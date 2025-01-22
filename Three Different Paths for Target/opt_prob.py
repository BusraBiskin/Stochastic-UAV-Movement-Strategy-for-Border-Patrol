#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 14:52:33 2024

@author: busrabiskin
"""

from math import comb
from scipy.optimize import fsolve , minimize 

#defining objective function

def objective(x):
    st_1 = comb(13,5) * ((x[0])**5) * ((x[1])**8)
    
    st_2 = comb(13,3) * ((x[0])**3) * ((x[1])**10)
    
    st_3 = comb(13,4) * ((x[0])**4) * ((x[1])**9)
    #st_4 = comb(8,4) * (x[0])**4 * (x[1])**4
    
    return -(st_1 + st_2 + st_3)
    

#defining constraints
            
#sum of probabilities should equal to 1
def constraint1(x):
    sum_p = 1
    for i in range(2):
        sum_p = sum_p - x[i]
    return sum_p

#starting solution, x0
x0 = [0.5,0.5]  

print(objective(x0))

#bounds on probabilities
bs = (0, 1.0)
bnds = (bs,bs)


#maximizing prob
cons1 = {'type': 'eq','fun':constraint1}
cons = [cons1]

sol = minimize(objective, x0, method = 'SLSQP', bounds = bnds, constraints = cons)
print(sol)


