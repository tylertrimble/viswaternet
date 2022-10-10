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
    model,
    ax,
    parameter=None,
    parameter_type=None,
    data_type=None,
    excel_columns=None,
    custom_data_values=None,
    unit=None,
    bins="automatic",
    bin_size_list=None,
    bin_shape_list=None,
    bin_edge_num=5,
    bin_width_list=None,
    bin_label_list=None,
    bin_border_list=None,
    bin_border_width_list=None,
    color_list=None,
    min_width=1,
    max_width=5,
    vmin=None,
    vmax=None,
    tanks=True,
    reservoirs=True,
    pumps=True,
    valves=True,
    cmap=default_cmap,
    legend=True,
    legend_title=None,
    node_size=100,
    node_shape=".",
    legend_loc_1="upper right",
    legend_loc_2="lower right",
    savefig=True,
    save_name=None,
    color_bar_title=None,
    edge_color=None,
    edge_width=None,
    font_size=15,
    font_color='k',
    legend_title_font_size=17,
    draw_frame=False,
    legend_sig_figs=3
):

    if parameter == "demand_patterns":

        demand_pattern_nodes, patterns = processing.get_demand_patterns(model)

        discrete.draw_discrete_nodes(
            model,
            ax,
            demand_pattern_nodes,
            patterns,
            bin_size_list=bin_size_list,
            bin_shape_list=bin_shape_list,
            bin_label_list=bin_label_list,
            bin_border_list=bin_border_list,
            bin_border_width_list=bin_border_width_list,
            cmap=cmap,
            color_list=color_list,
        )

        base.draw_base_elements(model, ax, nodes=False)

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
            )
        if savefig:

            save_fig(model, save_name=save_name)
        return
    if parameter == "diameter" or parameter == "roughness":

        parameter_results, link_list = processing.get_parameter(
            model, "link", parameter
        )

        if unit is not None:
            parameter_results = unit_conversion(parameter_results, parameter, unit)
        uniques = sorted(pd.unique(parameter_results))

        binNames = []

        for binName in uniques:

            binNames = np.append(binNames, ("{:.{j}f}".format(binName,j=legend_sig_figs)))
        binnedResults = {}

        for binName in binNames:

            binnedResults[binName] = {}
            
        for link in link_list:

            binnedResults["{:.{j}f}".format(parameter_results.loc[link],j=legend_sig_figs)][link] = model[
                "G_pipe_name_list"
            ].index(link)
        
        #return binnedResults,parameter_results,uniques
        discrete.draw_discrete_links(
            model,
            ax,
            binnedResults,
            binNames,
            bin_width_list=bin_width_list,
            bin_label_list=bin_label_list,
            cmap=cmap,
            color_list=color_list,
        )

        base.draw_base_elements(
            model,
            ax,
            nodes=False,
            links=False,
            tanks=tanks,
            reservoirs=reservoirs,
            pumps=pumps,
            valves=valves,
        )

        if legend:

            base.draw_legend(
                ax,
                binNames,
                title=legend_title,
                pumps=pumps,
                loc=legend_loc_1,
                loc2=legend_loc_2,
                font_size=font_size,
                font_color=font_color,
                legend_title_font_size=legend_title_font_size,
                draw_frame=draw_frame,
            )
        if savefig:

            save_fig(model, save_name=save_name)
        return
    if parameter == "tag":

        parameter_results, node_list = processing.get_parameter(
            model, "node", parameter
        )

        uniques = pd.unique(parameter_results)
        uniques = uniques[uniques is not None]

        binNames = []

        if len(uniques) != 0:

            for binName in uniques:

                binNames = binName
        binNames = np.append(binNames, "No Tag")

        binnedResults = {}

        for binName in binNames:

            binnedResults[binName] = {}
        for node in node_list:

            if parameter_results.loc[node] is None:

                binnedResults["No Tag"][node] = model["node_names"].index(node)

                continue
            binnedResults[parameter_results.loc[node]][node] = model[
                "node_names"
            ].index(node)
        discrete.draw_discrete_nodes(
            model,
            ax,
            binnedResults,
            binNames,
            bin_size_list=bin_size_list,
            bin_shape_list=bin_shape_list,
            bin_label_list=bin_label_list,
            bin_border_list=bin_border_list,
            bin_border_width_list=bin_border_width_list,
            cmap=cmap,
            color_list=color_list,
        )

        base.draw_base_elements(
            model,
            ax,
            nodes=False,
            tanks=tanks,
            reservoirs=reservoirs,
            pumps=pumps,
            valves=valves,
        )

        if legend:

            base.draw_legend(
                ax,
                binNames,
                title=legend_title,
                pumps=pumps,
                loc=legend_loc_1,
                loc2=legend_loc_2,
                font_size=font_size,
                font_color=font_color,
                legend_title_font_size=legend_title_font_size,
                draw_frame=draw_frame,
            )
        if savefig:

            save_fig(model, save_name=save_name)
        return
    if parameter == "custom_data":

        if data_type == "unique":

            if parameter_type == "link":

                discrete.draw_discrete_links(
                    model,
                    ax,
                    custom_data_values[0],
                    custom_data_values[1],
                    bin_width_list=bin_width_list,
                    bin_label_list=bin_label_list,
                    cmap=cmap,
                    color_list=color_list,
                )

                base.draw_base_elements(
                    model,
                    ax,
                    links=False,
                    nodes=False,
                    tanks=tanks,
                    reservoirs=reservoirs,
                    pumps=pumps,
                    valves=valves,
                )
            elif parameter_type == "node":

                discrete.draw_discrete_nodes(
                    model,
                    ax,
                    custom_data_values[0],
                    custom_data_values[1],
                    bin_size_list=bin_size_list,
                    bin_shape_list=bin_shape_list,
                    bin_label_list=bin_label_list,
                    bin_border_list=bin_border_list,
                    bin_border_width_list=bin_border_width_list,
                    cmap=cmap,
                    color_list=color_list,
                )

                base.draw_base_elements(
                    model,
                    ax,
                    nodes=False,
                    tanks=tanks,
                    reservoirs=reservoirs,
                    pumps=pumps,
                    valves=valves,
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
                )
            if savefig:

                save_fig(model, save_name=save_name)
            return
        if data_type == "discrete":
            binnedResults, binNames = processing.bin_parameter(
                model,
                custom_data_values[1],
                custom_data_values[0],
                bin_list=bins,
                bin_edge_num=bin_edge_num,
                legend_sig_figs=legend_sig_figs
            )

            if parameter_type == "link":

                discrete.draw_discrete_links(
                    model,
                    ax,
                    binnedResults,
                    binNames,
                    bin_width_list=bin_width_list,
                    bin_label_list=bin_label_list,
                    cmap=cmap,
                    color_list=color_list,
                )

                base.draw_base_elements(
                    model,
                    ax,
                    nodes=False,
                    links=False,
                    tanks=tanks,
                    reservoirs=reservoirs,
                    pumps=pumps,
                    valves=valves,
                )
            if parameter_type == "node":

                discrete.draw_discrete_nodes(
                    model,
                    ax,
                    binnedResults,
                    binNames,
                    bin_size_list=bin_size_list,
                    bin_shape_list=bin_shape_list,
                    bin_label_list=bin_label_list,
                    bin_border_list=bin_border_list,
                    bin_border_width_list=bin_border_width_list,
                    cmap=cmap,
                    color_list=color_list,
                )

                base.draw_base_elements(
                    model,
                    ax,
                    nodes=False,
                    tanks=tanks,
                    reservoirs=reservoirs,
                    pumps=pumps,
                    valves=valves,
                )
            if legend:

                base.draw_legend(
                    ax,
                    binNames,
                    title=legend_title,
                    pumps=pumps,
                    loc=legend_loc_1,
                    loc2=legend_loc_2,
                    font_size=font_size,
                    font_color=font_color,
                    legend_title_font_size=legend_title_font_size,
                    draw_frame=draw_frame,
                )
            if savefig:

                save_fig(model, save_name=save_name)

                return
        if data_type == "continuous":

            if parameter_type == "link":

                normalized_parameter = normalize_parameter(
                    model, custom_data_values[1], min_width, max_width
                )

                widths = normalized_parameter

                g = continuous.draw_links(
                    model,
                    ax,
                    custom_data_values[0],
                    parameter_results=custom_data_values[1],
                    cmap=cmap,
                    widths=widths,
                )

                base.draw_base_elements(
                    model,
                    ax,
                    links=False,
                    nodes=False,
                    tanks=tanks,
                    reservoirs=reservoirs,
                    pumps=pumps,
                    valves=valves,
                )
            elif parameter_type == "node":

                g = continuous.draw_nodes(
                    model,
                    ax,
                    custom_data_values[0],
                    parameter_results=custom_data_values[1],
                    node_size=node_size,
                    cmap=cmap,
                    node_shape=node_shape,
                )

                base.draw_base_elements(
                    model,
                    ax,
                    nodes=False,
                    tanks=tanks,
                    reservoirs=reservoirs,
                    pumps=pumps,
                    valves=valves,
                )
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
                                 )
            if savefig:

                save_fig(model, save_name=save_name)
            return
    if isinstance(parameter, str):

        if data_type == "unique":

            node_list, bin_list = convert_excel(
                model, parameter, data_type, excel_columns[0], excel_columns[1]
            )

            if parameter_type == "link":

                discrete.draw_discrete_links(
                    model,
                    ax,
                    node_list,
                    bin_list,
                    bin_width_list=bin_width_list,
                    bin_label_list=bin_label_list,
                    cmap=cmap,
                    color_list=color_list,
                )

                base.draw_base_elements(
                    model,
                    ax,
                    links=False,
                    nodes=False,
                    tanks=tanks,
                    reservoirs=reservoirs,
                    pumps=pumps,
                    valves=valves,
                )
            elif parameter_type == "node":

                discrete.draw_discrete_nodes(
                    model,
                    ax,
                    node_list,
                    bin_list,
                    bin_size_list=bin_size_list,
                    bin_shape_list=bin_shape_list,
                    bin_label_list=bin_label_list,
                    bin_border_list=bin_border_list,
                    bin_border_width_list=bin_border_width_list,
                    cmap=cmap,
                    color_list=color_list,
                )

                base.draw_base_elements(
                    model,
                    ax,
                    nodes=False,
                    tanks=tanks,
                    reservoirs=reservoirs,
                    pumps=pumps,
                    valves=valves,
                )
            if legend:

                base.draw_legend(
                    ax,
                    bin_list,
                    title=legend_title,
                    pumps=pumps,
                    loc=legend_loc_1,
                    loc2=legend_loc_2,
                    font_size=font_size,
                    font_color=font_color,
                    legend_title_font_size=legend_title_font_size,
                    draw_frame=draw_frame,
                )
            if savefig:

                save_fig(model, save_name=save_name)
            return
        if data_type == "discrete":

            data = convert_excel(
                model, parameter, data_type, excel_columns[0], excel_columns[1]
            )

            binnedResults, binNames = processing.bin_parameter(
                model,
                data["element_list"],
                data["index"],
                bin_list=bins,
                bin_edge_num=bin_edge_num,
                legend_sig_figs=legend_sig_figs
            )

            if parameter_type == "link":

                discrete.draw_discrete_links(
                    model,
                    ax,
                    binnedResults,
                    binNames,
                    bin_width_list=bin_width_list,
                    bin_label_list=bin_label_list,
                    cmap=cmap,
                    color_list=color_list,
                )

                base.draw_base_elements(
                    model,
                    ax,
                    nodes=False,
                    links=False,
                    tanks=tanks,
                    reservoirs=reservoirs,
                    pumps=pumps,
                    valves=valves,
                )
            if parameter_type == "node":

                discrete.draw_discrete_nodes(
                    model,
                    ax,
                    binnedResults,
                    binNames,
                    bin_size_list=bin_size_list,
                    bin_shape_list=bin_shape_list,
                    bin_label_list=bin_label_list,
                    bin_border_list=bin_border_list,
                    bin_border_width_list=bin_border_width_list,
                    cmap=cmap,
                    color_list=color_list,
                )

                base.draw_base_elements(
                    model,
                    ax,
                    nodes=False,
                    tanks=tanks,
                    reservoirs=reservoirs,
                    pumps=pumps,
                    valves=valves,
                )
            if legend:

                base.draw_legend(
                    ax,
                    binNames,
                    title=legend_title,
                    pumps=pumps,
                    loc=legend_loc_1,
                    loc2=legend_loc_2,
                    font_size=font_size,
                    font_color=font_color,
                    legend_title_font_size=legend_title_font_size,
                    draw_frame=draw_frame,
                )
            if savefig:

                save_fig(model, save_name=save_name)
            return
        if data_type == "continuous":

            data = convert_excel(
                model, parameter, data_type, excel_columns[0], excel_columns[1]
            )

            if parameter_type == "link":

                normalized_parameter = normalize_parameter(
                    model, data["element_list"], min_width, max_width
                )

                widths = normalized_parameter

                g = continuous.draw_links(
                    model,
                    ax,
                    data["index"],
                    parameter_results=data["element_list"],
                    cmap=cmap,
                    widths=widths,
                )

                base.draw_base_elements(
                    model,
                    ax,
                    links=False,
                    nodes=False,
                    tanks=tanks,
                    reservoirs=reservoirs,
                    pumps=pumps,
                    valves=valves,
                )
            elif parameter_type == "node":

                g = continuous.draw_nodes(
                    model,
                    ax,
                    data["index"],
                    parameter_results=data["element_list"],
                    node_size=node_size,
                    cmap=cmap,
                    node_shape=node_shape,
                )

                base.draw_base_elements(
                    model,
                    ax,
                    nodes=False,
                    tanks=tanks,
                    reservoirs=reservoirs,
                    pumps=pumps,
                    valves=valves,
                )
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
                                 )

            if savefig:

                save_fig(model, save_name=save_name)
        return
