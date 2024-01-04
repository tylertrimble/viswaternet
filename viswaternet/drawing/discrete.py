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

default_cmap = 'autumn_r'


def draw_discrete_nodes(
    self,
    ax,
    nodes,
    intervals,
    interval_node_size_list=None,
    interval_label_list=None,
    interval_node_shape_list=None,
    cmap="tab10",
    interval_node_border_color_list=None,
    interval_node_border_width_list=None,
    color_list=None,
):
    """Draws discretized nodal data onto the figure.

    Arguments
    ---------
    ax : axes._subplots.AxesSubplot
        Matplotlib axes object.

    nodes : string, array-like
        List of nodes to be drawn.

    intervals : dict
        The dictionary containting the intervals and the nodes assocaited with each interval.

    interval_node_size_list : integer, array-like
        List of node sizes for each interval.

    interval_label_list : string, array-like
        List of labels for each interval.

    interval_node_shape_list : string, array-like
        List of node shapes for each interval. Refer to matplotlib documentation for available marker types.

    cmap : string
        The matplotlib color map to be used for plotting. Refer to matplotlib documentation for possible inputs.

    interval_node_border_color_list : string, array-like
        The color of the node borders for each interval.

    interval_node_border_width_list : integer, array-like
        The width of the node borders for each interval.

    color_list : string, array-like
        The list of node colors for each interval. Both cmap and color_list can not be used at the same time to color nodes. If both are, then color_list takes priority.
    """
    
    model = self.model
    if interval_node_size_list is None:

        if len(model["node_names"]) < 300:

            interval_node_size_list = np.ones(len(intervals)) * 300
        elif len(model["node_names"]) >= 300 and len(model["node_names"]) < 1000:

            interval_node_size_list = np.ones(
                len(intervals)) * (80000 / len(model["node_names"]))
        else:

            interval_node_size_list = np.ones(len(intervals)) * 80
    if interval_label_list is None:

        interval_label_list = intervals
    if interval_node_shape_list is None:

        interval_node_shape_list = []

        for i in range(len(intervals)):

            interval_node_shape_list = np.append(interval_node_shape_list, ".")
    if interval_node_border_color_list is None:
        interval_node_border_color_list = []

        for i in range(len(intervals)):

            interval_node_border_color_list = np.append(
                interval_node_border_color_list, "k")
    if interval_node_border_width_list is None:
        interval_node_border_width_list = []

        for i in range(len(intervals)):

            interval_node_border_width_list = np.append(
                interval_node_border_width_list, 0)
    counter = 0
    empty_interval = False

    if (color_list is not None and cmap is not None) or color_list is not None:
        for interval_name in intervals:
            node_list = [model["node_names"][i]
                         for i in nodes.get(interval_name).values()]

            if node_list:
                nxp.draw_networkx_nodes(
                    model["G"],
                    model["pos_dict"],
                    ax=ax,
                    nodelist=[model["node_names"][0]],
                    node_size=interval_node_size_list[counter],
                    node_color=color_list[counter],
                    node_shape=interval_node_shape_list[counter],
                    label=interval_label_list[counter],
                    edgecolors=interval_node_border_color_list[counter],
                    linewidths=interval_node_border_width_list[counter],
                )

                empty_interval == True
            else:
                nxp.draw_networkx_nodes(
                    model["G"],
                    model["pos_dict"],
                    ax=ax,
                    nodelist=(
                        [model["node_names"][i]
                            for i in nodes.get(interval_name).values()]
                    ),
                    node_size=interval_node_size_list[counter],
                    node_color=color_list[counter],
                    node_shape=interval_node_shape_list[counter],
                    label=interval_label_list[counter],
                    edgecolors=interval_node_border_color_list[counter],
                    linewidths=interval_node_border_width_list[counter],
                )
            counter += 1
        if empty_interval:
            counter2 = 0

            for interval_name in intervals:
                node_list = [
                    model["node_names"][i] for i in nodes.get(interval_name).values()
                ]
                nxp.draw_networkx_nodes(
                    model["G"],
                    model["pos_dict"],
                    ax=ax,
                    nodelist=node_list,
                    node_size=interval_node_size_list[counter2],
                    node_color=color_list[counter2],
                    node_shape=interval_node_shape_list[counter2],
                    edgecolors=interval_node_border_color_list[counter2],
                    linewidths=interval_node_border_width_list[counter2],
                )

                counter2 += 1
    else:
        cmap = mpl.colormaps[cmap]
        cmapValue = 1 / len(intervals)

        for interval_name in intervals:
            node_list = [model["node_names"][i]
                         for i in nodes.get(interval_name).values()]
            if len(node_list) == 0:
                nxp.draw_networkx_nodes(
                    model["G"],
                    model["pos_dict"],
                    ax=ax,
                    nodelist=[model["node_names"][0]],
                    node_size=interval_node_size_list[counter],
                    node_color=[cmap(float(cmapValue))],
                    node_shape=interval_node_shape_list[counter],
                    label=interval_label_list[counter],
                    edgecolors=interval_node_border_color_list[counter],
                    linewidths=interval_node_border_width_list[counter],
                )

                empty_interval = True
            else:
                nxp.draw_networkx_nodes(
                    model["G"],
                    model["pos_dict"],
                    ax=ax,
                    nodelist=node_list,
                    node_size=interval_node_size_list[counter],
                    node_color=[cmap(float(cmapValue))],
                    node_shape=interval_node_shape_list[counter],
                    label=interval_label_list[counter],
                    edgecolors=interval_node_border_color_list[counter],
                    linewidths=interval_node_border_width_list[counter],
                )
            cmapValue += 1 / len(intervals)

            counter += 1
        if empty_interval:
            counter2 = 0

            cmap2 = cmap
            cmapValue2 = 1 / len(intervals)

            for interval_name in intervals:
                node_list = [
                    model["node_names"][i] for i in nodes.get(interval_name).values()
                ]
                nxp.draw_networkx_nodes(
                    model["G"],
                    model["pos_dict"],
                    ax=ax,
                    nodelist=node_list,
                    node_size=interval_node_size_list[counter2],
                    node_color=[cmap2(float(cmapValue2))],
                    node_shape=interval_node_shape_list[counter2],
                    edgecolors=interval_node_border_color_list[counter2],
                    linewidths=interval_node_border_width_list[counter2],
                )

                cmapValue2 += 1 / len(intervals)
                counter2 += 1


