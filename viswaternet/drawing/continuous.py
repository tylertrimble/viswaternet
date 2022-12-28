# -*- coding: utf-8 -*-
"""
Created on Sun Oct  2 21:05:57 2022

@author: Tyler
"""
import numpy as np
import matplotlib as mpl
import networkx.drawing.nx_pylab as nxp
from viswaternet.network import processing
from viswaternet.utils import save_fig, normalize_parameter, unit_conversion
from viswaternet.drawing import base


default_cmap = mpl.cm.get_cmap("autumn_r")


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
    edge_colors="k",
    line_widths=0,
    label=None,
):
    """Draws continuous nodal data onto the figure.
    
    Arguments
    ---------
    ax : axes._subplots.AxesSubplot
        Matplotlib axes object.
    
    node_list : string, array-like
        List of nodes to be drawn.
        
    parameter_results : array-like
        The data associated with each node.
        
    vmin : integer
        The minimum value of the color bar. 
        
    vmax : integer
        The maximum value of the color bar.
        
    node_size : integer, array-like
        Integer representing all node sizes, or array of sizes for each node.
        
    node_color : string
        Color of the nodes.

    cmap : string
        The matplotlib color map to be used for plotting. Refer to matplotlib
        documentation for possible inputs.
        
    node_shape : string
        Shape of the nodes. Refer to matplotlib documentation for available 
        marker types.
        
    edge_colors : string
        Color of the node borders.
        
    line_widths : integer
        Width of the node borders.
        
    label : string
        Matplotlib label of plotting instance.
    """
    model=self.model
    if parameter_results is None:
        parameter_results = []
    if node_size is None:
        node_size = []
    if len(parameter_results) != 0:

        negativeValues = False
    if isinstance(node_size, list) and len(node_size) == 0:

        node_size = np.ones(len(node_list)) * 100
    if isinstance(node_size, int):
        node_size = np.ones(len(node_list)) * node_size
    if len(parameter_results) != 0:
        for value in parameter_results:

            if value < -1e-5:

                negativeValues = True

                cmap = mpl.cm.get_cmap(cmap)

                if vmin is None and vmax is None:
                    g = nxp.draw_networkx_nodes(
                        model["G"],
                        model["pos_dict"],
                        ax=ax,
                        nodelist=node_list,
                        node_size=node_size,
                        node_color=parameter_results,
                        vmax=np.max(parameter_results),
                        vmin=-np.max(parameter_results),
                        cmap=cmap,
                        node_shape=node_shape,
                        linewidths=line_widths,
                        edgecolors=edge_colors,
                        label=label,
                    )
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
                        linewidths=line_widths,
                        edgecolors=edge_colors,
                        label=label,
                    )
                return g
        if negativeValues:
            pass
        else:
            cmap = mpl.cm.get_cmap(cmap)

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
                    linewidths=line_widths,
                    edgecolors=edge_colors,
                )
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
                    linewidths=line_widths,
                    edgecolors=edge_colors,
                    vmin=vmin,
                    vmax=vmax,
                )
            return g
    else:

        nxp.draw_networkx_nodes(
            model["G"],
            model["pos_dict"],
            ax=ax,
            nodelist=node_list,
            node_size=node_size,
            node_color=node_color,
            node_shape=node_shape,
            edgecolors=edge_colors,
            linewidths=line_widths,
            label=label,
        )


