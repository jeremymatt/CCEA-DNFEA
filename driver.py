# -*- coding: utf-8 -*-
"""
Created on Sun Jun 16 13:04:27 2019

@author: jmatt
"""

import numpy as np
import pandas as pd

from make_test import make_test
import CCEA_DNFEA_functions as fcn


y='y'

param = fcn.parameter_container()
CC_stats = fcn.parameter_container()

data = make_test(10,perc_missing=10)

param.var_ranges = fcn.find_ranges(data,y)
param.feature_order = fcn.find_max_input_feature_order(data,y)
CC_stats.matched_input_vectors = pd.Series(np.zeros(data.shape[0]))

