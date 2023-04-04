# -*- coding: utf-8 -*-
"""
The viswaternet.drawing.unique module handles custom data, excel data, and unique data drawing.
"""

import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from viswaternet.network import processing
from viswaternet.utils import convert_excel, save_fig, normalize_parameter, unit_conversion
from viswaternet.drawing import base
from viswaternet.drawing import discrete

default_cmap = 'autumn_r'


def plot_unique_data(
    self,
    ax=None,
    parameter=None,
    parameter_type=None,
    data_type=None,
    excel_columns=None,
    custom_data_values=None,
    unit=None,
    intervals="automatic",
    interval_node_size_list=None,
    interval_node_shape_list=None,
    num_intervals=5,
    interval_link_width_list=None,
    interval_label_list=None,
    interval_node_border_color_list=None,
    interval_node_border_width_list=None,
    color_list=None,
    widths=1,
    min_width=None,
    max_width=None,
    min_size=None,
    max_size=None,
    vmin=None,
    vmax=None,
    link_style='-',
    link_arrows=False,
    tanks=True,
    reservoirs=True,
    pumps=True,
    valves=True,
    cmap=default_cmap,
    legend=True,
    legend_title=None,
    node_size=100,
    node_shape=".",
    line_widths=None,
    edge_colors=None,
    legend_loc_1="upper right",
    legend_loc_2="lower right",
    savefig=False,
    save_name=None,
    dpi='figure',
    save_format='png',
    color_bar_title=None,
    font_size=15,
    font_color='k',
    legend_title_font_size=17,
    draw_frame=False,
    legend_sig_figs=3,
    element_size_intervals=None,
    element_size_legend_title=None,
    element_size_legend_loc=None,
    element_size_legend_labels=None,
    draw_base_legend=True,
    draw_intervals_legend=True,
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
    disable_interval_deleting=True,
    draw_color_bar=True,
    color_bar_width=0.03,
    color_bar_height=0.8
):
    """A complex function that accomplishes tasks relating to categorical data, or 'unique' as used in viswaternet, as well as data not retrieved from WNTR.

    There are three distinct modes of operation, and which one is used is controlled by the 'parameter' argument, which differs from previous use of the argument.

    Setting the parameter argument to 'demand_patterns', 'diameter', or 'roughness' simply plots that parameter. These parameters are treated differently from others because in usually they are categorical. For 
    instance, pipe diameters are not randomly chosen, and instead are chosen from a list of standard pipe sizes.

    When the parameter argument is set to 'excel_data', the function deals with excel data, or data imported from an .xlsx file. Two excel columns with elements and data pairs are provided by the user, which are then 
    converted into a format usable by viswaternet for plotting. 

    When the parameter argument is set to 'custom_data', the function deals with data directly inside of python. The user should expect to format the data themselves, although this shouldn't be difficult. An example of 'custom_data'
    being used can be seen in example 10 located in the github repository. 

    Arguments
    ---------
    ax : axes._subplots.AxesSubplot
        Matplotlib axes object.

    parameter : string
        Should be set to 'demand_patterns', 'diameter', 'roughness', 'custom_data' or 'excel_data'.

    parameter_type : string
        Type of parameter (nodal, link)

    data_type : string
        The type of data that the excel data is (Unique, continuous, or discrete.)

    excel_columns : array-like
        Two values should be provided:

        The first should be the excel column that contains element names. 
        Column A in excel is considered the 0th column for use with viswaternet.

        The second should be the excel column that contains element data. 
        Column A in excel is considered the 0th column for use with viswaternet.

    custom_data_values : array-like
        Similar to 'excel_columns' two values should be provided. The first value should be an array with element names, and the second should be one with the element data.

    unit : string
        The unit that the network data is to be converted to.

    intervals : integer, string
        If set to 'automatic' then intervals are created automatically on a equal interval basis. Otherwise, it is the edges of the intervals to be created. intervals array length should be num_intervals + 1.

    interval_node_size_list : integer, array-like
        List of node sizes for each interval.

    interval_node_shape_list : string, array-like
        List of node shapes for each interval. Refer to matplotlib documentation for available marker types.

    num_intervals : integer
        The number of intervals.

    interval_link_width_list : integer, array-like
        List of link widths for each interval.

    interval_label_list : string, array-like
        List of labels for each interval.

    interval_node_border_color_list : string, array-like
        The color of the node borders for each interval.

    interval_node_border_width_list : integer, array-like
        The width of the node borders for each interval.

    color_list : string, array-like
        The list of node colors for each interval. Both cmap and color_list can not be used at the same time to color nodes. If both are, then color_list
        takes priority.

    widths : integer, array-like
        Integer representing all link widrths, or array of widths for each link.

    min_width : integer
        Minimum size of links to be used with normalize_parameter.

    max_width : integer
        Maximum size of links to be used with normalize_parameter.

    min_size : integer
        Minimum size of nodes to be used with normalize_parameter.

    max_size : integer
        Maximum size of nodes to be used with normalize_parameter.

    vmin : integer
        The minimum value of the color bar. 

    vmax : integer
        The maximum value of the color bar.

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

    cmap : string
        The matplotlib color map to be used for plotting. Refer to matplotlib documentation for possible inputs.

    legend : boolean
        Determines if the base elements legend will be drawn. 

    legend_title : string
        Title of the intervals legend.

    node_size : integer, array-like
        Integer representing all node sizes, or array of sizes for each node.

    node_shape : string
        Shape of the nodes. Refer to matplotlib documentation for available 
        marker types.

    line_widths : integer
        Width of the node borders.

    edge_colors : string
        Color of the node borders.

    legend_loc_1 : string
        The location of the base elements legend on the figure. Refer to matplotlib documentation for possible inputs.

    legend_loc_2 : string
        The location of the intervals legend on the figure.

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

    color_bar_title : string
        The title of the color bar.

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

    element_size_intervals : integer
        The number of intervals to be used if an element size legend is used.

    element_size_legend_title : string
        The title of the element size legend.

    element_size_legend_loc : string
        The location of the element size legend on the figure.

    element_size_legend_labels : array-like
        The labels of each interval of the element size legend.

    draw_base_legend : boolean
        Determine if the base elements legend is drawn.

    draw_intervals_legend : boolean
        Determine if the intervals legend is drawn.

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
        Determines if an arrow is drawn in the direction of flow of the links
        with no data associated with them.

    disable_interval_deleting : boolean
        If True, empty intervals will be automatically deleted. 

    draw_color_bar : boolean
        Determines if color bar is drawn.
    """
    
    model = self.model
    
    if len(self.model['G_list_pumps_only'])==0:
        pumps = False
    if ax is None:
        if ax is None:
            fig, ax = plt.subplots(figsize=self.figsize)  
            ax.set_frame_on(self.axis_frame)
    if parameter == "demand_patterns":

        demand_pattern_nodes, patterns = processing.get_demand_patterns(self)

        discrete.draw_discrete_nodes(
            self,
            ax,
            demand_pattern_nodes,
            patterns,
            interval_node_size_list=interval_node_size_list,
            interval_node_shape_list=interval_node_shape_list,
            interval_label_list=interval_label_list,
            interval_node_border_color_list=interval_node_border_color_list,
            interval_node_border_width_list=interval_node_border_width_list,
            cmap=cmap,
            color_list=color_list,
        )

        base.draw_base_elements(self,
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

            base.draw_legend(
                ax,
                patterns,
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
                pump_line_style=pump_line_style,
                base_link_line_style=base_link_line_style,
                base_link_arrows=base_link_arrows,
                pump_arrows=pump_arrows,
                draw_base_links=True,
            )
        if savefig:

            save_fig(self, save_name=save_name,
                     dpi=dpi, save_format=save_format)
        return
    if parameter == "diameter" or parameter == "roughness":

        parameter_results, link_list = processing.get_parameter(
            self, "link", parameter
        )

        if unit is not None:
            parameter_results = unit_conversion(
                parameter_results, parameter, unit)
        uniques = sorted(pd.unique(parameter_results))

        interval_names = []

        for interval_name in uniques:

            interval_names = np.append(
                interval_names, ("{:.{j}f}".format(interval_name, j=legend_sig_figs)))
        interval_results = {}

        for interval_name in interval_names:

            interval_results[interval_name] = {}

        for link in link_list:

            interval_results["{:.{j}f}".format(parameter_results.loc[link], j=legend_sig_figs)][link] = model[
                "G_pipe_name_list"
            ].index(link)

        # return interval_results,parameter_results,uniques
        discrete.draw_discrete_links(
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

            base.draw_legend(
                ax,
                interval_names,
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
                pump_line_style=pump_line_style,
                base_link_line_style=base_link_line_style,
                base_link_arrows=base_link_arrows,
                pump_arrows=pump_arrows,
                draw_base_links=False,
            )
        if savefig:

            save_fig(self, save_name=save_name,
                     dpi=dpi, save_format=save_format)
        return
    if parameter == "tag":

        parameter_results, node_list = processing.get_parameter(
            self, "node", parameter
        )

        uniques = []

        if any(i is not None for i in (parameter_results.values.tolist())):
            uniques = pd.unique(parameter_results).tolist()
        interval_names = []
        if not uniques:
            pass
        else:
            for interval_name in uniques:

                interval_names.append(interval_name)

        if None in interval_names:
            interval_names.remove(None)

        interval_names.append('No Tag')
        interval_results = {}

        for interval_name in interval_names:

            interval_results[interval_name] = {}
        for node in node_list:

            if parameter_results.loc[node] is None:

                interval_results["No Tag"][node] = model["node_names"].index(
                    node)

                continue
            interval_results[parameter_results.loc[node]][node] = model[
                "node_names"
            ].index(node)
        discrete.draw_discrete_nodes(
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

            base.draw_legend(
                ax,
                interval_names,
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
                pump_line_style=pump_line_style,
                base_link_line_style=base_link_line_style,
                base_link_arrows=base_link_arrows,
                pump_arrows=pump_arrows,
                draw_base_links=True,
            )
        if savefig:

            save_fig(self, save_name=save_name,
                     dpi=dpi, save_format=save_format)
        return
    if parameter == "custom_data":

        if data_type == "unique":

            if parameter_type == "link":

                discrete.draw_discrete_links(
                    self,
                    ax,
                    custom_data_values[0],
                    custom_data_values[1],
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

                    base.draw_legend(
                        ax,
                        custom_data_values[1],
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
                        pump_line_style=pump_line_style,
                        base_link_line_style=base_link_line_style,
                        base_link_arrows=base_link_arrows,
                        pump_arrows=pump_arrows,
                        draw_base_links=False
                    )
            elif parameter_type == "node":

                discrete.draw_discrete_nodes(
                    self,
                    ax,
                    custom_data_values[0],
                    custom_data_values[1],
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

                    base.draw_legend(
                        ax,
                        custom_data_values[1],
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
                        pump_line_style=pump_line_style,
                        base_link_line_style=base_link_line_style,
                        base_link_arrows=base_link_arrows,
                        pump_arrows=pump_arrows,
                        draw_base_links=True
                    )
                    
            if savefig:

                save_fig(self, save_name=save_name,
                         dpi=dpi, save_format=save_format)
            return
        if data_type == "discrete":
            interval_results, interval_names = processing.bin_parameter(
                self,
                custom_data_values[1],
                custom_data_values[0],
                intervals=intervals,
                num_intervals=num_intervals,
                legend_sig_figs=legend_sig_figs,
                disable_interval_deleting=disable_interval_deleting,
            )

            if parameter_type == "link":

                discrete.draw_discrete_links(
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

                    base.draw_legend(
                        ax,
                        interval_names,
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
                        pump_line_style=pump_line_style,
                        base_link_line_style=base_link_line_style,
                        base_link_arrows=base_link_arrows,
                        pump_arrows=pump_arrows,
                        draw_base_links=False
                    )
                    
            if parameter_type == "node":

                discrete.draw_discrete_nodes(
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

                    base.draw_legend(
                        ax,
                        interval_names,
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
                        pump_line_style=pump_line_style,
                        base_link_line_style=base_link_line_style,
                        base_link_arrows=base_link_arrows,
                        pump_arrows=pump_arrows,
                        draw_base_links=True
                    )

            if savefig:

                save_fig(self, save_name=save_name,
                         dpi=dpi, save_format=save_format)

                return
        if data_type == "continuous":

            if parameter_type == "link":
                if min_width is not None and max_width is not None:
                    normalized_parameter = normalize_parameter(
                        custom_data_values[1], min_width, max_width
                    )

                    widths = normalized_parameter

                g = base.draw_links(
                    self,
                    ax,
                    custom_data_values[0],
                    parameter_results=custom_data_values[1],
                    cmap=cmap,
                    widths=widths,
                    vmin=vmin,
                    vmax=vmax,
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

                    base.draw_legend(ax,
                                     title=legend_title,
                                     pumps=pumps,
                                     loc=legend_loc_1,
                                     font_size=font_size,
                                     font_color=font_color,
                                     legend_title_font_size=legend_title_font_size,
                                     draw_frame=draw_frame,
                                     pump_color=pump_color,
                                     base_link_color=base_link_color,
                                     node_sizes=node_size,
                                     link_sizes=widths,
                                     element_size_intervals=element_size_intervals,
                                     element_size_legend_title=element_size_legend_title,
                                     element_size_legend_loc=element_size_legend_loc,
                                     element_size_legend_labels=element_size_legend_labels,
                                     draw_base_legend=draw_base_legend,
                                     draw_intervals_legend=draw_intervals_legend,
                                     pump_line_style='-',
                                     base_link_line_style='-',
                                     base_link_arrows=False,
                                     pump_arrows=False,
                                     draw_base_links=False,
                                     )
                    
            elif parameter_type == "node":
                if min_size is not None and max_size is not None:
                    normalized_parameter = normalize_parameter(
                        custom_data_values[1], min_size, max_size
                    )

                    node_size = normalized_parameter
                g = base.draw_nodes(
                    self,
                    ax,
                    custom_data_values[0],
                    parameter_results=custom_data_values[1],
                    node_size=node_size,
                    cmap=cmap,
                    vmin=vmin,
                    vmax=vmax,
                    node_shape=node_shape,
                    line_widths=line_widths,
                    edge_colors=edge_colors,
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

                    base.draw_legend(ax,
                                     title=legend_title,
                                     pumps=pumps,
                                     loc=legend_loc_1,
                                     font_size=font_size,
                                     font_color=font_color,
                                     legend_title_font_size=legend_title_font_size,
                                     draw_frame=draw_frame,
                                     pump_color=pump_color,
                                     base_link_color=base_link_color,
                                     node_sizes=node_size,
                                     link_sizes=widths,
                                     element_size_intervals=element_size_intervals,
                                     element_size_legend_title=element_size_legend_title,
                                     element_size_legend_loc=element_size_legend_loc,
                                     element_size_legend_labels=element_size_legend_labels,
                                     draw_base_legend=draw_base_legend,
                                     draw_intervals_legend=draw_intervals_legend,
                                     pump_line_style='-',
                                     base_link_line_style='-',
                                     base_link_arrows=False,
                                     pump_arrows=False,
                                     draw_base_links=True,
                                     )
                    
            if draw_color_bar == True:
                base.draw_color_bar(ax, 
                                    g, 
                                    cmap, 
                                    color_bar_title=color_bar_title,
                                    color_bar_width=color_bar_width,
                                    color_bar_height=color_bar_height)
                
            if savefig:

                save_fig(self, save_name=save_name,
                         dpi=dpi, save_format=save_format)
            return
    if isinstance(parameter, str):

        if data_type == "unique":

            element_list, intervals = convert_excel(
                self, parameter, parameter_type, data_type, excel_columns[0], excel_columns[1]
            )

            if parameter_type == "link":

                discrete.draw_discrete_links(
                    self,
                    ax,
                    element_list,
                    intervals,
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

                    base.draw_legend(
                        ax,
                        intervals,
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
                        pump_line_style='-',
                        base_link_line_style='-',
                        base_link_arrows=False,
                        pump_arrows=False,
                        draw_base_links=False,
                    )
                    
            elif parameter_type == "node":

                discrete.draw_discrete_nodes(
                    self,
                    ax,
                    element_list,
                    intervals,
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

                    base.draw_legend(
                        ax,
                        intervals,
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
                        pump_line_style='-',
                        base_link_line_style='-',
                        base_link_arrows=False,
                        pump_arrows=False,
                        draw_base_links=True,
                    )

            if savefig:

                save_fig(self, save_name=save_name,
                         dpi=dpi, save_format=save_format)
            return
        if data_type == "discrete":

            data = convert_excel(
                self, parameter, parameter_type, data_type, excel_columns[0], excel_columns[1]
            )

            interval_results, interval_names = processing.bin_parameter(
                self,
                data["element_list"],
                data["index"],
                intervals=intervals,
                num_intervals=num_intervals,
                legend_sig_figs=legend_sig_figs,
                disable_interval_deleting=disable_interval_deleting,
            )

            if parameter_type == "link":

                discrete.draw_discrete_links(
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

                    base.draw_legend(
                        ax,
                        interval_names,
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
                        pump_line_style='-',
                        base_link_line_style='-',
                        base_link_arrows=False,
                        pump_arrows=False,
                        draw_base_links=False,     
                    )
            if parameter_type == "node":

                discrete.draw_discrete_nodes(
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

                    base.draw_legend(
                        ax,
                        interval_names,
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
                        pump_line_style='-',
                        base_link_line_style='-',
                        base_link_arrows=False,
                        pump_arrows=False,
                        draw_base_links=True,     
                    )
           
            if savefig:

                save_fig(self, save_name=save_name,
                         dpi=dpi, save_format=save_format)
            return
        if data_type == "continuous":

            data = convert_excel(
                self, parameter, parameter_type, data_type, excel_columns[0], excel_columns[1]
            )

            if parameter_type == "link":

                if min_width is not None and max_width is not None:
                    normalized_parameter = normalize_parameter(
                        custom_data_values[1], min_width, max_width
                    )

                    widths = normalized_parameter

                g = base.draw_links(
                    self,
                    ax,
                    data["index"],
                    parameter_results=data["element_list"],
                    cmap=cmap,
                    widths=widths,
                    vmin=vmin,
                    vmax=vmax,
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

                    base.draw_legend(ax,
                                     title=legend_title,
                                     pumps=pumps,
                                     loc=legend_loc_1,
                                     font_size=font_size,
                                     font_color=font_color,
                                     legend_title_font_size=legend_title_font_size,
                                     draw_frame=draw_frame,
                                     pump_color=pump_color,
                                     base_link_color=base_link_color,
                                     node_sizes=node_size,
                                     link_sizes=widths,
                                     element_size_intervals=element_size_intervals,
                                     element_size_legend_title=element_size_legend_title,
                                     element_size_legend_loc=element_size_legend_loc,
                                     element_size_legend_labels=element_size_legend_labels,
                                     draw_base_legend=draw_base_legend,
                                     draw_intervals_legend=draw_intervals_legend,
                                     pump_line_style='-',
                                     base_link_line_style='-',
                                     base_link_arrows=False,
                                     pump_arrows=False,
                                     draw_base_links=False,
                                     )
                    
            elif parameter_type == "node":
                if min_size is not None and max_size is not None:
                    normalized_parameter = normalize_parameter(
                        custom_data_values[1], min_size, max_size
                    )

                    node_size = normalized_parameter
                g = base.draw_nodes(
                    self,
                    ax,
                    data["index"],
                    parameter_results=data["element_list"],
                    node_size=node_size,
                    cmap=cmap,
                    vmin=vmin,
                    vmax=vmax,
                    node_shape=node_shape,
                    line_widths=line_widths,
                    edge_colors=edge_colors,
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

                    base.draw_legend(ax,
                                     title=legend_title,
                                     pumps=pumps,
                                     loc=legend_loc_1,
                                     font_size=font_size,
                                     font_color=font_color,
                                     legend_title_font_size=legend_title_font_size,
                                     draw_frame=draw_frame,
                                     pump_color=pump_color,
                                     base_link_color=base_link_color,
                                     node_sizes=node_size,
                                     link_sizes=widths,
                                     element_size_intervals=element_size_intervals,
                                     element_size_legend_title=element_size_legend_title,
                                     element_size_legend_loc=element_size_legend_loc,
                                     element_size_legend_labels=element_size_legend_labels,
                                     draw_base_legend=draw_base_legend,
                                     draw_intervals_legend=draw_intervals_legend,
                                     pump_line_style='-',
                                     base_link_line_style='-',
                                     base_link_arrows=False,
                                     pump_arrows=False,
                                     draw_base_links=True,   
                                     )
                    
            if draw_color_bar == True:
                base.draw_color_bar(ax, 
                                    g, 
                                    cmap, 
                                    color_bar_title=color_bar_title,
                                    color_bar_width=color_bar_width,
                                    color_bar_height=color_bar_height)
            

            if savefig:

                save_fig(self, save_name=save_name,
                         dpi=dpi, save_format=save_format)
        return
