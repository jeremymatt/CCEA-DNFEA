# -*- coding: utf-8 -*-
"""
Created on Sun Jun 16 13:29:23 2019

@author: jmatt
"""

import pandas as pd
from collections import namedtuple

class parameter_container:
    """
    An empty object used to pass variables and data to a function
    """
    def __init__(self):
        breakhere=1
        
    def keys(self):
        """
        Return a list of tuples of the variable names and types
        """
        return [(x,type(self.__dict__[x])) for x in self.__dict__.keys()]

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
    var_ranges = pd.DataFrame()
    for var in data_cols:
        #Get the set of unique values for the current variable
        unique_vals = set(data.loc[~data[var].isna(),var])
        var_data.loc['max',var] = max(unique_vals)
        var_data.loc['min',var] = min(unique_vals)
        #If there are two unique values, the variable is binary
        if len(unique_vals)==2:
            var_data.loc['type',var] = 'binary'
        else:    
            #Convert the unique values to integers; if the integer values are
            #equal to the un-converted values, then the variable is contains
            #only integers.  Otherwise, call the variable a continuous variable
            unique_int = [int(x) for x in unique_vals]
            zipped = list(zip(unique_vals,unique_int))
            if all([x==y for x,y in zipped]):
                var_data.loc['type',var] = 'categorical'
            else:
                var_data.loc['type',var] = 'continuous'
    
    
    #Build dataframe of ranges
#    var_ranges = pd.DataFrame({'max':var_data.max(),'min':var_data.min(),'type':types}).transpose()
    
    return var_ranges



def gen_CC_clause_pop(var_ranges,new_pop, target_class, CC_stats):
    """
    Generates a random conjunctive clause given a set of variable ranges
    
    INPUTS
        var_ranges - pandas dataframe of variable ranges.  column names are 
            variable names and the min/max rows are labled as 'min' and 'max
            respectively
    
    OUTPUTS
        clause - a randomly generated clause
    """
    num_vars = len(var_ranges.keys())
    
    

def find_max_input_feature_order(data,y):
    """
    Finds the number of non-missing data in each of the input feature vectors
    
    
    INPUTS
        data - pandas dataframe of the input features and the outcome variable.
            Missing values must be denoted with NaN
        y - the name of the column in the pandas dataframe containing the 
            outcome variable
            
    OUTPUTS
        feat_order - pandas series containing the order of each feature vector
    """
    
    #Find the variable column names
    data_cols = [x for x in data.keys() if not x==y]
    
    feat_order = len(data_cols) - data[data_cols].isna().sum(axis=1)
    
    return feat_order
    
 
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