def draw_discrete_links(
    self,
    ax,
    links,
    intervals,
    interval_link_width_list=None,
    interval_label_list=None,
    cmap="tab10",
    color_list=None,
    link_style='-',
    link_arrows=False,
):
    """Draws discretized link data onto the figure.

    Arguments
    ---------
    ax : axes._subplots.AxesSubplot
        Matplotlib axes object.

    links : string, array-like
        List of links to be drawn.

    intervals : dict
        The dictionary containting the intervals and the links associated with each interval.

    interval_link_width_list : integer, array-like
        List of link widths for each interval.

    interval_label_list : string, array-like
        List of labels for each interval.

    cmap : string
        The matplotlib color map to be used for plotting. Refer to matplotlib documentation for possible inputs.

    color_list : string, array-like
        The list of node colors for each interval. Both cmap and color_list can not be used at the same time to color nodes. If both are, then color_list takes priority.

    link_style : string
        The style (solid, dashed, dotted, etc.) of the links. Refer to matplotlib documentation for available line styles.

    link_arrows : boolean
        Determines if an arrow is drawn in the direction of flow of the pump.
    """
    
    model = self.model
    if interval_link_width_list is None:
        interval_link_width_list = np.ones(len(intervals)) * 2
    if interval_label_list is None:
        interval_label_list = intervals
    empty_interval = False
    if (color_list is not None and cmap is not None) or color_list is not None:
        for counter, interval_name in enumerate(intervals):
            edge_list = [model["pipe_list"][i]
                         for i in links.get(interval_name).values()]
            if len(edge_list) == 0:
                nxp.draw_networkx_edges(
                    model["G"],
                    model["pos_dict"],
                    ax=ax,
                    edgelist=[model["pipe_list"][0]],
                    edge_color=color_list[counter],
                    width=interval_link_width_list[counter],
                    arrows=link_arrows,
                    style=link_style,
                    label=interval_label_list[counter],
                )

                empty_interval = True
            else:
                nxp.draw_networkx_edges(
                    model["G"],
                    model["pos_dict"],
                    ax=ax,
                    edgelist=edge_list,
                    edge_color=color_list[counter],
                    width=interval_link_width_list[counter],
                    arrows=link_arrows,
                    style=link_style,
                    label=interval_label_list[counter],
                )
        if empty_interval:

            for counter, interval_name in enumerate(intervals):
                edge_list = [model["pipe_list"][i]
                             for i in links.get(interval_name).values()]
                nxp.draw_networkx_edges(
                    model["G"],
                    model["pos_dict"],
                    ax=ax,
                    edgelist=edge_list,
                    edge_color=color_list[counter],
                    width=interval_link_width_list[counter],
                    arrows=link_arrows,
                    style=link_style,
                )

    else:
        cmap = mpl.colormaps[cmap]
        cmapValue = 1 / len(intervals)
        for counter, interval_name in enumerate(intervals):

            edge_list = [model["pipe_list"][i]
                         for i in links.get(interval_name).values()]
            if len(edge_list) == 0:

                nxp.draw_networkx_edges(
                    model["G"],
                    model["pos_dict"],
                    ax=ax,
                    edgelist=[model["pipe_list"][0]],
                    edge_color=[cmap(float(cmapValue))],
                    width=interval_link_width_list[counter],
                    arrows=link_arrows,
                    style=link_style,
                    label=interval_label_list[counter],
                )

                empty_interval = True
            else:
                nxp.draw_networkx_edges(
                    model["G"],
                    model["pos_dict"],
                    edgelist=edge_list,
                    ax=ax,
                    edge_color=[cmap(float(cmapValue))],
                    width=interval_link_width_list[counter],
                    arrows=link_arrows,
                    style=link_style,
                    label=interval_label_list[counter],
                )
            cmapValue += 1 / len(intervals)

        if empty_interval:
            cmap2 = cmap
            cmapValue2 = 1 / len(intervals)

            for counter, interval_name in enumerate(intervals):
                edge_list = [model["pipe_list"][i]
                             for i in links.get(interval_name).values()]
                nxp.draw_networkx_edges(
                    model["G"],
                    model["pos_dict"],
                    ax=ax,
                    edgelist=edge_list,
                    edge_color=[cmap2(float(cmapValue2))],
                    width=interval_link_width_list[counter],
                    arrows=link_arrows,
                    style=link_style,
                )

                cmapValue2 += 1 / len(intervals)


