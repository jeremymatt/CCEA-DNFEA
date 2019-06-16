# -*- coding: utf-8 -*-
"""
Created on Sun Jun 16 10:46:14 2019

@author: jmatt
"""

import pandas as pd
import numpy as np


def make_test(n,perc_missing = 25):
    """
    Make a test set of 10 variables with n entries of binary, categorical, and 
    realvalued variables.  5 of the variables (1,4,5,8,10) are significant:
        output=(1&8)|(5&8&10)|(1&10)|4
    """
    
    V1 = np.random.randint(3,high=10,size=n) #5,6,7
    V2 = np.random.normal(loc=20,scale=10,size=n) 
    V3 = np.random.randint(0,high=2,size=n) 
    V4 = np.random.exponential(scale=5,size=n) #>15
    V5 = np.array([0 if x<.25 else 1 for x in np.random.rand(n)]) #1
    V6 = np.random.exponential(scale=1,size=n)
    V7 = np.random.normal(loc=5,scale=2,size=n) 
    V8 = np.random.normal(loc=10,scale=2,size=n)  #>11
    V9 = [0 if x<.25 else 1 for x in np.random.rand(n)] 
    V10 = np.round(np.random.normal(loc=20,scale=10,size=n)) #18<X<22
    
    V1_bool = (V1>=5)&(V1<=7)
    V4_bool = V4>13
    V5_bool = V5>.5
    V8_bool = V8>8
    V10_bool = (V10>=15)&(V10<=28)
    
    
    P1 = (V1_bool&V8_bool)
    P2 = (V5_bool&V8_bool&V10_bool)
    P3 = (V1_bool&V10_bool)
    P4 = V4_bool
    OutBool = P1|P2|P3|P4
    
    y = [1 if x else 0 for x in OutBool]
    
    data = pd.DataFrame()
    data['V1'] = V1
    data['V2'] = V2
    data['V3'] = V3
    data['V4'] = V4
    data['V5'] = V5
    data['V6'] = V6
    data['V7'] = V7
    data['V8'] = V8
    data['V9'] = V9
    data['V10'] = V10
    data['y'] = y
    
    cols = data.keys()[:-1]
    rows = range(n)
    
    num_missing = np.round(n*perc_missing/100).astype(int)
    for i in range(num_missing):
        row = np.random.choice(rows)
        col = np.random.choice(cols)
        data.loc[row,col] = np.nan
        
    return data