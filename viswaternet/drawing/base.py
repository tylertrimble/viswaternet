# -*- coding: utf-8 -*-
import numpy as np
import networkx.drawing.nx_pylab as nxp
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.lines import Line2D
from mpl_toolkits.axes_grid1 import make_axes_locatable
from viswaternet.utils import save_fig, normalize_parameter
from viswaternet.utils.markers import *


def draw_nodes(
        self,
        ax,
        node_list,
        parameter_results=None,
        vmin=None,
        vmax=None,
        node_size=None,
        node_color="k",
        cmap="tab10",
        node_shape=".",
        node_border_color="k",
        node_border_width=0,
        label=None,
        draw_tanks=True,
        draw_reservoirs=True):
    # Initalize parameters
    model = self.model
    if parameter_results is None:
        parameter_results = []
    # Creates default list of node sizes
    if node_size is None:
        node_size = (np.ones(len(node_list)) * 100).tolist()
    if isinstance(node_size, tuple):
        min_size = node_size[0]
        max_size = node_size[1]
        if min_size is not None and max_size is not None:
            node_size = normalize_parameter(
                parameter_results, min_size, max_size)
    # Checks if some data values are given
    if parameter_results:
        # If values is less than this value, we treat it as a negative.
        parameter_results = [parameter_results[node_list.index(name)]
                             for name in node_list
                             if ((name not in model["tank_names"]
                                  or draw_tanks is False)
                             and (name not in model["reservoir_names"]
                                  or draw_reservoirs is False))]
        node_list = [node_list[node_list.index(name)]
                     for name in node_list
                     if ((name not in model["tank_names"]
                          or draw_tanks is False)
                     and (name not in model["reservoir_names"]
                          or draw_reservoirs is False))]

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
                    edgecolors=node_border_color,
                    label=label)
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
                    edgecolors=node_border_color,
                    label=label)
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
            linewidths=node_border_width,
            label=label)


def draw_links(
        self,
        ax,
        link_list,
        parameter_results=None,
        edge_color="k",
        cmap="tab10",
        link_width=None,
        vmin=None,
        vmax=None,
        link_style='-',
        link_arrows=False,
        pump_element='node',
        draw_pumps=True,
        valve_element='node',
        draw_valves=True):
    # Initalize parameters
    model = self.model
    if isinstance(link_list, np.ndarray):
        link_list = link_list.tolist()
    if parameter_results is None:
        parameter_results = []
    # Creates default list of link widths
    if link_width is None:
        link_width = (np.ones(len(link_list)) * 1).tolist()
    if isinstance(link_width, tuple):
        min_size = link_width[0]
        max_size = link_width[1]
        if min_size is not None and max_size is not None:
            link_width = normalize_parameter(
                parameter_results, min_size, max_size)
    # Checks if some data values are given
    if parameter_results:
        edges = [model["pipe_list"][model['G_pipe_name_list'].index(name)]
                 for name in link_list
                 if ((name not in model["pump_names"]
                      or pump_element == 'node'
                      or draw_pumps is False)
                 and (name not in model["valve_names"]
                      or valve_element == 'node'
                      or draw_valves is False))]
        pipe_names = model['G_pipe_name_list']
        parameter_results = [parameter_results[pipe_names.index(name)]
                             for name in link_list
                             if ((name not in model["pump_names"]
                                  or pump_element == 'node'
                                  or draw_pumps is False)
                             and (name not in model["valve_names"]
                                  or valve_element == 'node'
                                  or draw_valves is False))]
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
            edge_color=edge_color,
            style=link_style,
            arrows=link_arrows,
            width=link_width,
            node_size=0)