def plot_discrete_nodes(
    self,
    ax=None,
    num_intervals=5,
    parameter=None,
    value=None,
    unit=None,
    element_list=None,
    get_tanks=False,
    get_reservoirs=False,
    intervals="automatic",
    interval_node_size_list=None,
    interval_node_shape_list=None,
    interval_label_list=None,
    interval_node_border_color_list=None,
    interval_node_border_width_list=None,
    savefig=False,
    save_name=None,
    dpi='figure',
    save_format='png',
    tanks=True,
    reservoirs=True,
    pumps=True,
    valves=True,
    legend=True,
    legend_title=None,
    legend_loc_1="upper right",
    legend_loc_2="lower right",
    cmap=default_cmap,
    color_list=None,
    disable_interval_deleting=True,
    font_size=15,
    font_color='k',
    legend_title_font_size=17,
    draw_frame=False,
    legend_sig_figs=3,
    reservoir_size=150,
    reservoir_color='b',
    reservoir_shape='s',
    reservoir_border_color='k',
    reservoir_border_width=3,
    tank_size=200,
    tank_color='b',
    tank_shape='h',
    tank_border_color='k',
    tank_border_width=2,
    valve_size=200,
    valve_color='orange',
    valve_shape='P',
    valve_border_color='k',
    valve_border_width=1,
    pump_color='b',
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
    draw_interval_legend=True
):
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

    get_tanks : boolean
        Determines if data for tanks are retrieved.

    get_reservoirs : boolean
        Determines if data for reservoirs are retrieved.

    intervals : integer, string
        If set to 'automatic' then intervals are created automatically on a equal interval basis. Otherwise, it is the edges of the intervals to be created. intervals array length should be num_intervals + 1.

    interval_node_size_list : integer, array-like
        List of node sizes for each interval.

    interval_label_list : string, array-like
        List of labels for each interval.

    interval_node_shape_list : string, array-like
        List of node shapes for each interval. Refer to matplotlib documentation for available marker types.

    interval_node_border_color_list : string, array-like
        The color of the node borders for each interval.

    interval_node_border_width_list : integer, array-like
        The width of the node borders for each interval.

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

    reservoirs : boolean
        Determines if reservoirs with no data associated with them are drawn.

    tanks : boolean
        Determines if reservoirs with no data associated with them are drawn.

    pumps : boolean
        Determines if pumps with no data associated with them are drawn.

    valves : boolean
        Determines if valves with no data associated with them are drawn.

    legend : boolean
        Determines if the base elements legend will be drawn. 

    legend_title : string
        Title of the intervals legend.

    legend_loc_1 : string
        The location of the base elements legend on the figure. Refer to matplotlib documentation for possible inputs.

    legend_loc_2 : string
        The location of the intervals legend on the figure.

    cmap : string
        The matplotlib color map to be used for plotting. Refer to matplotlib documentation for possible inputs.

    color_list : string, array-like
        The list of node colors for each interval. Both cmap and color_list can not be used at the same time to color nodes. If both are, then color_list takes priority.

    disable_interval_deleting : boolean
        If True, empty intervals will be automatically deleted. 

    font_size : integer
        The font size of the non-title text for legends. 

    font_color : string
        The color of the legend text. Refer to matplotlib documentation for 
        available colors.

    legend_title_font_size : integer
        The font size of the title text for legends.

    draw_frame : boolean
        Determines if the frame around the legend is drawn.

    legend_sig_figs : integer
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

    pump_color : string
        The color of the pump line.

    pump_width : integer
        The width of the pump line in points.

    pump_line_style : string
        The style (solid, dashed, dotted, etc.) of the pump line. Refer to matplotlib documentation for available line styles.

    pump_arrows : boolean
        Determines if an arrow is drawn in the direction of flow of the pump.

    base_node_color : string
        The color of the nodes without data associated with them.

    base_node_size : integer
        The size of the nodes without data associated with them in points^2.

    base_link_color : string
        The color of the links without data associated with them.

    base_link_width : integer
        The width of the links without data associated with them in points.

    base_link_line_style : string
        The style (solid, dashed, dotted, etc) of the links with no data associated with them.

    base_link_arrows : boolean
        Determines if an arrow is drawn in the direction of flow of the links with no data associated with them.

    draw_base_legend : boolean
        Determine if the base elements legend is drawn.

    draw_intervals_legend : boolean
        Determine if the intervals legend is drawn.
    """
    
    if len(self.model['G_list_pumps_only'])==0:
        pumps = False
    
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
            tanks=get_tanks,
            reservoirs=get_reservoirs,
        )

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
            legend_sig_figs=legend_sig_figs
        )

        draw_discrete_nodes(
            self,
            ax,
            interval_results,
            interval_names,
            interval_node_size_list=interval_node_size_list,
            interval_node_shape_list=interval_node_shape_list,
            interval_label_list=interval_label_list,
            interval_node_border_color_list=interval_node_border_color_list,
            interval_node_border_width_list=interval_node_border_width_list,
            cmap=cmap,
            color_list=color_list,
        )

        base.draw_base_elements(
            self,
            ax,
            nodes=False,
            reservoirs=reservoirs,
            tanks=tanks,
            valves=valves,
            pumps=pumps,
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
            valve_size=valve_size,
            valve_color=valve_color,
            valve_shape=valve_shape,
            valve_border_color=valve_border_color,
            valve_border_width=valve_border_width,
            pump_color=pump_color,
            pump_width=pump_width,
            pump_line_style=pump_line_style,
            pump_arrows=pump_arrows,
            base_node_color=base_node_color,
            base_node_size=base_node_size,
            base_link_color=base_link_color,
            base_link_width=base_link_width,
            base_link_line_style=base_link_line_style,
            base_link_arrows=base_link_arrows
        )

        if legend:
            if legend_title is None:
                legend_title = label_generator(parameter,value,unit)
                
            base.draw_legend(
                ax,
                intervals=interval_names,
                title=legend_title,
                pumps=pumps,
                loc=legend_loc_1,
                loc2=legend_loc_2,
                font_size=font_size,
                font_color=font_color,
                legend_title_font_size=legend_title_font_size,
                draw_frame=draw_frame,
                pump_color=pump_color,
                base_link_color=base_link_color,
                draw_base_legend=draw_base_legend,
                draw_intervals_legend=draw_interval_legend,
                pump_line_style=pump_line_style,
                base_link_line_style=base_link_line_style,
                base_link_arrows=base_link_arrows,
                pump_arrows=pump_arrows,
                draw_base_links=True,
            )
    if savefig:

        save_fig(self, save_name=save_name, dpi=dpi, save_format=save_format)


def plot_discrete_links(
    self,
    ax=None,
    num_intervals=5,
    parameter=None,
    element_list=None,
    value=None,
    unit=None,
    intervals="automatic",
    interval_link_width_list=None,
    interval_label_list=None,
    color_list=None,
    link_style='-',
    link_arrows=False,
    tanks=True,
    reservoirs=True,
    pumps=True,
    valves=True,
    cmap=default_cmap,
    legend=True,
    legend_title=None,
    legend_loc_1="upper right",
    legend_loc_2="lower right",
    savefig=False,
    save_name=None,
    dpi='figure',
    save_format='png',
    disable_interval_deleting=True,
    font_size=15,
    font_color='k',
    legend_title_font_size=17,
    draw_frame=False,
    legend_sig_figs=3,
    reservoir_size=150,
    reservoir_color='b',
    reservoir_shape='s',
    reservoir_border_color='k',
    reservoir_border_width=3,
    tank_size=200,
    tank_color='b',
    tank_shape='h',
    tank_border_color='k',
    tank_border_width=2,
    valve_size=200,
    valve_color='orange',
    valve_shape='P',
    valve_border_color='k',
    valve_border_width=1,
    pump_color='b',
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
    draw_intervals_legend=True

):
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

    get_tanks : boolean
        Determines if data for tanks are retrieved.

    get_reservoirs : boolean
        Determines if data for reservoirs are retrieved.

    intervals : integer, string
        If set to 'automatic' then intervals are created automatically on an equal interval basis. Otherwise, it is the edges of the intervals to be created. intervals array length should be num_intervals + 1.

    interval_link_width_list : integer, array-like
        List of link widths for each interval.

    interval_label_list : string, array-like
        List of labels for each interval.

    color_list : string, array-like
        The list of node colors for each interval. Both cmap and color_list can not be used at the same time to color nodes. If both are, then color_list
        takes priority.

    link_style : string
        The style (solid, dashed, dotted, etc.) of the links. Refer to matplotlib documentation for available line styles.

    link_arrows : boolean
        Determines if an arrow is drawn in the direction of flow of the pump.

    reservoirs : boolean
        Determines if reservoirs with no data associated with them are drawn.

    tanks : boolean
        Determines if reservoirs with no data associated with them are drawn.

    pumps : boolean
        Determines if pumps with no data associated with them are drawn.

    valves : boolean
        Determines if valves with no data associated with them are drawn.

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

    cmap : string
        The matplotlib color map to be used for plotting. Refer to matplotlib documentation for possible inputs.

    legend : boolean
        Determines if the base elements legend will be drawn. 

    legend_title : string
        Title of the intervals legend.

    legend_loc_1 : string
        The location of the base elements legend on the figure. Refer to matplotlib documentation for possible inputs.

    legend_loc_2 : string
        The location of the intervals legend on the figure.

    disable_interval_deletingdisable_interval_deleting : boolean
        If True, empty intervals will be automatically deleted. 

    font_size : integer
        The font size of the non-title text for legends. 

    font_color : string
        The color of the legend text. Refer to matplotlib documentation for available colors.

    legend_title_font_size : integer
        The font size of the title text for legends.

    draw_frame : boolean
        Determines if the frame around the legend is drawn.

    legend_sig_figs : integer
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

    pump_color : string
        The color of the pump line.

    pump_width : integer
        The width of the pump line in points.

    pump_line_style : string
        The style (solid, dashed, dotted, etc.) of the pump line. Refer to matplotlib documentation for available line styles.

    pump_arrows : boolean
        Determines if an arrow is drawn in the direction of flow of the pump.

    base_node_color : string
        The color of the nodes without data associated with them.

    base_node_size : integer
        The size of the nodes without data associated with them in points^2.

    base_link_color : string
        The color of the links without data associated with them.

    base_link_width : integer
        The width of the links without data associated with them in points.

    base_link_line_style : string
        The style (solid, dashed, dotted, etc) of the links with no data associated with them.

    base_link_arrows : boolean
        Determines if an arrow is drawn in the direction of flow of the links with no data associated with them.

    draw_base_legend : boolean
        Determine if the base elements legend is drawn.

    draw_intervals_legend : boolean
        Determine if the intervals legend is drawn.
    """
    
    if len(self.model['G_list_pumps_only'])==0:
        pumps = False
    if ax is None:
        if ax is None:
            fig, ax = plt.subplots(figsize=self.figsize)  
            ax.set_frame_on(self.axis_frame)
    if parameter is not None:

        parameter_results, link_list = processing.get_parameter(
            self, "link", parameter, element_list=element_list, value=value
        )
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
            legend_sig_figs=legend_sig_figs
        )
        draw_discrete_links(
            self,
            ax,
            interval_results,
            interval_names,
            interval_link_width_list=interval_link_width_list,
            interval_label_list=interval_label_list,
            cmap=cmap,
            color_list=color_list,
            link_style=link_style,
            link_arrows=link_arrows,
        )
        base.draw_base_elements(
            self,
            ax,
            nodes=False,
            links=False,
            reservoirs=reservoirs,
            tanks=tanks,
            valves=valves,
            pumps=pumps,
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
            valve_size=valve_size,
            valve_color=valve_color,
            valve_shape=valve_shape,
            valve_border_color=valve_border_color,
            valve_border_width=valve_border_width,
            pump_color=pump_color,
            pump_width=pump_width,
            pump_line_style=pump_line_style,
            pump_arrows=pump_arrows,
            base_node_color=base_node_color,
            base_node_size=base_node_size,
            base_link_color=base_link_color,
            base_link_width=base_link_width,
            base_link_line_style=base_link_line_style,
            base_link_arrows=base_link_arrows
        )

        if legend:
            
            if legend_title is None:
                legend_title = label_generator(parameter,value,unit)
                
            base.draw_legend(
                ax,
                intervals=interval_names,
                title=legend_title,
                pumps=pumps,
                loc=legend_loc_1,
                loc2=legend_loc_2,
                font_size=font_size,
                font_color=font_color,
                legend_title_font_size=legend_title_font_size,
                draw_frame=draw_frame,
                pump_color=pump_color,
                base_link_color=base_link_color,
                draw_base_legend=draw_base_legend,
                draw_intervals_legend=draw_intervals_legend,
                pump_line_style=pump_line_style,
                base_link_line_style=base_link_line_style,
                base_link_arrows=base_link_arrows,
                pump_arrows=pump_arrows,
                draw_base_links=False,
            )
    if savefig:

        save_fig(self, save_name=save_name, dpi=dpi, save_format=save_format)
