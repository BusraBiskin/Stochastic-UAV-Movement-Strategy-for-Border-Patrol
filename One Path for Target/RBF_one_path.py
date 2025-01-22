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


#calling functions 
from Statistics_Plural_Function import Statistics_Plural
from Statistics_of_Simulation_Function import Statistics_of_Simulation
from Global_Search_Function import Global_Search

     
#Speed Ratio UAV/target : grid/time
radius = 2
h = 20
l = 20
    
#number of simulation runs
number_of_runs = 1500


#maximum number of steps that UAV can make"
max_number_of_steps = 200
    
"Radial Basis Function"
   
"starting solutions"
n = 10
np.random.seed(0)

#random
V = np.zeros((n,4))
for i in range(0,n):
    V[i,] = np.random.dirichlet(np.ones(4),size=1)

#Latin Hypercube

#lhs_samples = pd.read_excel("LHS.xlsx")
#lhs_samples = lhs_samples.to_numpy()
#V = lhs_samples[0:n, :]

for i in range(n):
    a = sum(V[i,])
    V[i,0]= (V[i,0]/a)
    V[i,1]=(V[i,1]/a)
    V[i,2]=(V[i,2]/a)
    V[i,3]=(V[i,3]/a)

#calculating fitness function values of starting solutions 
f = Statistics_Plural(V, number_of_runs, n, l, h, max_number_of_steps, radius) 
f = [row[2] for row in f] 
f = np.array(f).flatten() #converting PoS values into array 
f = np.multiply(-1,f) #multiplying PoS values with -1 to use in minimization

start_time = time.time()
elapsed = 0  
k = 0
   
"iteration starts"

while elapsed <= 400:
    
    print(k)
    
    k += 1
            
    "set up optimization for finding coefficient W, AW = b"
        
    #creating coefficient matrix, A
    a = np.zeros((n,n))
    for i in range(n):
        for j in range(n):
            d = m.sqrt(sum((V[i,0:4] - V[j,0:4]) ** 2))
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
            for j in range(4):
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
        sum_x = 1
        for i in range(4):
            sum_x = sum_x - x[i]
        return sum_x
        
    #bounds on probabilities
    bs = (0, 1.0)
    bnds = (bs, bs, bs, bs)
        
    #starting solution, x0
    x0 = [0.25, 0.25, 0.25, 0.25]  
            
    #minimizing RBF
    cons1 = {'type': 'eq','fun':constraint1}
    cons = [cons1]
        
    #generate a random solution in each 5 iterations
    if k % 5 == 0:
        X = np.random.dirichlet(np.ones(4),size=1)
    #generate a solution with global search in each 20 iterations    
    if k % 20 == 0:
       X = Global_Search(V, n)
    else:
        sol = minimize(rbf, x0, method = 'SLSQP', bounds = bnds, constraints = cons)
        X = sol.x
        
        
    V = np.append(V,[X],axis= 0)
    PoS_X = Statistics_of_Simulation(X, number_of_runs, l, h, max_number_of_steps, radius)[2] 
    f = np.append(f,-1*PoS_X)
        
    n = n+1
    
    elapsed = time.time() - start_time #update the time elapsed       
    
    #iteration is over here.
    

"finding the best solution and resampling (5times)"
    
Result= np.c_[V,f] #adding fitness func value of solutions
    
Result_sorted = Result[Result[:,4].argsort()] #ordering solutions wrt fitness values, increasing order

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


