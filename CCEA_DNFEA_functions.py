# -*- coding: utf-8 -*-
"""
Created on Sun Jun 16 13:29:23 2019

@author: jmatt
"""

import pandas as pd
import numpy as np
from collections import namedtuple

class parameter_container:
    """
    An empty object used to pass variables and data between functions
    """
    def __init__(self):
        breakhere=1
        
    def keys(self,prnt=True):
        """
        Return a list of tuples of the variable names and types
        
        INPUTS
            prnt - (default = True) print the keys and types.  False return
                as a list of key/type tuples
                
        OUTPUTS
            keylist - a list of key/type tuples
        """
        
        keylist = sorted([(x,type(self.__dict__[x])) for x in self.__dict__.keys()])
        if prnt:
            #print column width
            CW = 40 
            #print header
            print('{: ^{CW}}|{: ^{CW}}'.format(
                    'Variable',
                    'Type',
                    CW=CW))
            print('{:-^{CW}}|{:-^{CW}}'.format(
                    '-',
                    '-',
                    CW=CW))
            #Print sorted keys
            for name,v_type in keylist:
                print('{: ^{CW}}| {: <{CW}}'.format(
                        name,
                        str(v_type),
                        CW=CW))    
        else:
            return  keylist
        
class CC_clause:
    """
    An object to contain a single conjunctive clause
    """
    def __init__(self,data,param,source_feature,clause_order):
        """
        Initialize the clause based on the selected source_feature
    
        INPUTS
            data - pandas dataframe of the input features and the outcome variable.
                Missing values must be denoted with NaN
            y - the name of the column in the pandas dataframe containing the 
                outcome variable
            param - an object containing control parameters
            source_feature - index of the feature used as a template for the CC
            order - the order of the CC
        
        """
        
        feature_data = data.loc[source_feature,param.variable_keys]
        candidate_features = list(feature_data[~feature_data.isna()].index)
        self.features = np.random.choice(candidate_features,size=clause_order,replace=False)
        self.order = clause_order
        
        for feature in self.features:
            #decide ranges
            if param.var_ranges == 'integer':
                maxi = param.var_ranges.loc['max',feature]
                mini = param.var_ranges.loc['min',feature]
                lb = np.random.randint(maxi+1-mini)+mini
                ub = np.random.randint(maxi+1-lb)+lb
                
                
            elif param.var_ranges == 'continuous':
                bh=1
            elif param.var_ranges == 'binary':
                bh=1
            elif param.var_ranges == 'categorical':
                bh=1
        
        
    def identify_matches(self,inputvars):
        """
        docstring
        """
        breakhere=1
        
        
    def calc_fitness(self,inputvars):
        """
        docstring
        """
        breakhere=1
        

def find_ranges(data,param):
    """
    Finds the ranges of each input variable and returns a dataframe of the min 
    and max values
    
    INPUTS
        data - pandas dataframe of the input features and the outcome variable.
            Missing values must be denoted with NaN
        param
            .y - the name of the column in the pandas dataframe containing the 
            outcome variable
            
    OUTPUTS
        var_ranges - pandas dataframe containing the variable ranges
    """
    
    #Find the variable column names
    data_cols = [x for x in data.keys() if not x==param.y]
    #Extract the variable data
    var_data = pd.DataFrame(data[data_cols])
    
    
    types =[]
    #Determine if the variable is binary, integer, or continuous as a way
    #to reduce the search space
    var_ranges = pd.DataFrame()
    var_to_drop = []
    for var in data_cols:
        #Get the set of unique values for the current variable
        unique_vals = set(data.loc[~data[var].isna(),var])
