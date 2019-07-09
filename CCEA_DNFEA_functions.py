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
    def __init__(self,data,param,source_input_vector,clause_order):
        """
        Initialize the clause based on the selected source_feature.  Force the
        target ranges for each variable to be such that the clause will match
        the source feature
    
        INPUTS
            data - pandas dataframe of the input features and the outcome variable.
                Missing values must be denoted with NaN
            y - the name of the column in the pandas dataframe containing the 
                outcome variable
            param - an object containing control parameters
            source_input_vector - index of the feature used as a template for the CC
            order - the order of the CC
        
        """
        
#        
#        """
#        remove next lines
#        """
#        source_input_vector = 6
        
        #extract the data associated with the feature
        input_vector_data = data.loc[source_input_vector,param.variable_keys]
        #Find the candidates with valid values
        candidate_features = list(input_vector_data[~input_vector_data.isna()].index)
        #Randomly select clause_order features without replacement and store
        #in self
        self.source_input_vector = source_input_vector
        self.features = np.random.choice(candidate_features,size=clause_order,replace=False)
        
#        """
#        remove next lines
#        """
#        self.features = np.array(['V2','V7','V6','V13'])
        
        self.order = clause_order
        self.target_class = data.loc[source_input_vector,param.y]
                
        #decide ranges
        self.criteria = pd.DataFrame(dtype=object)
        for feature in self.features:
            #Extract the max and min values of the feature
            max_val = param.var_ranges.loc['max',feature]
            min_val = param.var_ranges.loc['min',feature]
            #Extract the feature value for the source target input vector
            feature_val = input_vector_data[feature]
            feature_type = param.var_ranges.loc['type',feature]
            
            if feature_type == 'integer':     
                lb,ub = range_calc_integer(max_val,min_val,feature_val)
                self.criteria.loc['lb',feature] = lb
                self.criteria.loc['ub',feature] = ub
                
            elif feature_type == 'continuous':
                #select a lower bound between the min value and the feature
                #value
                lb = np.random.rand()*(feature_val-min_val)+min_val
                #select an upper bound between the feature value and the max
                #value
                ub = np.random.rand()*(max_val-feature_val)+feature_val
                self.criteria.loc['lb',feature] = lb
                self.criteria.loc['ub',feature] = ub
                
#                print('Feature: {}, Value: {}, global min/max: {}/{}, lb: {}, ub: {}'.format(feature,feature_val,min_val,max_val,lb,ub))
                
            elif feature_type == 'binary':
                #Only one choice for binary to ensure clause matches input
                #feature vector
                self.criteria.loc['lb',feature] = np.NaN
                self.criteria = self.criteria.astype(object)
                self.criteria.at['target',feature] = feature_val
                
            elif feature_type == 'categorical':
                #Store the set of all values
                all_feature_values = param.var_ranges.loc['set',feature]
                #The maximum number of values the rule can match is one less 
                #than the total number of values (or it would match everything
                #and would not provide any useful info)
                max_elements = len(all_feature_values)-1
                #Determine the number of elements from the value set to include
                num_to_select = np.random.randint(max_elements)
                #select the values to include in the rule set. NOTE: This may
                #or may not include the value of the target input feature
                selected_values = np.random.choice(list(all_feature_values),size=num_to_select,replace=False)
                #Force the value of the target input feature to be in the 
                #rule set
                target = set([feature_val])
                #Add the previously selected values to the rule set
                target = target.union(selected_values)
                #Store in self.criteria
                self.criteria.loc['lb',feature] = np.NaN
                self.criteria = self.criteria.astype(object)
                self.criteria.at['target',feature] = target
            else:
                print('ERROR: unknown feature type ({}) for feature {}'.format(feature_type,feature))
                
                
