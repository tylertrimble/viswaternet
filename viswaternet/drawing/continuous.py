"""
The viswaternet.drawing.continuous module handles everything related to continuous data drawing.
"""

import matplotlib.pyplot as plt
from viswaternet.network import processing
from viswaternet.utils import save_fig, unit_conversion, \
    fancyarrowpatch_to_linecollection, label_generator
from viswaternet.drawing import base


def plot_continuous_nodes(
        self,
        ax=None,
        parameter=None,
        element_list=None,
        include_tanks=False,
        include_reservoirs=False,
        value=None,
        unit=None,
        vmin=None,
        vmax=None,
        draw_nodes=False,
        element_size_intervals=None,
        element_size_legend_title=None,
        element_size_legend_loc=None,
        element_size_legend_labels=None,
        color_bar_title=None,
        savefig=False,
        save_name=None,
        style=None):
    
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
    
    include_tanks : boolean
        Determines if data for draw_tanks are retrieved.
    
    include_reservoirs : boolean
        Determines if data for draw_reservoirs are retrieved.
    
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
    
    element_size_intervals : integer
        The number of intervals to be used if an element size legend is used.
    
    element_size_legend_title : string
        The title of the element size legend.
    
    element_size_legend_loc : string
        The location of the element size legend on the figure.
    
    element_size_legend_labels : array-like
        The labels of each interval of the element size legend.
        
    color_bar_title : string
         The title of the color bar.
         
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
    """
    if style is None:
        style = self.default_style
    args = style.args
    draw_color_bar = args['draw_color_bar']
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
            style=style)

        base.draw_base_elements(
            self,
            ax,
            element_list=node_list,
            style=style)
        if draw_color_bar is True:
            if color_bar_title is None:
                color_bar_title = label_generator(parameter, value, unit)
            base.draw_color_bar(self,
                                ax,
                                g,
                                color_bar_title=color_bar_title,
                                style=style)
    base.draw_legend(self,
                     ax,
                     element_size_intervals=element_size_intervals,
                     element_size_legend_title=element_size_legend_title,
                     element_size_legend_loc=element_size_legend_loc,
                     element_size_legend_labels=element_size_legend_labels,
                     style=style)
    if savefig:
        save_fig(self, save_name=save_name, style=style)


def plot_continuous_links(
        self,
        ax=None,
        parameter=None,
        element_list=None,
        include_pumps=True,
        include_valves=True,
        value=None,
        unit=None,
        vmin=None,
        vmax=None,
        draw_nodes=False,
        savefig=False,
        save_name=None,
        element_size_intervals=None,
        element_size_legend_title=None,
        element_size_legend_loc=None,
        element_size_legend_labels=None,
        color_bar_title=None,
        style=None):
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
    
    vmin : integer
        The minimum value of the color bar. 
    
    vmax : integer
        The maximum value of the color bar.
    
    element_size_intervals : integer
        The number of intervals to be used if an element size legend is used.
    
    element_size_legend_title : string
        The title of the element size legend.
   
    element_size_legend_loc : string
        The location of the element size legend on the figure.
    
    element_size_legend_labels : array-like
        The labels of each interval of the element size legend.
    
    color_bar_title : string
         The title of the color bar.
         
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
    """
    if style is None:
        style = self.default_style
    args = style.args
    link_arrows = args['link_arrows']
    cmap = args['cmap']
    draw_color_bar = args['draw_color_bar']
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
            vmin=vmin,
            vmax=vmax,
            style=style)

        base.draw_base_elements(
            self,
            ax,
            draw_nodes=draw_nodes,
            element_list=link_list,
            style=style)
        if link_arrows is True:
            g = fancyarrowpatch_to_linecollection(
                g, cmap, vmin, vmax, parameter_results)
        if draw_color_bar is True:
            if color_bar_title is None:
                color_bar_title = label_generator(parameter, value, unit)
            base.draw_color_bar(self,
                                ax,
                                g,
                                color_bar_title=color_bar_title)
    base.draw_legend(self,
                     ax,
                     element_size_intervals=element_size_intervals,
                     element_size_legend_title=element_size_legend_title,
                     element_size_legend_loc=element_size_legend_loc,
                     element_size_legend_labels=element_size_legend_labels,
                     style=style)
    if savefig:
        save_fig(self, save_name=save_name, style=style)
