# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 11:17:33 2019

@author: jmatt
"""

import numpy as np

def CC_mutation_naive(data,param,CC_clause,prob_remove):
    """
    
    """
    
    
    #Boolean array of locations to perform mutation
    to_mutate = pd.DataFrame(np.random.rand(param.num_features)<1/L)
    
    #If no locations selected, select one at random
    if not to_mutate.any()[0]:
        to_mutate.loc[np.random.randint(param.num_features)] = True
                                  
    #Extract the list of the variables to mutate
    features_to_flip = [param.data_features[feature] for feature,to_flip in enumerate(to_mutate.values) if to_flip]
    
    
    for feature in features_to_flip:
        present_in_clause = feature in t.features
        
        if present_in_clause:
            if (np.random.rand(1)[0] < prob_remove) & (CC_clause.order>1):
                #drop the variable
                CC_clause.drop_feature(data,param,feature)
            else:
                #mutate the variable
                feature_val = CC_clause.input_vector_data[feature]
                criteria = CC_clause.generate_CC_criteria(data,param,feature,feature_val)
                CC_clause.criteria[feature] = criteria[feature]
                CC_clause.update_fitness(data,param,[feature])
                
        else:
            #add the variable
            CC_clause.features.append(feature)
            CC_clause.order =  len(CC_clause.features)
            feature_val = CC_clause.input_vector_data[feature]