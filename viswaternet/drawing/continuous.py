"""
The viswaternet.drawing.continuous module handles everything related to continuous data drawing.
"""

import matplotlib.pyplot as plt
from viswaternet.network import processing
from viswaternet.utils import save_fig, unit_conversion, \
    fancyarrowpatch_to_linecollection, label_generator
from viswaternet.drawing import base
from viswaternet.utils.markers import *

default_cmap = 'autumn_r'


def plot_continuous_nodes(
        self,
        ax=None,
        parameter=None,
        element_list=None,
        value=None,
        unit=None,
        vmin=None,
        vmax=None,
        draw_tanks=True,
        draw_reservoirs=True,
        draw_pumps=True,
        draw_valves=True,
        draw_nodes=False,
        draw_links=True,
        cmap=default_cmap,
        color_bar_title=None,
        node_size=100,
        node_shape=".",
        node_border_color=None,
        node_border_width=None,
        draw_base_legend=True,
        base_legend_loc="upper right",
        base_legend_label_font_size=15,
        base_legend_label_color="k",
        draw_legend_frame=False,
        element_size_intervals=None,
        element_size_legend_title=None,
        element_size_legend_loc=None,
        element_size_legend_labels=None,
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
        draw_color_bar=True,
        color_bar_width=0.03,
        color_bar_height=0.8,
        include_tanks=False,
        include_reservoirs=False,
        savefig=False,
        save_name=None,
        dpi='figure',
        save_format='png'):
    
    """User-level function that draws continuous nodal data, base elements, legends, and saves the figure.
    
    Arguments
    ---------
    ax : axes._subplots.AxesSubplot
        Matplotlib axes object.
    
    parameter : string
        The parameter to be plotted. The following is a list of parameters available to use:
        **Static Parameters**    
        - base_demand
        - elevation
        - emitter_coefficient
        - initial_quality
        
        **Time-Dependent Parameters**
        - head
        - demand
        - pressure
        - quality
        - leak_demand
        - leak_area
        - leak_discharg_coeff
    
    element_list : list
        A list of junctions for which the parameter will be plotted. By default, this is the list of all junction names.
    
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
    
    vmin : integer
        The minimum value of the color bar. 
    
    vmax : integer
        The maximum value of the color bar.
    
    draw_tanks : boolean
        Determines if draw_reservoirs with no data associated with them are drawn.
    
    draw_reservoirs : boolean
        Determines if draw_reservoirs with no data associated with them are drawn.
    
    draw_pumps : boolean
        Determines if draw_pumps with no data associated with them are drawn.
    
    draw_valves : boolean
        Determines if draw_valves with no data associated with them are drawn.
    
    cmap : string
        The matplotlib color map to be used for plotting. Refer to matplotlib documentation for possible inputs.
    
    color_bar_title : string
        The title of the color bar.
    
    node_size : integer, array-like
        Integer representing all node sizes, or array of sizes for each node.
    
    node_shape : string
        Shape of the draw_nodes. Refer to matplotlib documentation for available marker types.
    
    node_border_color : string
        Color of the node borders.
    
    node_border_width : integer
        Width of the node borders.
    
    draw_base_legend : boolean
        Determines if the base elements legend will be drawn. 
    
    base_legend_loc : string
        The location of the base elements legend on the figure. Refer to matplotlib documentation for possible inputs.
    
    base_legend_label_font_size : integer
        The font size of the non-title text for the base legend. 
    
    base_legend_label_color : string
        The color of the base legend text. Refer to matplotlib documentation for available colors.
    
    draw_legend_frame : boolean
        Determines if the frame around the base legend is drawn.
    
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
    
    draw_color_bar : boolean
        Determines if color bar is drawn.
    
    color_bar_width : boolean
        Width of color bar.
    
    color_bar_height : boolean
        Height of color bar.
    
    include_tanks : boolean
        Determines if data for draw_tanks are retrieved.
    
    include_reservoirs : boolean
        Determines if data for draw_reservoirs are retrieved.
    
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
        fig, ax = plt.subplots(figsize=self.figsize)
        self.fig = fig
        self.ax = ax
        ax.set_frame_on(self.axis_frame)
    if parameter is not None:
        if not isinstance(value, list):
            parameter_results, node_list = processing.get_parameter(
                self,
                "node",
                parameter,
                value=value,
                element_list=element_list,
                include_tanks=include_tanks,
                include_reservoirs=include_reservoirs)
        else:
            parameter_results = value[0]
            node_list = value[1]
        if unit is not None:
            parameter_results = unit_conversion(
                parameter_results, parameter, unit)
        g = base.draw_nodes(
            self,
            ax,
            node_list,
            parameter_results=parameter_results,
            vmin=vmin,
            vmax=vmax,
            node_size=node_size,
            cmap=cmap,
            node_shape=node_shape,
            node_border_color=node_border_color,
            node_border_width=node_border_width,
            draw_tanks=draw_tanks,
            draw_reservoirs=draw_reservoirs)

        base.draw_base_elements(
            self,
            ax,
            draw_nodes=False,
            draw_reservoirs=draw_reservoirs,
            draw_tanks=draw_tanks,
            draw_valves=draw_valves,
            draw_pumps=draw_pumps,
            include_reservoirs=include_reservoirs,
            include_tanks=include_tanks,
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
            pump_arrows=pump_arrows,
            base_node_color=base_node_color,
            base_node_size=base_node_size,
            base_link_color=base_link_color,
            base_link_width=base_link_width,
            base_link_line_style=base_link_line_style,
            base_link_arrows=base_link_arrows)
        if draw_color_bar is True:
            if color_bar_title is None:
                color_bar_title = label_generator(parameter, value, unit)
            base.draw_color_bar(ax,
                                g,
                                cmap,
                                color_bar_title=color_bar_title,
                                color_bar_width=color_bar_width,
                                color_bar_height=color_bar_height)
    base.draw_legend(ax,
                     draw_pumps=draw_pumps,
                     base_legend_loc=base_legend_loc,
                     base_legend_label_font_size=base_legend_label_font_size,
                     base_legend_label_color=base_legend_label_color,
                     draw_legend_frame=draw_legend_frame,
                     pump_color=pump_color,
                     base_link_color=base_link_color,
                     element_size_intervals=element_size_intervals,
                     element_size_legend_title=element_size_legend_title,
                     element_size_legend_loc=element_size_legend_loc,
                     element_size_legend_labels=element_size_legend_labels,
                     draw_base_legend=draw_base_legend,
                     linewidths=node_border_width,
                     node_border_color=node_border_color,
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


def plot_continuous_links(
        self,
        ax=None,
        parameter=None,
        element_list=None,
        include_pumps=True,
        include_valves=True,
        value=None,
        unit=None,
        link_width=1,
        vmin=None,
        vmax=None,
        link_style='-',
        link_arrows=False,
        draw_tanks=True,
        draw_reservoirs=True,
        draw_pumps=True,
        draw_valves=True,
        draw_nodes=False,
        draw_links=True,
        cmap=default_cmap,
        color_bar_title=None,
        base_legend_loc="upper right",
        savefig=False,
        save_name=None,
        dpi='figure',
        save_format='png',
        base_legend_label_font_size=15,
        base_legend_label_color="k",
        draw_legend_frame=False,
        element_size_intervals=None,
        element_size_legend_title=None,
        element_size_legend_loc=None,
        element_size_legend_labels=None,
        draw_base_legend=True,
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
        draw_color_bar=True,
        color_bar_width=0.03,
        color_bar_height=0.8):
    """User-level function that draws continuous link data, base elements, legends, and saves the figure.
    
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
   
    element_list : list
        A list of links for which the parameter will be plotted. By default, this is the list of all link names.
    
    include_pumps : boolean
        Determines if data for draw_pumps are retreived.
    
    include_valves : boolean
        Determines if data for draw_valves are retrieved
    
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
    
    link_width : integer, array-like
        Integer representing all link widths, or array of widths for each link.
    
    vmin : integer
        The minimum value of the color bar. 
    
    vmax : integer
        The maximum value of the color bar.
    
    link_style : string
        The style (solid, dashed, dotted, etc.) of the draw_links. Refer to matplotlib documentation for available line styles.
    
    link_arrows : boolean
        Determines if an arrow is drawn in the direction of flow of the pump.
    
    draw_reservoirs : boolean
        Determines if draw_reservoirs with no data associated with them are drawn.
    
    draw_tanks : boolean
        Determines if draw_tanks with no data associated with them are drawn.
    
    draw_pumps : boolean
        Determines if draw_pumps with no data associated with them are drawn.
    
    draw_valves : boolean
        Determines if draw_valves with no data associated with them are drawn.
    
    cmap : string
        The matplotlib color map to be used for plotting. Refer to matplotlib documentation for possible inputs.
    
    color_bar_title : string
        The title of the color bar.
    
    base_legend_loc : string
        The location of the base elements legend on the figure. Refer to matplotlib documentation for possible inputs.
    
    base_legend_font_size : integer
        The font size of the non-title text for legends. 
    
    base_legend_label_color : string
        The color of the legend text. Refer to matplotlib documentation for available colors.
    
    draw_legend_frame : boolean
        Determines if the frame around the legend is drawn.
    
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
        Determines if valves are drawn as nodes or links.
    
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
        The style (solid, dashed, dotted, etc.) of the valve line. Refer to matplotlib documentation for available line styles.
    
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
    
    draw_color_bar : boolean
        Determines if color bar is drawn.
    
    color_bar_width : integer
        The width of the color bar.
    
    color_bar_height : integer
        The height of the color bar. 
    
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
        if not isinstance(value, list):
            parameter_results, link_list = processing.get_parameter(
                self,
                "link",
                parameter,
                value=value,
                element_list=element_list,
                include_pumps=include_pumps,
                include_valves=include_valves)
        else:
            parameter_results = value[0]
            link_list = value[1]
        if unit is not None:
            parameter_results = unit_conversion(
                parameter_results, parameter, unit)
        g = base.draw_links(
            self,
            ax,
            link_list,
            parameter_results=parameter_results,
            cmap=cmap,
            link_width=link_width,
            vmin=vmin,
            vmax=vmax,
            link_style=link_style,
            link_arrows=link_arrows,
            pump_element=pump_element,
            draw_pumps=draw_pumps,
            valve_element=valve_element,
            draw_valves=draw_valves)

        base.draw_base_elements(
            self,
            ax,
            draw_nodes=draw_nodes,
            draw_links=draw_links,
            draw_reservoirs=draw_reservoirs,
            draw_tanks=draw_tanks,
            draw_valves=draw_valves,
            draw_pumps=draw_pumps,
            include_pumps=include_pumps,
            include_valves=include_valves,
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
            base_link_arrows=base_link_arrows
        )
        if link_arrows is True:
            g = fancyarrowpatch_to_linecollection(
                g, cmap, vmin, vmax, parameter_results)
        if draw_color_bar is True:
            if color_bar_title is None:
                color_bar_title = label_generator(parameter, value, unit)
            base.draw_color_bar(ax,
                                g,
                                cmap,
                                color_bar_title=color_bar_title,
                                color_bar_width=color_bar_width,
                                color_bar_height=color_bar_height)

    link_list = [name for name in link_list
                 if ((name not in model["G_list_pumps_only"]
                      or pump_element == 'node'
                      or draw_pumps is False
                      or include_pumps is False)
                 and (name not in model["G_list_valves_only"]
                      or valve_element == 'node'
                      or draw_valves is False
                      or include_valves is False)
                 and (name not in link_list))]
    if not link_list:
        draw_links = False
    base.draw_legend(ax,
                     draw_pumps=draw_pumps,
                     base_legend_loc=base_legend_loc,
                     base_legend_label_font_size=base_legend_label_font_size,
                     base_legend_label_color=base_legend_label_color,
                     draw_legend_frame=draw_legend_frame,
                     pump_color=pump_color,
                     base_link_color=base_link_color,
                     element_size_intervals=element_size_intervals,
                     element_size_legend_title=element_size_legend_title,
                     element_size_legend_loc=element_size_legend_loc,
                     element_size_legend_labels=element_size_legend_labels,
                     draw_base_legend=draw_base_legend,
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
