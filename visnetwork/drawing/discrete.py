# -*- coding: utf-8 -*-
"""
Created on Sun Oct  2 20:55:15 2022

@author: Tyler
"""
import numpy as np
import matplotlib as mpl
import networkx.drawing.nx_pylab as nxp
from visnetwork.network import processing
from visnetwork.utils import save_fig, unit_conversion
from visnetwork.drawing import base

default_cmap = mpl.cm.get_cmap("autumn_r")


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
    model=self.model
    if interval_node_size_list is None:

        if len(model["node_names"]) < 300:

            interval_node_size_list = np.ones(len(intervals)) * 300
        elif len(model["node_names"]) >= 300 and len(model["node_names"]) < 1000:

            interval_node_size_list = np.ones(len(intervals)) * (80000 / len(model["node_names"]))
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

            interval_node_border_color_list = np.append(interval_node_border_color_list, "k")
    if interval_node_border_width_list is None:
        interval_node_border_width_list = []

        for i in range(len(intervals)):

            interval_node_border_width_list = np.append(interval_node_border_width_list, 0)
    counter = 0
    empty_interval = False

    if (color_list is not None and cmap is not None) or color_list is not None:
        for interval_name in intervals:
            node_list = [model["node_names"][i] for i in nodes.get(interval_name).values()]

            if len(node_list) == 0:
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
                        [model["node_names"][i] for i in nodes.get(interval_name).values()]
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
        cmap = mpl.cm.get_cmap(cmap)
        cmapValue = 1 / len(intervals)

        for interval_name in intervals:
            node_list = [model["node_names"][i] for i in nodes.get(interval_name).values()]
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

            cmap2 = mpl.cm.get_cmap(cmap)
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
    model=self.model
    if interval_link_width_list is None:
        interval_link_width_list = np.ones(len(intervals)) * 2
    if interval_label_list is None:
        interval_label_list = intervals    
    empty_interval = False
    if (color_list is not None and cmap is not None) or color_list is not None:
        for counter,interval_name in enumerate(intervals):
            edge_list = [model["pipe_list"][i] for i in links.get(interval_name).values()]
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

            for counter,interval_name in enumerate(intervals):
                edge_list = [model["pipe_list"][i] for i in links.get(interval_name).values()]
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
        cmap = mpl.cm.get_cmap(cmap)
        cmapValue = 1 / len(intervals)
        for counter,interval_name in enumerate(intervals):
            
            
            
            
            
            
            edge_list = [model["pipe_list"][i] for i in links.get(interval_name).values()]
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
            cmap2 = mpl.cm.get_cmap(cmap)
            cmapValue2 = 1 / len(intervals)

            for counter,interval_name in enumerate(intervals):
                edge_list = [model["pipe_list"][i] for i in links.get(interval_name).values()]
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
    ax,
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
    savefig=True,
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
            parameter_results = unit_conversion(parameter_results, parameter, unit)
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
                draw_intervals_legend=draw_interval_legend
            )
    if savefig:

        save_fig(self, save_name=save_name,dpi=dpi,save_format=save_format)


def plot_discrete_links(
    self,
    ax,
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
    savefig=True,
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
    if parameter is not None:

        parameter_results, link_list = processing.get_parameter(
            self, "link", parameter, element_list=element_list, value=value
        )
        if unit is not None:
            parameter_results = unit_conversion(parameter_results, parameter, unit)
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
                draw_intervals_legend=draw_intervals_legend
            )
    if savefig:

        save_fig(self, save_name=save_name,dpi=dpi,save_format=save_format)
