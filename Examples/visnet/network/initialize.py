# -*- coding: utf-8 -*-
"""
Created on Sun Oct  2 20:51:37 2022

@author: Tyler
"""
import os
import wntr


def initialize_model(inp_file):
    """Initializes all variables needed to perform other plotting functions
        Arguments:
    inp_file: Takes a string. Directorty location of network input file. Ends with .inp"""

    # =============================================================================
    #   Initilize model dictionary. Get directory code is stored in to set input
    #   file and saved images path
    # =============================================================================
    model = {}
    dirname = os.getcwd()
    inp_file = os.path.join(dirname, inp_file)
    model["inp_file"] = inp_file
    image_path = os.path.join(dirname)
    model["image_path"] = image_path

    # Run hydraulic simulation and store results
    wn = wntr.network.WaterNetworkModel(inp_file)
    model["wn"] = wn
    sim = wntr.sim.EpanetSimulator(wn)
    model["sim"] = sim

    results = sim.run_sim()
    model["results"] = results

    # =============================================================================
    #   Create name lists for easy reference
    #   junc_names excludes resevoirs and tanks
    #   node_names includes all nodes
    # =============================================================================
    model["junc_names"] = wn.junction_name_list
    model["valve_names"] = wn.valve_name_list
    model["tank_names"] = wn.tank_name_list
    model["node_names"] = wn.node_name_list
    model["reservoir_names"] = wn.reservoir_name_list

    # Gets start and end points of all links
    pipe_tp = []
    pipe_tp2 = []

    for link_name, link in wn.links():

        pipe_tp.append(link.start_node_name)
        pipe_tp2.append(link.end_node_name)
    pipe_list = list(zip(pipe_tp, pipe_tp2))
    model["pipe_list"] = pipe_list

    # Creates wntr graph
    G = wn.get_graph()
    model["G"] = G

    # Gets node coordiantes
    pos_dict = {}

    for i in range(len(model["node_names"])):

        pos_dict[model["node_names"][i]] = wn.get_node(
            model["node_names"][i]
        ).coordinates
    model["pos_dict"] = pos_dict

    # Stores pipe names, pump connections only, and valve connections only
    G_pipe_name_list = []
    G_list_pumps_only = []
    G_list_valves_only = []

    # Stores pipe names, as well as creating a list of pumps and valves only
    for j in range(len(pipe_tp)):

        G_pipe_name_list.append(wn.link_name_list[j])

        if wn.link_name_list[j] in wn.pump_name_list:

            G_list_pumps_only.append(pipe_list[j])

            continue
        if wn.link_name_list[j] in wn.valve_name_list:

            G_list_valves_only.append(pipe_list[j])
    model["G_pipe_name_list"] = G_pipe_name_list
    model["G_list_pumps_only"] = G_list_pumps_only
    model["G_list_valves_only"] = G_list_valves_only

    return model
