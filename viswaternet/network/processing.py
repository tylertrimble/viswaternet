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
            int                 lots element data for specified timestep
            min                 Plots minimum data point for each element
            max                 Plots maximum data point for each element
            mean                Plots mean for each element
            stddev              Plots standard deviation for each element
            range               Plots range for each element
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
    model = self.model
    if parameter_type == "node":
        # If no element list is provided, set element list to all nodes of
        # the model
        if element_list is None:
            element_list = list.copy(model["node_names"])
        # Get indices of nodes in model["node_names"]
        indices = [model["node_names"].index(i) for i in element_list]
        # WNTR differentiates between node attributes and simulation results.
        # To account for this all simulation result logic is put into a try
        # block and if a KeyError occurs, it goes into the except block to
        # get the node attribute instead.
        try:
            # If no value type is given (timestep, max, etc) then return
            # parameter at all timesteps
            if value is None:
                parameter_results = model["results"].node[parameter].iloc[:, indices]
            else:
                if value == "max":
                    parameter_results = np.max(
                        model["results"].node[parameter].iloc[:, indices],
                        axis=0)
                elif value == "min":
                    parameter_results = np.min(
                        model["results"].node[parameter].iloc[:, indices],
                        axis=0)
                elif value == "mean":
                    parameter_results = np.mean(
                        model["results"].node[parameter].iloc[:, indices],
                        axis=0)
                elif value == "stddev":
                    parameter_results = np.std(
                        model["results"].node[parameter].iloc[:, indices],
                        axis=0)
                elif value == "range":
                    parameter_results = np.ptp(
                        model["results"].node[parameter].iloc[:, indices],
                        axis=0)
                # If an int is given, assume it is a timestep and get parameter
                # at given timestep
                elif isinstance(value, int):
                    parameter_results = (
                        model["results"].node[parameter].iloc[value, indices])
        # Node attribute fetching logic
        except KeyError:
            parameter_results = model["wn"].query_node_attribute(parameter)
            elements_in_results = list(parameter_results.index)
            element_list_temp = list.copy(element_list)
            # Some elements do not have certain attributes. For instance,
            # reservoirs do not have an elevation. This code removes those
            # elements from the results
            for element in element_list_temp:
                try:
                    if elements_in_results.index(element):
                        pass
                except ValueError:
                    element_list.remove(element)
            indices = [elements_in_results.index(i) for i in element_list]
            parameter_results = parameter_results.iloc[indices]
        if tanks:
            pass
        else:
            for tank in model["tank_names"]:
                # Try block to catch KeyErrors in instance where tank does
                # not exist in parameter_results
                try:
                    parameter_results.drop(tank, axis=0, inplace=True)
                    element_list.remove(tank)
                except KeyError:
                    pass
        if reservoirs:
            pass
        else:
            for reservoir in model["reservoir_names"]:
                # Try block to catch KeyErrors in instance where reservoir
                # does not exist in parameter_results
                try:
                    parameter_results.drop(reservoir, axis=0, inplace=True)
                    element_list.remove(reservoir)
                except KeyError:
                    pass
    elif parameter_type == "link":
        # If no element list is provided, set element list to all links of
        # the model
        if element_list is None:
            element_list = list.copy(model["G_pipe_name_list"])
        indices = [model["G_pipe_name_list"].index(i) for i in element_list]
        # WNTR differentiates between link attributes and simulation results.
        # To account for this all simulation result logic is put into a try
        # block and if a KeyError occurs, it goes into the except block to
        # get the link attribute instead.
        try:
            if value is None:
                parameter_results = model["results"].link[parameter].iloc[:, indices]
            else:
                if value == "max":
                    parameter_results = np.max(
                        model["results"].link[parameter].iloc[:, indices],
                        axis=0)
                elif value == "min":
                    parameter_results = np.min(
                        model["results"].link[parameter].iloc[:, indices],
                        axis=0)
                elif value == "mean":
                    parameter_results = np.mean(
                        model["results"].link[parameter].iloc[:, indices],
                        axis=0)
                elif value == "stddev":
                    parameter_results = np.std(
                        model["results"].link[parameter].iloc[:, indices],
                        axis=0)
                elif value == "range":
                    parameter_results = np.ptp(
                        model["results"].link[parameter].iloc[:, indices],
                        axis=0)
                elif type(value) == int:
                    parameter_results = (
                        model["results"].link[parameter].iloc[value, indices])
        # Link attribute fetching logic
        except KeyError:
            parameter_results = model["wn"].query_link_attribute(parameter)
            elements_in_results = list(parameter_results.index)
            element_list_temp = list.copy(element_list)
            # Some elements do not have certain attributes. For instance,
            # reservoirs do not have an elevation. This code removes those
            # elements from the results
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
    model = self.model
    demand_patterns = []
    
    # Get list of patterns
    patterns = model["wn"].pattern_name_list
    patterns.append("None")
    patterns = sorted(patterns)
    
    #Loop through junctions only (no reservoirs, tanks)
    for junction in model["junc_names"]:
        # Attempt to extract pattern name for each junction. If an attribute
        # error occurs, then the junction has no demand pattern associated with
        # it.
        try:
            demand_pattern = (
                model["wn"].get_node(
                    junction).demand_timeseries_list[0].pattern.name)
            demand_patterns = np.append(demand_patterns, demand_pattern)
        except AttributeError:
            demand_patterns = np.append(demand_patterns, "None")
    
    # Initialize pattern dictionary
    demand_pattern_nodes = {}
    for pattern in patterns:
        demand_pattern_nodes[pattern] = {}
    # Create pattern dictionary in the same form as what get_parameter outputs
    for i, junc_name in enumerate(model["junc_names"]):
        for pattern in patterns:
            if demand_patterns[i] == pattern:
                demand_pattern_nodes[pattern][junc_name] = model["junc_names"].index(
                    junc_name)
    
    # Remove None key if no junctions are in it
    if len(demand_pattern_nodes['None']) == 0:
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
    model = self.model
    if intervals == "automatic":
        bins = num_intervals + 1
        intervals = np.linspace(
            np.min(parameter_results), np.max(parameter_results), bins)
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
                interval_names = np.append(
                    interval_names, "< {0:1.{j}f}".format(intervals[i], 
                                                          j=legend_sig_figs))
            interval_names = np.append(
                interval_names, "{0:1.{j}f} - {1:1.{j}f}".format(
                    intervals[i], intervals[i + 1], j=legend_sig_figs)
            )
        elif i < len(intervals) - 1:
            interval_names = np.append(
                interval_names, "{0:1.{j}f} - {1:1.{j}f}".format(
                    intervals[i], intervals[i + 1], j=legend_sig_figs)
            )
        elif i == len(intervals) - 1:
            if np.max(parameter_results) > intervals[i]:
                interval_names = np.append(
                    interval_names, "> {0:1.{j}f}".format(intervals[i], 
                                                          j=legend_sig_figs))
    for binName in interval_names:
        interval_results[binName] = {}
    for i in range(len(intervals)):
        if i == 0:
            counter = 0
            for parameter in parameter_results:
                if parameter >= intervals[i] and parameter < intervals[i + 1]:
                    interval_results[
                        "{0:1.{j}f} - {1:1.{j}f}".format(
                            intervals[i], intervals[i + 1], j=legend_sig_figs)]
                    [elementsWithParameter[counter]] = element_list.index(
                        elementsWithParameter[counter])
                if parameter < intervals[i]:
                    interval_results["< {0:1.{j}f}".format(intervals[i], 
                                                           j=legend_sig_figs)]
                    [elementsWithParameter[counter]] = element_list.index(
                        elementsWithParameter[counter],)
                counter += 1
        elif i == len(intervals) - 2:
            counter = 0
            for parameter in parameter_results:
                if parameter >= intervals[i] and parameter <= intervals[i + 1]:
                    interval_results[
                        "{0:1.{j}f} - {1:1.{j}f}".format(
                            intervals[i], intervals[i + 1], j=legend_sig_figs)
                    ][elementsWithParameter[counter]] = element_list.index(
                        elementsWithParameter[counter]
                    )
                counter += 1
        elif i < len(intervals) - 2:
            counter = 0
            for parameter in parameter_results:
                if parameter >= intervals[i] and parameter < intervals[i + 1]:
                    interval_results[
                        "{0:1.{j}f} - {1:1.{j}f}".format(
                            intervals[i], intervals[i + 1], j=legend_sig_figs)
                    ][elementsWithParameter[counter]] = element_list.index(
                        elementsWithParameter[counter]
                    )
                counter += 1
        elif i == len(intervals) - 1:
            counter = 0
            for parameter in parameter_results:
                if parameter > intervals[i]:
                    interval_results["> {0:1.{j}f}".format(intervals[i], j=legend_sig_figs)][
                        elementsWithParameter[counter]
                    ] = element_list.index(elementsWithParameter[counter])
                counter += 1
    if disable_interval_deleting:
        pass
    else:
        for binName in interval_names:
            if len(interval_results[binName]) == 0:
                interval_names = np.delete(
                    interval_names, np.where(interval_names == binName))
                del interval_results[binName]
    return interval_results, interval_names