def draw_links(
    self,
    ax,
    link_list,
    parameter_results=None,
    edge_color="k",
    cmap="tab10",
    widths=None,
    vmin=None,
    vmax=None,
    link_style='-',
    link_arrows=False
):
    """Draws continuous link data onto the figure.
    
    Arguments
    ---------
    ax : axes._subplots.AxesSubplot
        Matplotlib axes object.
    
    link_list : string, array-like
        List of links to be drawn.
        
    parameter_results : array-like
        The data associated with each node.
    
    edge_colors : string
        Color of links.
        
    cmap : string
        The matplotlib color map to be used for plotting. Refer to matplotlib
        documentation for possible inputs.
        
    widths : integer, array-like
        Integer representing all link widrths, or array of widths for each link.
        
    vmin : integer
        The minimum value of the color bar. 
        
    vmax : integer
        The maximum value of the color bar.
    
    link_style : string
        The style (solid, dashed, dotted, etc.) of the links. Refer to 
        matplotlib documentation for available line styles.
        
    link_arrows : boolean
        Determines if an arrow is drawn in the direction of flow of the pump.
    """
    model=self.model
    if parameter_results is None:
        parameter_results = []
    if widths is None:
        widths = []
    
    if isinstance(widths, list) and len(widths) == 0:

        widths = np.ones(len(widths)) * 100
        
    if isinstance(widths, int):
        widths = np.ones(len(link_list)) * widths
        
    edgeList = {}

    if len(widths) == 0:

        widths = np.ones(len(link_list)) * 1
    negativeValues = False

    if len(parameter_results) != 0:
        for i in link_list:
            edgeList[i] = model["G_pipe_name_list"].index(i)
        for value in parameter_results:

            if value < -1e-5:

                negativeValues = True

                cmap = mpl.cm.get_cmap(cmap)

                if vmin is None and vmax is None:
                    g = nxp.draw_networkx_edges(
                        model["G"],
                        model["pos_dict"],
                        ax=ax,
                        edgelist=([model["pipe_list"][i] for i in edgeList.values()]),
                        edge_color=parameter_results,
                        edge_vmax=np.max(parameter_results),
                        edge_vmin=-np.max(parameter_results),
                        edge_cmap=cmap,
                        style=link_style,
                        arrows=link_arrows,
                        width=widths,
                    )
                else:
                    g = nxp.draw_networkx_edges(
                        model["G"],
                        model["pos_dict"],
                        ax=ax,
                        edgelist=([model["pipe_list"][i] for i in edgeList.values()]),
                        edge_color=parameter_results,
                        edge_vmax=vmax,
                        edge_vmin=vmin,
                        edge_cmap=cmap,
                        style=link_style,
                        arrows=link_arrows,
                        width=widths,
                    )
                return g
        if negativeValues:
            pass
        else:
            cmap = mpl.cm.get_cmap(cmap)

            if vmin is None and vmax is None:
                g = nxp.draw_networkx_edges(
                    model["G"],
                    model["pos_dict"],
                    ax=ax,
                    edgelist=([model["pipe_list"][i] for i in edgeList.values()]),
                    edge_color=parameter_results,
                    edge_cmap=cmap,
                    style=link_style,
                    arrows=link_arrows,
                    width=widths,
                )
            else:
                g = nxp.draw_networkx_edges(
                    model["G"],
                    model["pos_dict"],
                    ax=ax,
                    edgelist=([model["pipe_list"][i] for i in edgeList.values()]),
                    edge_color=parameter_results,
                    edge_cmap=cmap,
                    style=link_style,
                    arrows=link_arrows,
                    width=widths,
                    edge_vmin=vmin,
                    edge_vmax=vmax
                )
            return g
    else:
        for i in link_list:
            edgeList[i] = model["G_pipe_name_list"].index(i)
        nxp.draw_networkx_edges(
            model["G"],
            model["pos_dict"],
            ax=ax,
            edgelist=([model["pipe_list"][i] for i in edgeList.values()]),
            edge_color=edge_color,
            style=link_style,
            arrows=link_arrows,
            width=widths,
        )


