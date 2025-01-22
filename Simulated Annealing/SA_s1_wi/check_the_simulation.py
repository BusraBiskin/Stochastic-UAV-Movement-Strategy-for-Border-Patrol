#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 15:21:14 2024

@author: busrabiskin
"""
import numpy as np
import math
from statistics import mean
import pandas as pd
import random

from UAV_Movement_Function import UAV_Movement
from Distance_Matrix_Function import Distance_Matrix

number_of_runs = 1500
l = 56 
h = 61 
radius = 40
ratio = 10

#different paths for the target
loc_target_1 = pd.read_excel("TargetPathCoordinates - 1.xlsx")
loc_target_2 = pd.read_excel("TargetPathCoordinates - 2.xlsx")
loc_target_3 = pd.read_excel("TargetPathCoordinates - 3.xlsx")

loc_UAV = pd.read_excel("UAVCoordinates.xlsx")

#creates different distance matrices
Dist_Matrix_1 = Distance_Matrix(loc_target_1, loc_UAV, h)
Dist_Matrix_2 = Distance_Matrix(loc_target_2, loc_UAV, h)
Dist_Matrix_3 = Distance_Matrix(loc_target_3, loc_UAV, h)
    

PoS_matrix = []
ET_matrix = []

M = [0.633, 0.001, 0.001, 0.365]

for i in range(100):
    
    Trials = []
    Success = []
    
    for j in range(number_of_runs):
        #target chooses a path, randomly
        path = random.randint(0,2)
             
        if path == 0:
            Dist_Matrix = Dist_Matrix_1
        elif path == 1:
            Dist_Matrix = Dist_Matrix_2
        else:
            Dist_Matrix = Dist_Matrix_3             
                
        #UAV starting location
        u = [0, 0]
                
        D = 0
        t = 0
                
        while D < 1 and t < (Dist_Matrix.shape[1]-1)*ratio :
            
            "Signal Part"
            if t == 3*(ratio) and (path == 0 or path == 1): 
                 
                 geo_dist = Dist_Matrix[u[1] * (h+1) + u[0], int(t/ratio)]
                 t += int(geo_dist/10)
                
                 u = [48,26]
              
            u = UAV_Movement(u, M, l, h)
                 
            t = t + 1
                
            #find the distance between target's position and UAV  
            geo_dist = Dist_Matrix[ u[1] * (h+1) + u[0], int(t/ratio) ]
                     
            if  (geo_dist <= radius) :
                D = 1
                                                                                    
        if D == 1 :
            Success.append(1)
            Trials.append(t)
        else:
            Success.append(0)
            Trials.append(10000)
                    
    if Trials.count(10000) > 0 :
        Trials = list(filter(lambda x: x != 10000, Trials))
                
    ET = np.average(Trials)
    SD = np.std(Trials)        
    NS = sum(Success)
    PoS = NS / number_of_runs #proportion of success
        
    PoS_matrix.append(PoS)  
    ET_matrix.append(ET)                  

print(mean(PoS_matrix))
print(mean(ET_matrix))
    
    