# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 09:31:35 2019

@author: jmatt
"""
import numpy as np
import pandas as pd

md = pd.DataFrame()

try: md
except: print('does not exist')

md['V1'] = [True,True,True,False]
md['V2'] = [False,True,True,True]
md['V3'] = [True,False,True,True]

md.all(axis=1)


md.drop('V1',axis=1,inplace=True)

t = 'one'
t2 = 'two2'

if (t=='one')|(t2 == 'two'):
    print('true')
else:
    print('false')
    
lb_matches = data[feature]>new_pop[0].criteria.loc['lb',feature]
ub_matches = data[feature]<new_pop[0].criteria.loc['ub',feature]

t = lb_matches&ub_matches

tt = pd.DataFrame({'lb':lb_matches,'ub':ub_matches,'t':t})


tt = pd.Series([1,2,6,6,6,7,3,7,4])
t = {2,3,4}

match = tt in t

tt.isin(t)
 


pd.DataFrame.i
tt = 2 in t
tt
print(tt)


