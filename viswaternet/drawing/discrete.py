# -*- coding: utf-8 -*-
"""
The viswaternet.drawing.discrete module handles everything related to discrete data drawing.
"""

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import networkx.drawing.nx_pylab as nxp
from viswaternet.network import processing
from viswaternet.utils import save_fig, unit_conversion, label_generator
from viswaternet.drawing import base


def draw_discrete_nodes(
        self,
        ax,
        element_list,
        intervals,
        label_list=None,
        style=None):
    """Draws discretized nodal data onto the figure.
    
    Arguments
    ---------
    ax : axes._subplots.AxesSubplot
        Matplotlib axes object.
        
    element_list : array-like
        List of network elements that data will be retrieved for.
        
    intervals : dict
        The dictionary containting the intervals and the draw_nodes assocaited with each interval.
        
    label_list : string, array-like
        List of labels for each interval.
    """
    model = self.model
    if style is None:
        style = self.default_style
    args = style.args
    node_size = args['node_size']
    node_shape = args['node_shape']
    node_border_color = args['node_border_color']
    node_border_width = args['node_border_width']
    color_list = args['color_list']
    cmap = args['cmap']
    if node_size is None:
        if len(model["node_names"]) < 300:
            node_size = (np.ones(len(intervals)) * 300).tolist()
        elif len(model["node_names"]) >= 300 \
                and len(model["node_names"]) < 1000:
            node_size = (np.ones(
                len(intervals)) * (80000 / len(model["node_names"]))).tolist()
        else:
            node_size = (np.ones(len(intervals)) * 80).tolist()
    if isinstance(node_size, int) or isinstance(node_size, float):
        node_size = (np.ones(len(intervals)) * node_size).tolist()
    if label_list is None:
        label_list = intervals
    if node_shape is None:
        node_shape = ['.' for i in range(len(intervals))]
    if isinstance(node_shape, str):
        node_shape = [node_shape for i in range(len(intervals))]
    if node_border_color is None:
        node_border_color = ['k' for i in range(len(intervals))]    
    if isinstance(node_border_color, str):
        node_border_color = [node_border_color for i in range(len(intervals))]
    if node_border_width is None:
       node_border_width = [0 for i in range(len(intervals))]
    if isinstance(node_border_width, int) \
            or isinstance(node_border_width, float):
        node_border_width = [node_border_width for i in range(len(intervals))]
    if (color_list is not None and cmap is not None) or color_list is not None:
        for j, interval_name in enumerate(intervals):
            interval_elements = element_list.get(interval_name)
            if interval_elements:
                node_list = [model["node_names"][i]
                             for i in element_list.get(interval_name).values()]
                nxp.draw_networkx_nodes(
                    model["G"], model["pos_dict"], ax=ax,
                    nodelist=(
                        [model["node_names"][i]
                         for i in element_list.get(interval_name).values()]),
                    node_size=node_size[j],
                    node_color=color_list[j],
                    node_shape=node_shape[j],
                    label=label_list[j],
                    edgecolors=node_border_color[j],
                    linewidths=node_border_width[j])
            else:
                m = Line2D([], [], color=color_list[j],
                              marker=node_shape[j], 
                              linestyle='None',
                              markersize=node_size[j]**(1/2),
                              markeredgecolor=node_border_color[j],
                              markeredgewidth=node_border_width[j],
                              label=label_list[j])
                ax.add_artist(m)          
    else:
        cmap = mpl.colormaps[cmap]
        cmapValue = 1 / len(intervals)
        for j, interval_name in enumerate(intervals):
            interval_elements = element_list.get(interval_name)
            if interval_elements:
                node_list = [model["node_names"][i]
                             for i in element_list.get(interval_name).values()]
                nxp.draw_networkx_nodes(
                    model["G"],
                    model["pos_dict"],
                    ax=ax,
                    nodelist=node_list,
                    node_size=node_size[j],
                    node_color=[cmap(float(cmapValue))],
                    node_shape=node_shape[j],
                    label=label_list[j],
                    edgecolors=node_border_color[j],
                    linewidths=node_border_width[j])
            else:
                m = Line2D([], [], color=cmap(float(cmapValue)),
                              marker=node_shape[j], 
                              linestyle='None',
                              markersize=node_size[j]**(1/2),
                              markeredgecolor=node_border_color[j],
                              markeredgewidth=node_border_width[j],
                              label=label_list[j])
                ax.add_artist(m)
            cmapValue += 1 / len(intervals)




