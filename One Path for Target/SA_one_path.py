#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  1 16:10:53 2023

@author: busrabiskin
"""

"Simulated Annealing - 3 paths, 4dv, 1UAV"

import time
import numpy as np
import pandas as pd
import sys
import math
import matplotlib.pyplot as plt


#calling functions 
from Statistics_of_Simulation_Function import Statistics_of_Simulation
from Neighbourhood_Function_v2 import Neighbourhood


radius = 2
h = 20
l = 20

#number of simulation runs
number_of_runs = 1500
    
#maximum number of steps that UAV can make"
max_number_of_steps = 200
                 
"starting solution and temperature, variables"
P = [0.25,0.25,0.25,0.25]
Temp = 80
n = 8#number of solutions for each temperature
k = 0
i = 0
TempF = -((0.01)/math.log(0.2)) #deciding stopping criteria
bad_soln = 0
std = 0.5

Perf = Statistics_of_Simulation(P, number_of_runs, l, h, max_number_of_steps, radius)
f = Perf[2]
f_best = Perf[2]
P_best = P

Result = np.empty((10000*n,7))
Best_f = []

start_time = time.time()

elapsed = 0 
count = 0 

while elapsed <= 400:

    i = i + 1
    
    for j in range(n):
             
        count = count + 1
        P_1 = Neighbourhood(P)
        Perf_1 = Statistics_of_Simulation(P_1, number_of_runs, l, h, max_number_of_steps, radius)
        
        f_1 = Perf_1[2]
    
        "delta-acceptance" 
        delta = f_1 - f
    
        if delta >= 0:
            P = P_1
            f = f_1 
            P_best = P_1
            f_best = f_1
            Perf = Perf_1
    
        else: 
            bad_soln = bad_soln + 1
            prob = math.exp(delta / Temp)
            if prob > np.random.uniform(0, 1, 1):
                P = P_1
                f = f_1
                Perf = Perf_1
                
        soln = np.append(P, Perf[0:3])
        Result[count, 0:7] = soln
        Best_f.append(f_best)
        
    n = n+1
    Temp = Temp * 0.8
    k = k + 1
    print(k)
    elapsed = time.time() - start_time #update the time elapsed
       
"finding the best solution"
Result = Result[0:count,]

Result_sorted = Result[(-Result[:,6]).argsort()]

Result_sorted_5 = Result_sorted[0:5,] #taking first 5 
    
#resampling first 5
for j in range(5):
    resampled = np.zeros((5,3))
    for i in range(5):
        resampled[i,0:3] = Statistics_of_Simulation(Result_sorted_5[j,0:4], number_of_runs, l, h, max_number_of_steps, radius)[0:3]
    Result_sorted_5[j,4] = np.average(resampled[0:5,0])
    Result_sorted_5[j,5] = np.average(resampled[0:5,1])
    Result_sorted_5[j,6] = np.average(resampled[0:5,2])

"best solution"
best_soln_sort = Result_sorted_5[(-Result_sorted_5[:,6]).argsort()]
best_soln = best_soln_sort[0,0:7]

sum(best_soln[0:3])

