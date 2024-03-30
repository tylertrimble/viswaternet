# -*- coding: utf-8 -*-
"""
The viswaternet.drawing.discrete module handles everything related to discrete data drawing.
"""

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import networkx.drawing.nx_pylab as nxp
from viswaternet.network import processing
from viswaternet.utils import save_fig, unit_conversion, label_generator
from viswaternet.drawing import base
from viswaternet.utils.markers import *

default_cmap = 'autumn_r'


def draw_discrete_nodes(
        self,
        ax,
        element_list,
        intervals,
        node_size=None,
        label_list=None,
        node_shape=None,
        cmap="tab10",
        node_border_color=None,
        node_border_width=None,
        color_list=None):
    """Draws discretized nodal data onto the figure.
    
    Arguments
    ---------
    ax : axes._subplots.AxesSubplot
        Matplotlib axes object.
        
    element_list : array-like
        List of network elements that data will be retrieved for.
        
    intervals : dict
        The dictionary containting the intervals and the draw_nodes assocaited with each interval.
        
    node_size : integer, array-like
        List of node sizes for each interval.
        
    label_list : string, array-like
        List of labels for each interval.
        
    node_shape : string, array-like
        List of node shapes for each interval. Refer to matplotlib documentation for available marker types.
        
    cmap : string
        The matplotlib color map to be used for plotting. Refer to matplotlib documentation for possible inputs.
        
    node_border_color : string, array-like
        The color of the node borders for each interval.
        
    node_border_width  : integer, array-like
        The width of the node borders for each interval.
        
    color_list : string, array-like
        The list of node colors for each interval. Both cmap and color_list can not be used at the same time to color draw_nodes. If both are, then color_list takes priority.
    """
    model = self.model
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
    empty_interval = False
    if (color_list is not None and cmap is not None) or color_list is not None:
        for j, interval_name in enumerate(intervals):
            node_list = [model["node_names"][i]
                         for i in element_list.get(interval_name).values()]

            if not node_list:
                nxp.draw_networkx_nodes(
                    model["G"],
                    model["pos_dict"],
                    ax=ax,
                    nodelist=[model["node_names"][0]],
                    node_size=node_size[j],
                    node_color=color_list[j],
                    node_shape=node_shape[j],
                    label=label_list[j],
                    edgecolors=node_border_color[j],
                    linewidths=node_border_width[j])
                empty_interval is True
            else:
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
        if empty_interval:
            for k, interval_name in enumerate(intervals):
                node_list = [
                    model["node_names"][i]
                    for i in element_list.get(interval_name).values()]
                nxp.draw_networkx_nodes(
                    model["G"],
                    model["pos_dict"],
                    ax=ax,
                    nodelist=node_list,
                    node_size=node_size[k],
                    node_color=color_list[k],
                    node_shape=node_shape[k],
                    edgecolors=node_border_color[k],
                    linewidths=node_border_width[k])
    else:
        cmap = mpl.colormaps[cmap]
        cmapValue = 1 / len(intervals)
        for j, interval_name in enumerate(intervals):
            node_list = [model["node_names"][i]
                         for i in element_list.get(interval_name).values()]
            if not node_list:
                nxp.draw_networkx_nodes(
                    model["G"],
                    model["pos_dict"],
                    ax=ax,
                    nodelist=[model["node_names"][0]],
                    node_size=node_size[j],
                    node_color=[cmap(float(cmapValue))],
                    node_shape=node_shape[j],
                    label=label_list[j],
                    edgecolors=node_border_color[j],
                    linewidths=node_border_width[j])
                empty_interval = True
            else:
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
            cmapValue += 1 / len(intervals)
        if empty_interval:
            cmap2 = cmap
            cmapValue2 = 1 / len(intervals)
            for k, interval_name in enumerate(intervals):
                node_list = [
                    model["node_names"][i]
                    for i in element_list.get(interval_name).values()]
                nxp.draw_networkx_nodes(
                    model["G"],
                    model["pos_dict"],
                    ax=ax,
                    nodelist=node_list,
                    node_size=node_size[k],
                    node_color=[cmap2(float(cmapValue2))],
                    node_shape=node_shape[k],
                    edgecolors=node_border_color[k],
                    linewidths=node_border_width[k])
                cmapValue2 += 1 / len(intervals)