def draw_discrete_links(
        self,
        ax,
        element_list,
        intervals,
        label_list=None,
        style=None):
    """Draws discretized link data onto the figure.
    
    Arguments
    ---------
    ax : axes._subplots.AxesSubplot
        Matplotlib axes object.
        
    element_list : array-like
        List of network elements that data will be retrieved for.
        
    intervals : dict
        The dictionary containting the intervals and the draw_links associated with each interval.
        
    label_list : string, array-like
        List of labels for each interval.
    """
    model = self.model
    if style is None:
        style = self.default_style
    args = style.args
    link_width = args['link_width']
    link_style = args['link_style']
    link_arrows = args['link_arrows']
    color_list = args['color_list']
    cmap = args['cmap']
    if link_width is None:
        link_width = (np.ones(len(intervals)) * 2).tolist()
    if isinstance(link_width, int) or isinstance(link_width, float):
        link_width = (np.ones(len(intervals)) * link_width).tolist()
    if label_list is None:
        label_list = intervals
    if isinstance(link_style, str):
        link_style = [link_style for i in range(len(intervals))]
    if isinstance(link_arrows, bool):
        link_arrows = [link_arrows for i in range(len(intervals))]
    if (color_list is not None and cmap is not None) or color_list is not None:
        for j, interval_name in enumerate(intervals):
            interval_elements = element_list.get(interval_name)
            if interval_elements:
                edge_list = [model["pipe_list"][i]
                             for i in element_list.get(interval_name).values()]
                nxp.draw_networkx_edges(
                    model["G"],
                    model["pos_dict"],
                    ax=ax,
                    edgelist=edge_list,
                    edge_color=color_list[j],
                    width=link_width[j],
                    arrows=link_arrows[j],
                    style=link_style[j],
                    label=label_list[j])
            else:
                nxp.draw_networkx_edges(
                    model["G"],
                    model["pos_dict"],
                    ax=ax,
                    edgelist=[(model['node_names'][0], 
                               model['node_names'][0])],
                    edge_color=color_list[j],
                    width=link_width[j],
                    arrows=link_arrows[j],
                    style=link_style[j],
                    label=label_list[j])    
    else:
        cmap = mpl.colormaps[cmap]
        cmapValue = 1 / len(intervals)
        for j, interval_name in enumerate(intervals):
            interval_elements = element_list.get(interval_name)
            if interval_elements:
                edge_list = [model["pipe_list"][i]
                             for i in element_list.get(interval_name).values()]
                nxp.draw_networkx_edges(
                    model["G"],
                    model["pos_dict"],
                    ax=ax,
                    edgelist=edge_list,
                    edge_color=[cmap(float(cmapValue))],
                    width=link_width[j],
                    arrows=link_arrows[j],
                    style=link_style[j],
                    label=label_list[j])
            else:
                # Janky as always :)
                nxp.draw_networkx_edges(
                    model["G"],
                    model["pos_dict"],
                    ax=ax,
                    edgelist=[(model['node_names'][0], 
                               model['node_names'][0])],
                    edge_color=[cmap(float(cmapValue))],
                    width=link_width[j],
                    arrows=link_arrows[j],
                    style=link_style[j],
                    label=label_list[j])
            cmapValue += 1 / len(intervals)
    pos = model["pos_dict"]
    edge_list_x = []
    edge_list_y = []
    for edge in pos.values():
        edge_list_x.append(edge[0])
        edge_list_y.append(edge[1])
    minx = np.min(edge_list_x)
    maxx = np.max(edge_list_x)
    miny = np.min(edge_list_y)
    maxy = np.max(edge_list_y)
    w = maxx - minx
    h = maxy - miny
    padx, pady = 0.05 * w, 0.05 * h
    corners = (minx - padx, miny - pady), (maxx + padx, maxy + pady)
    ax.update_datalim(corners)
    ax.autoscale_view()


