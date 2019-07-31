# -*- coding: utf-8 -*-
"""
Created on Sun Jun 16 13:04:27 2019

@author: jmatt
"""

import numpy as np
import pandas as pd

from make_test import make_test
import CCEA_DNFEA_functions as fcn



param = fcn.parameter_container()
CC_stats = fcn.parameter_container()

data = make_test(15,perc_missing=10,inc_uni_valued=True)




param.y='y'
param.var_ranges = fcn.find_ranges(data,param)
param.data_features = [x for x in data.keys() if not x==param.y]
param.num_features = len(param.data_features)
param.feature_order = fcn.find_max_input_feature_order(data,param)
param.treat_int_as_categorical = False
CC_stats.matched_input_vectors = pd.Series(np.zeros(data.shape[0]))

num_new_pop = 2
pop = fcn.gen_CC_clause_pop(data,param,num_new_pop,CC_stats)

