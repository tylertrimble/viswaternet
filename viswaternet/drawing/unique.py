# -*- coding: utf-8 -*-
"""
The viswaternet.drawing.unique module handles custom data, excel data, and unique data drawing.
"""
import matplotlib.pyplot as plt
import pandas as pd
from viswaternet.network import processing
from viswaternet.utils import convert_excel, save_fig, unit_conversion
from viswaternet.drawing import base
from viswaternet.drawing import discrete
from viswaternet.utils.markers import *

default_cmap = 'autumn_r'


def plot_unique_data(
        self,
        ax=None,
        parameter=None,
        parameter_type=None,
        data_type=None,
        data_file=None,
        excel_columns=None,
        custom_data_values=None,
        unit=None,
        intervals="automatic",
        node_size=100,
        node_shape='.',
        num_intervals=5,
        label_list=None,
        node_border_color=None,
        node_border_width=None,
        color_list=None,
        link_width=1,
        vmin=None,
        vmax=None,
        link_style='-',
        link_arrows=False,
        draw_tanks=True,
        draw_reservoirs=True,
        draw_pumps=True,
        draw_valves=True,
        draw_links=True,
        draw_nodes=False,
        cmap=default_cmap,
        draw_base_legend=True,
        legend_title=None,
        base_legend_loc="upper right",
        discrete_legend_loc="lower right",
        savefig=False,
        save_name=None,
        dpi='figure',
        save_format='png',
        color_bar_title=None,
        base_legend_label_font_size=15,
        base_legend_label_color="k",
        discrete_legend_label_font_size=15,
        discrete_legend_label_color="k",
        discrete_legend_title_font_size=17,
        discrete_legend_title_color='k',
        draw_legend_frame=False,
        legend_decimal_places=3,
        element_size_intervals=None,
        element_size_legend_title=None,
        element_size_legend_loc=None,
        element_size_legend_labels=None,
        draw_discrete_legend=True,
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
        disable_interval_deleting=True,
        draw_color_bar=True,
        color_bar_width=0.03,
        color_bar_height=0.8):
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
        
    data_file : string
        
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
    
    num_intervals : integer
         The number of intervals.       
    
    disable_interval_deleting : boolean
        If True, empty intervals will be automatically deleted. 
   
    node_size : integer, array-like
        List of node sizes for each interval.
   
    node_shape : string, array-like
        List of node shapes for each interval. Refer to matplotlib documentation for available marker types.
  
    link_width : integer, array-like
        List of link widths for each interval.
  
    label_list : string, array-like
        List of labels for each interval.
   
    node_border_color : string, array-like
        The color of the node borders for each interval.
   
    node_border_width  : integer, array-like
        The width of the node borders for each interval.
   
    color_list : string, array-like
        The list of node colors for each interval. Both cmap and color_list can not be used at the same time to color draw_nodes. If both are, then color_list
        takes priority. 
    
    cmap : string
        The matplotlib color map to be used for plotting. Refer to matplotlib documentation for possible inputs.
      
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
        Determines if draw_reservoirs with no data associated with them are drawn.
    
    draw_pumps : boolean
        Determines if draw_pumps with no data associated with them are drawn.
    
    draw_valves : boolean
        Determines if draw_valves with no data associated with them are drawn.
    
    draw_links : boolean
        Determines if draw_links with no data associated with them are drawn.
        
    draw_nodes : boolean
        Determines if draw_nodes with no data associated with them are drawn.
    
    draw_base_legend : boolean
        Determines if the base elements legend will be drawn. 
    
    legend_title : string
        Title of the intervals legend.
    
    base_legend_loc : string
        The location of the base elements legend on the figure. Refer to matplotlib documentation for possible inputs.
    
    base_legend_label_font_size : integer
        The font size of the non-title text for the base elements legend. 
    
    base_legend_label_color : string
        The color of the base elements legend text. Refer to matplotlib documentation for 
        available colors.
    
    draw_discrete_legend : boolean
           Determine if the intervals legend is drawn. 
    
    discrete_legend_loc : string
        The location of the intervals legend on the figure.   
    
    discrete_legend_label_font_size : integer
        The font size of the non-title text for the intervals legend. 
    
    discrete_legend_label_color : string
        The color of the intervals legend text. Refer to matplotlib documentation for 
        available colors.    
    
    discrete_legend_title_font_size : integer
        The font size of the title text for the intervals legend.
        
    discrete_legend_title_color : string
        The color of the intervals legend title text.
        
    draw_legend_frame : boolean
        Determines if the frame around the legend is drawn.
    
    legend_decimal_places : integer
        The number of significant figures, or decimal points, that numbers in the legend will be displayed with. 0 should be passed for whole numbers.
   
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
    
    color_bar_title : string
         The title of the color bar.
        
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
        fig, ax = plt.subplots(figsize=self.figsize)
        ax.set_frame_on(self.axis_frame)

    def call_draw_base_elements(element_list=None):
        base.draw_base_elements(self,
                                ax,
                                draw_nodes=draw_nodes,
                                draw_links=draw_links,
                                draw_reservoirs=draw_reservoirs,
                                draw_tanks=draw_tanks,
                                draw_valves=draw_valves,
                                draw_pumps=draw_pumps,
                                element_list=element_list,
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

    def call_draw_legend(intervals=None, element_list=None):
        draw_links = True
        if parameter_type == 'link' \
                or parameter == 'diameter' \
                or parameter == 'roughness':
            link_list = [name for name in element_list
                         if ((name not in model["pump_names"]
                              or pump_element == 'node'
                              or draw_pumps is False)
                         and (name not in model["valve_names"]
                              or valve_element == 'node'
                              or draw_valves is False)
                         and (name not in element_list))]
            if not link_list:
                draw_links = False
        base.draw_legend(
            ax,
            intervals=intervals,
            title=legend_title,
            draw_pumps=draw_pumps,
            base_legend_loc=base_legend_loc,
            discrete_legend_loc=discrete_legend_loc,
            base_legend_label_font_size=base_legend_label_font_size,
            base_legend_label_color=base_legend_label_color,
            discrete_legend_label_font_size=discrete_legend_label_font_size,
            discrete_legend_label_color=discrete_legend_label_color,
            discrete_legend_title_font_size=discrete_legend_title_font_size,
            discrete_legend_title_color=discrete_legend_title_color,
            cmap=cmap,
            color_list=color_list,
            draw_legend_frame=draw_legend_frame,
            pump_color=pump_color,
            base_link_color=base_link_color,
            node_size=node_size,
            link_width=link_width,
            element_size_intervals=element_size_intervals,
            element_size_legend_title=element_size_legend_title,
            element_size_legend_loc=element_size_legend_loc,
            element_size_legend_labels=element_size_legend_labels,
            node_border_color=node_border_color,
            linewidths=node_border_width,
            draw_base_legend=draw_base_legend,
            draw_discrete_legend=draw_discrete_legend,
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

    def call_draw_color_bar():
        base.draw_color_bar(ax,
                            g,
                            cmap,
                            color_bar_title=color_bar_title,
                            color_bar_width=color_bar_width,
                            color_bar_height=color_bar_height)
    if parameter == "demand_patterns":
        demand_pattern_nodes, patterns = processing.get_demand_patterns(self)
        discrete.draw_discrete_nodes(
            self,
            ax,
            demand_pattern_nodes,
            patterns,
            node_size=node_size,
            node_shape=node_shape,
            label_list=label_list,
            node_border_color=node_border_color,
            node_border_width=node_border_width,
            cmap=cmap,
            color_list=color_list)
        call_draw_base_elements(element_list=model['node_names'])
        call_draw_legend(intervals=patterns, element_list=model['node_names'])
        if savefig:
            save_fig(self, save_name=save_name,
                     dpi=dpi, save_format=save_format)
        return
    elif parameter == "diameter" or parameter == "roughness":
        parameter_results, link_list = processing.get_parameter(
            self, "link", parameter)
        link_list = [link_list[link_list.index(name)]
                     for name in link_list
                     if ((name not in model["pump_names"]
                          or pump_element == 'node'
                          or draw_pumps is False)
                     and (name not in model["valve_names"]
                          or valve_element == 'node'
                          or draw_valves is False))]
        parameter_results = parameter_results.loc[link_list]
        parameter_results = parameter_results.values.tolist()
        if unit is not None:
            parameter_results = unit_conversion(
                parameter_results, parameter, unit)
        uniques = sorted(list(set(parameter_results)))
        interval_names = [("{:.{j}f}".format(i, j=legend_decimal_places))
                          for i in uniques]
        interval_results = {}
        for interval_name in interval_names:
            interval_results[interval_name] = {}
        for i, link in enumerate(link_list):
            interval_results["{:.{j}f}".format(
                parameter_results[i],
                j=legend_decimal_places)][link] = \
                model["G_pipe_name_list"].index(link)
        # return interval_results,parameter_results,uniques
        discrete.draw_discrete_links(
            self,
            ax,
            interval_results,
            interval_names,
            link_width=link_width,
            label_list=label_list,
            cmap=cmap,
            color_list=color_list,
            link_style=link_style,
            link_arrows=link_arrows)
        call_draw_base_elements(element_list=link_list)
        call_draw_legend(intervals=interval_names, element_list=link_list)
        if savefig:
            save_fig(self, save_name=save_name,
                     dpi=dpi, save_format=save_format)
        return
    elif parameter == "tag":
        parameter_results, node_list = processing.get_parameter(
            self, "node", parameter)
        uniques = []
        if any(i is not None for i in (parameter_results)):
            uniques = list(set(parameter_results))
        interval_names = uniques
        if not uniques:
            pass
        if None in interval_names:
            interval_names.remove(None)
        interval_names.append('No Tag')
        interval_results = {}
        for interval_name in interval_names:
            interval_results[interval_name] = {}
        for i, node in enumerate(node_list):
            if parameter_results[i] is None:
                interval_results["No Tag"][node] = model["node_names"].index(
                    node)
                continue
            interval_results[parameter_results[i]][node] = model[
                "node_names"
            ].index(node)
        discrete.draw_discrete_nodes(
            self,
            ax,
            interval_results,
            interval_names,
            node_size=node_size,
            node_shape=node_shape,
            label_list=label_list,
            node_border_color=node_border_color,
            node_border_width=node_border_width,
            cmap=cmap,
            color_list=color_list)
        call_draw_base_elements(element_list=model["node_names"])
        call_draw_legend(intervals=interval_names,
                         element_list=model["node_names"])
        if savefig:
            save_fig(self, save_name=save_name,
                     dpi=dpi, save_format=save_format)
        return
    elif parameter == "custom_data":
        if data_type == "unique":
            interval_names = list(sorted(set(custom_data_values[1])))
            interval_results = {}
            for interval in interval_names:
                interval_results[interval] = {}
            if parameter_type == 'node':
                for element, data in zip(
                        custom_data_values[0],
                        custom_data_values[1]):
                    interval_results[data][element] = \
                        model["node_names"].index(element)
                discrete.draw_discrete_nodes(
                    self,
                    ax,
                    interval_results,
                    interval_names,
                    node_size=node_size,
                    node_shape=node_shape,
                    label_list=label_list,
                    node_border_color=node_border_color,
                    node_border_width=node_border_width,
                    cmap=cmap,
                    color_list=color_list)
            elif parameter_type == 'link':
                for element, data in zip(
                        custom_data_values[0],
                        custom_data_values[1]):
                    interval_results[data][element] = \
                        model["G_pipe_name_list"].index(element)
                discrete.draw_discrete_links(
                    self,
                    ax,
                    interval_results,
                    interval_names,
                    link_width=link_width,
                    label_list=label_list,
                    cmap=cmap,
                    color_list=color_list,
                    link_style=link_style,
                    link_arrows=link_arrows)
            call_draw_base_elements(element_list=custom_data_values[0])
            call_draw_legend(intervals=interval_names,
                             element_list=custom_data_values[0])
            if savefig:
                save_fig(self, save_name=save_name,
                         dpi=dpi, save_format=save_format)
            return
        elif data_type == "discrete":
            interval_results, interval_names = processing.bin_parameter(
                self,
                custom_data_values[1],
                custom_data_values[0],
                intervals=intervals,
                num_intervals=num_intervals,
                legend_decimal_places=legend_decimal_places,
                disable_interval_deleting=disable_interval_deleting)
            if parameter_type == "link":
                discrete.draw_discrete_links(
                    self,
                    ax,
                    interval_results,
                    interval_names,
                    link_width=link_width,
                    label_list=label_list,
                    cmap=cmap,
                    color_list=color_list,
                    link_style=link_style,
                    link_arrows=link_arrows)
                call_draw_base_elements(element_list=custom_data_values[0])
                call_draw_legend(element_list=custom_data_values[0],
                                 intervals=interval_names)
            elif parameter_type == "node":
                discrete.draw_discrete_nodes(
                    self,
                    ax,
                    interval_results,
                    interval_names,
                    node_size=node_size,
                    node_shape=node_shape,
                    label_list=label_list,
                    node_border_color=node_border_color,
                    node_border_width=node_border_width,
                    cmap=cmap,
                    color_list=color_list)
                call_draw_base_elements(element_list=custom_data_values[0])
                call_draw_legend(intervals=interval_names,
                                 element_list=custom_data_values[0])
            if savefig:
                save_fig(self, save_name=save_name,
                         dpi=dpi, save_format=save_format)
            return
        elif data_type == "continuous":
            if parameter_type == "link":
                if isinstance(custom_data_values[1], list):
                    parameter_results = pd.Series(custom_data_values[1],
                                                  custom_data_values[0])
                else:
                    parameter_results = custom_data_values[1]
                g = base.draw_links(
                    self,
                    ax,
                    custom_data_values[0],
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
                call_draw_base_elements(element_list=custom_data_values[0])
                call_draw_legend(element_list=custom_data_values[0])
            elif parameter_type == "node":
                if isinstance(custom_data_values[1], list):
                    parameter_results = pd.Series(custom_data_values[1],
                                                  custom_data_values[0])
                else:
                    parameter_results = custom_data_values[1]
                g = base.draw_nodes(
                    self,
                    ax,
                    custom_data_values[0],
                    parameter_results=parameter_results,
                    node_size=node_size,
                    cmap=cmap,
                    vmin=vmin,
                    vmax=vmax,
                    node_shape=node_shape,
                    node_border_width=node_border_width,
                    node_border_color=node_border_color,
                    draw_tanks=draw_tanks,
                    draw_reservoirs=draw_reservoirs)
                call_draw_base_elements(element_list=custom_data_values[0])
                call_draw_legend(element_list=custom_data_values[0])
            if draw_color_bar is True:
                call_draw_color_bar()
            if savefig:
                save_fig(self, save_name=save_name,
                         dpi=dpi, save_format=save_format)
            return
    elif parameter == 'excel_data':
        if data_type == "unique":
            interval_results, intervals = convert_excel(
                self,
                data_file,
                parameter_type,
                data_type,
                excel_columns[0],
                excel_columns[1])
            element_list, results = convert_excel(
                self,
                data_file,
                parameter_type,
                'discrete',
                excel_columns[0],
                excel_columns[1])
            if parameter_type == "link":
                discrete.draw_discrete_links(
                    self,
                    ax,
                    interval_results,
                    intervals,
                    link_width=link_width,
                    label_list=label_list,
                    cmap=cmap,
                    color_list=color_list,
                    link_style=link_style,
                    link_arrows=link_arrows)
                call_draw_base_elements(element_list=element_list)
                call_draw_legend(element_list=element_list,
                                 intervals=intervals)
            elif parameter_type == "node":
                discrete.draw_discrete_nodes(
                    self,
                    ax,
                    interval_results,
                    intervals,
                    node_size=node_size,
                    node_shape=node_shape,
                    label_list=label_list,
                    node_border_color=node_border_color,
                    node_border_width=node_border_width,
                    cmap=cmap,
                    color_list=color_list)
                call_draw_base_elements(element_list=element_list)
                call_draw_legend(intervals=intervals,
                                 element_list=element_list)
            if savefig:
                save_fig(self, save_name=save_name,
                         dpi=dpi, save_format=save_format)
            return
        if data_type == "discrete":
            element_list, results = convert_excel(
                self,
                data_file,
                parameter_type,
                data_type,
                excel_columns[0],
                excel_columns[1])
            results = results.values.tolist()
            interval_results, interval_names = processing.bin_parameter(
                self,
                results,
                element_list,
                intervals=intervals,
                num_intervals=num_intervals,
                legend_decimal_places=legend_decimal_places,
                disable_interval_deleting=disable_interval_deleting)
            if parameter_type == "link":
                discrete.draw_discrete_links(
                    self,
                    ax,
                    interval_results,
                    interval_names,
                    link_width=link_width,
                    label_list=label_list,
                    cmap=cmap,
                    color_list=color_list,
                    link_style=link_style,
                    link_arrows=link_arrows)
                call_draw_base_elements(element_list=element_list)
                call_draw_legend(element_list=element_list,
                                 intervals=interval_names)
            if parameter_type == "node":
                discrete.draw_discrete_nodes(
                    self,
                    ax,
                    interval_results,
                    interval_names,
                    node_size=node_size,
                    node_shape=node_shape,
                    label_list=label_list,
                    node_border_color=node_border_color,
                    node_border_width=node_border_width,
                    cmap=cmap,
                    color_list=color_list)
                call_draw_base_elements(element_list=element_list)
                call_draw_legend(intervals=interval_names,
                                 element_list=element_list)
            if savefig:
                save_fig(self, save_name=save_name,
                         dpi=dpi, save_format=save_format)
            return
        if data_type == "continuous":
            element_list, results = convert_excel(
                self,
                data_file,
                parameter_type,
                data_type,
                excel_columns[0],
                excel_columns[1])
            if parameter_type == "link":
                g = base.draw_links(
                    self,
                    ax,
                    element_list,
                    results,
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
                call_draw_base_elements(element_list=element_list)
                call_draw_legend(element_list=element_list)
            elif parameter_type == "node":
                g = base.draw_nodes(
                    self,
                    ax,
                    element_list,
                    results,
                    node_size=node_size,
                    cmap=cmap,
                    vmin=vmin,
                    vmax=vmax,
                    node_shape=node_shape,
                    node_border_width=node_border_width,
                    node_border_color=node_border_color,
                    draw_tanks=draw_tanks,
                    draw_reservoirs=draw_reservoirs)
                call_draw_base_elements(element_list=element_list)
                call_draw_legend(element_list=element_list)
            if draw_color_bar is True:
                call_draw_color_bar()
            if savefig:
                save_fig(self, save_name=save_name,
                         dpi=dpi, save_format=save_format)
        return
    elif isinstance(parameter, str):
        pass
    else:
        raise Exception("Invalid input, check docs for valid inputs.")
