"""
The viswaternet.utils.base module contains plotting functions that are 
frequently utilized by other plotting functions. This includes base element
drawing, legend drawing, color map, and label drawing functions.
"""
import numpy as np
import networkx.drawing.nx_pylab as nxp
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib as mpl
from matplotlib.lines import Line2D


from viswaternet.utils import save_fig

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
def draw_base_elements(
    self,
    ax,
    nodes=True,
    links=True,
    reservoirs=True,
    tanks=True,
    pumps=True,
    valves=True,
    legend=True,
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
):
    """
    Draws base elements (nodes, links, reservoirs, tanks, pumps, and valves)
    without any data associated with the elements.
    
    Arguments
    ---------
    ax : axes._subplots.AxesSubplot
        Matplotlib axes object.
    
    nodes : boolean
        Determines if base nodes with no data associated with them are drawn.
        Set to False for all functions excep plot_basic_elements by default.
    
    links : boolean
        Determines if base links with no data associated with them are drawn.
        Set to False for all functions that deal with link data plotting.
        
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
    
    reservoir_size : integer
        The size of the reservoir marker on the plot in points^2. 
        
    reservoir_color : string
        The color of the reservoir marker. Refer to matplotlib documentation for 
        available colors.
        
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
    """
    model=self.model
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
            edgelist=[i for i in model["pipe_list"] if i not in model["G_list_pumps_only"]],
            ax=ax,
            edge_color=base_link_color,
            width=base_link_width,
            style=base_link_line_style,
            arrows=base_link_arrows,
        )
    if pumps:

        nxp.draw_networkx_edges(
            model["G"],
            model["pos_dict"],
            ax=ax,
            edgelist=model["G_list_pumps_only"],
            edge_color=pump_color,
            width=pump_width,
            style=pump_line_style,
            arrows=pump_arrows
        )


