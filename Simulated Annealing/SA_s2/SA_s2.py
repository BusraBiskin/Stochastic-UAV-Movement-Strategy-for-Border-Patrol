#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  1 16:10:53 2023

@author: busrabiskin
"""

"Simulated Annealing - 3 paths, 8dv, 1UAV"

import time
import numpy as np
import pandas as pd
import sys
import math
import matplotlib.pyplot as plt

#calling functions 
from Statistics_of_Simulation_Function import Statistics_of_Simulation
from Distance_Matrix_Function import Distance_Matrix
from Neighbourhood_Function_v2 import Neighbourhood

#Speed Ratio UAV/target : grid/time
ratio = 10
radius = 20
h = 61
l = 56

time_step = 50

#number of simulation runs
number_of_runs = 1500

#different paths for the target
loc_target_1 = pd.read_excel("TargetPathCoordinates - 1.xlsx")
loc_target_2 = pd.read_excel("TargetPathCoordinates - 2.xlsx")
loc_target_3 = pd.read_excel("TargetPathCoordinates - 3.xlsx")

loc_UAV = pd.read_excel("UAVCoordinates.xlsx")

#creates different distance matrices
Dist_Matrix_1 = Distance_Matrix(loc_target_1, loc_UAV, h)
Dist_Matrix_2 = Distance_Matrix(loc_target_2, loc_UAV, h)
Dist_Matrix_3 = Distance_Matrix(loc_target_3, loc_UAV, h)
    
#maximum number of steps that UAV can make"
max_number_of_steps = 350
                 
"starting solution and temperature, variables"
P = [0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25]
Temp = 100
n = 8 #number of solutions for each temperature
k = 0
i = 0
#TempF = -((0.01)/math.log(0.2)) #deciding stopping criteria
t = 0
std = 0.5

Perf = Statistics_of_Simulation(P, number_of_runs, ratio, l, h, max_number_of_steps, Dist_Matrix_1,Dist_Matrix_2,Dist_Matrix_3,radius, time_step)
f = Perf[2]
f_best = Perf[2]
P_best = P

Result = np.zeros((100*n, 11))

start_time = time.time()
elapsed = 0  

while elapsed < 400:

    i = i + 1
    
    for j in range(n):
    
        P_1 = Neighbourhood(P, number_of_runs, ratio, l, h, max_number_of_steps, Dist_Matrix_1, Dist_Matrix_2, Dist_Matrix_3,radius)
        Perf_1 = Statistics_of_Simulation(P_1, number_of_runs, ratio, l, h, max_number_of_steps, Dist_Matrix_1,Dist_Matrix_2,Dist_Matrix_3, radius, time_step)
        f_1 = Perf_1[2]
    
        "delta-acceptance" 
        delta = f_1 - f
    
        if delta > 0:
            P = P_1
            f = f_1
            P_best = P_1
            f_best = f_1
            Perf = Perf_1
    
        else: 
            prob = math.exp(delta / Temp)
            if prob > np.random.uniform(0, 1, 1):
                P = P_1
                f = f_1
                Perf = Perf_1
                
        soln = np.append(P, Perf[0:3])        
        Result[(i-1)*n+j, ] = soln
  
    Temp = Temp * 0.9
    k = k + 1
    print(k)
    
    elapsed = time.time() - start_time #update the time elapsed

    
"finding the best solution and resampling (5times)"

Result_sorted = Result[(-Result[:,10]).argsort()]
        
Result_sorted_5 = Result_sorted[0:5,] #taking first 5 
    
#resampling first 5
for j in range(5):
    resampled = np.zeros((5,3))
    for i in range(5):
        resampled[i,0:3] = Statistics_of_Simulation(Result_sorted_5[j,0:8], number_of_runs, ratio, l, h, max_number_of_steps, Dist_Matrix_1,Dist_Matrix_2,Dist_Matrix_3, radius, time_step)[0:3]
    Result_sorted_5[j,8] = np.average(resampled[0:5,0])
    Result_sorted_5[j,9] = np.average(resampled[0:5,1])
    Result_sorted_5[j,10] = np.average(resampled[0:5,2])

"best solution"
best_soln_sort = Result_sorted_5[(-Result_sorted_5[:,10]).argsort()]
best_soln = best_soln_sort[0,0:11]



