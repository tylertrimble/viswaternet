# -*- coding: utf-8 -*-
"""
The viswaternet.network.processing module performs data retrieving and processing
tasks in preparation for drawing functions.
"""
import numpy as np


def get_parameter(
    self,
    parameter_type,
    parameter,
    value=None,
    element_list=None,
    tanks=False,
    reservoirs=False,
):
    """Retrieves network data of a specified parameter. 
    
    Arguments
    ---------
    parameter_type : string
        Type of parameter (nodal, link)
        
    parameter : string
        Parameter that network data will be retrieved for.
        
    value : int, string
        For time-varying parameters only. Specifies which timestep or data
        summary will be plotted.
        
        .. rubric:: Possible Inputs
        
        ======================= =========================================
            :attr:'int'         Plots element data for specified timestep
            :attr:'min'         Plots minimum data point for each element
            :attr:'max'         Plots maximum data point for each element
            :attr:'mean'        Plots mean for each element
            :attr:'stddev'      Plots standard deviation for each element
            :attr:'range'       Plots range for each element
        ======================= =========================================
        
    element_list : array-like
        List of network elements that data will be retrieved for.
        
    tanks : boolean
        Determines if data for tanks are retrieved.
        
    reservoirs : boolean
        Determines if data for reservoirs are retrieved.
    
    Returns
    -------
    array-like
        Network data formatted for use in other functions
        
    array-like
        Elements that have had their data retrieved
    """
    model=self.model
    if parameter_type == "node":
        if element_list is None:
            element_list = list.copy(model["node_names"])
        indices = [model["node_names"].index(i) for i in element_list]
        try:

            if value is None:

                parameter_results = model["results"].node[parameter].iloc[:, indices]
            else:
                if value == "max":

                    parameter_results = np.max(
                        model["results"].node[parameter].iloc[:, indices],
                        axis=0
                    )
                elif value == "min":

                    parameter_results = np.min(
                        model["results"].node[parameter].iloc[:, indices],
                        axis=0
                    )
                elif value == "mean":

                    parameter_results = np.mean(
                        model["results"].node[parameter].iloc[:, indices],
                        axis=0
                    )
                elif value == "stddev":
                    parameter_results = np.std(
                        model["results"].node[parameter].iloc[:, indices],
                        axis=0
                    )
                elif value == "range":
                    parameter_results = np.ptp(
                        model["results"].node[parameter].iloc[:, indices],
                        axis=0
                        )
                elif isinstance(value, int):

                    parameter_results = (
                        model["results"].node[parameter].iloc[value, indices]
                    )
            try:

                if tanks:
                    pass
                else:
                    for tank in model["tank_names"]:

                        parameter_results.drop(tank, axis=0, inplace=True)

                        element_list.remove(tank)
                if reservoirs:
                    pass
                else:
                    for reservoir in model["reservoir_names"]:

                        parameter_results.drop(reservoir, axis=0, inplace=True)

                        element_list.remove(reservoir)
            except KeyError:

                pass
        except KeyError:

            parameter_results = model["wn"].query_node_attribute(parameter)

            elements_in_results = list(parameter_results.index)
            element_list_temp = list.copy(element_list)
            for element in element_list_temp:
                try:
                    if elements_in_results.index(element):
                        pass
                except ValueError:
                    element_list.remove(element)
            indices = [elements_in_results.index(i) for i in element_list]
            parameter_results = parameter_results.iloc[indices]
            try:

                if tanks:
                    pass
                else:
                    for tank in model["tank_names"]:

                        parameter_results.drop(tank, axis=0, inplace=True)

                        element_list.remove(tank)
                if reservoirs:
                    pass
                else:
                    for reservoir in model["reservoir_names"]:

                        parameter_results.drop(reservoir, axis=0, inplace=True)

                        element_list.remove(reservoir)
            except KeyError:

                pass
            
    elif parameter_type == "link":
        if element_list is None:
            element_list = list.copy(model["G_pipe_name_list"])
        indices = [model["G_pipe_name_list"].index(i) for i in element_list]
        try:

            if value is None:

                parameter_results = model["results"].link[parameter].iloc[:, indices]
            else:

                if value == "max":

                    parameter_results = np.max(
                        model["results"].link[parameter].iloc[:, indices],
                        axis=0
                    )
                elif value == "min":

                    parameter_results = np.min(
                        model["results"].link[parameter].iloc[:, indices],
                        axis=0
                    )
                elif value == "mean":

                    parameter_results = np.mean(
                        model["results"].link[parameter].iloc[:, indices],
                        axis=0
                    )
                elif value == "stddev":
                    parameter_results = np.std(
                        model["results"].link[parameter].iloc[:, indices],
                        axis=0
                    )
                elif value == "range":
                    parameter_results = np.ptp(
                        model["results"].link[parameter].iloc[:, indices],
                        axis=0
                        )
                elif type(value) == int:

                    parameter_results = (
                        model["results"].link[parameter].iloc[value, indices]
                    )
        except KeyError:

            parameter_results = model["wn"].query_link_attribute(parameter)

            elements_in_results = list(parameter_results.index)
            element_list_temp = list.copy(element_list)
            for element in element_list_temp:
                try:
                    if elements_in_results.index(element):
                        pass
                except ValueError:
                    element_list.remove(element)
            indices = [elements_in_results.index(i) for i in element_list]
            parameter_results = parameter_results.iloc[indices]

    return parameter_results, element_list


