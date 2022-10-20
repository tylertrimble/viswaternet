# -*- coding: utf-8 -*-
"""
Created on Sun Oct  2 20:58:38 2022

@author: Tyler
"""
import numpy as np
import networkx.drawing.nx_pylab as nxp
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D
from mpl_toolkits.axes_grid1 import make_axes_locatable


from visnet.utils import save_fig


def draw_base_elements(
    model,
    ax,
    nodes=True,
    links=True,
    reservoirs=True,
    tanks=True,
    pumps=True,
    valves=True,
    legend=True,
    reservoir_size=200,
    reservoir_color='k',
    reservoir_shape='s',
    reservoir_border_color=None,
    reservoir_border_width=None,
    tank_size=200,
    tank_color='k',
    tank_shape='d',
    tank_border_color=None,
    tank_border_width=None,
    valve_size=200,
    valve_color='orange',
    valve_shape='P',
    valve_border_color='k',
    valve_border_width=1,
    pump_color='b',
    pump_width=3,
    base_node_color='k',
    base_node_size=30,
    base_link_color='k',
    base_link_width=1
):
    """Draws nodes, links, resevoirs, tanks, pumps and valves without any data
    attached to them.
    Arguments:
    model: Takes dictionary.
    ax: Axis of the figure the user wants the elements to be plotted on.
    reservoirs: Takes Boolean. Determines whether to draw reservoirs or not.
    tanks: Takes Boolean. Determines whether to draw tanks or not.
    pumps: Takes Boolean. Determines whether to draw pumps or not.
    valves: Takes Boolean. Determines whether to draw valves or not.
    legend: Takes Boolean. Determines whether to draw legend or not."""
    if nodes:

        nxp.draw_networkx_nodes(
            model["G"], model["pos_dict"], node_size=base_node_size, node_color=base_node_color
        )
    if reservoirs:

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
            label="Reservoirs",
        )
    if tanks:

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
            label="Tanks",
        )
    if valves:

        valve_coordinates = {}
        valveCounter = 0

        for point1, point2 in model["G_list_valves_only"]:

            midpoint = [
                (
                    model["wn"].get_node(point1).coordinates[0]
                    + model["wn"].get_node(point2).coordinates[0]
                )
                / 2,
                (
                    model["wn"].get_node(point1).coordinates[1]
                    + model["wn"].get_node(point2).coordinates[1]
                )
                / 2,
            ]

            valve_coordinates[model["valve_names"][valveCounter]] = midpoint
            valveCounter += 1
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
            label="Valves",
        )
    if links:

        nxp.draw_networkx_edges(
            model["G"],
            model["pos_dict"],
            ax=ax, arrows=False,
            edge_color=base_link_color,
            width=base_link_width
        )
    if pumps:

        nxp.draw_networkx_edges(
            model["G"],
            model["pos_dict"],
            ax=ax,
            edgelist=model["G_list_pumps_only"],
            edge_color=pump_color,
            width=pump_width,
            arrows=False,
        )


def plot_basic_elements(
    model,
    ax,
    pumps=True,
    valves=True,
    reservoirs=True,
    tanks=True,
    links=True,
    nodes=True,
    savefig=True,
    save_name=None,
    legend=True,
    legend_loc="upper right",
    font_size=15,
    font_color='k',
    legend_title_font_size=17,
    draw_frame=False,
    legend_sig_figs=3,
    reservoir_size=200,
    reservoir_color='k',
    reservoir_shape='s',
    reservoir_border_color=None,
    reservoir_border_width=None,
    tank_size=200,
    tank_color='k',
    tank_shape='d',
    tank_border_color=None,
    tank_border_width=None,
    valve_size=200,
    valve_color='orange',
    valve_shape='P',
    valve_border_color='k',
    valve_border_width=1,
    pump_color='b',
    pump_width=3,
    base_node_color='k',
    base_node_size=30,
    base_link_color='k',
    base_link_width=1
):
    """Creates a basic plot, similar to the default seen in EPANET.
    Arguments:
    model: Saved initilization done with initializeModel
    savefig: Boolean. Determines whether plot is saved to /Images directory"""

    draw_base_elements(
        model,
        ax,
        nodes=nodes,
        reservoirs=reservoirs,
        tanks=tanks,
        links=links,
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
        base_node_color=base_node_color,
        base_node_size=base_node_size,
        base_link_color=base_link_color,
        base_link_width=base_link_width
    )

    if legend:

        draw_legend(ax, 
                    pumps=pumps, 
                    loc=legend_loc,
                    font_size=font_size,
                    font_color=font_color,
                    legend_title_font_size=legend_title_font_size,
                    draw_frame=draw_frame,
                    pump_color=pump_color,
                    base_link_color=base_link_color)
    if savefig:

        save_fig(model, save_name=save_name)


