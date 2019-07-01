# -*- coding: utf-8 -*-
"""
Created on Wed Jun 26 23:46:17 2019

@author: jmatt
"""

import pandas as pd
import numpy as np


crit = pd.DataFrame()
crit.loc['lb','V1'] = 4.0
crit.loc['ub','V1'] = 8.0

crit.loc['lb','V2'] = -8.14132
crit.loc['ub','V2'] = 33.9162

crit.loc['target','V3'] = 1.0
crit.loc['lb','V4'] = np.NaN  #NEED TO INIT COLUMN
crit = crit.astype('object')  #AND THEN CHANGE DTYPE
crit.at['target','V4'] = set([1,2,3])
crit
crit = pd.DataFrame(crit,dtype=object)
crit.at['target','V4'] = set([1,2,3])
crit