def plot_basic_elements(
    self,
    ax,
    nodes=True,
    links=True,
    reservoirs=True,
    tanks=True,
    pumps=True,
    valves=True,
    savefig=True,
    save_name=None,
    dpi='figure',
    save_format='png',
    legend=True,
    legend_loc="upper right",
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
):
    """User-level function that draws base elements with no data assocaited with
    them, draws a legend, and saves the figure.
    
    Arguments
    ---------
    ax : axes._subplots.AxesSubplot
        Matplotlib axes object.
        
    nodes : boolean
        Determines if base nodes with no data associated with them are drawn.
        Set to False for all functions excep plot_basic_elements by default.
    
    links : boolean
        Determines if base links with no data associated with them are drawn.
        Set to False for all functions that deal with link data plotting.
        
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
        
    legend : boolean
        Determines if the base elements legend will be drawn. 
         
    legend_loc_1 : string
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
    """
    
    draw_base_elements(
        self,
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

        save_fig(self, save_name=save_name,dpi=dpi,save_format=save_format)


def draw_legend(
    ax,
    intervals=None,
    title=None,
    pumps=True,
    loc="upper right",
    loc2="lower right",
    font_size=15,
    font_color="k",
    legend_title_font_size=17,
    draw_frame=False,
    pump_color='b',
    base_link_color='k',
    node_sizes=None,
    link_sizes=None,
    element_size_intervals=None,
    element_size_legend_title=None,
    element_size_legend_loc=None,
    element_size_legend_labels=None,
    draw_base_legend=True,
    draw_intervals_legend=True,
    edge_colors='k',
    linewidths=1
):
    """Draws the legends for all other plotting functions. There are two legends
    that might be drawn. One is the base elements legend with displays what markers
    are associated with each element type (nodes, links, etc.) The other legend
    is the intervals legend which is the legend for discrete drawing.
    
    Under normal use, draw_legends is not normally called by the user directly,
    even with more advanced applications. However, some specialized plots may 
    require draw_legend to be called directly.
    
    Arguments
    ---------
    ax : axes._subplots.AxesSubplot
        Matplotlib axes object.
        
    intervals : array-like, string
        If set to 'automatic' then intervals are created automatically on a 
        equal interval basis. Otherwise, it is the edges of the intervals to be
        created. intervals array length should be num_intervals + 1.
    
    title : string
        The title text of the legend.
        
    loc : string
        The location of the base elements legend on the figure. Refer to matplotlib
        documentation for possible inputs.
        
    loc2 : string
        The location of the intervals legend on the figure.
        
    font_size : integer
        The font size of the non-title text for legends. 
        
    font_color : string
        The color of the legend text. Refer to matplotlib documentation for 
        available colors.
        
    legend_title_font_size : integer
        The font size of the title text for legends.
        
    draw_frame : boolean
        Determines if the frame around the legend is drawn.
    
    pump_color : string
        The color of the pump line.
    
    base_link_color : string
        The color of the links without data associated with them.
    
    node_sizes : integer, array-like
        The size of the node elements. Can either be an integer if the node
        sizes are uniform, or an array-like if variable node sizes are present.
        
    link_sizes : integer, array-like
        The size of the link elements. Can either be an integer if the link
        sizes are uniform, or an array-like if variable link sizes are present.
        
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
        
    edge_colors : string
        The color of the legend nodes edges when plotting element size legend.
        
    linewidths: integer
        The width of the line of the legend nodes when plotting element size legend.
    """
    if intervals is None:
        intervals = []
    handles, labels = ax.get_legend_handles_labels()

    if pumps:

        patch1 = mpatches.Patch(color=pump_color, label="Pumps")
        patch2 = mpatches.Patch(color=base_link_color, label="Pipes")

        handles.extend([patch1, patch2])
    else:
        patch = mpatches.Patch(color=base_link_color, label="Pipes")
    
        handles.extend([patch])
    
    if len(intervals) != 0:
        if draw_base_legend==True:
            legend = ax.legend(
                handles=handles[len(intervals) :],
                loc=loc,
                fontsize=font_size,
                labelcolor=font_color,
                frameon=draw_frame,
            )
            legend._legend_box.align = "left"
            ax.add_artist(legend)
        if draw_intervals_legend==True:
            legend2 = ax.legend(
                title=title,
                handles=handles[: len(intervals)],
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
        if isinstance(node_sizes,list):
            handles_2=[]
            min_size=np.min(node_sizes)
            max_size=np.max(node_sizes)
            marker_sizes=np.linspace(min_size,max_size,element_size_intervals)
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
        if isinstance(link_sizes,list):
            handles_2=[]
            min_size=np.min(link_sizes)
            max_size=np.max(link_sizes)
            marker_sizes=np.linspace(min_size,max_size,element_size_intervals)
            print(marker_sizes)
            for size,label in zip(marker_sizes,element_size_legend_labels):
                handles_2.append(Line2D([],
                                         [],
                                         marker=None,
                                         color='k',
                                         linewidth=size,
                                         label=label))
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

def draw_color_bar(ax, g, cmap, color_bar_title=None):
    """Draws the color bar for all continuous plotting functions.
    
    Like draw_legends, under normal use, draw_color_bar is not normally called 
    by the user directly, even with more advanced applications. However, some 
    specialized plots may require draw_color_bar to be called directly.
    
    Arguments
    ---------
    ax : axes._subplots.AxesSubplot
        Matplotlib axes object.
    
    g : NetworkX path collection
        The list of elements drawn by NetworkX function.
        
    cmap : string
        The matplotlib color map to be used for plotting. Refer to matplotlib
        documentation for possible inputs.
        
    color_bar_title : string
        The title of the color bar.
    """
    global cbar
    fig=plt.gcf()
    ax.set_aspect('auto')
    cax = fig.add_axes([0.9,0.2, 0.03, 0.6])
    cbar = plt.colorbar(g,cax=cax)
    cbar.set_label(color_bar_title, fontsize=10)
    
def draw_label(self, ax, labels, x_coords, y_coords, nodes=None, draw_arrow=True,label_font_size=11):
    """Draws customizable labels on the figure.
    
    There are two modes of coordinate input:
    If the 'nodes' argument is not specified, then the label coordinates are 
    processed as absolute coordinates with possible values from 0 to 1. For 
    instance, (0,0) would place the label in the bottom left of the figure, 
    while (1,1) would place the label in the top right of the figure.
    
    If the 'nodes' argument IS specified, then the coordinates are processed
    as coordinates relative to it's associated node. The scale of the coordinates
    scaling differs between networks. For instance, (50,100) would place the 
    label 50 units to the right, and 100 units above the associated node.

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
        
    nodes : string, array-like
        A list of the nodes the labels are to be associated with.
        
    draw_arrow : boolean
        Determine if an arrow is drawn from the associated nodes to labels.
        
    label_font_size : integer
        The font size of the labels.
    """
    model=self.model
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