def draw_legend(
    ax,
    bin_list=None,
    title=None,
    pumps=True,
    loc="upper right",
    loc2="lower right",
    font_size=15,
    draw_frame=False,
    legend_title_font_size=17,
    font_color="k",
    pump_color='b',
    base_link_color='k',
    node_sizes=None,
    link_sizes=None,
    element_size_bins=None,
    element_size_legend_title=None,
    element_size_legend_loc=None,
    element_size_legend_labels=None,
    draw_base_legend=True,
    draw_bins_legend=True,
    edge_colors='k',
    linewidths=1
):
    """Draws legend for basic elements.
    Arguments:
    ax: Axis of the figure the user wants the elements to be plotted on.
    bin_list: Takes List. List of bins.
    title: Takes String. Legend title.
    pumps: Takes Boolean. Determines whether pumps are drawn or not.
    loc: Takes String. Location of elements legend.
    loc2 = Takes String. Location of bins legend"""

    if bin_list is None:
        bin_list = []
    handles, labels = ax.get_legend_handles_labels()

    if pumps:

        patch1 = mpatches.Patch(color=pump_color, label="Pumps")
        patch2 = mpatches.Patch(color=base_link_color, label="Pipes")

        handles.extend([patch1, patch2])
    else:
        patch = mpatches.Patch(color=base_link_color, label="Pipes")
    
        handles.extend([patch])
    
    if len(bin_list) != 0:
        if draw_base_legend==True:
            legend = ax.legend(
                handles=handles[len(bin_list) :],
                loc=loc,
                fontsize=font_size,
                labelcolor=font_color,
                frameon=draw_frame,
            )
            legend._legend_box.align = "left"
            ax.add_artist(legend)
        if draw_bins_legend==True:
            legend2 = ax.legend(
                title=title,
                handles=handles[: len(bin_list)],
                loc=loc2,
                fontsize=font_size,
                labelcolor=font_color,
                title_fontsize=legend_title_font_size,
                frameon=draw_frame,
            )
            legend2._legend_box.align = "left"
            plt.setp(legend2.get_title(), color=font_color)
            ax.add_artist(legend2)
    else:
        if draw_base_legend==True:
            legend = ax.legend(
                handles=handles,
                loc=loc,
                fontsize=font_size,
                labelcolor=font_color,
                frameon=False,
            )
            legend._legend_box.align = "left"
            ax.add_artist(legend)
            
    if node_sizes is not None:
        if len(node_sizes) > 1:
            handles_2=[]
            min_size=np.min(node_sizes)
            max_size=np.max(node_sizes)
            marker_sizes=np.linspace(min_size,max_size,element_size_bins)
            print(marker_sizes)
            for size,label in zip(marker_sizes,element_size_legend_labels):
                handles_2.append(Line2D([],
                                         [],
                                         marker='.',
                                         color='w',
                                         markeredgecolor=edge_colors,
                                         markeredgewidth=linewidths,
                                         label=label,
                                         markerfacecolor='k',
                                         markersize=np.sqrt(size)))
            legend3 = ax.legend(
                handles=handles_2,
                title=element_size_legend_title,
                loc=element_size_legend_loc,
                fontsize=font_size,
                title_fontsize=legend_title_font_size,
                labelcolor=font_color,
                frameon=False,
                )
            legend3._legend_box.align = "left"
            ax.add_artist(legend3)
    if link_sizes is not None:
        if len(link_sizes) > 1:
            handles_2=[]
            min_size=np.min(link_sizes)
            max_size=np.max(link_sizes)
            marker_sizes=np.linspace(min_size,max_size,element_size_bins)
            for size, label in zip(marker_sizes,element_size_legend_labels):
                handles_2.append([Line2D([0],
                                         [0],
                                         color='w',
                                         label=label,
                                         markersize=size)])
            legend3 = ax.legend(
                handles_2,
                element_size_legend_labels,
                title=element_size_legend_title,
                loc=element_size_legend_loc,
                fontsize=font_size,
                title_fontsize=legend_title_font_size,
                labelcolor=font_color,
                frameon=False,
                )
            legend3._legend_box.align = "left"
            ax.add_artist(legend3)

