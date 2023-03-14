# -*- coding: utf-8 -*-
"""
The viswaternet.network.initialize module initializes a viswaternet model object.
"""
import os
import wntr
import matplotlib.pyplot as plt

class VisWNModel:
    """Viswaternet model class.

    The resulting object created from VisWNModel is the basis for nearly all
    functionality that viswaternet has to offer.

    Arguments
    ---------
    inp_file : string
        Input file to be used.

    network_model : wntr.network.model.WaterNetworkModel
        WNTR WaterNetworkModel object.
    """

    def __init__(self, inp_file, network_model=None,figsize=(12,12),axis_frame=False):
        model = {}
        dirname = os.getcwd()

        if network_model is not None:
            wn = network_model
            inp_file = os.path.join(dirname, inp_file)
            model["inp_file"] = inp_file
        else:
            inp_file = os.path.join(dirname, inp_file)
            model["inp_file"] = inp_file
            wn = wntr.network.WaterNetworkModel(inp_file)
        image_path = os.getcwd()
        model["image_path"] = image_path

        # Run hydraulic simulation and store results
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

        self.model = model
        fig, ax = plt.subplots(figsize=figsize)  
        self.fig = fig
        self.ax = ax
        self.ax.set_frame_on(axis_frame)
        
    from viswaternet.network.processing import get_parameter, bin_parameter
    from viswaternet.drawing.base import draw_nodes, draw_links, draw_base_elements, plot_basic_elements, draw_label
    from viswaternet.drawing.discrete import draw_discrete_nodes, draw_discrete_links, plot_discrete_nodes, plot_discrete_links
    from viswaternet.drawing.continuous import plot_continuous_links, plot_continuous_nodes
    from viswaternet.drawing.animate import animate_plot
    from viswaternet.drawing.unique import plot_unique_data
    from viswaternet.utils.convert_excel import convert_excel