def plot_discrete_nodes(
        self,
        ax=None,
        num_intervals=5,
        parameter=None,
        value=None,
        unit=None,
        element_list=None,
        include_tanks=False,
        include_reservoirs=False,
        intervals="automatic",
        label_list=None,
        savefig=False,
        save_name=None,
        draw_nodes=True,
        discrete_legend_title=None,
        disable_interval_deleting=True,
        style=None):
    """User-level function that draws discretized nodal data, base elements, legends, and saves the figure.
   
    Arguments
    ---------
    ax : axes._subplots.AxesSubplot
        Matplotlib axes object.
        
    num_intervals : integer
        The number of intervals.
        
    parameter : string
        The parameter to be plotted. The following is a list of parameters
        available to use:
        **Static Parameters**    
        - base_demand
        - elevation
        - emitter_coefficient
        - initial_quality
        
        **Time-Dependent Parameters**
        - head
        - demand
        - leak_demand
        - leak_area
        - leak_discharg_coeff
        - quality
        
    value : integer, string
        For time-varying parameters only. Specifies which timestep or data
        summary will be plotted.
        
        .. rubric:: Possible Inputs
        
        ======================= =========================================
            int                 Plots element data for specified timestep
            'min'               Plots minimum data point for each element
            'max'               Plots maximum data point for each element
            'mean'              Plots mean for each element
            'stddev'            Plots standard deviation for each element
            'range'             Plots range for each element
        ======================= =========================================
        
    unit : string
        The unit that the network data is to be converted to.
        
    element_list : array-like
        List of network elements that data will be retrieved for.
        
    include_tanks : boolean
        Determines if data for draw_tanks are retrieved.
        
    include_reservoirs : boolean
        Determines if data for draw_reservoirs are retrieved.
        
    intervals : integer, string
        If set to 'automatic' then intervals are created automatically on a equal interval basis. Otherwise, it is the edges of the intervals to be created. Intervals array length should be num_intervals + 1.
        
    label_list : string, array-like
        List of labels for each interval.
        
    draw_nodes : boolean
        Determines if draw_nodes with no data associated with them are drawn.

    disable_interval_deleting : boolean
        If True, empty intervals will be automatically deleted. 
    
    discrete_legend_title : string
        Title of the intervals legend.
    
    savefig : boolean
        Determines if the figure is saved. 
    
    save_name : string
        The inputted string will be appended to the name of the network.
    
        Example
        -------
        >>>import viswaternet as vis
        >>>model = vis.VisWNModel(r'Networks/Net3.inp')
        ...
        >>>model.save_fig(save_name='_example')
        <Net3_example.png>
    """
    model = self.model
    if style is None:
        style = self.default_style
    args = style.args
    draw_reservoirs = args['draw_reservoirs']
    draw_tanks = args['draw_tanks']
    if ax is None:
        if ax is None:
            fig, ax = plt.subplots(figsize=self.figsize)
            ax.set_frame_on(self.axis_frame)
    if parameter is not None:
        if not isinstance(value, list):
            parameter_results, node_list = processing.get_parameter(
                self,
                "node",
                parameter,
                element_list=element_list,
                value=value,
                include_tanks=include_tanks,
                include_reservoirs=include_reservoirs)
        else:
            parameter_results = value[0]
            node_list = value[1]
        node_list = [node_list[node_list.index(name)]
                     for name in node_list
                     if ((name not in model["reservoir_names"]
                          or draw_reservoirs is False)
                     and (name not in model["tank_names"]
                          or draw_tanks is False))]
        parameter_results = parameter_results.loc[node_list]
        parameter_results = parameter_results.values.tolist()
        if unit is not None:
            parameter_results = unit_conversion(
                parameter_results, parameter, unit)
        interval_results, interval_names = processing.bin_parameter(
            self,
            parameter_results,
            node_list,
            intervals=intervals,
            num_intervals=num_intervals,
            disable_interval_deleting=disable_interval_deleting,
            style=style)
        draw_discrete_nodes(
            self,
            ax,
            interval_results,
            interval_names,
            label_list=label_list)
        base.draw_base_elements(
            self,
            ax,
            draw_nodes=draw_nodes,
            include_reservoirs=include_reservoirs,
            include_tanks=include_tanks,
            element_list=node_list,
            style=style)

        if discrete_legend_title is None:
            discrete_legend_title = label_generator(parameter, value, unit)

        base.draw_legend(
            ax,
            intervals=interval_names,
            title=discrete_legend_title,
            style=style)
    if savefig:
        save_fig(self, save_name=save_name, style=style)