def draw_color_bar(ax, g, cmap, color_bar_title=None):
    """Draws Color Bar.
    Arguments:
    g: NetworkX graph of plotted elements.
    cmap: Colormap
    color_bar_title: Takes String. Title of Color Bar."""

    global cbar
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)
    cbar = plt.colorbar(g,cax=cax)
    cbar.set_label(color_bar_title, fontsize=10)


def draw_label(model, ax, labels, x_coords, y_coords, nodes=None, draw_arrow=True,label_font_size=11):

    if nodes is not None:

        for label, node, xCoord, yCoord in zip(labels, nodes, x_coords, y_coords):

            if draw_arrow:
                edge_list = []
                if label == node:
                    pass
                else:
                    model["G"].add_node(label, pos=(xCoord, yCoord))

                    model["pos_dict"][label] = (
                        model["wn"].get_node(node).coordinates[0] + xCoord,
                        model["wn"].get_node(node).coordinates[1] + yCoord,
                    )

                    edge_list.append((node, label))

                    nxp.draw_networkx_edges(
                        model["G"],
                        model["pos_dict"],
                        edgelist=edge_list,
                        edge_color="g",
                        width=0.8,
                        arrows=False,
                    )

                    model["G"].remove_node(label)
                    model["pos_dict"].pop(label, None)
                    edge_list.append((node, label))
            if draw_arrow==True:
                if xCoord < 0:
                    ax.text(
                        model["wn"].get_node(node).coordinates[0] + xCoord,
                        model["wn"].get_node(node).coordinates[1] + yCoord,
                        s=label,
                        bbox=dict(
                            facecolor="mediumaquamarine", alpha=0.9, edgecolor="black"
                        ),
                        horizontalalignment="right",
                        verticalalignment="center",
                        fontsize=label_font_size,
                    )
                if xCoord >= 0:
                    ax.text(
                        model["wn"].get_node(node).coordinates[0] + xCoord,
                        model["wn"].get_node(node).coordinates[1] + yCoord,
                        s=label,
                        bbox=dict(
                            facecolor="mediumaquamarine", alpha=0.9, edgecolor="black"
                        ),
                        horizontalalignment="left",
                        verticalalignment="center",
                        fontsize=label_font_size,
                    )
            else:
                ax.text(
                    model["wn"].get_node(node).coordinates[0] + xCoord,
                    model["wn"].get_node(node).coordinates[1] + yCoord,
                    s=label,
                    bbox=dict(
                        facecolor="mediumaquamarine", alpha=0.9, edgecolor="black"
                    ),
                    horizontalalignment="center",
                    verticalalignment="center",
                    fontsize=label_font_size,
                    )
    elif nodes is None:

        for label, xCoord, yCoord in zip(labels, x_coords, y_coords):

            ax.text(
                xCoord,
                yCoord,
                s=label,
                bbox=dict(facecolor="mediumaquamarine", alpha=0.9, edgecolor="black"),
                horizontalalignment="center",
                fontsize=label_font_size,
                transform=ax.transAxes,
            )
