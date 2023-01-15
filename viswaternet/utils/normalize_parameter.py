"""
The viswaternet.utils.normalize_parameter linearlly normalizes network data 
between two values.
"""
import numpy as np


def normalize_parameter(parameter_results, min_value, max_value):
    """Normalizes input data between a min and max value.
    
    Arguments
    ---------
    parameter_results : array-like
        Network data to be normalized.
    
    min_value : float, int
        Lower bound value for normalization.
        
    max_value : float, int
        Upper bound value for normalization
    """
    minParameter = np.min(parameter_results,axis=0)
    maxParameter = np.max(parameter_results,axis=0)

    normalized_parameter = np.copy(parameter_results)

    for counter, parameter in enumerate(parameter_results):

        normalized_parameter[counter] = (
            (max_value - min_value)
            * ((parameter - minParameter) / (maxParameter - minParameter))
        ) + min_value
    return normalized_parameter