def plot_discrete_links(
        self,
        ax=None,
        num_intervals=5,
        parameter=None,
        element_list=None,
        include_pumps=True,
        include_valves=True,
        value=None,
        unit=None,
        intervals="automatic",
        label_list=None,
        draw_nodes=False,
        discrete_legend_title=None,
        savefig=False,
        save_name=None,
        disable_interval_deleting=True,
        style=None):
    """User-level function that draws discretized link data, base elements, legends, and saves the figure.
    
    Arguments
    ---------
    ax : axes._subplots.AxesSubplot
        Matplotlib axes object.
        
    num_intervals : integer
        The number of intervals.
        
    parameter : string
        The parameter to be plotted. The following is a list of parameters
        available to use:
        **Static Parameters**    
        - length
        - minor_loss
        - bulk_coeff
        - wall_coeff
       
        **Time-Dependent Parameters**
        - flowrate
        - velocity
        - headloss
        - friction_factor
        - reaction_rate
        - quality
    
    value : integer, string
        For time-varying parameters only. Specifies which timestep or data summary will be plotted.
        
        .. rubric:: Possible Inputs
        
        ======================= =========================================
            int                 Plots element data for specified timestep
            'min'               Plots minimum data point for each element
            'max'               Plots maximum data point for each element
            'mean'              Plots mean for each element
            'stddev'            Plots standard deviation for each element
            'range'             Plots range for each element
        ======================= =========================================
        
    unit : string
        The unit that the network data is to be converted to.
    
    element_list : array-like
        List of network elements that data will be retrieved for.
    
    include_pumps : boolean
        Determines if data for draw_pumps are retrieved.
    
    include_valves : boolean
        Determines if data for draw_valves are retrieved.
    
    intervals : integer, string
        If set to 'automatic' then intervals are created automatically on an equal interval basis. Otherwise, it is the edges of the intervals to be created. intervals array length should be num_intervals + 1.
    
    disable_interval_deleting : boolean
        If True, empty intervals will be automatically deleted.     
    
    label_list : string, array-like
        List of labels for each interval.
        
    draw_nodes : boolean
        Determines if draw_nodes with no data associated with them are drawn.
        
    discrete_legend_title : string
        Title of the intervals legend.
        
    savefig : boolean
        Determines if the figure is saved. 
    
    save_name : string
        The inputted string will be appended to the name of the network.
    
        Example
        -------
        >>>import viswaternet as vis
        >>>model = vis.VisWNModel(r'Networks/Net3.inp')
        ...
        >>>model.save_fig(save_name='_example')
        <Net3_example.png>
    """
    model = self.model
    if style is None:
        style = self.default_style
    args = style.args
    pump_element = args['pump_element']
    draw_pumps = args['draw_pumps']
    valve_element = args['valve_element']
    draw_valves = args['draw_valves']
    if ax is None:
        if ax is None:
            fig, ax = plt.subplots(figsize=self.figsize)
            ax.set_frame_on(self.axis_frame)
    if parameter is not None:
        if not isinstance(value, list):
            parameter_results, link_list = processing.get_parameter(
                self,
                "link",
                parameter,
                element_list=element_list,
                value=value,
                include_pumps=include_pumps,
                include_valves=include_valves)
        else:
            parameter_results = value[0]
            link_list = value[1]
        link_list = [link_list[link_list.index(name)]
                     for name in link_list
                     if ((name not in model["pump_names"]
                          or pump_element == 'node'
                          or draw_pumps is False
                          or include_pumps is False)
                     and (name not in model["valve_names"]
                          or valve_element == 'node'
                          or draw_valves is False
                          or include_valves is False))]
        parameter_results = parameter_results.loc[link_list]
        parameter_results = parameter_results.values.tolist()
        if unit is not None:
            parameter_results = unit_conversion(
                parameter_results, parameter, unit)
        interval_results, interval_names = processing.bin_parameter(
            self,
            parameter_results,
            link_list,
            intervals=intervals,
            num_intervals=num_intervals,
            disable_interval_deleting=disable_interval_deleting,
            style=style)
        draw_discrete_links(
            self, ax, interval_results, interval_names,
            label_list=label_list, style=style)
        base.draw_base_elements(
            self,
            ax,
            draw_nodes=draw_nodes,
            include_pumps=include_pumps,
            include_valves=include_valves,
            element_list=link_list,
            style=style)
        if discrete_legend_title is None:
            discrete_legend_title = label_generator(parameter, value, unit)
        base.draw_legend(
            ax,
            intervals=interval_names,
            title=discrete_legend_title,
            style=style)
    if savefig:
        save_fig(self, save_name=save_name, style=style)
