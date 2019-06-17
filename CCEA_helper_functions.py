# -*- coding: utf-8 -*-
"""
Created on Sun Jun 16 13:29:23 2019

@author: jmatt
"""

import pandas as pd
 
def calc_Nk(data,y,clause):
    """
    Finds the number of input feature vectors with no missing data for the 
    given clause for each output class.
    
    INPUTS
        data - pandas dataframe of the input features and the outcome variable.
            Missing values must be denoted with NaN
        y - the name of the column in the pandas dataframe containing the 
            outcome variable
        clause - List of variables included in the current conjunctive clause 
            (for a CCEA) or disjunctive normal form clause (for a DNFEA)
    """
    
    #find all NaN values
    is_missing = data[clause].isna()
    #Mask all rows missing at one or more value
    is_missing = is_missing.any(axis=1)
    #Extract the non-missing output values
    nm = data.loc[~is_missing,y]
    #Find the number of complete input feature vectors for each class
    class_counts = nm.value_counts()
    #Find the set of classes in the full dataset (required in case there is a
    #class for which all input feature vectors are missing at least one value)
    classes = set(data[y])
    
    Nk = {}
    #For each class, try to add the count to the dictionary, otherwise set the 
    #count to zero
    for k in classes:
        try: Nk[k] = class_counts[k]
        except: Nk[k] = 0
