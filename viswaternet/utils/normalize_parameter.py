import numpy as np


def normalize_parameter(parameter_results, min_value, max_value):
    minParameter = np.min(parameter_results, axis=0)
    maxParameter = np.max(parameter_results, axis=0)

    normalized_parameter = np.copy(parameter_results)
    if (maxParameter-minParameter) == 0:
        pass
    else:
        for counter, parameter in enumerate(parameter_results):
            normalized_parameter[counter] = (
                (max_value - min_value)
                * ((parameter - minParameter) / (maxParameter - minParameter)))
            + min_value
    return normalized_parameter.tolist()
