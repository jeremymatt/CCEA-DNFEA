# -*- coding: utf-8 -*-
"""
Created on Sun Jun 16 13:29:23 2019

@author: jmatt
"""

import pandas as pd
from collections import namedtuple

def find_ranges(data,y):
    """
    Finds the ranges of each input variable and returns a dataframe of the min 
    and max values
    
    INPUTS
        data - pandas dataframe of the input features and the outcome variable.
            Missing values must be denoted with NaN
        y - the name of the column in the pandas dataframe containing the 
            outcome variable
            
    OUTPUTS
        var_ranges - pandas dataframe containing the variable ranges
    """
    
    #Find the variable column names
    data_cols = [x for x in data.keys() if not x==y]
    #Extract the variable data
    var_data = pd.DataFrame(data[data_cols])
    
    
    types =[]
    #Determine if the variable is binary, integer, or continuous as a way
    #to reduce the search space
    for var in data_cols:
        #Get the set of unique values for the current variable
        unique_vals = set(data.loc[~data[var].isna(),var])
        #If there are two unique values, the variable is binary
        if len(unique_vals)==2:
            types.append('bin')
        else:    
            #Convert the unique values to integers; if the integer values are
            #equal to the un-converted values, then the variable is contains
            #only integers.  Otherwise, call the variable a continuous variable
            unique_int = [int(x) for x in unique_vals]
            zipped = list(zip(unique_vals,unique_int))
            if all([x==y for x,y in zipped]):
                types.append('int')
            else:
                types.append('cont')
    
    
    #Build dataframe of ranges
    var_ranges = pd.DataFrame({'max':var_data.max(),'min':var_data.min(),'type':types}).transpose()
    
    return var_ranges



def rand_CC_clause(var_ranges):
    """
    Generates a random conjunctive clause given a set of variable ranges
    
    INPUTS
        var_ranges - pandas dataframe of variable ranges.  column names are 
            variable names and the min/max rows are labled as 'min' and 'max
            respectively
    
    OUTPUTS
        clause - a randomly generated clause
    """
 
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
            
    OUTPUTS
        Nk - dict containg the number of complete input feature vectors for
            each output class
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
        
    return Nk


def calc_Nmatchk(data,y,):
    """
    
    """
    
    t=1