def draw_discrete_links(
        self,
        ax,
        element_list,
        intervals,
        link_width=None,
        label_list=None,
        cmap="tab10",
        color_list=None,
        link_style='-',
        link_arrows=False):
    """Draws discretized link data onto the figure.
    
    Arguments
    ---------
    ax : axes._subplots.AxesSubplot
        Matplotlib axes object.
        
    element_list : array-like
        List of network elements that data will be retrieved for.
        
    intervals : dict
        The dictionary containting the intervals and the draw_links associated with each interval.
        
    link_width : integer, array-like
        List of link widths for each interval.
        
    label_list : string, array-like
        List of labels for each interval.
        
    cmap : string
        The matplotlib color map to be used for plotting. Refer to matplotlib documentation for possible inputs.
        
    color_list : string, array-like
        The list of node colors for each interval. Both cmap and color_list can not be used at the same time to color draw_nodes. If both are, then color_list takes priority.
        
    link_style : string
        The style (solid, dashed, dotted, etc.) of the draw_links. Refer to matplotlib documentation for available line styles.
        
    link_arrows : boolean
        Determines if an arrow is drawn in the direction of flow of the pump.
    """   
    
    model = self.model
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
    empty_interval = False
    if (color_list is not None and cmap is not None) or color_list is not None:
        for j, interval_name in enumerate(intervals):
            edge_list = [model["pipe_list"][i]
                         for i in element_list.get(interval_name).values()]
            if not edge_list:
                nxp.draw_networkx_edges(
                    model["G"],
                    model["pos_dict"],
                    ax=ax,
                    edgelist=[model["pipe_list"][0]],
                    edge_color=color_list[j],
                    width=link_width[j],
                    arrows=link_arrows[j],
                    style=link_style[j],
                    label=label_list[j])

                empty_interval = True
            else:
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
        if empty_interval:
            for k, interval_name in enumerate(intervals):
                edge_list = [model["pipe_list"][i]
                             for i in element_list.get(interval_name).values()]
                nxp.draw_networkx_edges(
                    model["G"],
                    model["pos_dict"],
                    ax=ax,
                    edgelist=edge_list,
                    edge_color=color_list[k],
                    width=link_width[k],
                    arrows=link_arrows[k],
                    style=link_style[k])
    else:
        cmap = mpl.colormaps[cmap]
        cmapValue = 1 / len(intervals)
        for j, interval_name in enumerate(intervals):
            edge_list = [model["pipe_list"][i]
                         for i in element_list.get(interval_name).values()]
            if not edge_list:
                nxp.draw_networkx_edges(
                    model["G"],
                    model["pos_dict"],
                    ax=ax,
                    edgelist=[model["pipe_list"][0]],
                    edge_color=[cmap(float(cmapValue))],
                    width=link_width[j],
                    arrows=link_arrows[j],
                    style=link_style[j],
                    label=label_list[j])
                empty_interval = True
            else:
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
            cmapValue += 1 / len(intervals)
        if empty_interval:
            cmap2 = cmap
            cmapValue2 = 1 / len(intervals)
            for k, interval_name in enumerate(intervals):
                edge_list = [model["pipe_list"][i]
                             for i in element_list.get(interval_name).values()]
                nxp.draw_networkx_edges(
                    model["G"],
                    model["pos_dict"],
                    ax=ax,
                    edgelist=edge_list,
                    edge_color=[cmap2(float(cmapValue2))],
                    width=link_width[k],
                    arrows=link_arrows[k],
                    style=link_style[k])
                cmapValue2 += 1 / len(intervals)


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
        node_size=None,
        node_shape=None,
        label_list=None,
        node_border_color=None,
        node_border_width=None,
        savefig=False,
        save_name=None,
        dpi='figure',
        save_format='png',
        draw_tanks=True,
        draw_reservoirs=True,
        draw_pumps=True,
        draw_valves=True,
        draw_nodes=False,
        draw_links=True,
        discrete_legend_title=None,
        base_legend_loc="upper right",
        discrete_legend_loc="lower right",
        cmap=default_cmap,
        color_list=None,
        disable_interval_deleting=True,
        base_legend_label_font_size=15,
        base_legend_label_color="k",
        discrete_legend_label_font_size=15,
        discrete_legend_label_color="k",
        discrete_legend_title_font_size=17,
        discrete_legend_title_color='k',
        draw_legend_frame=False,
        legend_decimal_places=3,
        reservoir_size=150,
        reservoir_color='k',
        reservoir_shape=epa_res,
        reservoir_border_color='k',
        reservoir_border_width=3,
        tank_size=200,
        tank_color='k',
        tank_shape=epa_tank,
        tank_border_color='k',
        tank_border_width=2,
        valve_element='node',
        valve_size=200,
        valve_color='k',
        valve_shape=epa_valve,
        valve_border_color='k',
        valve_border_width=1,
        valve_width=3,
        valve_line_style='-',
        valve_arrows=False,
        pump_element='node',
        pump_size=200,
        pump_color='k',
        pump_shape=epa_pump,
        pump_border_color='k',
        pump_border_width=1,
        pump_width=3,
        pump_line_style='-',
        pump_arrows=False,
        base_node_color='k',
        base_node_size=30,
        base_link_color='k',
        base_link_width=1,
        base_link_line_style='-',
        base_link_arrows=False,
        draw_base_legend=True,
        draw_interval_legend=True):
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
        
    node_size : integer, array-like
        List of node sizes for each interval.
        
    node_shape : string, array-like
        List of node shapes for each interval. Refer to matplotlib documentation for available marker types.
   
    node_border_color : string, array-like
        The color of the node borders for each interval.
   
    node_border_width  : integer, array-like
        The width of the node borders for each interval.
    
    draw_reservoirs : boolean
        Determines if draw_reservoirs with no data associated with them are drawn.
    
    draw_tanks : boolean
        Determines if draw_reservoirs with no data associated with them are drawn.
    
    draw_pumps : boolean
        Determines if draw_pumps with no data associated with them are drawn.
    
    draw_valves : boolean
        Determines if draw_valves with no data associated with them are drawn.
    
    draw_nodes : boolean
        Determines if draw_nodes with no data associated with them are drawn.
    
    draw_links : boolean
        Determines if draw_links with no data associated with them are drawn.
    
    cmap : string
        The matplotlib color map to be used for plotting. Refer to matplotlib documentation for possible inputs.
    
    color_list : string, array-like
        The list of node colors for each interval. Both cmap and color_list can not be used at the same time to color draw_nodes. If both are, then color_list takes priority.
    
    disable_interval_deleting : boolean
        If True, empty intervals will be automatically deleted. 
    
    draw_interval_legend : boolean
        Determine if the intervals legend is drawn.
    
    discrete_legend_title : string
        Title of the intervals legend.
    
    discrete_legend_loc : string
        The location of the intervals legend on the figure.
    
    discrete_legend_label_font_size : integer
        The font size of the intervals legend text.
    
    discrete_legend_label_color : string
        The color of the intervals legend text. Refer to matplotlib documentation for available colors.
    
    discrete_legend_title_font_size : integer
        The font size of the title text for the intervals legend.
    
    discrete_legend_title_color : string
        The color of the title tect for the intervals legend.
  
    draw_base_legend : boolean
        Determine if the base elements legend is drawn.
    
    base_legend_loc : string
        The location of the base elements legend on the figure. Refer to matplotlib documentation for possible inputs.
    
    base_legend_font_size : integer
        The font size of the non-title text for the base elements legend. 
    
    base_legend_label_color : string
        The color of the legend text. Refer to matplotlib documentation for 
        available colors.
    
    draw_legend_frame : boolean
        Determines if the frame around the legend is drawn.
    
    legend_decimal_places : integer
        The number of significant figures, or decimal points, that numbers in the legend will be displayed with. 0 should be passed for whole numbers.
    
    reservoir_size : integer
        The size of the reservoir marker on the plot in points^2. 
    
    reservoir_color : string
        The color of the reservoir marker.
    
    reservoir_shape : string
        The shape of the reservoir marker. Refer to matplotlib documentation for available marker types.
    
    reservoir_border_color : string
        The color of the border around the reservoir marker.
    
    reservoir_border_width : integer
        The width in points of the border around the reservoir marker.

    tank_size : integer
        The size of the tank marker on the plot in points^2. 
    
    tank_color : string
        The color of the tank marker.
    
    tank_shape : string
        The shape of the tank marker.
    
    tank_border_color : string
        The color of the border around the tank marker.
    
    tank_border_width : integer
        The width in points of the border around the tank marker.
    
    valve_element : string
        Determines if the valves are drawn as nodes or links.
    
    valve_size : integer
        The size of the valve marker on the plot in points^2. 
    
    valve_color : string
        The color of the valve marker.
    
    valve_shape : string
        The shape of the valve marker.
    
    valve_border_color : string
        The color of the border around the valve marker.
    
    valve_border_width : integer
        The width in points of the border around the valve marker.
    
    valve_width : integer
        The width of the valve line in points.
    
    valve_line_style : string
        The line style of valves if they are drawn as links. Refer to matplotlib documentation for available line styles.
    
    valve_arrows : boolean
        Determines if an arrow is drawn in the direction of flow of the valves. 
    
    pump_element : string
        Determines if pumps are drawn as links or nodes. 
    
    pump_size : integer
        The size of the pump marker on the plot in points^2.
    
    pump_color : string
        The color of the pump line.
    
    pump_shape : string
        The shape of the pump marker.
    
    pump_border_color : string
        The color of the border around the pump marker.
    
    pump_border_width : integer
        The width in points of the border around the pump marker.
    
    pump_width : integer
        The width of the pump line in points.
    
    pump_line_style : string
        The style (solid, dashed, dotted, etc.) of the pump line. Refer to matplotlib documentation for available line styles.
    
    pump_arrows : boolean
        Determines if an arrow is drawn in the direction of flow of the pump.
    
    base_node_color : string
        The color of the draw_nodes without data associated with them.
    
    base_node_size : integer
        The size of the draw_nodes without data associated with them in points^2.
    
    base_link_color : string
        The color of the draw_links without data associated with them.
    
    base_link_width : integer
        The width of the draw_links without data associated with them in points.
    
    base_link_line_style : string
        The style (solid, dashed, dotted, etc) of the draw_links with no data associated with them.
    
    base_link_arrows : boolean
        Determines if an arrow is drawn in the direction of flow of the draw_links with no data associated with them.
    
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
    
    dpi : int, string
        The dpi that the figure will be saved with.
    
    save_format : string
        The file format that the figure will be saved as.
    """
    
    if len(self.model['G_list_pumps_only']) == 0:
        draw_pumps = False
    if ax is None:
        if ax is None:
            fig, ax = plt.subplots(figsize=self.figsize)
            ax.set_frame_on(self.axis_frame)
    if parameter is not None:
        parameter_results, node_list = processing.get_parameter(
            self,
            "node",
            parameter,
            element_list=element_list,
            value=value,
            include_tanks=include_tanks,
            include_reservoirs=include_reservoirs)
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
            legend_decimal_places=legend_decimal_places)
        draw_discrete_nodes(
            self,
            ax,
            interval_results,
            interval_names,
            node_size=node_size,
            node_shape=node_shape,
            label_list=label_list,
            node_border_color=node_border_color,
            node_border_width=node_border_width,
            cmap=cmap,
            color_list=color_list)
        base.draw_base_elements(
            self,
            ax,
            draw_nodes=draw_nodes,
            draw_reservoirs=draw_reservoirs,
            draw_tanks=draw_tanks,
            draw_valves=draw_valves,
            draw_pumps=draw_pumps,
            element_list=node_list,
            reservoir_size=reservoir_size,
            reservoir_color=reservoir_color,
            reservoir_shape=reservoir_shape,
            reservoir_border_color=reservoir_border_color,
            reservoir_border_width=reservoir_border_width,
            tank_size=tank_size,
            tank_color=tank_color,
            tank_shape=tank_shape,
            tank_border_color=tank_border_color,
            tank_border_width=tank_border_width,
            valve_element=valve_element,
            valve_size=valve_size,
            valve_color=valve_color,
            valve_shape=valve_shape,
            valve_border_color=valve_border_color,
            valve_border_width=valve_border_width,
            valve_width=valve_width,
            valve_line_style=valve_line_style,
            valve_arrows=valve_arrows,
            pump_element=pump_element,
            pump_size=pump_size,
            pump_color=pump_color,
            pump_shape=pump_shape,
            pump_border_color=pump_border_color,
            pump_border_width=pump_border_width,
            pump_width=pump_width,
            pump_line_style=pump_line_style,
            pump_arrows=pump_arrows, base_node_color=base_node_color,
            base_node_size=base_node_size, base_link_color=base_link_color,
            base_link_width=base_link_width,
            base_link_line_style=base_link_line_style,
            base_link_arrows=base_link_arrows)

        if discrete_legend_title is None:
            discrete_legend_title = label_generator(parameter, value, unit)

        base.draw_legend(
            ax,
            intervals=interval_names,
            title=discrete_legend_title,
            draw_pumps=draw_pumps,
            base_legend_loc=base_legend_loc,
            discrete_legend_loc=discrete_legend_loc,
            base_legend_label_font_size=base_legend_label_font_size,
            base_legend_label_color=base_legend_label_color,
            discrete_legend_label_font_size=discrete_legend_label_font_size,
            discrete_legend_label_color=discrete_legend_label_color,
            discrete_legend_title_font_size=discrete_legend_title_font_size,
            discrete_legend_title_color=discrete_legend_title_color,
            cmap=cmap,
            color_list=color_list,
            draw_legend_frame=draw_legend_frame,
            pump_color=pump_color,
            base_link_color=base_link_color,
            draw_base_legend=draw_base_legend,
            draw_discrete_legend=draw_interval_legend,
            pump_line_style=pump_line_style,
            base_link_line_style=base_link_line_style,
            base_link_arrows=base_link_arrows,
            pump_arrows=pump_arrows,
            draw_links=draw_links,
            draw_valves=draw_valves,
            valve_element=valve_element,
            valve_line_style=valve_line_style,
            valve_color=valve_color,
            valve_arrows=valve_arrows,
            pump_element=pump_element)
    if savefig:
        save_fig(self, save_name=save_name, dpi=dpi, save_format=save_format)


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
        link_width=None,
        label_list=None,
        color_list=None,
        link_style='-',
        link_arrows=False,
        draw_tanks=True,
        draw_reservoirs=True,
        draw_pumps=True,
        draw_valves=True,
        draw_nodes=False,
        draw_links=False,
        cmap=default_cmap,
        discrete_legend_title=None,
        base_legend_loc="upper right",
        discrete_legend_loc="lower right",
        savefig=False,
        save_name=None,
        dpi='figure',
        save_format='png',
        disable_interval_deleting=True,
        base_legend_label_font_size=15,
        base_legend_label_color="k",
        discrete_legend_label_font_size=15,
        discrete_legend_label_color="k",
        discrete_legend_title_font_size=17,
        discrete_legend_title_color='k',
        draw_legend_frame=False,
        legend_decimal_places=3,
        reservoir_size=150,
        reservoir_color='k',
        reservoir_shape=epa_res,
        reservoir_border_color='k',
        reservoir_border_width=3,
        tank_size=200,
        tank_color='k',
        tank_shape=epa_tank,
        tank_border_color='k',
        tank_border_width=2,
        valve_element='node',
        valve_size=200,
        valve_color='k',
        valve_shape=epa_valve,
        valve_border_color='k',
        valve_border_width=1,
        valve_width=3,
        valve_line_style='-',
        valve_arrows=False,
        pump_element='node',
        pump_size=200,
        pump_color='k',
        pump_shape=epa_pump,
        pump_border_color='k',
        pump_border_width=1,
        pump_width=3,
        pump_line_style='-',
        pump_arrows=False,
        base_node_color='k',
        base_node_size=30,
        base_link_color='k',
        base_link_width=1,
        base_link_line_style='-',
        base_link_arrows=False,
        draw_base_legend=True,
        draw_discrete_legend=True):
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
    
    link_width : integer, array-like
        List of link widths for each interval.
    
    label_list : string, array-like
        List of labels for each interval.
    
    color_list : string, array-like
        The list of node colors for each interval. Both cmap and color_list can not be used at the same time to color draw_nodes. If both are, then color_list takes priority.
    
    cmap : string
        The matplotlib color map to be used for plotting. Refer to matplotlib documentation for possible inputs.
    
    link_style : string
        The style (solid, dashed, dotted, etc.) of the draw_links. Refer to matplotlib documentation for available line styles.
    
    link_arrows : boolean
        Determines if an arrow is drawn in the direction of flow of the pump.
    
    draw_reservoirs : boolean
        Determines if draw_reservoirs with no data associated with them are drawn.
    
    draw_tanks : boolean
        Determines if draw_reservoirs with no data associated with them are drawn.
    
    draw_pumps : boolean
        Determines if draw_pumps with no data associated with them are drawn.
    
    draw_valves : boolean
        Determines if draw_valves with no data associated with them are drawn.
    
    draw_nodes : boolean
        Determines if draw_nodes with no data associated with them are drawn.
    
    draw_links : boolean
        Determines if draw_links with no data associated with them are drawn.
    
    draw_discrete_legend : boolean
        Determine if the intervals legend is drawn.
    
    discrete_legend_title : string
        Title of the intervals legend.
    
    discrete_legend_loc : string
        The location of the intervals legend on the figure.
    
    discrete_legend_label_font_size : integer
        The font size of the intervals legend text.
    
    discrete_legend_label_color : string
        The color of the intervals legend text. Refer to matplotlib documentation for available colors.
    
    discrete_legend_title_font_size : integer
        The font size of the title text for the intervals legend.
    
    discrete_legend_title_color : string
        The color of the title tect for the intervals legend.
    
    draw_base_legend : boolean
        Determine if the base elements legend is drawn.
    
    base_legend_loc : string
        The location of the base elements legend on the figure. Refer to matplotlib documentation for possible inputs.
    
    base_legend_font_size : integer
        The font size of the non-title text for the base elements legend. 
    
    base_legend_label_color : string
        The color of the legend text. Refer to matplotlib documentation for available colors.
    
    draw_legend_frame : boolean
        Determines if the frame around the legend is drawn.
    
    legend_decimal_places : integer
        The number of significant figures, or decimal points, that numbers in the legend will be displayed with. 0 should be passed for whole numbers.
    
    reservoir_size : integer
        The size of the reservoir marker on the plot in points^2. 
    
    reservoir_color : string
        The color of the reservoir marker.
    
    reservoir_shape : string
        The shape of the reservoir marker. Refer to matplotlib documentation for available marker types.
    
    reservoir_border_color : string
        The color of the border around the reservoir marker.
    
    reservoir_border_width : integer
        The width in points of the border around the reservoir marker.
    
    tank_size : integer
        The size of the tank marker on the plot in points^2. 
    
    tank_color : string
        The color of the tank marker.
    
    tank_shape : string
        The shape of the tank marker.
    
    tank_border_color : string
        The color of the border around the tank marker.
    
    tank_border_width : integer
        The width in points of the border around the tank marker.
    
    valve_element : string
        Determines if the valves are drawn as nodes or links.
    
    valve_size : integer
        The size of the valve marker on the plot in points^2. 
    
    valve_color : string
        The color of the valve marker.
    
    valve_shape : string
        The shape of the valve marker.
    
    valve_border_color : string
        The color of the border around the valve marker.
    
    valve_border_width : integer
        The width in points of the border around the valve marker.
    
    valve_width : integer
        The width of the valve line in points.
    
    valve_line_style : string
        The line style of valves if they are drawn as links. Refer to matplotlib documentation for available line styles.
    
    valve_arrows : boolean
        Determines if an arrow is drawn in the direction of flow of the valves. 
    
    pump_element : string
        Determines if pumps are drawn as links or nodes. 
    
    pump_size : integer
        The size of the pump marker on the plot in points^2.
    
    pump_color : string
        The color of the pump line.
    
    pump_shape : string
        The shape of the pump marker.
    
    pump_border_color : string
        The color of the border around the pump marker.
    
    pump_border_width : integer
        The width in points of the border around the pump marker.
    
    pump_width : integer
        The width of the pump line in points.
    
    pump_line_style : string
        The style (solid, dashed, dotted, etc.) of the pump line. Refer to matplotlib documentation for available line styles.
    
    pump_arrows : boolean
        Determines if an arrow is drawn in the direction of flow of the pump.
    
    base_node_color : string
        The color of the draw_nodes without data associated with them.
    
    base_node_size : integer
        The size of the draw_nodes without data associated with them in points^2.
    
    base_link_color : string
        The color of the draw_links without data associated with them.
    
    base_link_width : integer
        The width of the draw_links without data associated with them in points.
    
    base_link_line_style : string
        The style (solid, dashed, dotted, etc) of the draw_links with no data associated with them.
    
    base_link_arrows : boolean
        Determines if an arrow is drawn in the direction of flow of the draw_links with no data associated with them.
    
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
    
    dpi : int, string
        The dpi that the figure will be saved with.
    
    save_format : string
        The file format that the figure will be saved as.
    """

    model = self.model
    if len(self.model['G_list_pumps_only']) == 0:
        draw_pumps = False
    if ax is None:
        if ax is None:
            fig, ax = plt.subplots(figsize=self.figsize)
            ax.set_frame_on(self.axis_frame)
    if parameter is not None:
        parameter_results, link_list = processing.get_parameter(
            self,
            "link",
            parameter,
            element_list=element_list,
            value=value,
            include_pumps=include_pumps,
            include_valves=include_valves)
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
            legend_decimal_places=legend_decimal_places)
        draw_discrete_links(
            self, ax, interval_results, interval_names,
            link_width=link_width,
            label_list=label_list,
            cmap=cmap,
            color_list=color_list,
            link_style=link_style,
            link_arrows=link_arrows)
        base.draw_base_elements(
            self,
            ax,
            draw_nodes=draw_nodes,
            draw_links=draw_links,
            draw_reservoirs=draw_reservoirs,
            draw_tanks=draw_tanks,
            draw_valves=draw_valves,
            draw_pumps=draw_pumps,
            element_list=link_list,
            reservoir_size=reservoir_size,
            reservoir_color=reservoir_color,
            reservoir_shape=reservoir_shape,
            reservoir_border_color=reservoir_border_color,
            reservoir_border_width=reservoir_border_width,
            tank_size=tank_size,
            tank_color=tank_color,
            tank_shape=tank_shape,
            tank_border_color=tank_border_color,
            tank_border_width=tank_border_width,
            valve_element=valve_element,
            valve_size=valve_size,
            valve_color=valve_color,
            valve_shape=valve_shape,
            valve_border_color=valve_border_color,
            valve_border_width=valve_border_width,
            valve_width=valve_width,
            valve_line_style=valve_line_style,
            valve_arrows=valve_arrows,
            pump_element=pump_element,
            pump_size=pump_size,
            pump_color=pump_color,
            pump_shape=pump_shape,
            pump_border_color=pump_border_color,
            pump_border_width=pump_border_width,
            pump_width=pump_width,
            pump_line_style=pump_line_style,
            pump_arrows=pump_arrows,
            base_node_color=base_node_color,
            base_node_size=base_node_size,
            base_link_color=base_link_color,
            base_link_width=base_link_width,
            base_link_line_style=base_link_line_style,
            base_link_arrows=base_link_arrows)
        if discrete_legend_title is None:
            discrete_legend_title = label_generator(parameter, value, unit)
        link_list = [name for name in link_list
                     if ((name not in model["G_list_pumps_only"]
                          or pump_element == 'node'
                          or draw_pumps is False)
                     and (name not in model["G_list_valves_only"]
                          or valve_element == 'node'
                          or draw_valves is False)
                     and (name not in link_list))]
        if not link_list:
            draw_links = False
        base.draw_legend(
            ax,
            intervals=interval_names,
            title=discrete_legend_title,
            draw_pumps=draw_pumps,
            base_legend_loc=base_legend_loc,
            discrete_legend_loc=discrete_legend_loc,
            base_legend_label_font_size=base_legend_label_font_size,
            base_legend_label_color=base_legend_label_color,
            discrete_legend_label_font_size=discrete_legend_label_font_size,
            discrete_legend_label_color=discrete_legend_label_color,
            discrete_legend_title_font_size=discrete_legend_title_font_size,
            discrete_legend_title_color=discrete_legend_title_color,
            cmap=cmap,
            color_list=color_list,
            draw_legend_frame=draw_legend_frame,
            pump_color=pump_color,
            base_link_color=base_link_color,
            draw_base_legend=draw_base_legend,
            draw_discrete_legend=draw_discrete_legend,
            pump_line_style=pump_line_style,
            base_link_line_style=base_link_line_style,
            base_link_arrows=base_link_arrows,
            pump_arrows=pump_arrows,
            draw_links=draw_links,
            draw_valves=draw_valves,
            valve_element=valve_element,
            valve_line_style=valve_line_style,
            valve_color=valve_color,
            valve_arrows=valve_arrows,
            pump_element=pump_element)
    if savefig:
        save_fig(self, save_name=save_name, dpi=dpi, save_format=save_format)
