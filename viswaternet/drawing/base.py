# -*- coding: utf-8 -*-
"""
The viswaternet.utils.base module contains plotting functions that are 
frequently utilized by other plotting functions. This includes base element
drawing, legend drawing, color map, and label drawing functions.
"""
import numpy as np
import pandas as pd
import networkx.drawing.nx_pylab as nxp
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.lines import Line2D
from mpl_toolkits.axes_grid1 import make_axes_locatable
from viswaternet.utils import save_fig, normalize_parameter


def draw_nodes(
        self,
        ax,
        node_list,
        parameter_results=None,
        node_size = None,
        node_shape = None,
        node_border_width = None,
        node_border_color = None,
        node_color = None,
        vmin=None,
        vmax=None,
        label=None,
        style=None):
    """Draws continuous nodal data onto the figure.
    
    Arguments
    ---------
    ax : axes._subplots.AxesSubplot
        Matplotlib axes object.
        
    node_list : string, array-like
        List of draw_nodes to be drawn.
        
    parameter_results : array-like
        The data associated with each node.
        
    vmin : integer
        The minimum value of the color bar. 
        
    vmax : integer
        The maximum value of the color bar. 
    """
    
    # Initalize parameters
    model = self.model
    if style is None:
        style = self.default_style
    args = style.args
    if parameter_results is None:
        parameter_results = pd.DataFrame([])
    args = style.args
    if node_size is None:
        node_size = args['node_size']
    draw_tanks = args['draw_tanks']
    draw_reservoirs = args['draw_reservoirs']
    cmap = args['cmap']
    if node_shape is None:
        node_shape = args['node_shape']
    if node_border_width is None:
        node_border_width = args['node_border_width']
    if node_border_color is None:
        node_border_color = args['node_border_color']
    if node_color is None:
        node_color = args['node_color']
    if node_size is None:
        node_size = (np.ones(len(node_list)) * 100).tolist()
    # Checks if some data values are given
    if parameter_results.values.tolist():
        # If values is less than this value, we treat it as a negative.
        node_list = [node_list[node_list.index(name)]
                     for name in node_list
                     if ((name not in model["tank_names"]
                          or draw_tanks is False)
                     and (name not in model["reservoir_names"]
                          or draw_reservoirs is False))]
        parameter_results = parameter_results.loc[node_list]
        parameter_results = parameter_results.values.tolist()
        if isinstance(node_size, tuple):
            min_size = node_size[0]
            max_size = node_size[1]
            if min_size is not None and max_size is not None:
                node_size = normalize_parameter(
                    parameter_results, min_size, max_size)
        if np.min(parameter_results) < -1e-5:
            # Gets the cmap object from matplotlib
            cmap = mpl.colormaps[cmap]
            # If both vmin and vmax are None, set vmax to the max data
            # value and vmin to the negative of the max data value. This
            # ensures that the colorbar is centered at 0.
            if vmin is None and vmax is None:
                g = nxp.draw_networkx_nodes(
                    model["G"],
                    model["pos_dict"],
                    ax=ax,
                    nodelist=node_list,
                    node_size=node_size,
                    node_color=parameter_results,
                    cmap=cmap,
                    vmax=np.max(parameter_results),
                    vmin=-np.max(parameter_results),
                    node_shape=node_shape,
                    linewidths=node_border_width,
                    edgecolors=node_border_color)
            # Otherwise, just pass the user-given parameters
            else:
                g = nxp.draw_networkx_nodes(
                    model["G"],
                    model["pos_dict"],
                    ax=ax,
                    nodelist=node_list,
                    node_size=node_size,
                    node_color=parameter_results,
                    vmax=vmax,
                    vmin=vmin,
                    cmap=cmap,
                    node_shape=node_shape,
                    linewidths=node_border_width,
                    edgecolors=node_border_color)
            # Return networkx object
            return g
        else:
            # Gets the cmap object from matplotlib
            cmap = mpl.colormaps[cmap]
            # If both vmin and vmax are None, don't pass vmin and vmax,
            # as networkx will handle the limits of the colorbar
            # itself.
            if vmin is None and vmax is None:
                g = nxp.draw_networkx_nodes(
                    model["G"],
                    model["pos_dict"],
                    ax=ax,
                    nodelist=node_list,
                    node_size=node_size,
                    node_color=parameter_results,
                    cmap=cmap,
                    node_shape=node_shape,
                    linewidths=node_border_width,
                    edgecolors=node_border_color)
            # Otherwise, just pass the user-given parameters
            else:
                g = nxp.draw_networkx_nodes(
                    model["G"],
                    model["pos_dict"],
                    ax=ax,
                    nodelist=node_list,
                    node_size=node_size,
                    node_color=parameter_results,
                    cmap=cmap,
                    node_shape=node_shape,
                    linewidths=node_border_width,
                    edgecolors=node_border_color,
                    vmin=vmin,
                    vmax=vmax)
            # Return networkx object
            return g
    # Draw without any data associated with draw_nodes
    else:
        nxp.draw_networkx_nodes(
            model["G"],
            model["pos_dict"],
            ax=ax,
            nodelist=node_list,
            node_size=node_size,
            node_color=node_color,
            node_shape=node_shape,
            edgecolors=node_border_color,
            linewidths=node_border_width)


