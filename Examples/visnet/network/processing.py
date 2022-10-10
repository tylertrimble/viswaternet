# -*- coding: utf-8 -*-
"""
Created on Sun Oct  2 20:50:12 2022

@author: Tyler
"""
import numpy as np


def get_parameter(
    model,
    parameter_type,
    parameter,
    value=None,
    element_list=None,
    tanks=False,
    reservoirs=False,
):
    """Gets parameter for each node in the network and stores it in
    parameter_results. Also grabs the indices of the nodes that had that
    parameter.
    Arguments:
    model: Takes dictionary. Utilizes network model and results from WNTR to
    get parameters.
    parameter_type: Takes String. The type of node, can be 'Node' or 'Link'.
    parameter: Takes String. The name of the parameter.
    value: Takes Integer. Parameters from results must include a value
    with it. The value given is the value index, not time.
    Takes node parameters:
        'base_demand'
        'elevation'
    Takes node-value parameters:
        'pressure'
        'quality'
        'head'
        'demand'
    Takes link parameters:
        'length'
        'diameter'
        'roughness'
        'minor_loss'
    Takes link-value parameters:
        'velocity'
        'flowrate'
        'headloss'
        'friction_factor'
        'reaction_rate'
        'link_quality'"""

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
                        model["results"].node[parameter].iloc[:, indices]
                    )
                elif value == "min":

                    parameter_results = np.min(
                        model["results"].node[parameter].iloc[:, indices]
                    )
                elif value == "mean":

                    parameter_results = np.mean(
                        model["results"].node[parameter].iloc[:, indices]
                    )
                elif value == "stddev":
                    parameter_results = np.std(
                        model["results"].node[parameter].iloc[:, indices]
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
            return parameter_results, element_list
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
                        model["results"].link[parameter].iloc[:, indices]
                    )
                elif value == "min":

                    parameter_results = np.min(
                        model["results"].link[parameter].iloc[:, indices]
                    )
                elif value == "mean":

                    parameter_results = np.mean(
                        model["results"].link[parameter].iloc[:, indices]
                    )
                elif value == "stddev":
                    parameter_results = np.std(
                        model["results"].link[parameter].iloc[:, indices]
                    )
                elif type(value) == int:

                    parameter_results = (
                        model["results"].link[parameter].iloc[value, indices]
                    )
            return parameter_results, element_list
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


def get_demand_patterns(model):

    demandPatterns = []

    patterns = model["wn"].pattern_name_list

    patterns = np.append(patterns, "None")

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
    for pattern in patterns:

        if len(demand_pattern_nodes[pattern]) == 0:

            patterns = np.delete(patterns, np.where(patterns == pattern))

            del demand_pattern_nodes[pattern]
    return demand_pattern_nodes, patterns


def bin_parameter(
    model,
    parameter_results,
    element_list,
    bin_edge_num,
    bin_list="automatic",
    disable_bin_deleting=False,
    legend_sig_figs=3,
):
    """Bins results from get_parameter based on user specifications.
    Arguments:
    model: Takes Dictionary. Gets pipe or node name list.
    parameter_results: Takes Series. Results from get_parameter.
    bin_edge_num: Number of bin edges that the user wants.
    bin_list: List of bin edges. When set to 'Automatic' it will create bin
    edges."""

    if bin_list == "automatic":

        bins = bin_edge_num

        bin_list = np.linspace(
            np.min(parameter_results), np.max(parameter_results), bins
        )
    binnedParameter = {}
    binNames = []

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
    for i in range(len(bin_list)):

        if i == 0:

            if np.min(parameter_results) < bin_list[i]:

                binNames = np.append(binNames, "< {0:1.{j}f}".format(bin_list[i],j=legend_sig_figs))
            binNames = np.append(
                binNames, "{0:1.{j}f} - {1:1.{j}f}".format(bin_list[i], bin_list[i + 1],j=legend_sig_figs)
            )
        elif i < len(bin_list) - 1:

            binNames = np.append(
                binNames, "{0:1.{j}f} - {1:1.{j}f}".format(bin_list[i], bin_list[i + 1],j=legend_sig_figs)
            )
        elif i == len(bin_list) - 1:

            if np.max(parameter_results) > bin_list[i]:

                binNames = np.append(binNames, "> {0:1.{j}f}".format(bin_list[i],j=legend_sig_figs))
    for binName in binNames:

        binnedParameter[binName] = {}
    for i in range(len(bin_list)):

        if i == 0:

            counter = 0

            for parameter in parameter_results:

                if parameter >= bin_list[i] and parameter < bin_list[i + 1]:

                    binnedParameter[
                        "{0:1.{j}f} - {1:1.{j}f}".format(bin_list[i], bin_list[i + 1],j=legend_sig_figs)
                    ][elementsWithParameter[counter]] = element_list.index(
                        elementsWithParameter[counter]
                    )
                if parameter < bin_list[i]:

                    binnedParameter["< {0:1.{j}f}".format(bin_list[i],j=legend_sig_figs)][
                        elementsWithParameter[counter]
                    ] = element_list.index(elementsWithParameter[counter],)
                counter += 1
        elif i == len(bin_list) - 2:

            counter = 0

            for parameter in parameter_results:

                if parameter >= bin_list[i] and parameter <= bin_list[i + 1]:

                    binnedParameter[
                        "{0:1.{j}f} - {1:1.{j}f}".format(bin_list[i], bin_list[i + 1],j=legend_sig_figs)
                    ][elementsWithParameter[counter]] = element_list.index(
                        elementsWithParameter[counter]
                    )
                counter += 1
        elif i < len(bin_list) - 2:

            counter = 0

            for parameter in parameter_results:

                if parameter >= bin_list[i] and parameter < bin_list[i + 1]:

                    binnedParameter[
                        "{0:1.{j}f} - {1:1.{j}f}".format(bin_list[i], bin_list[i + 1],j=legend_sig_figs)
                    ][elementsWithParameter[counter]] = element_list.index(
                        elementsWithParameter[counter]
                    )
                counter += 1
        elif i == len(bin_list) - 1:

            counter = 0

            for parameter in parameter_results:

                if parameter > bin_list[i]:

                    binnedParameter["> {0:1.{j}f}".format(bin_list[i],j=legend_sig_figs)][
                        elementsWithParameter[counter]
                    ] = element_list.index(elementsWithParameter[counter])
                counter += 1
    if disable_bin_deleting:
        pass
    else:
        for binName in binNames:

            if len(binnedParameter[binName]) == 0:

                binNames = np.delete(binNames, np.where(binNames == binName))

                del binnedParameter[binName]
    return binnedParameter, binNames
