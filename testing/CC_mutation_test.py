# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
import matplotlib.pyplot as plt


L = 100
Pw =1
Pz = .25
num_reps=1000
num_runs = 50
#
#Pw_Pz_ratio = Pz/Pw
#
#predicted = L-L*(.5-.5*Pw_Pz_ratio)
#
#print('predicted: {}'.format(predicted))




traces = []
for i in range(num_runs):
    clause = np.ones(L)   
    trace = []
    for i in range(num_reps):
        
        for feature in range(L):
            if np.random.rand(1)[0] < 1/L:
                if clause[feature]==0:
                    if np.random.rand(1)[0] < Pz:
                        clause[feature]=1
                else:
                    if np.random.rand(1)[0] < Pw:
                        clause[feature]=0
                
        trace.append(np.sum(clause))
        
    traces.append(trace)
    
yval = np.array(traces)
yval = yval.mean(axis=0)
    
plt.plot(range(num_reps),yval)
plt.plot([0,num_reps],[predicted,predicted],'r--')
plt.grid()
plt.xlabel('Mutation Num')
plt.ylabel('CC Order')