def draw_links(
        self,
        ax,
        link_list,
        parameter_results=None,
        link_width=None,
        link_style=None,
        link_arrows=None,
        link_color=None,
        vmin=None,
        vmax=None,
        style=None):
    """Draws continuous link data onto the figure.
    
    Arguments
    ---------
    ax : axes._subplots.AxesSubplot
        Matplotlib axes object.
    
    link_list : string, array-like
        List of draw_links to be drawn.
    
    parameter_results : array-like
        The data associated with each node.
    
    vmin : integer
        The minimum value of the color bar. 
    
    vmax : integer
        The maximum value of the color bar.    
    """
    # Initalize parameters
    model = self.model
    if style is None:
        style = self.default_style
    args = style.args
    if link_width is None:
        link_width = args['link_width']
    pump_element = args['pump_element']
    draw_pumps = args['draw_pumps']
    valve_element = args['valve_element']
    draw_valves = args['draw_valves']
    cmap = args['cmap']
    if link_style is None:
        link_style = args['link_style']
    if link_arrows is None:
        link_arrows = args['link_arrows']
    if link_color is None:
        link_color = args['link_color']
    if isinstance(link_list, np.ndarray):
        link_list = link_list.tolist()
    if parameter_results is None:
        parameter_results = pd.DataFrame([])
    # Creates default list of link widths
    if link_width is None:
        link_width = (np.ones(len(link_list)) * 1).tolist()
    # Checks if some data values are given
    if parameter_results.values.tolist():
        link_list = [link_list[link_list.index(name)]
                     for name in link_list
                     if ((name not in model["pump_names"]
                          or pump_element == 'node'
                          or draw_pumps is False)
                     and (name not in model["valve_names"]
                          or valve_element == 'node'
                          or draw_valves is False))]
        edges = [model["pipe_list"][model['G_pipe_name_list'].index(name)]
                 for name in link_list]
        parameter_results = parameter_results.loc[link_list]
        parameter_results = parameter_results.values.tolist()
        if isinstance(link_width, tuple):
            min_size = link_width[0]
            max_size = link_width[1]
            if min_size is not None and max_size is not None:
                link_width = normalize_parameter(
                    parameter_results, min_size, max_size)
        if np.min(parameter_results) < -1e-5:
            # Gets the cmap object from matplotlib
            cmap = mpl.colormaps[cmap]
            # If both vmin and vmax are None, set vmax to the max data
            # value and vmin to the negative of the max data value. This
            # ensures that the colorbar is centered at 0.
            if vmin is None and vmax is None:
                g = nxp.draw_networkx_edges(
                    model["G"],
                    model["pos_dict"],
                    ax=ax,
                    edgelist=edges,
                    edge_color=parameter_results,
                    edge_vmax=np.max(parameter_results),
                    edge_vmin=-np.max(parameter_results),
                    edge_cmap=cmap,
                    style=link_style,
                    arrows=link_arrows,
                    width=link_width,
                    node_size=0)
            # Otherwise, just pass the user-given parameters
            else:
                g = nxp.draw_networkx_edges(
                    model["G"],
                    model["pos_dict"],
                    ax=ax,
                    edgelist=edges,
                    edge_color=parameter_results,
                    edge_vmax=vmax,
                    edge_vmin=vmin,
                    edge_cmap=cmap,
                    style=link_style,
                    arrows=link_arrows,
                    width=link_width,
                    node_size=0)
            # Return networkx object
            return g
        else:
            # Gets the cmap object from matplotlib
            cmap = mpl.colormaps[cmap]
            # If both vmin and vmax are None, don't pass vmin and vmax,
            # as networkx will handle the limits of the colorbar
            # itself.
            if vmin is None and vmax is None:
                g = nxp.draw_networkx_edges(
                    model["G"],
                    model["pos_dict"],
                    ax=ax,
                    edgelist=edges,
                    edge_color=parameter_results,
                    edge_cmap=cmap,
                    style=link_style,
                    arrows=link_arrows,
                    width=link_width,
                    node_size=0)
            # Otherwise, just pass the user-given parameters
            else:
                g = nxp.draw_networkx_edges(
                    model["G"],
                    model["pos_dict"],
                    ax=ax,
                    edgelist=edges,
                    edge_color=parameter_results,
                    edge_cmap=cmap,
                    style=link_style,
                    arrows=link_arrows,
                    width=link_width,
                    edge_vmin=vmin,
                    edge_vmax=vmax,
                    node_size=0)
            # Return networkx object
            return g
    # Draw without any data associated with draw_links
    else:
        edges = ([model["pipe_list"][i]
                  for i, name in enumerate(link_list)])
        nxp.draw_networkx_edges(
            model["G"],
            model["pos_dict"],
            ax=ax,
            edgelist=edges,
            edge_color=link_color,
            style=link_style,
            arrows=link_arrows,
            width=link_width,
            node_size=0)


