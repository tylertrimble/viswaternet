# -*- coding: utf-8 -*-
import numpy as np


def get_parameter(
        self,
        parameter_type,
        parameter,
        value=None,
        element_list=None,
        include_tanks=False,
        include_reservoirs=False,
        include_pumps=True,
        include_valves=True):
    model = self.model
    results = model["results"]
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
                parameter_results = results.node[parameter].iloc[:, indices]
            else:
                if value == "max":
                    parameter_results = np.max(
                        results.node[parameter].iloc[:, indices],
                        axis=0)
                elif value == "min":
                    parameter_results = np.min(
                        results.node[parameter].iloc[:, indices],
                        axis=0)
                elif value == "mean":
                    parameter_results = np.mean(
                        results.node[parameter].iloc[:, indices],
                        axis=0)
                elif value == "stddev":
                    parameter_results = np.std(
                        results.node[parameter].iloc[:, indices],
                        axis=0)
                elif value == "range":
                    parameter_results = np.ptp(
                        results.node[parameter].iloc[:, indices],
                        axis=0)
                # If an int is given, assume it is a timestep and get parameter
                # at given timestep
                elif isinstance(value, int):
                    parameter_results = (
                        results.node[parameter].iloc[value, indices])
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
        if include_tanks:
            pass
        else:
            for tank in model["tank_names"]:
                # Try block to catch KeyErrors in instance where tank does
                # not exist in parameter_results
                try:
                    parameter_results.drop(tank,inplace=True)
                    element_list.remove(tank)
                except KeyError:
                    pass
        if include_reservoirs:
            pass
        else:
            for reservoir in model["reservoir_names"]:
                # Try block to catch KeyErrors in instance where reservoir
                # does not exist in parameter_results
                try:
                    parameter_results.drop(reservoir,inplace=True)
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
                parameter_results = results.link[parameter].iloc[:, indices]
            else:
                if value == "max":
                    parameter_results = np.max(
                        results.link[parameter].iloc[:, indices],
                        axis=0)
                elif value == "min":
                    parameter_results = np.min(
                        results.link[parameter].iloc[:, indices],
                        axis=0)
                elif value == "mean":
                    parameter_results = np.mean(
                        results.link[parameter].iloc[:, indices],
                        axis=0)
                elif value == "stddev":
                    parameter_results = np.std(
                        results.link[parameter].iloc[:, indices],
                        axis=0)
                elif value == "range":
                    parameter_results = np.ptp(
                        results.link[parameter].iloc[:, indices],
                        axis=0)
                elif type(value) == int:
                    parameter_results = (
                        results.link[parameter].iloc[value, indices])
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
        if include_pumps:
            pass
        else:
            for pump in model["pump_names"]:
                # Try block to catch KeyErrors in instance where pump does
                # not exist in parameter_results
                try:
                    parameter_results.drop(pump,inplace=True)
                    element_list.remove(pump)
                except KeyError:
                    pass
        if include_valves:
            pass
        else:
            for valve in model["valve_names"]:
                # Try block to catch KeyErrors in instance where valve
                # does not exist in parameter_results
                try:
                    parameter_results.drop(valve,inplace=True)
                    element_list.remove(valve)
                except KeyError:
                    pass
    print(parameter_results)
    return parameter_results, element_list


def get_demand_patterns(self):
    model = self.model
    demand_patterns = []

    # Get list of patterns
    patterns = model["wn"].pattern_name_list
    patterns.append("None")
    patterns = sorted(patterns)

    # Loop through junctions only (no reservoirs, tanks)
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
                demand_pattern_nodes[pattern][junc_name] = \
                    model["junc_names"].index(junc_name)

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
        legend_decimal_places=3):
    model = self.model
    # Code that generates bins automatically based on number of intervals
    # specified. The code does this by creating num_intervals + 1 linearlly
    # spaced bins. There are currently no options to automatically create
    # bins other than linearlly spaced ones, use custom bin intervals to do
    # this
    if intervals == "automatic":
        bins = num_intervals + 1
        intervals = np.linspace(
            np.min(parameter_results), np.max(parameter_results), bins)
        intervals = intervals.tolist()
    interval_results = {}
    interval_names = []
    elements_with_parameter = element_list
    element_type = None
    for element_with_parameter in elements_with_parameter:
        if (element_with_parameter in model["node_names"]) is True:
            continue
        else:
            element_list = model["G_pipe_name_list"]
            element_type = "link"
            break
    if element_type != "link":
        element_list = model["node_names"]
    for i in range(len(intervals)):
        if i == 0:
            if np.min(parameter_results) < intervals[i]:
                interval_names.append("< {0:1.{j}f}".format(
                    intervals[i],
                    j=legend_decimal_places))
            interval_names.append("{0:1.{j}f} - {1:1.{j}f}".format(
                intervals[i], intervals[i + 1],
                j=legend_decimal_places))
        elif i < len(intervals) - 1:
            interval_names.append("{0:1.{j}f} - {1:1.{j}f}".format(
                intervals[i], intervals[i + 1],
                j=legend_decimal_places))
        elif i == len(intervals) - 1:
            if np.max(parameter_results) > intervals[i]:
                interval_names.append("> {0:1.{j}f}".format(
                    intervals[i],
                    j=legend_decimal_places))
    for bin_name in interval_names:
        interval_results[bin_name] = {}
    for i in range(len(intervals)):
        if i == 0:
            for j, parameter in enumerate(parameter_results):
                if parameter >= intervals[i] and parameter < intervals[i + 1]:

                    interval_results["{0:1.{j}f} - {1:1.{j}f}".format(
                        intervals[i],
                        intervals[i + 1],
                        j=legend_decimal_places)][elements_with_parameter[j]] \
                        = element_list.index(elements_with_parameter[j])
                if parameter < intervals[i]:
                    interval_results["< {0:1.{j}f}".format(
                        intervals[i],
                        j=legend_decimal_places)][elements_with_parameter[j]] \
                        = element_list.index(elements_with_parameter[j])
        elif i == len(intervals) - 2:
            for j, parameter in enumerate(parameter_results):
                if parameter >= intervals[i] and parameter <= intervals[i + 1]:
                    interval_results["{0:1.{j}f} - {1:1.{j}f}".format(
                        intervals[i],
                        intervals[i + 1],
                        j=legend_decimal_places)][elements_with_parameter[j]] \
                        = element_list.index(elements_with_parameter[j])
        elif i < len(intervals) - 2:
            for j, parameter in enumerate(parameter_results):
                if parameter >= intervals[i] and parameter < intervals[i + 1]:
                    interval_results["{0:1.{j}f} - {1:1.{j}f}".format(
                        intervals[i],
                        intervals[i + 1],
                        j=legend_decimal_places)][elements_with_parameter[j]] \
                        = element_list.index(elements_with_parameter[j])
        elif i == len(intervals) - 1:
            for j, parameter in enumerate(parameter_results):
                if parameter > intervals[i]:
                    interval_results["> {0:1.{j}f}".format(
                        intervals[i],
                        j=legend_decimal_places)][elements_with_parameter[j]] \
                        = element_list.index(elements_with_parameter[j])
    if disable_interval_deleting:
        pass
    else:
        for bin_name in interval_names:
            if len(interval_results[bin_name]) == 0:
                interval_names = np.delete(
                    interval_names, np.where(interval_names == bin_name))
                del interval_results[bin_name]
    return interval_results, interval_names
