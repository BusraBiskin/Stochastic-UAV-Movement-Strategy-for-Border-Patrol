# -*- coding: utf-8 -*-
"""
Created on Wed May 18 11:38:02 2022

@author: bb2r20
"""

import time
import numpy as np
import pandas as pd
import random
import sys
import math as m
import matplotlib.pyplot as plt
from scipy.optimize import fsolve , minimize 
#sys.path.append('//filestore.soton.ac.uk/users/bb2r20/mydesktop/RBF-with real coordinates')

#calling functions 
from Statistics_Plural_Function import Statistics_Plural
from Statistics_of_Simulation_Function import Statistics_of_Simulation
from Global_Search_Function import Global_Search
from Distance_Matrix_Function import Distance_Matrix
     
#Speed Ratio UAV/target : grid/time
ratio = 10
radius = 20
h = 61
l = 56
    
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


#change probability set after n moves
time_step = 50


"Radial Basis Function"
    
"starting solutions"
    
#random statring solution generation
np.random.seed(0) #to have the same p each time
# n: number of starting solutions
n = 20
V = np.zeros((n,8))
for i in range(n):
    V[i,0:4] = np.random.dirichlet(np.ones(4),size=1)
    V[i,4:8] = np.random.dirichlet(np.ones(4),size=1)
        
#calculating fitness function values of starting solutions 
f = Statistics_Plural(V, number_of_runs, n, ratio, l, h, max_number_of_steps, Dist_Matrix_1, Dist_Matrix_2, Dist_Matrix_3, radius, time_step) 
f = [row[2] for row in f] 
f = np.array(f).flatten() #converting PoS values into array 
f = np.multiply(-1,f) #multiplying PoS values with -1 to use in minimization
   
start_time = time.time()
elapsed = 0
k = 0  
    
"iteration starts"
while elapsed < 400:
    
    print(k)
    k += 1
        
    
    "set up optimization for finding coefficient W, AW = b"
        
    #creating coefficient matrix, A
    a = np.zeros((n,n))
    for i in range(n):
        for j in range(n):
            d = m.sqrt(sum((V[i,0:8] - V[j,0:8]) ** 2))
            if d == 0:
                a[i,j] = 0
            else:
                a[i,j] = (pow(d,2)) * (m.log10(d))
    A = a
        
    #creating RHS, b
    b = f
                
    #finding variables, Wi
    W= np.linalg.lstsq(A, b, rcond=None)[0]
        
    "defining and minimizing Radial Basis Function"
        
    #defining RBF
    def rbf(x):
        sum_rbf = 0
        for i in range(n):
            sub_sum = 0
            for j in range(8):
                sub_sum = sub_sum + (x[j] - V[i,j]) ** 2
            d = m.sqrt(sub_sum)#
            if d == 0:
                sum_rbf = sum_rbf
            else:    
                sum_rbf= sum_rbf + W[i] * (d**2) * (m.log10(d))
        return sum_rbf
        
    #defining constraints
        
    #sum of probabilities should equal to 1
    def constraint1(x):
        sum_x1 = 1
        for i in range(4):
            sum_x1 = sum_x1 - x[i]
        return sum_x1
    
    def constraint2(x):
        sum_x2 = 1
        for i in range(4,8):
            sum_x2 = sum_x2 - x[i]
        return sum_x2
        
    #bounds on probabilities
    bs = (0.001, 1.0)
    bnds = (bs, bs, bs, bs, bs, bs, bs, bs)
        
    #starting solution, x0
    x0 = [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25]  
            
    #minimizing RBF
    cons1 = {'type': 'eq','fun':constraint1}
    cons2 = {'type': 'eq','fun':constraint2}
    cons = [cons1, cons2]
    
    #generate a random solution in each 5 iterations
    X = np.zeros(8)
    if k % 5 == 0:
        X[0:4] = np.random.dirichlet(np.ones(4), size=1)
        X[4:8] = np.random.dirichlet(np.ones(4), size=1)
    #generate a solution with global search in each 20 iterations    
    if k % 20 == 0:
        X = Global_Search(V, n)
    else:
        sol = minimize(rbf, x0, method = 'SLSQP', bounds = bnds, constraints = cons)
        X = sol.x
        
    V = np.append(V,[X],axis= 0)
    PoS_X = Statistics_of_Simulation(X, number_of_runs, ratio, l, h, max_number_of_steps, Dist_Matrix_1, Dist_Matrix_2, Dist_Matrix_3, radius,time_step)[2]
        
    f = np.append(f,-1*PoS_X)
    
    n = n+1
        
  
    #iteration is over here.
    
    elapsed = time.time() - start_time #update the time elapsed  
    

"finding the best solution and resampling (5times)"
    
Result= np.c_[V,f] #adding fitness func value of solutions
Result_sorted = Result[Result[:,8].argsort()] #ordering solutions wrt fitness values, increasing order
Result_sorted_5 = Result_sorted[0:5,] #taking first 5 

resampled_best = np.zeros((5,11))
#resampling V_sort
for j in range(5):
    
    resampled = np.zeros((5,3))
    for i in range(5):
        resampled[i,0:3] = Statistics_of_Simulation(Result_sorted_5[j,0:8], number_of_runs, ratio, l, h, max_number_of_steps, Dist_Matrix_1,Dist_Matrix_2,Dist_Matrix_3, radius, time_step)[0:3]
    
    resampled_best[j,0:8] = Result_sorted_5[j,0:8]
    resampled_best[j,8] = np.average(resampled[0:4,0])
    resampled_best[j,9] = np.average(resampled[0:4,1])
    resampled_best[j,10] = np.average(resampled[0:4,2])

"best solution"
best_soln_sort = resampled_best[(resampled_best[:,10]).argsort()]
best_soln = best_soln_sort[3,0:11]



