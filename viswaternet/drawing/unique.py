# -*- coding: utf-8 -*-
"""
The viswaternet.drawing.unique module handles custom data, excel data, and
unique data drawing.
"""
import matplotlib.pyplot as plt
import pandas as pd
from viswaternet.network import processing
from viswaternet.utils import convert_excel, save_fig, unit_conversion
from viswaternet.drawing import base
from viswaternet.drawing import discrete


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
        num_intervals=5,
        label_list=None,
        vmin=None,
        vmax=None,
        draw_nodes=False,
        discrete_legend_title=None,
        savefig=False,
        save_name=None,
        color_bar_title=None,
        element_size_intervals=None,
        element_size_legend_title=None,
        element_size_legend_loc=None,
        element_size_legend_labels=None,
        disable_interval_deleting=True,
        style=None):
    """A complex function that accomplishes tasks relating to categorical data,
    or 'unique' as used in viswaternet, as well as data not retrieved from
    WNTR.

    There are three distinct modes of operation, and which one is used is
    controlled by the 'parameter' argument, which differs from previous use of
    the argument.

    Setting the parameter argument to 'demand_patterns', 'diameter', or
    'roughness' simply plots that parameter. These parameters are treated
    differently from others because in usually they are categorical. For
    instance, pipe diameters are not randomly chosen, and instead are chosen
    from a list of standard pipe sizes.

    When the parameter argument is set to 'excel_data', the function deals with
    excel data, or data imported from an .xlsx file. Two excel columns with
    elements and data pairs are provided by the user, which are then converted
    into a format usable by viswaternet for plotting.

    When the parameter argument is set to 'custom_data', the function deals
    with data directly inside of python. The user should expect to format the
    data themselves, although this shouldn't be difficult. An example of
    'custom_data' being used can be seen in example 10 located in the github
    repository.

    Arguments
    ---------
    ax : axes._subplots.AxesSubplot
        Matplotlib axes object.

    parameter : string
        Should be set to 'demand_patterns', 'diameter', 'roughness',
        'custom_data' or 'excel_data'.

    parameter_type : string
        Type of parameter (nodal, link)

    data_type : string
        The type of data that the excel data is (Unique, continuous, or
        discrete.)

    data_file : string

    excel_columns : array-like
        Two values should be provided:

        The first should be the excel column that contains element names.
        Column A in excel is considered the 0th column for use with
        viswaternet.

        The second should be the excel column that contains element data.
        Column A in excel is considered the 0th column for use with
        viswaternet.

        If intending to animate data using this method, all columns except
        the first column are treated as data columns and will be animated
        in order.

    custom_data_values : array-like
        Similar to 'excel_columns' two values should be provided. The first
        value should be an array with element names, and the second should be
        one with the element data.
  
        If intending to animate data using this method, all values except the
        first value are treated as data values and will be animated in order.
        This means that, for example, when animating 10 timesteps using
        this method you should have 11 arrays inside this array.

    unit : string
        The unit that the network data is to be converted to.

    intervals : integer, string
        If set to 'automatic' then intervals are created automatically on a
        equal interval basis. Otherwise, it is the edges of the intervals to be
        created. intervals array length should be num_intervals + 1.

    num_intervals : integer
         The number of intervals.

    disable_interval_deleting : boolean
        If True, empty intervals will be automatically deleted.

    vmin : integer
        The minimum value of the color bar.

    vmax : integer
        The maximum value of the color bar.

    label_list : string, array-like
        List of labels for each interval.

    draw_nodes : boolean
        Determines if draw_nodes with no data associated with them are drawn.

    discrete_legend_title : string
        Title of the intervals legend.

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

    color_bar_title : string
         The title of the color bar.

    element_size_intervals : integer
        The number of intervals to be used if an element size legend is used.

    element_size_legend_title : string
        The title of the element size legend.

    element_size_legend_loc : string
        The location of the element size legend on the figure.

    element_size_legend_labels : array-like
        The labels of each interval of the element size legend.

    disable_interval_deleting : boolean
        If True, empty intervals will be automatically deleted.

    style : VisWaterNet Style Object
        The style object to be used.
    """

    model = self.model
    if style is None:
        style = self.default_style
    args = style.args
    draw_color_bar = args['draw_color_bar']
    pump_element = args['pump_element']
    draw_pumps = args['draw_pumps']
    valve_element = args['valve_element']
    draw_valves = args['draw_valves']
    legend_decimal_places = args['legend_decimal_places']
    if len(self.model['G_list_pumps_only']) == 0:
        draw_pumps = False
    if ax is None:
        fig, ax = plt.subplots(figsize=self.figsize)
        ax.set_frame_on(self.axis_frame)

    def call_draw_base_elements(element_list=None):
        base.draw_base_elements(self,
                                ax,
                                draw_nodes=draw_nodes,
                                element_list=element_list,
                                draw_originator=parameter_type,
                                style=style)

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
            self,
            ax,
            intervals=intervals,
            title=discrete_legend_title,
            element_size_intervals=element_size_intervals,
            element_size_legend_title=element_size_legend_title,
            element_size_legend_loc=element_size_legend_loc,
            element_size_legend_labels=element_size_legend_labels,
            style=style)

    def call_draw_color_bar():
        base.draw_color_bar(self,
                            ax,
                            g,
                            color_bar_title=color_bar_title,
                            style=style)
    if parameter == "demand_patterns":
        demand_pattern_nodes, patterns = processing.get_demand_patterns(self)
        discrete.draw_discrete_nodes(
            self,
            ax,
            demand_pattern_nodes,
            patterns,
            label_list=label_list,
            style=style)
        call_draw_base_elements(element_list=model['node_names'])
        call_draw_legend(intervals=patterns, element_list=model['node_names'])
        if savefig:
            save_fig(self, save_name=save_name, style=style)
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
            label_list=label_list,
            style=style)
        call_draw_base_elements(element_list=link_list)
        call_draw_legend(intervals=interval_names, element_list=link_list)
        if savefig:
            save_fig(self, save_name=save_name, style=style)
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
            label_list=label_list,
            style=style)
        call_draw_base_elements(element_list=model["node_names"])
        call_draw_legend(intervals=interval_names,
                         element_list=model["node_names"])
        if savefig:
            save_fig(self, save_name=save_name, style=style)
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
                    label_list=label_list,
                    style=style)
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
                    style=style)
            call_draw_base_elements(element_list=custom_data_values[0])
            call_draw_legend(intervals=interval_names,
                             element_list=custom_data_values[0])
            if savefig:
                save_fig(self, save_name=save_name, style=style)
            return
        elif data_type == "discrete":
            interval_results, interval_names = processing.bin_parameter(
                self,
                custom_data_values[1],
                custom_data_values[0],
                intervals=intervals,
                num_intervals=num_intervals,
                disable_interval_deleting=disable_interval_deleting,
                style=style)
            if parameter_type == "link":
                discrete.draw_discrete_links(
                    self,
                    ax,
                    interval_results,
                    interval_names,
                    label_list=label_list,
                    style=style)
                call_draw_base_elements(element_list=custom_data_values[0])
                call_draw_legend(element_list=custom_data_values[0],
                                 intervals=interval_names)
            elif parameter_type == "node":
                discrete.draw_discrete_nodes(
                    self,
                    ax,
                    interval_results,
                    interval_names,
                    label_list=label_list,
                    style=style)
                call_draw_base_elements(element_list=custom_data_values[0])
                call_draw_legend(intervals=interval_names,
                                 element_list=custom_data_values[0])
            if savefig:
                save_fig(self, save_name=save_name, style=style)
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
                    vmin=vmin,
                    vmax=vmax,
                    style=style)
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
                    vmin=vmin,
                    vmax=vmax,
                    style=style)
                call_draw_base_elements(element_list=custom_data_values[0])
                call_draw_legend(element_list=custom_data_values[0])
            if draw_color_bar is True:
                call_draw_color_bar()
            if savefig:
                save_fig(self, save_name=save_name, style=style)
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
                    label_list=label_list,
                    style=style)
                call_draw_base_elements(element_list=element_list)
                call_draw_legend(element_list=element_list,
                                 intervals=intervals)
            elif parameter_type == "node":
                discrete.draw_discrete_nodes(
                    self,
                    ax,
                    interval_results,
                    intervals,
                    label_list=label_list,
                    style=style)
                call_draw_base_elements(element_list=element_list)
                call_draw_legend(intervals=intervals,
                                 element_list=element_list)
            if savefig:
                save_fig(self, save_name=save_name, style=style)
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
                disable_interval_deleting=disable_interval_deleting,
                style=style)
            if parameter_type == "link":
                discrete.draw_discrete_links(
                    self,
                    ax,
                    interval_results,
                    interval_names,
                    label_list=label_list,
                    style=style)
                call_draw_base_elements(element_list=element_list)
                call_draw_legend(element_list=element_list,
                                 intervals=interval_names)
            if parameter_type == "node":
                discrete.draw_discrete_nodes(
                    self,
                    ax,
                    interval_results,
                    interval_names,
                    label_list=label_list,
                    style=style)
                call_draw_base_elements(element_list=element_list)
                call_draw_legend(intervals=interval_names,
                                 element_list=element_list)
            if savefig:
                save_fig(self, save_name=save_name, style=style)
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
                    vmin=vmin,
                    vmax=vmax,
                    style=style)
                call_draw_base_elements(element_list=element_list)
                call_draw_legend(element_list=element_list)
            elif parameter_type == "node":
                g = base.draw_nodes(
                    self,
                    ax,
                    element_list,
                    results,
                    vmin=vmin,
                    vmax=vmax,
                    style=style)
                call_draw_base_elements(element_list=element_list)
                call_draw_legend(element_list=element_list)
            if draw_color_bar is True:
                call_draw_color_bar()
            if savefig:
                save_fig(self, save_name=save_name, style=style)
        return
    elif isinstance(parameter, str):
        pass
    else:
        raise Exception("Invalid input, check docs for valid inputs.")