def plot_continuous_nodes(
    self,
    ax,
    parameter=None,
    element_list=None,
    value=None,
    unit=None,
    vmin=None,
    vmax=None,
    get_tanks=False,
    get_reservoirs=False,
    tanks=True,
    reservoirs=True,
    pumps=True,
    valves=True,
    cmap=default_cmap,
    color_bar_title=None,
    node_size=100,
    min_size=100,
    max_size=100,
    node_shape=".",
    edge_colors=None,
    line_widths=None,
    legend=True,
    legend_loc="upper right",
    savefig=True,
    save_name=None,
    dpi='figure',
    save_format='png',
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
    draw_color_bar=True,
):
    """User-level function that draws continuous nodal data, base elements,
    legends, and saves the figure.
    
    Arguments
    ---------
    ax : axes._subplots.AxesSubplot
        Matplotlib axes object.
        
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
            :attr:'int'         Plots element data for specified timestep
            :attr:'min'         Plots minimum data point for each element
            :attr:'max'         Plots maximum data point for each element
            :attr:'mean'        Plots mean for each element
            :attr:'stddev'      Plots standard deviation for each element
            :attr:'range'       Plots range for each element
        ======================= =========================================
    
    unit : string
        The unit that the network data is to be converted to.
    
    vmin : integer
        The minimum value of the color bar. 
        
    vmax : integer
        The maximum value of the color bar.
        
    element_list : array-like
        List of network elements that data will be retrieved for.
    
    get_tanks : boolean
        Determines if data for tanks are retrieved.
        
    get_reservoirs : boolean
        Determines if data for reservoirs are retrieved.
     
    reservoirs : boolean
        Determines if reservoirs with no data associated with them are drawn.
    
    tanks : boolean
        Determines if reservoirs with no data associated with them are drawn.
        
    pumps : boolean
        Determines if pumps with no data associated with them are drawn.
        
    valves : boolean
        Determines if valves with no data associated with them are drawn.
    
    cmap : string
        The matplotlib color map to be used for plotting. Refer to matplotlib
        documentation for possible inputs.
    
    color_bar_title : string
        The title of the color bar.
    
    node_size : integer, array-like
        Integer representing all node sizes, or array of sizes for each node.
    
    min_size : integer
        Minimum size of nodes to be used with normalize_parameter.
        
    max_size : integer
        Maximum size of nodes to be used with normalize_parameter.
        
    node_shape : string
        Shape of the nodes. Refer to matplotlib documentation for available 
        marker types.
        
    edge_colors : string
        Color of the node borders.
        
    line_widths : integer
        Width of the node borders.
        
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
        
    legend : boolean
        Determines if the base elements legend will be drawn. 

    legend_loc : string
        The location of the base elements legend on the figure. Refer to matplotlib
        documentation for possible inputs.

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
        The number of significant figures, or decimal points, that numbers in the
        legend will be displayed with. 0 should be passed for whole numbers.
     
    element_size_intervals : integer
        The number of intervals to be used if an element size legend is used.
     
    element_size_legend_title : string
        The title of the element size legend.
     
    element_size_legend_loc : string
        The location of the element size legend on the figure.
         
    element_size_legend_labels : array-like
        The labels of each interval of the element size legend.
        
    reservoir_size : integer
        The size of the reservoir marker on the plot in points^2. 
        
    reservoir_color : string
        The color of the reservoir marker.
        
    reservoir_shape : string
        The shape of the reservoir marker. Refer to matplotlib documentation for
        available marker types.
        
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
        The style (solid, dashed, dotted, etc.) of the pump line. Refer to 
        matplotlib documentation for available line styles.
        
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
        The style (solid, dashed, dotted, etc) of the links with no data associated
        with them.
        
    base_link_arrows : boolean
        Determines if an arrow is drawn in the direction of flow of the links
        with no data associated with them.
        
    draw_color_bar : boolean
        Determines if color bar is drawn.
    """
    if parameter is not None:

        parameter_results, node_list = processing.get_parameter(
            self,
            "node",
            parameter,
            value=value,
            element_list=element_list,
            tanks=get_tanks,
            reservoirs=get_reservoirs,
        )

        if unit is not None:
            parameter_results = unit_conversion(parameter_results, parameter, unit)
        if min_size is not None and max_size is not None:
            normalized_parameter = normalize_parameter(
                parameter_results, min_size, max_size
            )

            node_size = normalized_parameter
            
        g = draw_nodes(
            self,
            ax,
            node_list,
            parameter_results=parameter_results,
            vmin=vmin,
            vmax=vmax,
            node_size=node_size,
            cmap=cmap,
            node_shape=node_shape,
            edge_colors=edge_colors,
            line_widths=line_widths,
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
        if draw_color_bar == True:
            base.draw_color_bar(ax, g, cmap, color_bar_title=color_bar_title)
    if legend:

        base.draw_legend(ax,
                         pumps=pumps, 
                         loc=legend_loc,
                         font_size=font_size,
                         font_color=font_color,
                         legend_title_font_size=legend_title_font_size,
                         draw_frame=draw_frame,
                         pump_color=pump_color,
                         base_link_color=base_link_color,
                         node_sizes=node_size,
                         element_size_intervals=element_size_intervals,
                         element_size_legend_title=element_size_legend_title,
                         element_size_legend_loc=element_size_legend_loc,
                         element_size_legend_labels=element_size_legend_labels,
                         draw_base_legend= draw_base_legend,
                         linewidths=line_widths,
                         edge_colors=edge_colors,
                         )
    if savefig:

        save_fig(self, save_name=save_name,dpi=dpi,save_format=save_format)


def plot_continuous_links(
    self,
    ax,
    parameter=None,
    element_list=None,
    value=None,
    unit=None,
    widths=1,
    min_width=1,
    max_width=1,
    vmin=None,
    vmax=None,
    link_style='-',
    link_arrows=False,
    tanks=True,
    reservoirs=True,
    pumps=True,
    valves=True,
    cmap=default_cmap,
    color_bar_title=None,
    legend=True,
    legend_loc="upper right",
    savefig=True,
    save_name=None,
    dpi='figure',
    save_format='png',
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
    draw_color_bar=True,
):
    """User-level function that draws continuous link data, base elements,
    legends, and saves the figure.
    
    Arguments
    ---------
    ax : axes._subplots.AxesSubplot
        Matplotlib axes object.
        
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
        For time-varying parameters only. Specifies which timestep or data
        summary will be plotted.
        
        .. rubric:: Possible Inputs
        
        ======================= =========================================
            :attr:'int'         Plots element data for specified timestep
            :attr:'min'         Plots minimum data point for each element
            :attr:'max'         Plots maximum data point for each element
            :attr:'mean'        Plots mean for each element
            :attr:'stddev'      Plots standard deviation for each element
            :attr:'range'       Plots range for each element
        ======================= =========================================
    
    unit : string
        The unit that the network data is to be converted to.
        
    widths : integer, array-like
        Integer representing all link widrths, or array of widths for each link.
     
    min_width : integer
        Minimum size of links to be used with normalize_parameter.
        
    max_width : integer
        Maximum size of links to be used with normalize_parameter.
        
    vmin : integer
        The minimum value of the color bar. 
        
    vmax : integer
        The maximum value of the color bar.
     
    link_style : string
        The style (solid, dashed, dotted, etc.) of the links. Refer to 
        matplotlib documentation for available line styles.
        
    link_arrows : boolean
        Determines if an arrow is drawn in the direction of flow of the pump.
        
    element_list : array-like
        List of network elements that data will be retrieved for.
    
    get_tanks : boolean
        Determines if data for tanks are retrieved.
        
    get_reservoirs : boolean
        Determines if data for reservoirs are retrieved.
     
    reservoirs : boolean
        Determines if reservoirs with no data associated with them are drawn.
    
    tanks : boolean
        Determines if reservoirs with no data associated with them are drawn.
        
    pumps : boolean
        Determines if pumps with no data associated with them are drawn.
        
    valves : boolean
        Determines if valves with no data associated with them are drawn.
    
    cmap : string
        The matplotlib color map to be used for plotting. Refer to matplotlib
        documentation for possible inputs.
    
    color_bar_title : string
        The title of the color bar.
        
    node_shape : string
        Shape of the nodes. Refer to matplotlib documentation for available 
        marker types.
        
    edge_colors : string
        Color of the node borders.
        
    line_widths : integer
        Width of the node borders.
        
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
        
    legend : boolean
        Determines if the base elements legend will be drawn. 

    legend_loc : string
        The location of the base elements legend on the figure. Refer to matplotlib
        documentation for possible inputs.

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
        The number of significant figures, or decimal points, that numbers in the
        legend will be displayed with. 0 should be passed for whole numbers.
     
    element_size_intervals : integer
        The number of intervals to be used if an element size legend is used.
     
    element_size_legend_title : string
        The title of the element size legend.
     
    element_size_legend_loc : string
        The location of the element size legend on the figure.
         
    element_size_legend_labels : array-like
        The labels of each interval of the element size legend.
        
    reservoir_size : integer
        The size of the reservoir marker on the plot in points^2. 
        
    reservoir_color : string
        The color of the reservoir marker.
        
    reservoir_shape : string
        The shape of the reservoir marker. Refer to matplotlib documentation for
        available marker types.
        
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
        The style (solid, dashed, dotted, etc.) of the pump line. Refer to 
        matplotlib documentation for available line styles.
        
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
        The style (solid, dashed, dotted, etc) of the links with no data associated
        with them.
        
    base_link_arrows : boolean
        Determines if an arrow is drawn in the direction of flow of the links
        with no data associated with them.
        
    draw_color_bar : boolean
        Determines if color bar is drawn.
    """
    if parameter is not None:

        parameter_results, link_list = processing.get_parameter(
            self, "link", parameter, value=value,element_list=element_list
        )

        if unit is not None:
            parameter_results = unit_conversion(parameter_results, parameter, unit)
        normalized_parameter = normalize_parameter(
            parameter_results, min_width, max_width
        )

        widths = normalized_parameter

        g = draw_links(
            self,
            ax,
            link_list,
            parameter_results=parameter_results,
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
        if draw_color_bar == True:
            base.draw_color_bar(ax, g, cmap, color_bar_title=color_bar_title)
        
    if legend:

        base.draw_legend(ax, 
                         pumps=pumps, 
                         loc=legend_loc,
                         font_size=font_size,
                         font_color=font_color,
                         legend_title_font_size=legend_title_font_size,
                         draw_frame=draw_frame,
                         pump_color=pump_color,
                         base_link_color=base_link_color,
                         link_sizes=widths,
                         element_size_intervals=element_size_intervals,
                         element_size_legend_title=element_size_legend_title,
                         element_size_legend_loc=element_size_legend_loc,
                         element_size_legend_labels=element_size_legend_labels,
                         draw_base_legend= draw_base_legend,
                         )
    if savefig:

        save_fig(self, save_name=save_name,dpi=dpi,save_format=save_format)
