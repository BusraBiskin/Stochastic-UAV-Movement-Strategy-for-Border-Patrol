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
from Finding_Alpha import Finding_Alpha
from Finding_Gamma import Finding_Gamma
from NeighbourhoodLS_Function import NeighbourhoodLS
from Neighbourhood_Function_v2 import Neighbourhood

     
#Speed Ratio UAV/target : grid/time

radius = 2
h = 20
l = 20

#number of simulation runs
number_of_runs = 1500


#maximum number of steps that UAV can make"
max_number_of_steps = 200


"Step 0: Generation of initial set, p+1 extreme points"

n = 3 #our problem is 3-dimensioned
V = np.zeros((n+1,n+1))

"logical solutions"
V[0,] = [1/6,1/6,1/6,1/2]
V[1,] = [1/2,1/6,1/6,1/6]
V[2,] = [1/6,1/2,1/6,1/6]
V[3,] = [1/6,1/6,1/2,1/6]

#calculating fitness function values of starting solutions 
f = Statistics_Plural(V, number_of_runs, n, l, h, max_number_of_steps, radius) 
f = [row[2] for row in f] 
f = np.array(f).flatten() #converting PoS values into array 
f  = f.reshape((4,1))

V = np.append(V,-f,axis= 1)

Result = np.zeros((1000*n, 5))
Result[0:4,] = V[0:4,]
Result_best = np.zeros((1000*n, 5))

"Step1: Order"
V_sort = V[V[:,n+1].argsort()]
V_sort

"parameters"
beta = 0.5
P_s = 0.75

start_time = time.time()
elapsed = 0  
k = 0
k_max = 500

"loop starts here"

while elapsed < 400:
    
    Result_best[k,] = V_sort[0,]
  
    #finding centroid
    X_cent = [np.mean(V_sort[0:n,0]),np.mean(V_sort[0:n,1]),np.mean(V_sort[0:n,2]),np.mean(V_sort[0:n,3])]
    X_cent = X_cent/sum(X_cent)
    X_cent
  
    #finding X.max
    X_max = V_sort[n,]
    g_X_max = X_max[n+1]
  
    #finding X.2max
    X_2max = V_sort[n-1,]
    g_X_2max = X_2max[n+1]
        
    #finding X.min
    X_min = V_sort[0,]
    g_X_min = X_min[n+1]
  
    #finding reflection point
    X_max = X_max[ : -1]
  
    #deciding alpha
    if X_max.all == X_cent.all:
        alpha = np.random.uniform(0.1, 1, 1)  
    else:
        alpha = Finding_Alpha(X_max, X_cent, n)
        X_ref = ((1+alpha) * X_cent) - (alpha * X_max)
        X_ref = X_ref / sum(X_ref)  #normalizing
  
    #dealing with negative probabilities
    if len(np.where(X_ref < 0)) > 0:
        g_X_ref = 1000
    else:
        g_X_ref = - Statistics_of_Simulation(X_ref, number_of_runs, l, h, max_number_of_steps, radius)[2]
                
    "Step 3a"
    if g_X_min <= g_X_ref and g_X_ref < g_X_2max:
        V_sort = V_sort[ : -1]
        X_ref = np.append(X_ref, g_X_ref)
        V_sort = np.vstack([V_sort, X_ref])
        Result[k+4,] = X_ref
    
    " Step 3b: Expand "
  
    #finding expanded point
    if len(X_ref) == 5:
        X_ref = X_ref[ : -1]
    
    if g_X_ref < g_X_min:
        gamma = Finding_Gamma(X_ref, X_cent, n)
        X_exp = (gamma * X_ref) + ((1 - gamma) * X_cent)
        X_exp = X_exp / sum(X_exp)
        
        #dealing with negative probabilities
        if len(np.where(X_ref < 0)) > 0:
            g_X_exp = 1000
        else:
            g_X_exp =  - Statistics_of_Simulation(X_exp, number_of_runs, l, h, max_number_of_steps, radius)[2]

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
            X_ref = X_ref[0:(n+1)]
            X_cont = (beta * X_ref) + ((1 - beta) * X_cent)
            X_cont = X_cont/sum(X_cont)
            
            if len(np.where(X_cont < 0)) > 0:
                g_X_cont = 1000
            else:
                g_X_cont = - Statistics_of_Simulation(X_exp, number_of_runs, l, h, max_number_of_steps, radius)[2]
     
            if g_X_cont <= g_X_ref:
                V_sort = V_sort[ : -1]
                X_cont = np.append(X_cont, g_X_cont)
                V_sort = np.vstack([V_sort, X_cont])
                Result[k+4,] = X_cont
                accept = 1
                
        #inside contraction
        if g_X_ref >= g_X_max:
            #contraction point
            X_cont = (beta * X_max) + ((1 - beta) * X_cent)
            X_cont = X_cont / sum(X_cont)
            g_X_cont = - Statistics_of_Simulation(X_cont, number_of_runs, l, h, max_number_of_steps, radius)[2]

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
                    a = (1 / V_sort[ : ,n+1])
                    F_total = sum(a)
                    
                    for i in range(n+1):
                        fitness_func.append((1 / V_sort[i,n+1]) / F_total)
          
                    N = V_sort[np.argmax(fitness_func),]
                    N = N[0:(n+1)]
                    X_ARS = Neighbourhood(N)
                    
                else:
                    #global search
                    X_ARS = np.random.dirichlet(np.ones(4),size=1)
                    X_ARS = X_ARS[0]
                    
                g_X_ARS = - Statistics_of_Simulation(X_ARS, number_of_runs, l, h, max_number_of_steps, radius)[2]
                cr1 += 1
                
                if g_X_ARS <= g_X_max :
                    V_sort = V_sort[ : -1]
                    X_ARS = np.append(X_ARS, g_X_ARS)
                    V_sort = np.vstack([V_sort, X_ARS])
                    Result[k+4,] = X_ARS
                    m = 10
                
    "Order"
    
    V = V_sort
    V_sort = V[V[:,n+1].argsort()]
    k += 1
    print(k)
        
    elapsed = time.time() - start_time #update the time elapsed   
    
"finding the best solution"

Result_sorted = Result[(Result[:,4]).argsort()]

Result_sorted_5 = np.zeros((5, 7))

Result_sorted_5[0:5,0:4] = Result_sorted[0:5,0:4] #taking first 5    

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


                     
