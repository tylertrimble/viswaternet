# -*- coding: utf-8 -*-
import os
import wntr
import numpy as np
from packaging.version import Version, parse

class VisWNModel:
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
        valve_names = wn.valve_name_list
        pump_names = wn.pump_name_list
        model["junc_names"] = wn.junction_name_list
        model["valve_names"] = valve_names
        model["pump_names"] = pump_names
        model["tank_names"] = wn.tank_name_list
        model["node_names"] = wn.node_name_list
        model["reservoir_names"] = wn.reservoir_name_list
        # Gets start and end points of all links
        pipe_list = []
        for link_name, link in wn.links():
            pipe_list.append((link.start_node_name,link.end_node_name))
        model["pipe_list"] = pipe_list
        # Creates wntr graph
        if parse(str(wntr.__version__)) < parse('0.5.0'):
            G = wn.get_graph()
        else:
            G = wn.to_graph()
        model["G"] = G

        # Gets node coordinates
        pos_dict = {}
        
        for name, node in wn.nodes():

            pos_dict[name] = node.coordinates
        model["pos_dict"] = pos_dict

        G_pipe_name_list = np.array(wn.link_name_list)
        G_list_pumps_only_mask = np.isin(np.array(G_pipe_name_list),np.array(pump_names))
        G_list_valves_only_mask = np.isin(np.array(G_pipe_name_list),np.array(valve_names))
        G_list_pumps_only = np.array(pipe_list)[G_list_pumps_only_mask]
        G_list_valves_only = np.array(pipe_list)[G_list_valves_only_mask]
        model["G_pipe_name_list"] = G_pipe_name_list.tolist()
        model["G_list_pumps_only"] = G_list_pumps_only.tolist()
        model["G_list_valves_only"] = G_list_valves_only.tolist()

        self.model = model
        self.figsize=figsize
        self.axis_frame=axis_frame
    from viswaternet.network.processing import get_parameter, bin_parameter
    from viswaternet.drawing.base import draw_nodes, draw_links, draw_base_elements, plot_basic_elements, draw_label
    from viswaternet.drawing.discrete import draw_discrete_nodes, draw_discrete_links, plot_discrete_nodes, plot_discrete_links
    from viswaternet.drawing.continuous import plot_continuous_links, plot_continuous_nodes
    from viswaternet.drawing.animate import animate_plot
    from viswaternet.drawing.unique import plot_unique_data
    from viswaternet.utils.convert_excel import convert_excel