def draw_base_elements(
        self,
        ax,
        draw_nodes=True,
        element_list=None,
        style=None):
    """
    Draws base elements (draw_nodes, draw_links, draw_reservoirs, draw_tanks, draw_pumps, and draw_valves)
    without any data associated with the elements.
    
    Arguments
    ---------
    ax : axes._subplots.AxesSubplot
        Matplotlib axes object.
        
    draw_nodes : boolean
        Determines if base draw_nodes with no data associated with them are drawn. Set to False for all functions excep plot_basic_elements by default.
   """
    model = self.model
    if style is None:
        style = self.default_style
    args = style.args
    draw_tanks = args['draw_tanks']
    draw_reservoirs = args['draw_reservoirs']
    base_node_size = args['base_node_size']
    base_node_color = args['base_node_color']
    reservoir_size = args['reservoir_size']
    reservoir_color = args['reservoir_color']
    reservoir_border_color = args['reservoir_border_color']
    reservoir_border_width = args['reservoir_border_width']
    reservoir_shape = args['reservoir_shape']
    tank_size = args['tank_size']
    tank_color = args['tank_color']
    tank_border_color = args['tank_border_color']
    tank_border_width = args['tank_border_width']
    tank_shape = args['tank_shape']
    pump_element = args['pump_element']
    draw_pumps = args['draw_pumps']
    valve_element = args['valve_element']
    draw_valves = args['draw_valves']
    base_link_color = args['base_link_color']
    base_link_width = args['base_link_width']
    base_link_line_style = args['base_link_line_style']
    base_link_arrows = args['base_link_arrows']
    valve_size = args['valve_size']
    valve_color = args['valve_color']
    valve_border_color = args['valve_border_color']
    valve_border_width = args['valve_border_width']
    valve_shape = args['valve_shape']
    pump_size = args['pump_size']
    pump_color = args['pump_color']
    pump_border_color = args['pump_border_color']
    pump_border_width = args['pump_border_width']
    pump_shape = args['pump_shape']
    valve_width = args['valve_width']
    valve_line_style = args['valve_line_style']
    valve_arrows = args['valve_arrows']
    pump_width = args['pump_width']
    pump_line_style = args['pump_line_style']
    pump_arrows = args['pump_arrows']
    # If draw_nodes is True, then draw draw_nodes
    if draw_nodes:
        node_list = model['node_names']
        if element_list is None:
            node_list = [node_list[node_list.index(name)]
                         for name in node_list
                         if ((name not in model["tank_names"]
                              or draw_tanks is False)
                         and (name not in model["reservoir_names"]
                              or draw_reservoirs is False))]
        else:
            node_list = [node_list[node_list.index(name)]
                         for name in node_list
                         if ((name not in model["tank_names"]
                              or draw_tanks is False)
                         and (name not in model["reservoir_names"]
                              or draw_reservoirs is False)
                         and (name not in element_list))]
        nxp.draw_networkx_nodes(
            model["G"],
            model["pos_dict"],
            node_size=base_node_size,
            nodelist=node_list,
            node_color=base_node_color,
            ax=ax)
    # If draw_reservoirs is True, then draw draw_reservoirs
    if draw_reservoirs:
        nxp.draw_networkx_nodes(
            model["G"],
            model["pos_dict"],
            ax=ax,
            nodelist=model["reservoir_names"],
            node_size=reservoir_size,
            node_color=reservoir_color,
            edgecolors=reservoir_border_color,
            linewidths=reservoir_border_width,
            node_shape=reservoir_shape,
            label="Reservoirs")
    # If draw_tanks is True, then draw draw_tanks
    if draw_tanks:
        nxp.draw_networkx_nodes(
            model["G"],
            model["pos_dict"],
            ax=ax,
            nodelist=model["tank_names"],
            node_size=tank_size,
            node_color=tank_color,
            edgecolors=tank_border_color,
            linewidths=tank_border_width,
            node_shape=tank_shape,
            label="Tanks")
    # If draw_links is True, then draw draw_links
    if draw_links:
        pipe_name_list = model['G_pipe_name_list']
        if element_list is None:
            edgelist = [model['pipe_list'][pipe_name_list.index(name)]
                        for name in pipe_name_list
                        if ((name not in model["pump_names"]
                             or pump_element == 'node'
                             or draw_pumps is False)
                        and (name not in model["valve_names"]
                             or valve_element == 'node'
                             or draw_valves is False))]
        else:
            edgelist = [model['pipe_list'][pipe_name_list.index(name)]
                        for name in pipe_name_list
                        if ((name not in model["pump_names"]
                             or pump_element == 'node'
                             or draw_pumps is False)
                        and (name not in model["valve_names"]
                             or valve_element == 'node'
                             or draw_valves is False)
                        and (name not in element_list))]
        nxp.draw_networkx_edges(
            model["G"],
            model["pos_dict"],
            edgelist=edgelist,
            ax=ax,
            edge_color=base_link_color,
            width=base_link_width,
            style=base_link_line_style,
            arrows=base_link_arrows)
    # If draw_valves is True, then draw draw_valves
    if draw_valves:
        if valve_element == 'node':
            valve_coordinates = {}
            # For each valve, calculate midpoint along link it is located at
            # then store the coordinates of where valve should be drawn
            for i, (point1, point2) in enumerate(model["G_list_valves_only"]):
                midpoint = [(model["wn"].get_node(point1).coordinates[0]
                             + model["wn"].get_node(point2).coordinates[0])/2,
                            (model["wn"].get_node(point1).coordinates[1]
                             + model["wn"].get_node(point2).coordinates[1])/2]
                valve_coordinates[model["valve_names"][i]] = midpoint
            # Draw draw_valves after midpoint calculations
            nxp.draw_networkx_nodes(
                model["G"],
                valve_coordinates,
                ax=ax,
                nodelist=model["valve_names"],
                node_size=valve_size,
                node_color=valve_color,
                edgecolors=valve_border_color,
                linewidths=valve_border_width,
                node_shape=valve_shape,
                label="Valves")
        elif valve_element == 'link':
            nxp.draw_networkx_edges(
                model["G"],
                model["pos_dict"],
                ax=ax,
                edgelist=model["G_list_valves_only"],
                edge_color=valve_color,
                width=valve_width,
                style=valve_line_style,
                arrows=valve_arrows)
    # If draw_pumps is True, then draw draw_pumps
    if draw_pumps:
        if pump_element == 'node':
            pump_coordinates = {}
            # For each valve, calculate midpoint along link it is located at
            # then store the coordinates of where pump should be drawn
            for i, (point1, point2) in enumerate(model["G_list_pumps_only"]):
                midpoint = [(model["wn"].get_node(point1).coordinates[0]
                             + model["wn"].get_node(point2).coordinates[0])/2,
                            (model["wn"].get_node(point1).coordinates[1]
                             + model["wn"].get_node(point2).coordinates[1])/2]
                pump_coordinates[model["pump_names"][i]] = midpoint
            # Draw draw_valves after midpoint calculations
            nxp.draw_networkx_nodes(
                model["G"],
                pump_coordinates,
                ax=ax,
                nodelist=model["pump_names"],
                node_size=pump_size,
                node_color=pump_color,
                edgecolors=pump_border_color,
                linewidths=pump_border_width,
                node_shape=pump_shape,
                label="Pumps")
        elif pump_element == 'link':
            nxp.draw_networkx_edges(
                model["G"],
                model["pos_dict"],
                ax=ax,
                edgelist=model["G_list_pumps_only"],
                edge_color=pump_color,
                width=pump_width,
                style=pump_line_style,
                arrows=pump_arrows)