def get_demand_patterns(self):
    """Retrieves the demand pattern for each network node.
    
    Returns
    -------
    array-like
        Demand pattern for each node.
        
    array-like
        Name of each pattern.
    """
    model=self.model
    demandPatterns = []

    patterns = model["wn"].pattern_name_list
    patterns.append("None")
    patterns = sorted(patterns)
    for junction in model["junc_names"]:

        try:

            demandPattern = (
                model["wn"].get_node(junction).demand_timeseries_list[0].pattern.name
            )

            demandPatterns = np.append(demandPatterns, demandPattern)
        except AttributeError:

            demandPatterns = np.append(demandPatterns, "None")
    demand_pattern_nodes = {}

    for pattern in patterns:

        demand_pattern_nodes[pattern] = {}
    counter = 0
    for junc_name in model["junc_names"]:

        for pattern in patterns:
            if demandPatterns[counter] == pattern:

                demand_pattern_nodes[pattern][junc_name] = model["junc_names"].index(
                    junc_name
                )
        counter += 1

    if len(demand_pattern_nodes['None'])==0:
        patterns.remove("None")
        del demand_pattern_nodes['None']
       
    return demand_pattern_nodes, patterns


def bin_parameter(
    self,
    parameter_results,
    element_list,
    num_intervals,
    intervals="automatic",
    disable_interval_deleting=False,
    legend_sig_figs=3,
):
    """Discretizes network data for use in disrete drawing functions.
    
    An important feature of bin_parameter to know of is if the intervals created
    do not fully encapsulate the full range of network data, then a new interval
    will be created.
    
    Arguments
    ---------
    parameter_results : array-like
        Network data to be discretized.
    
    element_list : array-like
        Network elements to be discretized.
    
    num_intervals : int
        The number of intervals to be created.
    
    intervals : array-like, string
        If set to 'automatic' then intervals are created automatically on a 
        equal interval basis. Otherwise, it is the edges of the intervals to be
        created. intervals array length should be num_intervals + 1.
    
    disable_interval_deleting : boolean
        If True, empty intervals will be automatically deleted. 
        
    legend_sig_figs : int
        Number of decimal places that the resulting discretized data will display
        in the legend.
    
    Returns
    -------
    dictionary
        Dictionary of discretized network data.
    
    array-like
        Label names of each interval.
        
    Example
    -------
    >>>from viswaternet.network.processing import bin_parameter
    >>>fake_data=[1,6,10,14,15,21]
    >>>fake_elements=['E1','E2','E3','E4','E5','E6']
    >>>intervals,interval_names = bin_parameter(self,fake_data,fake_elements,3,intervals=[0,5,10,15])
    [<dict>,['0.000-5.000','5.000-10.000','10.000-15.000','>15.000']]
    """
    model=self.model
    
    if intervals == "automatic":

        bins = num_intervals

        intervals = np.linspace(
            np.min(parameter_results), np.max(parameter_results), bins
        )
    interval_results = {}
    interval_names = []

    elementsWithParameter = element_list
    elementType = None

    for elementWithParameter in elementsWithParameter:

        if (elementWithParameter in model["node_names"]) is True:

            continue
        else:
            element_list = model["G_pipe_name_list"]
            elementType = "link"

            break
    if elementType != "link":

        element_list = model["node_names"]
    for i in range(len(intervals)):

        if i == 0:

            if np.min(parameter_results) < intervals[i]:

                interval_names = np.append(interval_names, "< {0:1.{j}f}".format(intervals[i],j=legend_sig_figs))
            interval_names = np.append(
                interval_names, "{0:1.{j}f} - {1:1.{j}f}".format(intervals[i], intervals[i + 1],j=legend_sig_figs)
            )
        elif i < len(intervals) - 1:

            interval_names = np.append(
                interval_names, "{0:1.{j}f} - {1:1.{j}f}".format(intervals[i], intervals[i + 1],j=legend_sig_figs)
            )
        elif i == len(intervals) - 1:

            if np.max(parameter_results) > intervals[i]:

                interval_names = np.append(interval_names, "> {0:1.{j}f}".format(intervals[i],j=legend_sig_figs))
    for binName in interval_names:

        interval_results[binName] = {}
    for i in range(len(intervals)):

        if i == 0:

            counter = 0

            for parameter in parameter_results:

                if parameter >= intervals[i] and parameter < intervals[i + 1]:

                    interval_results[
                        "{0:1.{j}f} - {1:1.{j}f}".format(intervals[i], intervals[i + 1],j=legend_sig_figs)
                    ][elementsWithParameter[counter]] = element_list.index(
                        elementsWithParameter[counter]
                    )
                if parameter < intervals[i]:

                    interval_results["< {0:1.{j}f}".format(intervals[i],j=legend_sig_figs)][
                        elementsWithParameter[counter]
                    ] = element_list.index(elementsWithParameter[counter],)
                counter += 1
        elif i == len(intervals) - 2:

            counter = 0

            for parameter in parameter_results:

                if parameter >= intervals[i] and parameter <= intervals[i + 1]:

                    interval_results[
                        "{0:1.{j}f} - {1:1.{j}f}".format(intervals[i], intervals[i + 1],j=legend_sig_figs)
                    ][elementsWithParameter[counter]] = element_list.index(
                        elementsWithParameter[counter]
                    )
                counter += 1
        elif i < len(intervals) - 2:

            counter = 0

            for parameter in parameter_results:

                if parameter >= intervals[i] and parameter < intervals[i + 1]:

                    interval_results[
                        "{0:1.{j}f} - {1:1.{j}f}".format(intervals[i], intervals[i + 1],j=legend_sig_figs)
                    ][elementsWithParameter[counter]] = element_list.index(
                        elementsWithParameter[counter]
                    )
                counter += 1
        elif i == len(intervals) - 1:

            counter = 0

            for parameter in parameter_results:

                if parameter > intervals[i]:

                    interval_results["> {0:1.{j}f}".format(intervals[i],j=legend_sig_figs)][
                        elementsWithParameter[counter]
                    ] = element_list.index(elementsWithParameter[counter])
                counter += 1
    if disable_interval_deleting:
        pass
    else:
        for binName in interval_names:

            if len(interval_results[binName]) == 0:

                interval_names = np.delete(interval_names, np.where(interval_names == binName))

                del interval_results[binName]
    return interval_results, interval_names
