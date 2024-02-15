# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
from viswaternet.network import processing
from viswaternet.utils import convert_excel, save_fig, unit_conversion
from viswaternet.drawing import base
from viswaternet.drawing import discrete

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
    node_border_width =None,
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
    cmap=default_cmap,
    legend=True,
    legend_title=None,
    base_legend_loc="upper right",
    discrete_legend_loc="lower right",
    savefig=False,
    save_name=None,
    dpi='figure',
    save_format='png',
    color_bar_title=None,
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
    draw_intervals_legend=True,
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
    disable_interval_deleting=True,
    draw_color_bar=True,
    color_bar_width=0.03,
    color_bar_height=0.8
):
    model = self.model

    if len(self.model['G_list_pumps_only']) == 0:
        draw_pumps = False
    if ax is None:
        fig, ax = plt.subplots(figsize=self.figsize)
        ax.set_frame_on(self.axis_frame)

    def call_draw_base_elements(draw_links=True):
        base.draw_base_elements(self, ax, draw_nodes=False, draw_links=draw_links,
                                draw_reservoirs=draw_reservoirs, draw_tanks=draw_tanks,
                                draw_valves=draw_valves, draw_pumps=draw_pumps,
                                reservoir_size=reservoir_size,
                                reservoir_color=reservoir_color,
                                reservoir_shape=reservoir_shape,
                                reservoir_border_color=reservoir_border_color,
                                reservoir_border_width=reservoir_border_width,
                                tank_size=tank_size, tank_color=tank_color,
                                tank_shape=tank_shape,
                                tank_border_color=tank_border_color,
                                tank_border_width=tank_border_width,
                                valve_size=valve_size, valve_color=valve_color,
                                valve_shape=valve_shape,
                                valve_border_color=valve_border_color,
                                valve_border_width=valve_border_width,
                                pump_color=pump_color, pump_width=pump_width,
                                pump_line_style=pump_line_style,
                                pump_arrows=pump_arrows,
                                base_node_color=base_node_color,
                                base_node_size=base_node_size,
                                base_link_color=base_link_color,
                                base_link_width=base_link_width,
                                base_link_line_style=base_link_line_style,
                                base_link_arrows=base_link_arrows)

    def call_draw_legend(continuous=False, base_links=True, intervals=None):
        if continuous == True:
            base.draw_legend(ax, intervals=intervals, title=legend_title,
                             draw_pumps=draw_pumps, base_legend_loc=base_legend_loc, 
                             discrete_legend_loc=discrete_legend_loc,
                             font_size=font_size, font_color=font_color,
                             legend_title_font_size=legend_title_font_size,
                             draw_frame=draw_frame, pump_color=pump_color,
                             base_link_color=base_link_color,
                             node_size=node_size, link_width=link_width,
                             element_size_intervals=element_size_intervals,
                             element_size_legend_title=element_size_legend_title,
                             element_size_legend_loc=element_size_legend_loc,
                             element_size_legend_labels=element_size_legend_labels,
                             node_border_color=node_border_color, linewidths=node_border_width,
                             draw_base_legend=draw_base_legend,
                             draw_intervals_legend=draw_intervals_legend,
                             pump_line_style=pump_line_style,
                             base_link_line_style=base_link_line_style,
                             base_link_arrows=base_link_arrows,
                             pump_arrows=pump_arrows,
                             draw_base_links=False)
        else:
            base.draw_legend(ax, intervals=intervals, title=legend_title,
                             draw_pumps=draw_pumps, base_legend_loc=base_legend_loc, 
                             discrete_legend_loc=discrete_legend_loc,
                             font_size=font_size, font_color=font_color,
                             legend_title_font_size=legend_title_font_size,
                             draw_frame=draw_frame, pump_color=pump_color,
                             base_link_color=base_link_color,
                             node_sizs=node_size, link_width=link_width,
                             element_size_intervals=element_size_intervals,
                             element_size_legend_title=element_size_legend_title,
                             element_size_legend_loc=element_size_legend_loc,
                             element_size_legend_labels=element_size_legend_labels,
                             node_border_color=node_border_color, linewidths=node_border_width,
                             draw_base_legend=draw_base_legend,
                             draw_intervals_legend=draw_intervals_legend,
                             pump_line_style=pump_line_style,
                             base_link_line_style=base_link_line_style,
                             base_link_arrows=base_link_arrows,
                             pump_arrows=pump_arrows,
                             draw_base_links=base_links)

    def call_draw_color_bar():
        base.draw_color_bar(ax, g, cmap, color_bar_title=color_bar_title,
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
            node_border_width =node_border_width ,
            cmap=cmap,
            color_list=color_list,
        )

        call_draw_base_elements()

        if legend:
            call_draw_legend(intervals=patterns)

        if savefig:

            save_fig(self, save_name=save_name,
                     dpi=dpi, save_format=save_format)
        return
    elif parameter == "diameter" or parameter == "roughness":

        parameter_results, link_list = processing.get_parameter(
            self, "link", parameter
        )

        if unit is not None:
            parameter_results = unit_conversion(
                parameter_results, parameter, unit)
        uniques = sorted(list(set(parameter_results)))

        interval_names = [("{:.{j}f}".format(i, j=legend_sig_figs))
                          for i in uniques]

        interval_results = {}

        for interval_name in interval_names:

            interval_results[interval_name] = {}

        for i, link in enumerate(link_list):

            interval_results["{:.{j}f}".format(parameter_results[i], j=legend_sig_figs)][link] = model[
                "G_pipe_name_list"
            ].index(link)

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
            link_arrows=link_arrows,
        )

        call_draw_base_elements(draw_links=False)

        if legend:
            call_draw_legend(base_links=False, intervals=interval_names)

        if savefig:

            save_fig(self, save_name=save_name,
                     dpi=dpi, save_format=save_format)
        return

    elif parameter == "tag":

        parameter_results, node_list = processing.get_parameter(
            self, "node", parameter
        )

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
            node_border_width =node_border_width ,
            cmap=cmap,
            color_list=color_list,
        )

        call_draw_base_elements()

        if legend:
            call_draw_legend(intervals=interval_names)

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
                    custom_data_values[1]
                ):

                    interval_results[data][element] = model["node_names"].index(
                        element)

            if parameter_type == 'link':
                for element, data in zip(
                    custom_data_values[0],
                    custom_data_values[1]
                ):

                    interval_results[data][element] = model["G_pipe_name_list"].index(
                        element)
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
                    link_arrows=link_arrows,
                )

                call_draw_base_elements(draw_links=False)

                if legend:
                    call_draw_legend(base_links=False,
                                     intervals=custom_data_values[1])
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
                    node_border_width =node_border_width ,
                    cmap=cmap,
                    color_list=color_list,
                )

                call_draw_base_elements()

                if legend:
                    call_draw_legend(intervals=custom_data_values[1])

            if savefig:

                save_fig(self, save_name=save_name,
                         dpi=dpi, save_format=save_format)
            return
        if data_type == "discrete":
            interval_results, interval_names = processing.bin_parameter(
                self,
                custom_data_values[1],
                custom_data_values[0],
                intervals=intervals,
                num_intervals=num_intervals,
                legend_sig_figs=legend_sig_figs,
                disable_interval_deleting=disable_interval_deleting,
            )

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
                    link_arrows=link_arrows,
                )

                call_draw_base_elements(draw_links=False)

                if legend:
                    call_draw_legend(base_links=False,
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
                    node_border_width =node_border_width ,
                    cmap=cmap,
                    color_list=color_list,
                )

                call_draw_base_elements()

                if legend:
                    call_draw_legend(intervals=interval_names)

            if savefig:
                save_fig(self, save_name=save_name,
                         dpi=dpi, save_format=save_format)

                return
        if data_type == "continuous":

            if parameter_type == "link":
                g = base.draw_links(
                    self,
                    ax,
                    custom_data_values[0],
                    parameter_results=custom_data_values[1],
                    cmap=cmap,
                    widths=link_width,
                    vmin=vmin,
                    vmax=vmax,
                    link_style=link_style,
                    link_arrows=link_arrows,
                )

                call_draw_base_elements(draw_links=False)

                if legend:
                    call_draw_legend(continuous=True, base_links=False)

            elif parameter_type == "node":
                g = base.draw_nodes(
                    self,
                    ax,
                    custom_data_values[0],
                    parameter_results=custom_data_values[1],
                    node_size=node_size,
                    cmap=cmap,
                    vmin=vmin,
                    vmax=vmax,
                    node_shape=node_shape,
                    node_border_width=node_border_width,
                    node_border_color=node_border_color,
                )

                call_draw_base_elements()

                if legend:
                    call_draw_legend(continuous=True)

            if draw_color_bar == True:
                call_draw_color_bar()

            if savefig:

                save_fig(self, save_name=save_name,
                         dpi=dpi, save_format=save_format)
            return
    elif parameter == 'excel_data':

        if data_type == "unique":

            element_list, intervals = convert_excel(
                self, data_file, parameter_type, data_type, excel_columns[0], excel_columns[1]
            )

            if parameter_type == "link":

                discrete.draw_discrete_links(
                    self,
                    ax,
                    element_list,
                    intervals,
                    link_width=link_width,
                    label_list=label_list,
                    cmap=cmap,
                    color_list=color_list,
                    link_style=link_style,
                    link_arrows=link_arrows,
                )

                call_draw_base_elements(draw_links=False)

                if legend:
                    call_draw_legend(base_links=False, intervals=intervals)

            elif parameter_type == "node":

                discrete.draw_discrete_nodes(
                    self,
                    ax,
                    element_list,
                    intervals,
                    node_size=node_size,
                    node_shape=node_shape,
                    label_list=label_list,
                    node_border_color=node_border_color,
                    node_border_width =node_border_width ,
                    cmap=cmap,
                    color_list=color_list,
                )

                call_draw_base_elements()

                if legend:
                    call_draw_legend(intervals=intervals)

            if savefig:

                save_fig(self, save_name=save_name,
                         dpi=dpi, save_format=save_format)
            return
        if data_type == "discrete":

            data = convert_excel(
                self, data_file, parameter_type, data_type, excel_columns[0], excel_columns[1]
            )

            interval_results, interval_names = processing.bin_parameter(
                self,
                data["results"],
                data["element_list"],
                intervals=intervals,
                num_intervals=num_intervals,
                legend_sig_figs=legend_sig_figs,
                disable_interval_deleting=disable_interval_deleting,
            )

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
                    link_arrows=link_arrows,
                )

                call_draw_base_elements(draw_links=False)

                if legend:
                    call_draw_legend(base_links=False,
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
                    node_border_width =node_border_width ,
                    cmap=cmap,
                    color_list=color_list,
                )

                call_draw_base_elements()

                if legend:
                    call_draw_legend(intervals=interval_names)

            if savefig:

                save_fig(self, save_name=save_name,
                         dpi=dpi, save_format=save_format)
            return
        if data_type == "continuous":

            data = convert_excel(
                self, data_file, parameter_type, data_type, excel_columns[0], excel_columns[1]
            )

            if parameter_type == "link":
                g = base.draw_links(
                    self,
                    ax,
                    data["element_list"],
                    parameter_results=data["results"],
                    cmap=cmap,
                    widths=link_width,
                    vmin=vmin,
                    vmax=vmax,
                    link_style=link_style,
                    link_arrows=link_arrows,
                )

                call_draw_base_elements(draw_links=False)

                if legend:
                    call_draw_legend(continuous=True, base_links=False)

            elif parameter_type == "node":
                g = base.draw_nodes(
                    self,
                    ax,
                    data["element_list"],
                    parameter_results=data["results"],
                    node_size=node_size,
                    cmap=cmap,
                    vmin=vmin,
                    vmax=vmax,
                    node_shape=node_shape,
                    node_border_width=node_border_width,
                    node_border_color=node_border_color,
                )

                call_draw_base_elements()

                if legend:
                    call_draw_legend(continuous=True)

            if draw_color_bar == True:
                call_draw_color_bar()

            if savefig:

                save_fig(self, save_name=save_name,
                         dpi=dpi, save_format=save_format)
        return
    elif isinstance(parameter, str):
        pass
    else:
        raise Exception("Invalid input, check docs for valid inputs.")
