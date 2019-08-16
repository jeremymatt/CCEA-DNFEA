# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time


L = 100

Pw = 1
Pz = .25
num_reps=400
num_runs = 50

Pw_Pz_ratio = Pz/Pw

predicted = L/2-(L/2)*(.5-.5*Pw_Pz_ratio)

print('predicted: {}'.format(predicted))




traces = []

tic = time.time()
for i in range(num_runs):
    clause = np.ones(L)
    trace = []
    for i in range(num_reps):
        
        to_mutate = pd.DataFrame(np.random.rand(L)<1/L)
        
        if not to_mutate.any()[0]:
            to_mutate.loc[np.random.randint(L)] = True
            
#        features_to_mutate = list(to_mutate[to_mutate[0]==True].index)
        
        #Worse time as below, around 30-sec
#        for feature,to_flip in enumerate(to_mutate.values):
#            if to_flip & (clause[feature]==0) & (np.random.rand(1)[0] < Pz):
#                clause[feature]=1
#            elif to_flip & (clause[feature]==1) & (np.random.rand(1)[0] < Pw):
#                clause[feature]=0
#        
        #Similar time as below (9.7-9.8 sec)
#        for feature,to_flip in enumerate(to_mutate.values):
#            if to_flip:
#                if (clause[feature]==0) & (np.random.rand(1)[0] < Pz):
#                    clause[feature]=1
#                elif np.random.rand(1)[0] < Pw:
#                    clause[feature]=0
        
        for feature,to_flip in enumerate(to_mutate.values):
            if to_flip:
                if clause[feature]==0:
                    if np.random.rand(1)[0] < Pz:
                        clause[feature]=1
                else:
                    if np.random.rand(1)[0] < Pw:
                        clause[feature]=0
            
        
#        for feature in range(L):
#            if np.random.rand(1)[0] < 1/L:
#                if clause[feature]==0:
#                    if np.random.rand(1)[0] < Pz:
#                        clause[feature]=1
#                else:
#                    if np.random.rand(1)[0] < Pw:
#                        clause[feature]=0
                
        trace.append(np.sum(clause))
        
    traces.append(trace)
    

toc = time.time()
print('Runtime: {:.1f}sec'.format(toc-tic))
            
    
yval = np.array(traces)
yval = yval.mean(axis=0)
    
plt.plot(range(num_reps),yval)
plt.plot([0,num_reps],[predicted,predicted],'r--')
plt.grid()
plt.xlabel('Mutation Num')
plt.ylabel('CC Order')
