import numpy as np


def normalize_parameter(parameter_results, min_value, max_value):
    min_parameter = np.min(parameter_results, axis=0)
    max_parameter = np.max(parameter_results, axis=0)

    normalized_parameter = np.copy(parameter_results)
    if (max_parameter-min_parameter) == 0:
        pass
    else:
        for i, value in enumerate(parameter_results):
            normalized_parameter[i] = (((max_value - min_value)
                                       * (value - min_parameter)
                                       / (max_parameter - min_parameter))
                                       + min_value)
    return normalized_parameter.tolist()