def plot_basic_elements(
        self,
        ax=None,
        draw_nodes=True,
        savefig=False,
        save_name=None,
        style=None):
    """User-level function that draws base elements with no data assocaited with
    them, draws a legend, and saves the figure.
    
    Arguments
    ---------
    ax : axes._subplots.AxesSubplot
        Matplotlib axes object.
   
    draw_nodes : boolean
        Determines if base draw_nodes with no data associated with them are drawn. Set to False for all functions excep plot_basic_elements by default.
    
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
    if style is None:
        style = self.default_style
    args = style.args
    # Checks if an axis as been specified
    if ax is None:
        if ax is None:
            fig, ax = plt.subplots(figsize=self.figsize)
            ax.set_frame_on(self.axis_frame)
    # Draw all base elements w/o data associated with them
    draw_base_elements(
        self,
        ax,
        draw_nodes=draw_nodes,
        style=style)
    # Draw legend if legend is True. Only draws base elements legend
    draw_legend(
        self,
        ax,
        style=style)
    # Save figure if savefig is set to True
    if savefig:
        save_fig(self, save_name=save_name, style=style)


def draw_legend(
        self,
        ax,
        intervals=None,
        title=None,
        element_size_intervals=None,
        element_size_legend_title=None,
        element_size_legend_loc=None,
        element_size_legend_labels=None,
        style=None):
    """Draws the legends for all other plotting functions. There are two legends that might be drawn. One is the base elements legend with displays what markers are associated with each element type (draw_nodes, draw_links, etc.) The other legend is the intervals legend which is the legend for discrete drawing. Under normal use, draw_legends is not normally called by the user directly, even with more advanced applications. However, some specialized plots may require draw_legend to be called directly.
    
    Arguments
    ---------
    ax : axes._subplots.AxesSubplot
        Matplotlib axes object.
   
    intervals : array-like, string
        If set to 'automatic' then intervals are created automatically on a equal interval basis. Otherwise, it is the edges of the intervals to be created. intervals array length should be num_intervals + 1.
    
    color_list : string, array-like
        The list of node colors for each interval. Both cmap and color_list can not be used at the same time to color draw_nodes. If both are, then color_list takes priority.
    
    cmap : string
        The matplotlib color map to be used for plotting. Refer to matplotlib documentation for possible inputs.
    
    title : string
        The title text of the legend.
    
    element_size_intervals : integer
        The number of intervals to be used if an element size legend is used.
    
    element_size_legend_title : string
        The title of the element size legend.
    
    element_size_legend_loc : string
        The location of the element size legend on the figure.
    
    element_size_legend_labels : array-like
        The labels of each interval of the element size legend.
    
    node_border_color : string
        The color of the legend draw_nodes edges when plotting element size legend.
    
    linewidths: integer
        The width of the line of the legend draw_nodes when plotting element size legend.
    """
    # If no intervals for data legend are specified, then create empty array
    if intervals is None:
        intervals = []
    if style is None:
        style = self.default_style
    args = style.args
    pump_color = args['pump_color']
    pump_element = args['pump_element']
    draw_pumps = args['draw_pumps']
    valve_color = args['valve_color']
    valve_element = args['valve_element']
    draw_valves = args['draw_valves']
    valve_line_style = args['valve_line_style']
    valve_arrows = args['valve_arrows']
    pump_line_style = args['pump_line_style']
    pump_arrows = args['pump_arrows']
    base_link_color = args['base_link_color']
    base_link_line_style = args['base_link_line_style']
    base_link_arrows = args['base_link_arrows']
    draw_base_legend = args['draw_base_legend']
    base_legend_loc = args['base_legend_loc']
    base_legend_label_font_size = args['base_legend_label_font_size']
    base_legend_label_color = args['base_legend_label_color']
    draw_legend_frame = args['draw_legend_frame']
    draw_discrete_legend = args['draw_discrete_legend']
    discrete_legend_loc = args['discrete_legend_loc']
    discrete_legend_label_font_size = args['discrete_legend_label_font_size']
    discrete_legend_label_color = args['discrete_legend_label_color']
    draw_legend_frame = args['draw_legend_frame']
    discrete_legend_title_color = args['discrete_legend_title_color']
    discrete_legend_title_font_size = args['discrete_legend_title_font_size']
    cmap = args['cmap']
    color_list = args['color_list']
    node_size = args['node_size']
    node_border_width = args['node_border_width']
    node_border_color = args['node_border_color']
    link_width = args['link_width']
    # Get handles, labels
    handles, labels = ax.get_legend_handles_labels()

    # Where new handles will be stored
    extensions = []

    # If draw_pumps is True, then add legend element. Note that right now
    # pump_arrows does not affect legend entry, but that it may in the future,
    # hence the if statement
    if draw_pumps and pump_element == 'link':
        if pump_arrows:
            extensions.append(Line2D([0], [0], color=pump_color,
                              linestyle=pump_line_style, lw=4, label='Pumps'))
        else:
            extensions.append(Line2D([0], [0], color=pump_color,
                              linestyle=pump_line_style, lw=4, label='Pumps'))
    if draw_valves and valve_element == 'link':
        if valve_arrows:
            extensions.append(Line2D([0], [0], color=valve_color,
                              linestyle=valve_line_style, lw=4,
                              label='Valves'))
        else:
            extensions.append(Line2D([0], [0], color=valve_color,
                              linestyle=valve_line_style, lw=4,
                              label='Valves'))
    # If draw_base_links is True, then add legend element. Note that right now
    # base_link_arrows does not affect legend entry, but that it may in the
    # future, hence the if statement
    if draw_links:
        if base_link_arrows:
            extensions.append(Line2D([0], [0], color=base_link_color,
                              linestyle=base_link_line_style, lw=4,
                              label='Pipes'))
        else:
            extensions.append(Line2D([0], [0], color=base_link_color,
                              linestyle=base_link_line_style, lw=4,
                              label='Pipes'))
    # Extend handles list
    handles.extend(extensions)

    # If discrete intervals are given
    if intervals:
        # Draws base legend, which includes the legend for draw_reservoirs,
        # draw_tanks, and so on
        if draw_base_legend is True:
            legend = ax.legend(handles=handles[len(intervals):],
                               loc=base_legend_loc,
                               fontsize=base_legend_label_font_size,
                               labelcolor=base_legend_label_color,
                               frameon=draw_legend_frame)
            # Align legend text to the left, add legend to ax
            legend._legend_box.align = "left"
            ax.add_artist(legend)
        # Draws intervals, or data, legend to the ax
        if draw_discrete_legend is True:
            if isinstance(discrete_legend_label_color, str) \
                    and discrete_legend_label_color != 'interval_color':
                legend2 = ax.legend(
                    title=title,
                    handles=handles[: len(intervals)],
                    loc=discrete_legend_loc,
                    fontsize=discrete_legend_label_font_size,
                    labelcolor=discrete_legend_label_color,
                    title_fontsize=discrete_legend_title_font_size,
                    frameon=draw_legend_frame)

            if discrete_legend_label_color == 'interval_color':
                legend2 = ax.legend(
                    title=title, handles=handles[: len(intervals)],
                    loc=discrete_legend_loc,
                    fontsize=discrete_legend_label_font_size,
                    title_fontsize=discrete_legend_title_font_size,
                    frameon=draw_legend_frame)
                if color_list:
                    for i, text in enumerate(legend2.get_texts()):
                        text.set_color(color_list[i])
                elif cmap:
                    cmap = mpl.colormaps[cmap]
                    cmap_value = 1 / len(intervals)
                    for i, text in enumerate(legend2.get_texts()):
                        text.set_color(cmap(float(cmap_value)))
                        cmap_value += 1 / len(intervals)
            if isinstance(discrete_legend_label_color, list):
                legend2 = ax.legend(
                    title=title,
                    handles=handles[: len(intervals)],
                    loc=discrete_legend_loc,
                    fontsize=discrete_legend_label_font_size,
                    title_fontsize=discrete_legend_title_font_size,
                    frameon=draw_legend_frame)
                for i, text in enumerate(legend2.get_texts()):
                    text.set_color(discrete_legend_label_color[i])
            # Align legend text to the left, adds title, and adds to ax
            legend2._legend_box.align = "left"
            legend2.get_title().set_color(discrete_legend_title_color)
            ax.add_artist(legend2)
    # If there are no intervals, just draw base legend
    else:
        # Draws base legend, which includes the legend for draw_reservoirs,
        # draw_tanks, and so on
        if draw_base_legend is True:
            legend = ax.legend(handles=handles,
                               loc=base_legend_loc,
                               fontsize=base_legend_label_font_size,
                               labelcolor=base_legend_label_color,
                               frameon=draw_legend_frame)
            # Align legend text to the left, add legend to ax
            legend._legend_box.align = "left"
            ax.add_artist(legend)

    # The following code is for a node/link legend. This adds a 2nd dimension
    # to the data that can be plotted, by allowing for changes in size of
    # a node/link to represent some parameter. For now it is limited to
    # discrete node sizes, which works the same as discrete data for the color
    # of draw_nodes. To use it requires a much more involved process than all
    # other functions that viswaternet performs, and improvements to ease of
    # use will be made in the future.
    if node_size is not None and element_size_intervals is not None:
        if isinstance(node_size, list):
            handles_2 = []
            min_size = np.min(node_size)
            max_size = np.max(node_size)
            marker_sizes = np.linspace(
                min_size, max_size, element_size_intervals)
            for size, label in zip(marker_sizes, element_size_legend_labels):
                handles_2.append(Line2D([], [], marker='.', color='w',
                                 markeredgecolor=node_border_color,
                                 markeredgewidth=node_border_width,
                                 label=label, markerfacecolor='k',
                                 markersize=np.sqrt(size)))
            legend3 = ax.legend(
                handles=handles_2,
                title=element_size_legend_title,
                loc=element_size_legend_loc,
                fontsize=discrete_legend_label_font_size,  # Change later!
                title_fontsize=discrete_legend_title_font_size,
                labelcolor=discrete_legend_label_color,
                frameon=draw_legend_frame)
            legend3._legend_box.align = "left"
            ax.add_artist(legend3)
    if link_width is not None and element_size_intervals is not None:
        if isinstance(link_width, list):
            handles_2 = []
            min_size = np.min(link_width)
            max_size = np.max(link_width)
            marker_sizes = np.linspace(
                min_size, max_size, element_size_intervals)
            for size, label in zip(marker_sizes, element_size_legend_labels):
                handles_2.append(Line2D([], [], marker=None, color='k',
                                 linewidth=size, label=label))
            legend3 = ax.legend(
                handles=handles_2,
                title=element_size_legend_title,
                loc=element_size_legend_loc,
                fontsize=discrete_legend_label_font_size,
                title_fontsize=discrete_legend_title_font_size,
                labelcolor=discrete_legend_label_color,
                frameon=draw_legend_frame)
            legend3._legend_box.align = "left"
            ax.add_artist(legend3)


def draw_color_bar(
        self,
        ax,
        g,
        color_bar_title=None,
        style=None):
    """Draws the color bar for all continuous plotting functions.Like draw_legends, under normal use, draw_color_bar is not normally called by the user directly, even with more advanced applications. However, some specialized plots may require draw_color_bar to be called directly.
    
    Arguments
    ---------
    ax : axes._subplots.AxesSubplot
        Matplotlib axes object.
    
    g : NetworkX path collection
        The list of elements drawn by NetworkX function.
    
    cmap : string
        The matplotlib color map to be used for plotting. Refer to matplotlib documentation for possible inputs.
    
    color_bar_title : string
        The title of the color bar.
    """
    # Unruly code to make colorbar location nice and symmetrical when dealing
    # with subplots especially.
    if style is None:
        style = self.default_style
    args = style.args
    color_bar_height = args['color_bar_height']
    color_bar_width = args['color_bar_width']
    cmap = args['cmap']
    divider = make_axes_locatable(ax)
    fig = plt.gcf()
    cax = fig.add_axes([divider.get_position()[0]+divider.get_position()[2]
                        + 0.02, (divider.get_position()[1])
                        + ((divider.get_position()[3]
                            * (1-color_bar_height)))/2,
                        color_bar_width,
                        divider.get_position()[3]*color_bar_height])
    cbar = fig.colorbar(g, cax=cax)
    cbar.set_label(color_bar_title, fontsize=10)


def draw_label(
        self,
        labels,
        x_coords,
        y_coords,
        ax=None,
        draw_nodes=None,
        draw_arrow=True,
        label_font_size=11,
        label_text_color='k',
        label_face_color='white',
        label_edge_color='k',
        label_alpha=0.9,
        label_font_style=None,
        label_edge_width=None
        ):
    """Draws customizable labels on the figure.
    There are two modes of coordinate input: If the 'draw_nodes' argument is not specified, then the label coordinates are processed as absolute coordinates with possible values from 0 to 1. For instance, (0,0) would place the label in the bottom left of the figure, while (1,1) would place the label in the top right of the figure. If the 'draw_nodes' argument IS specified, then the coordinates are processed as coordinates relative to it's associated node. The scale of the coordinates scaling differs between networks. For instance, (50,100) would place the label 50 units to the right, and 100 units above the associated node.
    
    Arguments
    ---------
    ax : axes._subplots.AxesSubplot
        Matplotlib axes object.
    
    labels : string, array-like
        The label(s) textual content.
    
    x_coords : integer, array-like
        The x coordinate(s) of the labels.
    
    y_coords : integer, array-like
        The y coordinate(s) of the labels.
    
    draw_nodes : string, array-like
        A list of the draw_nodes the labels are to be associated with.
    
    draw_arrow : boolean
        Determine if an arrow is drawn from the associated draw_nodes to labels.
    
    label_font_size : integer
        The font size of the labels.
        
    label_text_color : string
        The color of the text of the labels.
        
    label_face_color : string
    
    label_edge_color : string
    
    label_alpha : integer
    
    label_font_style : string
        
    label_edge_width : integer
    """
    model = self.model
    if ax is None:
        ax = self.ax
    if draw_nodes is not None:
        for label, node, xCoord, yCoord in \
                zip(labels, draw_nodes, x_coords, y_coords):
            if draw_arrow:
                edge_list = []
                if label == node:
                    pass
                else:
                    model["G"].add_node(label, pos=(xCoord, yCoord))
                    model["pos_dict"][label] = (
                        model["wn"].get_node(node).coordinates[0] + xCoord,
                        model["wn"].get_node(node).coordinates[1] + yCoord)
                    edge_list.append((node, label))
                    nxp.draw_networkx_edges(
                        model["G"], model["pos_dict"], edgelist=edge_list,
                        edge_color="g", width=0.8, arrows=False)
                    model["G"].remove_node(label)
                    model["pos_dict"].pop(label, None)
                    edge_list.append((node, label))
            if draw_arrow is True:
                if xCoord < 0:
                    ax.text(
                        model["wn"].get_node(node).coordinates[0] + xCoord,
                        model["wn"].get_node(node).coordinates[1] + yCoord,
                        s=label,
                        color=label_text_color,
                        style=label_font_style,
                        bbox=dict(facecolor=label_face_color,
                                  alpha=label_alpha,
                                  edgecolor=label_edge_color,
                                  lw=label_edge_width),
                        horizontalalignment="right",
                        verticalalignment="center",
                        fontsize=label_font_size)
                if xCoord >= 0:
                    ax.text(
                        model["wn"].get_node(node).coordinates[0] + xCoord,
                        model["wn"].get_node(node).coordinates[1] + yCoord,
                        s=label,
                        color=label_text_color,
                        style=label_font_style,
                        bbox=dict(facecolor=label_face_color,
                                  alpha=label_alpha,
                                  edgecolor=label_edge_color,
                                  lw=label_edge_width),
                        horizontalalignment="left",
                        verticalalignment="center",
                        fontsize=label_font_size)
            else:
                ax.text(
                    model["wn"].get_node(node).coordinates[0] + xCoord,
                    model["wn"].get_node(node).coordinates[1] + yCoord,
                    s=label, color=label_text_color, style=label_font_style,
                    bbox=dict(facecolor=label_face_color,
                              alpha=label_alpha, edgecolor=label_edge_color,
                              lw=label_edge_width),
                    horizontalalignment="center",
                    verticalalignment="center", fontsize=label_font_size)
    elif draw_nodes is None:
        for label, xCoord, yCoord in zip(labels, x_coords, y_coords):
            ax.text(
                xCoord,
                yCoord,
                s=label,
                color=label_text_color,
                style=label_font_style,
                bbox=dict(facecolor=label_face_color,
                          alpha=label_alpha,
                          edgecolor=label_edge_color,
                          lw=label_edge_width),
                horizontalalignment="center",
                fontsize=label_font_size,
                transform=ax.transAxes)
