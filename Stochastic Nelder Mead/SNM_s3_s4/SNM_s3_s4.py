#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 22:30:22 2023

@author: busrabiskin
"""

"-Stochastic Nelder Mead-"

import time
import numpy as np
import pandas as pd
import sys
import matplotlib.pyplot as plt

#calling functions 
from Statistics_Plural_Function import Statistics_Plural
from Statistics_of_Simulation_Function import Statistics_of_Simulation
from Distance_Matrix_Function import Distance_Matrix
from Finding_Alpha import Finding_Alpha
from Finding_Gamma import Finding_Gamma
#from NeighbourhoodLS_Function import NeighbourhoodLS
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


"Step 0: Generation of initial set, p+1 extreme points"

n = 3 #our problem is 3-dimensioned
V = np.zeros((n+1,8))

"logical solutions"
a=0.5
b=0.167
c=0.167
d=0.166
V[0,] = [a,b,c,d,  d,c,b,a]
V[1,] = [d,a,b,c,  a,d,c,b]
V[2,] = [c,d,a,b,  b,a,d,c]
V[3,] = [b,c,d,a,  c,b,a,d]    

#calculating fitness function values of starting solutions 
f = Statistics_Plural(V, number_of_runs, n, ratio, l, h, max_number_of_steps, Dist_Matrix_1, Dist_Matrix_2, Dist_Matrix_3, radius) 
f = [row[2] for row in f] 
f = np.array(f).flatten() #converting PoS values into array 
f  = f.reshape((4,1))

V = np.append(V,-f,axis= 1)

Result = np.zeros((100*n, 9))
Result[0:4,] = V[0:4,]
Result_best = np.zeros((100*n, 9))

"Step1: Order"
V_sort = V[V[:,8].argsort()]
V_sort

"parameters"
beta = 0.5
P_s = 0.25

start_time = time.time()
elapsed = 0  
k = 0

"loop starts here"

while elapsed < 400:
    
    Result_best[k,] = V_sort[0,]
    
    #finding centroid
    X_cent_1 = [np.mean(V_sort[0:n,0]),np.mean(V_sort[0:n,1]),np.mean(V_sort[0:n,2]),np.mean(V_sort[0:n,3])]
    X_cent_1 = X_cent_1/sum(X_cent_1)
    X_cent_2 = [np.mean(V_sort[0:n,4]),np.mean(V_sort[0:n,5]),np.mean(V_sort[0:n,6]),np.mean(V_sort[0:n,7])]
    X_cent_2 = X_cent_2/sum(X_cent_2)
    X_cent = np.concatenate((X_cent_1,X_cent_2))
  
    #finding X.max
    X_max = V_sort[n,]
    g_X_max = X_max[8]
  
    #finding X.2max
    X_2max = V_sort[n-1,]
    g_X_2max = X_2max[8]
        
    #finding X.min
    X_min = V_sort[0,]
    g_X_min = X_min[8]
  
    #finding reflection point
    X_max = X_max[ : -1]
  
    #deciding alpha
    if X_max.all == X_cent.all:
        alpha = (np.random.uniform(0.1, 1, 1), np.random.uniform(0.1, 1, 1))  
    else:
        alpha = Finding_Alpha(X_max, X_cent, n)
        
    X_ref = np.zeros(8)
    X_ref[0:4] = ((1+alpha[0]) * X_cent[0:4]) - (alpha[0] * X_max[0:4])
    X_ref[0:4] = X_ref[0:4] / sum(X_ref[0:4])  #normalizing
    X_ref[4:8] = ((1+alpha[1]) * X_cent[4:8]) - (alpha[1] * X_max[4:8])
    X_ref[4:8] = X_ref[4:8] / sum(X_ref[4:8])  #normalizing
  
    #dealing with negative probabilities
    if len(np.where(X_ref < 0)) > 0:
        g_X_ref = 1000
    else:
        g_X_ref = - Statistics_of_Simulation(X_ref, number_of_runs, ratio, l, h, max_number_of_steps, Dist_Matrix_1, Dist_Matrix_2, Dist_Matrix_3, radius)[2]
                
    "Step 3a"
    if g_X_min <= g_X_ref and g_X_ref < g_X_2max:
        V_sort = V_sort[ : -1]
        X_ref = np.append(X_ref, g_X_ref)
        V_sort = np.vstack([V_sort, X_ref])
        Result[k+4,] = X_ref
    
    " Step 3b: Expand "
  
    #finding expanded point
    if len(X_ref) == 9:
        X_ref = X_ref[ : -1]
    
    if g_X_ref < g_X_min:
        gamma = Finding_Gamma(X_ref, X_cent, n)
        X_exp = np.zeros(8)
        X_exp[0:4] = (gamma[0] * X_ref[0:4]) + ((1 - gamma[0]) * X_cent[0:4])
        X_exp[0:4] = X_exp[0:4] / sum(X_exp[0:4])
        X_exp[4:8] = (gamma[1] * X_ref[4:8]) + ((1 - gamma[1]) * X_cent[4:8])
        X_exp[4:8] = X_exp[4:8] / sum(X_exp[4:8])
        
        
        #dealing with negative probabilities
        if len(np.where(X_exp < 0)) > 0:
            g_X_exp = 1000
        else:
            g_X_exp =  - Statistics_of_Simulation(X_exp, number_of_runs, ratio, l, h, max_number_of_steps, Dist_Matrix_1, Dist_Matrix_2, Dist_Matrix_3, radius)[2]

        if g_X_exp < g_X_ref :
            V_sort = V_sort[ : -1]
            X_exp = np.append(X_exp, g_X_exp)
            V_sort = np.vstack([V_sort, X_exp])
            Result[k+4,] = X_exp
        else:
            V_sort = V_sort[ : -1]
            X_ref = np.append(X_ref, g_X_ref)
            V_sort = np.vstack([V_sort, X_ref])
            Result[k+4,] = X_ref
        
    "Step 3c: Contract"
    
    if g_X_ref >= g_X_2max:
    
        accept=0
        
        #outside contraction
        if g_X_2max <= g_X_ref and g_X_ref < g_X_max:
            #contraction point
            X_ref = X_ref[0:8]
            X_cont = np.zeros(8)
            X_cont[0:4] = (beta * X_ref[0:4]) + ((1 - beta) * X_cent[0:4])
            X_cont[0:4] = X_cont[0:4]/sum(X_cont[0:4])
            X_cont[4:8] = (beta * X_ref[4:8]) + ((1 - beta) * X_cent[4:8])
            X_cont[4:8] = X_cont[4:8]/sum(X_cont[4:8])
            
            if len(np.where(X_cont < 0)) > 0:
                g_X_cont = 1000
            else:
                g_X_cont = - Statistics_of_Simulation(X_exp, number_of_runs, ratio, l, h, max_number_of_steps, Dist_Matrix_1, Dist_Matrix_2, Dist_Matrix_3, radius)[2]
     
            if g_X_cont <= g_X_ref:
                V_sort = V_sort[ : -1]
                X_cont = np.append(X_cont, g_X_cont)
                V_sort = np.vstack([V_sort, X_cont])
                Result[k+4,] = X_cont
                accept = 1
                
        #inside contraction
        if g_X_ref >= g_X_max:
            #contraction point
            X_cont = np.zeros(8)
            X_cont[0:4] = (beta * X_max[0:4]) + ((1 - beta) * X_cent[0:4])
            X_cont[0:4] = X_cont[0:4]/sum(X_cont[0:4])
            X_cont[4:8] = (beta * X_max[4:8]) + ((1 - beta) * X_cent[4:8])
            X_cont[4:8] = X_cont[4:8]/sum(X_cont[4:8])
            
            g_X_cont = - Statistics_of_Simulation(X_cont, number_of_runs, ratio, l, h, max_number_of_steps, Dist_Matrix_1, Dist_Matrix_2, Dist_Matrix_3, radius)[2]

            if g_X_cont <= g_X_max:
                V_sort = V_sort[ : -1]
                X_cont = np.append(X_cont, g_X_cont)
                V_sort = np.vstack([V_sort, X_cont])
                Result[k+4,] = X_cont
                accept = 1
                
        if accept == 0:
            
            "Adaptive Random Search"
            m = 1
            cr1 = 0
            while m != 10 and cr1 != 5 :
                
                r = np.random.uniform(0, 1, 1)
                
                if r < P_s:
                    #if local search is chosen
                    fitness_func = []
                    a = (1 / V_sort[ : ,8])
                    F_total = sum(a)
                    
                    for i in range(4):
                        fitness_func.append((1 / V_sort[i,8]) / F_total)
          
                    N = V_sort[np.argmax(fitness_func),]
                    N = N[0:8]
                    
                    X_ARS = Neighbourhood(N, number_of_runs, ratio, l, h, max_number_of_steps, Dist_Matrix_1, Dist_Matrix_2, Dist_Matrix_3,radius)
                    
                else:
                    #global search
                    X_ARS = np.zeros(8)
                    X_ARS[0:4] = np.random.dirichlet(np.ones(4),size=1)
                    X_ARS[4:8] = np.random.dirichlet(np.ones(4),size=1)
                    
                    
                g_X_ARS = - Statistics_of_Simulation(X_ARS, number_of_runs, ratio, l, h, max_number_of_steps, Dist_Matrix_1, Dist_Matrix_2, Dist_Matrix_3, radius)[2]
                cr1 += 1
                
                if g_X_ARS <= g_X_max :
                    V_sort = V_sort[ : -1]
                    X_ARS = np.append(X_ARS, g_X_ARS)
                    V_sort = np.vstack([V_sort, X_ARS])
                    Result[k+4,] = X_ARS
                    m = 10
                
    "Order"
    
    V = V_sort
    V_sort = V[V[:,8].argsort()]
    
    k += 1
    print(k)
    
        
    elapsed = time.time() - start_time #update the time elapsed       
    
resampled_best = np.zeros((4,11))
#resampling V_sort
for j in range(4):
    
    resampled = np.zeros((5,3))
    for i in range(5):
        resampled[i,0:3] = Statistics_of_Simulation(V_sort[j,0:8], number_of_runs, ratio, l, h, max_number_of_steps, Dist_Matrix_1,Dist_Matrix_2,Dist_Matrix_3, radius)[0:3]
     
    
    resampled_best[j,0:8] = V_sort[j,0:8]
    resampled_best[j,8] = np.average(resampled[0:4,0])
    resampled_best[j,9] = np.average(resampled[0:4,1])
    resampled_best[j,10] = np.average(resampled[0:4,2])

"best solution"
best_soln_sort = resampled_best[(resampled_best[:,10]).argsort()]
best_soln = best_soln_sort[3,0:11]

                     