#        print(self.criteria)
        
    def identify_matches(self,data,param,features_to_update = 'all'):
        """
        Identifies the input feature vectors that the clause matches
        """
        #if all, update all features
        if features_to_update == 'all':
            features_to_update = self.features
            
        #Check if dictionary of matches exists, if it doesn't, create
        try: self.matches
        except: self.matches = pd.DataFrame()
        
        for feature in features_to_update:
            feature_type = param.var_ranges.loc['type',feature]
            
            if (feature_type == 'integer')|(feature_type == 'continuous'):
                lb_matches = data[feature]>=self.criteria.loc['lb',feature]
                ub_matches = data[feature]<=self.criteria.loc['ub',feature]
                self.matches[feature] = lb_matches&ub_matches
                
                
            elif feature_type == 'binary':                
                self.matches[feature] = data[feature]==self.criteria.loc['target',feature]
                
            elif feature_type == 'categorical':
                self.matches[feature] = data[feature].isin(self.criteria.loc['target',feature])
            else:
                print('ERROR: unknown feature type ({}) for feature {}'.format(feature_type,feature))
                
        self.matches['clause_match'] = self.matches.all(axis=1) 
            
        
        
    def calc_fitness(self,inputvars):
        """
        docstring
        """
        breakhere=1
 

        
def range_calc_integer(max_val,min_val,feature_val):
    """
    Generates a range with integer start & end points that:
        1. does not contain both the minimum and the maximum value in the 
            data, and
        2. contains the feature value
        
    INPUTS
        max_val - the maximum value in the data
        min_val - the minimum value in the data
        feature_val - the value of the current feature for the source vector
        
    OUTPUTS
        The lower and upper bounds of the range
    """
    #Define a continuous range beginning and ending on integers
    #Select a lower bound on the integers in [min_val,feature_val]
    lb = np.random.randint(min_val,high=feature_val+1)
    #Select an upper bound on the integers in [lb,max_val]
    ub = np.random.randint(feature_val,high=max_val+1)
    #If the selected bounds contain the entire range (which would 
    #indicate that the variable would have no contribution towards
    #discriminating the output), randomly select either the upper 
    #or lower bound to shift.
    if (lb==min_val)&(ub == max_val):
        #determine which bound to adjust
        if feature_val == min_val:
            decrease_ub = True
        elif feature_val == max_val:
            decrease_ub = False
        elif np.random.rand()>0.5:
            decrease_ub = True
        else:
            decrease_ub = False
        #Adjust the bound
        if decrease_ub:
            #Calculate the adjustment as a random integer between 1 and
            #the difference between the min and value
            adjustment = np.random.randint(max_val-feature_val)+1
            ub-=adjustment
        else:
            #Calculate the adjustment as a random integer between 
            #the difference between the min and value
            adjustment = np.random.randint(feature_val-min_val)+1
            lb+=adjustment
            
    return lb,ub

       

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
            
        #If there are two unique values, the variable is binary
        elif len(unique_vals)==2:
            values = list(unique_vals)
            var_ranges.loc['max',var] = values[0]
            var_ranges.loc['min',var] = values[1]
            var_ranges.loc['type',var] = 'binary'
            var_ranges.at['set',var] = unique_vals
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
    
    return var_ranges



def gen_CC_clause_pop(data,param,new_pop,CC_stats):
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
    for i in range(new_pop):
        clause_order = np.random.randint(param.num_features)+1
        candidate_mask = param.feature_order>=clause_order
        cand_match_counts = CC_stats.matched_input_vectors[candidate_mask]
        source_input_vector = sel_input_vector(cand_match_counts)
        
        new_pop_list.append(CC_clause(data,param,source_input_vector,clause_order))
        
        inputvars = 'figure these out'
        new_pop_list[-1].identify_matches(data,param)
        new_pop_list[-1].calc_fitness(inputvars)
        
    return new_pop_list
        
def sel_input_vector(cand_match_counts):
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
    input_vector = list(selection_CDF[selection_CDF>=rand].index)[0]
    
    return input_vector
    
    

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