def draw_base_elements(
        self,
        ax,
        draw_nodes=True,
        draw_links=True,
        draw_reservoirs=True,
        draw_tanks=True,
        draw_pumps=True,
        draw_valves=True,
        element_list=None,
        legend=True,
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
        base_link_arrows=False):
    model = self.model
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
        draw_links=True,
        draw_reservoirs=True,
        draw_tanks=True,
        draw_pumps=True,
        draw_valves=True,
        savefig=False,
        save_name=None,
        dpi='figure',
        save_format='png',
        legend=True,
        base_legend_loc="upper right",
        base_legend_label_font_size=15,
        base_legend_label_color='k',
        draw_legend_frame=False,
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
        base_link_arrows=False):
    # Checks if there is no draw_pumps
    if not self.model['G_list_pumps_only']:
        draw_pumps = False
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
        draw_reservoirs=draw_reservoirs,
        draw_tanks=draw_tanks,
        draw_links=draw_links,
        draw_valves=draw_valves,
        draw_pumps=draw_pumps,
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
    # Draw legend if legend is True. Only draws base elements legend
    if legend:
        draw_legend(
            ax,
            draw_pumps=draw_pumps,
            base_legend_loc=base_legend_loc,
            base_legend_label_color=base_legend_label_color,
            base_legend_label_font_size=base_legend_label_font_size,
            draw_legend_frame=draw_legend_frame,
            pump_color=pump_color,
            base_link_color=base_link_color,
            pump_line_style=pump_line_style,
            base_link_line_style=base_link_line_style,
            base_link_arrows=base_link_arrows,
            pump_arrows=pump_arrows,
            draw_links=True,
            draw_valves=draw_valves,
            valve_element=valve_element,
            valve_line_style=valve_line_style,
            valve_color=valve_color,
            valve_arrows=valve_arrows,
            pump_element=pump_element)
    # Save figure if savefig is set to True
    if savefig:
        save_fig(self, save_name=save_name, dpi=dpi, save_format=save_format)


def draw_legend(
        ax,
        intervals=None,
        title=None,
        draw_pumps=True,
        pump_element='node',
        draw_valves=True,
        valve_element='node',
        base_legend_loc="upper right",
        discrete_legend_loc="lower right",
        base_legend_label_font_size=15,
        base_legend_label_color="k",
        discrete_legend_label_font_size=15,
        discrete_legend_label_color="k",
        discrete_legend_title_font_size=17,
        discrete_legend_title_color='k',
        cmap=None,
        color_list=None,
        draw_legend_frame=False,
        pump_color='b',
        valve_color='orange',
        valve_line_style='-',
        valve_arrows=False,
        base_link_color='k',
        node_size=None,
        link_width=None,
        element_size_intervals=None,
        element_size_legend_title=None,
        element_size_legend_loc=None,
        element_size_legend_labels=None,
        draw_base_legend=True,
        draw_discrete_legend=True,
        node_border_color='k',
        linewidths=1,
        pump_line_style='-',
        base_link_line_style='-',
        base_link_arrows=False,
        pump_arrows=False,
        draw_links=True):
    # If no intervals for data legend are specified, then create empty array
    if intervals is None:
        intervals = []
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
                                 markeredgewidth=linewidths,
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
        ax,
        g,
        cmap,
        color_bar_title=None,
        color_bar_width=0.03,
        color_bar_height=0.8):
    # Unruly code to make colorbar location nice and symmetrical when dealing
    # with subplots especially.
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
        label_text_color = 'k',
        label_face_color = 'white',
        label_edge_color = 'k',
        label_alpha = 0.9,
        label_font_style = None,
        label_edge_width = None
        ):
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
                        s=label, color = label_text_color, style = label_font_style,
                        bbox=dict(facecolor=label_face_color,
                                  alpha=label_alpha, edgecolor=label_edge_color,
                                  lw=label_edge_width),
                        horizontalalignment="right",
                        verticalalignment="center",
                        fontsize=label_font_size)
                if xCoord >= 0:
                    ax.text(
                        model["wn"].get_node(node).coordinates[0] + xCoord,
                        model["wn"].get_node(node).coordinates[1] + yCoord,
                        s=label, color = label_text_color, style = label_font_style,
                        bbox=dict(facecolor=label_face_color,
                                  alpha=label_alpha, edgecolor=label_edge_color,
                                  lw=label_edge_width),
                        horizontalalignment="left",
                        verticalalignment="center",
                        fontsize=label_font_size)
            else:
                ax.text(
                    model["wn"].get_node(node).coordinates[0] + xCoord,
                    model["wn"].get_node(node).coordinates[1] + yCoord,
                    s=label, color = label_text_color, style = label_font_style,
                    bbox=dict(facecolor=label_face_color,
                              alpha=label_alpha, edgecolor=label_edge_color,
                              lw=label_edge_width),
                    horizontalalignment="center",
                    verticalalignment="center", fontsize=label_font_size)
    elif draw_nodes is None:
        for label, xCoord, yCoord in zip(labels, x_coords, y_coords):
            ax.text(
                xCoord, yCoord, s=label, color = label_text_color, style = label_font_style,
                bbox=dict(facecolor=label_face_color,
                          alpha=label_alpha, edgecolor=label_edge_color,
                          lw=label_edge_width),
                horizontalalignment="center", fontsize=label_font_size,
                transform=ax.transAxes)
