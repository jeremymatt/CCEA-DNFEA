# -*- coding: utf-8 -*-
"""
Created on Tue Jun 25 22:58:21 2019

@author: jmatt
"""

import numpy as np
import matplotlib.pyplot as plt

max_val = 5
min_val = 2
feature_val = 2

lb_trace = []
ub_trace = []
for i in range(1000):
    
    #Define a continuous range beginning and ending on integers
    #Select a lower bound on the integers in [min_val,feature_val]
    lb = np.random.randint(feature_val+1-min_val)+min_val
    #Select an upper bound on the integers in [lb,max_val]
    ub = np.random.randint(max_val+1-feature_val)+feature_val
    #If the selected bounds contain the entire range (which would 
    #indicate that the variable would have no contribution towards
    #discriminating the output), randomly select either the upper 
    #or lower bound to shift.
    if (lb==min_val)&(ub == max_val): 
        if feature_val == min_val:
            decrease_ub = True
        elif feature_val == max_val:
            decrease_ub = False
        elif np.random.rand()>0.5:
            decrease_ub = True
        else:
            decrease_ub = False
            
        if decrease_ub:
            #Calculate the adjustment as a random integer between 1 and
            #the difference between the min and max
            adjustment = np.random.randint(max_val-feature_val)+1
            ub-=adjustment
        else:
            #Calculate the adjustment as a random integer between 
            #the difference between the min and max
            adjustment = np.random.randint(feature_val-min_val)+1
            lb+=adjustment
    
    lb_trace.append(lb)
    ub_trace.append(ub)
   
plt.figure()
plt.hist(lb_trace)
plt.figure()
plt.hist(ub_trace)
