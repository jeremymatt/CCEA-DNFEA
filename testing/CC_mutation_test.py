# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
import matplotlib.pyplot as plt


L = 100
Pw = .25
num_reps=500
num_runs = 50



traces = []
for i in range(num_runs):
    clause = np.zeros(L)   
    trace = []
    for i in range(num_reps):
        
        
        feature = np.random.randint(L)
        if clause[feature]==0:
            clause[feature]=1
        else:
            if np.random.rand(1)[0] < Pw:
                clause[feature]=0
                
        trace.append(np.sum(clause))
        
    traces.append(trace)
    
yval = np.array(traces)
yval = yval.mean(axis=0)
    
plt.plot(range(num_reps),yval)
