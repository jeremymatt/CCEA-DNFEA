# -*- coding: utf-8 -*-
"""
Created on Sun Jun 23 22:56:48 2019

@author: jmatt
"""

import pandas as pd
import matplotlib.pyplot as plt




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
    
    return feature,selection_CDF,selection_PMF




cand_match_counts = pd.Series([0,5,5,10,0,0,0,0,0,0,0,0,0,0,0])

num_sel = 100000
selections = []
for i in range(num_sel):
    feature,selection_CDF,selection_PMF=sel_input_feature(cand_match_counts)
    selections.append(feature)


plt.hist(selections,bins=len(cand_match_counts),normed=True)
