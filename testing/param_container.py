# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 22:01:52 2019

@author: jmatt
"""


class parameter_container:
    """
    An empty object used to pass variables and data to a function
    """
    def __init__(self):
        breakhere=1
        
    def keys(self):
        """
        Return a list of the variables in the object
        """
        return [x for x in self.__dict__.keys()]


tt = parameter_container()
tt.rocks = 5
tt.beans = 'wiggle'
tt.keys()