#        var_ranges['set',var] = np.NaN
        breakhere=1
        
        #If there are less than 2 unique values, warn user of useless variable 
        #and add variable to the droplist
        if len(unique_vals)<2:
            print('WARNING:')
            print('     Variable {} contains {} unique, non-NaN values and contains no useful information'.format(var,len(unique_vals)))
            print('     Dropping Variable {} from the dataset'.format(var))
            var_to_drop.append(var)
        else:
            #test to see if values are numeric
            try: 
                t = np.array(list(unique_vals))+2 
                is_numeric = True
            except:
                is_numeric = False
                
            #If the values are all numeric, find the min and max, and categorize
            #as binary, integer, or continuous
            if is_numeric:
                var_ranges.loc['max',var] = max(unique_vals)
                var_ranges.loc['min',var] = min(unique_vals)
                #If there are two unique values, the variable is binary
                if len(unique_vals)==2:
                    var_ranges.loc['type',var] = 'binary'
                    var_ranges.at['set',var] = unique_vals
                else:    
                    #Convert the unique values to integers; if the integer values are
                    #equal to the un-converted values, then the variable is contains
                    #only integers.  Otherwise, call the variable a continuous variable
                    unique_int = [int(x) for x in unique_vals]
                    zipped = list(zip(unique_vals,unique_int))
                    if all([x==y for x,y in zipped]):
                        var_ranges.loc['type',var] = 'integer'
                        var_ranges.at['set',var] = unique_vals
                    else:
                        var_ranges.loc['type',var] = 'continuous'
                        
            else:    
                var_ranges.loc['max',var] = np.NaN
                var_ranges.loc['min',var] = np.NaN
                var_ranges.loc['type',var] = 'categorical'
                var_ranges.at['set',var] = unique_vals
                print('WARNING: \n     Variable {} contains non-numeric data.'.format(var))
                
            
    
    data.drop(columns=var_to_drop,inplace=True)
#    var_ranges.drop(columns=var_to_drop,inplace=True)
    
    return var_ranges



def gen_CC_clause_pop(param,new_pop, target_class, CC_stats):
    """
    Generates a random conjunctive clause given a set of variable ranges
    
    INPUTS
        var_ranges - pandas dataframe of variable ranges.  column names are 
            variable names and the min/max rows are labled as 'min' and 'max
            respectively
    
    OUTPUTS
        clause - a randomly generated clause
    """
    
    new_pop_list = []
    for i in new_pop:
        clause_order = np.random.randint(param.num_features)
        candidate_mask = param.feature_order>=clause_order
        cand_match_counts = CC_stats.matched_input_vectors[candidate_mask]
        source_feature = sel_input_feature(cand_match_counts)
        
        new_pop_list.append(CC_clause(data,param,source_feature,clause_order))
        
        inputvars = 'figure these out'
        new_pop_list[-1].identify_matches(inputvars)
        new_pop_list[-1].calc_fitness(inputvars)
        
def sel_input_feature(cand_match_counts):
    """
    Selects an input feature as the 'template'.  The probability of a feature 
    being selected is inversely proportional to the number of clauses it is 
    matched by
    
    INPUTS
        CC_stats
                .matched_input_vectors - a pandas series containing the match
                    counts
        candidates - the input feature vectors that have enough non-NaN values
            to build a clause of the desired order
            
    OUTPUTS
        feature - the index of the selected feature
        
    """
    
    #Find the number of times input feature vectors are matched
    num_matched = sum(cand_match_counts)
    
    #If none are matched, use a uniform probability of selection
    if num_matched == 0:
        selection_PMF = (1-cand_match_counts)/sum(1-cand_match_counts)
    else:
        #The probability mass function that a feature is matched
        match_PMF = cand_match_counts/sum(cand_match_counts)
        #The probability mass function that a feature will be selected
        selection_PMF = (1-match_PMF)/sum(1-match_PMF)
    
    #The cumulative distribution function for selection
    selection_CDF = selection_PMF.cumsum()
    
    #Randomly select a feature
    rand = np.random.rand()
    feature = list(selection_CDF[selection_CDF>=rand].index)[0]
    print(feature)
    
    return feature
    
    

def find_max_input_feature_order(data,param):
    """
    Finds the number of non-missing data in each of the input feature vectors
    
    
    INPUTS
        data - pandas dataframe of the input features and the outcome variable.
            Missing values must be denoted with NaN
        param
            .y - the name of the column in the pandas dataframe containing the 
            outcome variable
            
    OUTPUTS
        feat_order - pandas series containing the order of each feature vector
    """
    
    #Find the variable column names
    data_cols = [x for x in data.keys() if not x==param.y]
    
    feat_order = len(data_cols) - data[data_cols].isna().sum(axis=1)
    
    return feat_order
    
 
def calc_Nk(data,param,clause):
    """
    Finds the number of input feature vectors with no missing data for the 
    given clause for each output class.
    
    INPUTS
        data - pandas dataframe of the input features and the outcome variable.
            Missing values must be denoted with NaN
        param
            .y - the name of the column in the pandas dataframe containing the 
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
    classes = set(data[param.y])
    
    Nk = {}
    #For each class, try to add the count to the dictionary, otherwise set the 
    #count to zero
    for k in classes:
        try: Nk[k] = class_counts[k]
        except: Nk[k] = 0
        
    return Nk


def calc_Nmatchk(data,param,):
    """
    
    """
    
    t=1