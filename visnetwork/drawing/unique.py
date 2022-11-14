# -*- coding: utf-8 -*-
"""
Created on Sun Oct  2 21:09:29 2022

@author: Tyler
"""
import numpy as np
import pandas as pd
import matplotlib as mpl
from visnet.network import processing
from visnet.utils import convert_excel, save_fig, normalize_parameter, unit_conversion
from visnet.drawing import base
from visnet.drawing import discrete
from visnet.drawing import continuous

default_cmap = mpl.cm.get_cmap("autumn_r")


def plot_unique_data(
    self,
    ax,
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
    savefig=True,
    save_name=None,
    dpi='figure',
    save_format='png',
    color_bar_title=None,
    edge_color=None,
    edge_width=None,
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
):
    model=self.model
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
                base_link_color=base_link_color
            )
        if savefig:

            save_fig(self, save_name=save_name,dpi=dpi,save_format=save_format)
        return
    if parameter == "diameter" or parameter == "roughness":

        parameter_results, link_list = processing.get_parameter(
            self, "link", parameter
        )

        if unit is not None:
            parameter_results = unit_conversion(parameter_results, parameter, unit)
        uniques = sorted(pd.unique(parameter_results))

        interval_names = []

        for interval_name in uniques:

            interval_names = np.append(interval_names, ("{:.{j}f}".format(interval_name,j=legend_sig_figs)))
        interval_results = {}

        for interval_name in interval_names:

            interval_results[interval_name] = {}
            
        for link in link_list:

            interval_results["{:.{j}f}".format(parameter_results.loc[link],j=legend_sig_figs)][link] = model[
                "G_pipe_name_list"
            ].index(link)
        
        #return interval_results,parameter_results,uniques
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
                base_link_color=base_link_color
            )
        if savefig:

            save_fig(self, save_name=save_name,dpi=dpi,save_format=save_format)
        return
    if parameter == "tag":

        parameter_results, node_list = processing.get_parameter(
            self, "node", parameter
        )
        
        uniques=[]
        
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

                interval_results["No Tag"][node] = model["node_names"].index(node)

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
                base_link_color=base_link_color
            )
        if savefig:

            save_fig(self, save_name=save_name,dpi=dpi,save_format=save_format)
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
                    base_link_color=base_link_color
                )
            if savefig:

                save_fig(self, save_name=save_name,dpi=dpi,save_format=save_format)
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
                    base_link_color=base_link_color
                )
            if savefig:

                save_fig(self, save_name=save_name,dpi=dpi,save_format=save_format)

                return
        if data_type == "continuous":

            if parameter_type == "link":
                if min_width is not None and max_width is not None:
                    normalized_parameter = normalize_parameter(
                        self, custom_data_values[1], min_width, max_width
                    )
    
                    widths = normalized_parameter

                g = continuous.draw_links(
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
            elif parameter_type == "node":
                if min_size is not None and max_size is not None:
                    normalized_parameter = normalize_parameter(
                        self, custom_data_values[1], min_size, max_size
                    )
    
                    node_size = normalized_parameter
                g = continuous.draw_nodes(
                    self,
                    ax,
                    custom_data_values[0],
                    parameter_results=custom_data_values[1],
                    node_size=node_size,
                    cmap=cmap,
                    vmin=vmin,
                    vmax=vmax,
                    node_shape=node_shape,
                    line_widths= line_widths,
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
            if draw_color_bar==True:
                base.draw_color_bar(ax, g, cmap, color_bar_title=color_bar_title)

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
                                 link_sizes=widths,
                                 node_sizes=node_size,
                                 element_size_intervals=element_size_intervals,
                                 element_size_legend_title=element_size_legend_title,
                                 element_size_legend_loc=element_size_legend_loc,
                                 element_size_legend_labels=element_size_legend_labels,
                                 draw_base_legend= draw_base_legend,
                                 draw_intervals_legend=draw_intervals_legend
                                 )
            if savefig:

                save_fig(self, save_name=save_name,dpi=dpi,save_format=save_format)
            return
    if isinstance(parameter, str):

        if data_type == "unique":

            node_list, intervals = convert_excel(
                self, parameter, data_type, excel_columns[0], excel_columns[1]
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
            elif parameter_type == "node":

                discrete.draw_discrete_nodes(
                    self,
                    ax,
                    node_list,
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
                    base_link_color=base_link_color
                )
            if savefig:

                save_fig(self, save_name=save_name,dpi=dpi,save_format=save_format)
            return
        if data_type == "discrete":

            data = convert_excel(
                self, parameter, data_type, excel_columns[0], excel_columns[1]
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
                    base_link_color=base_link_color
                )
            if savefig:

                save_fig(self, save_name=save_name,dpi=dpi,save_format=save_format)
            return
        if data_type == "continuous":

            data = convert_excel(
                self, parameter, data_type, excel_columns[0], excel_columns[1]
            )

            if parameter_type == "link":

                if min_width is not None and max_width is not None:
                    normalized_parameter = normalize_parameter(
                        self, custom_data_values[1], min_width, max_width
                    )
    
                    widths = normalized_parameter

                g = continuous.draw_links(
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
            elif parameter_type == "node":
                if min_size is not None and max_size is not None:
                    normalized_parameter = normalize_parameter(
                        self, custom_data_values[1], min_size, max_size
                    )
    
                    node_size = normalized_parameter
                g = continuous.draw_nodes(
                    self,
                    ax,
                    data["index"],
                    parameter_results=data["element_list"],
                    node_size=node_size,
                    cmap=cmap,
                    vmin=vmin,
                    vmax=vmax,
                    node_shape=node_shape,
                    line_widths= line_widths,
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
                
            if draw_color_bar==True:
                base.draw_color_bar(ax, g, cmap, color_bar_title=color_bar_title)
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
                                 element_size_intervals= element_size_intervals,
                                 element_size_legend_title=element_size_legend_title,
                                 element_size_legend_loc=element_size_legend_loc,
                                 element_size_legend_labels=element_size_legend_labels,
                                 draw_base_legend= draw_base_legend,
                                 draw_intervals_legend=draw_intervals_legend
                                 )

            if savefig:

                save_fig(self, save_name=save_name,dpi=dpi,save_format=save_format)
        return
