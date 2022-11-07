# -*- coding: utf-8 -*-
"""
Created on Sun Oct  2 20:45:59 2022

@author: Tyler
"""
import numpy as np


def normalize_parameter(model, parameter_results, min_value, max_value):
    minParameter = np.min(parameter_results)
    maxParameter = np.max(parameter_results)

    normalized_parameter = np.copy(parameter_results)

    for counter, parameter in enumerate(parameter_results):

        normalized_parameter[counter] = (
            (max_value - min_value)
            * ((parameter - minParameter) / (maxParameter - minParameter))
        ) + min_value
    return normalized_parameter
