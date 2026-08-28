# -*- coding: utf-8 -*-

"""
The viswaternet.drawing.style module contains the NetworkStyle object, which
is used to define all the cosmetic options for VisWaterNet Plots. Styles can
be created and modifed.
"""
from viswaternet.utils.markers import *


class NetworkStyle:
    def __init__(self,
                 **kwargs):
        """Creates a style object than can be passed into any VisWaterNet
        function.

        Arguments
        ---------
        node_color : string
            Color of the draw_nodes.

        node_shape : string, array-like
            The shape of the nodes being drawn. Can either be a single string
            value or an array of values for each node being drawn.

            Refer to the matplotlib documentation for available marker types.
                https://matplotlib.org/stable/api/markers_api.html

        node_border_color : string, array-like
            The color of the node borders for the nodes being drawn. Can either
            be a single string value or an array of values for each node being
            drawn.

        node_border_width  : integer, array-like
            The width of the node borders. Can either be a single string value
            or an array of values for each node being drawn.

        color_list : string, array-like
            The list of node colors for each interval. Both cmap and color_list
            can not be used at the same time to color draw_nodes. If both are,
            then color_list takes priority.

        link_width : string, array-like
            The width of the link being drawn. Can either be a single string
            value or an array of values for each link being drawn.

        link_style : string, array-like
            The style of the link being drawn. Can either be a single string
            value or an array of values for each link being drawn.

            Refer to the matplotlib documentation for available link styles.
                https://matplotlib.org/stable/gallery/lines_bars_and_markers/linestyles.html

        link_arrows : string, array-like
            Whether arrows should be drawn for each link. Can either be a
            single string value or an array of values for each link being
            drawn.

        link_color : string, array-like
            The color the link being drawn. Can either be a single string value
            or an array of values for each link being drawn.

        draw_tanks : boolean
            Determines if draw_reservoirs with no data associated with them are
            drawn.

        draw_reservoirs : boolean
            Determines if draw_reservoirs with no data associated with them are
            drawn.

        draw_pumps : boolean
            Determines if draw_pumps with no data associated with them are
            drawn.

        draw_valves : boolean
            Determines if draw_valves with no data associated with them are
            drawn.

        draw_links : boolean
            Determines if base draw_links with no data associated with them are
            drawn. Set to False for all functions that deal with link data
            plotting.

        cmap : string
            The matplotlib color map to be used for plotting. Refer to
            matplotlib documentation for possible inputs.
                https://matplotlib.org/stable/users/explain/colors/colormaps.html

        draw_base_legend : boolean
            Determine if the base elements legend is drawn.

        draw_discrete_legend : boolean
            Determine if the intervals legend is drawn.

        base_legend_loc : string
            The location of the base elements legend on the figure. Refer to
            matplotlib documentation for possible inputs.
                https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.legend.html

        discrete_legend_loc : string
            The location of the intervals legend on the figure. Refer to
            matplotlib documentation for possible inputs.
                https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.legend.html

        base_legend_label_font_size : integer
            The font size of the non-title text for the base elements legend.

        base_legend_label_color : string
            The color of the legend text. Refer to matplotlib documentation for
            available colors.

        discrete_legend_label_font_size : integer
            The font size of the intervals legend text.

        discrete_legend_label_color : string
            The color of the intervals legend text.

        discrete_legend_title_font_size : integer
            The font size of the title text for the intervals legend.

        discrete_legend_title_color : string
            The color of the title tect for the intervals legend.

        draw_legend_frame : boolean
            Determines if the frame around the legend is drawn.

        legend_decimal_places : integer
            The number of decimal places that will be used on the discrete
            legend.

        reservoir_size : float
            The size of the reservoir marker on the plot in points^2.

        reservoir_color : string
            The color of the reservoir marker.

        reservoir_shape : string
            The shape of the reservoir marker. Refer to matplotlib
            documentation for available marker types.
                https://matplotlib.org/stable/api/markers_api.html

        reservoir_border_color : string
            The color of the border around the reservoir marker.

        reservoir_border_width : float
            The width in points of the border around the reservoir marker.

        tank_size : float
            The size of the tank marker on the plot in points^2.

        tank_color : string
            The color of the tank marker.

        tank_shape : string
            The shape of the tank marker. Refer to matplotlib
            documentation for available marker types.
                https://matplotlib.org/stable/api/markers_api.html

        tank_border_color : string
            The color of the border around the tank marker.

        tank_border_width : float
            The width in points of the border around the tank marker.

        valve_elememt : string
            Determines whether the valves are drawn as links or nodes.

        valve_size : float
            The size of the valve marker on the plot in points^2.

        valve_color : string
            The color of the valve marker.

        valve_shape : string
            The shape of the valve marker. Refer to matplotlib
            documentation for available marker types.
                https://matplotlib.org/stable/api/markers_api.html

        valve_border_color : string
            The color of the border around the valve marker.

        valve_border_width : float
            The width in points of the border around the valve marker.

        valve_width : float
            The width of the valve line in points

        valve_line_style : string
            The line style of valves if they are drawn as links. Refer to
            matplotlib documentation for available line styles.
                https://matplotlib.org/stable/gallery/lines_bars_and_markers/linestyles.html
        valve_arrows : boolean
           Determines if an arrow is drawn in the direction of flow of the
           valves.

        pump_element : string
           Determines if pumps are drawn as links or nodes.

        pump_size : float
            The size of the pump marker on the plot in points^2.

        pump_color : string
            The color of the pump line.

        pump_shape : string
            The shape of the pump marker. Refer to matplotlib
            documentation for available marker types.
                https://matplotlib.org/stable/api/markers_api.html

        pump_border_color : string
            The color of the border around the pump marker.

        pump_border_width : float
            The width in points of the border around the pump marker.

        pump_width : float
            The width of the pump line in points.

        pump_line_style : string
            The style (solid, dashed, dotted, etc.) of the pump line. Refer to
            matplotlib documentation for available line styles.
                https://matplotlib.org/stable/gallery/lines_bars_and_markers/linestyles.html

        pump_arrows : boolean
            Determines if an arrow is drawn in the direction of flow of the
            pump.

        base_node_color : string
            The color of the nodes without data associated with them.

        base_node_size : float
            The size of the nodes without data associated with them in
            points^2.

        base_link_color : string
            The color of the links without data associated with them.

        base_link_width : float
            The width of the links without data associated with them in points.

        base_link_line_style : string
            The style (solid, dashed, dotted, etc) of the links with no
            data associated with them.

        base_link_arrows : boolean
            Determines if an arrow is drawn in the direction of flow of the
            links with no data associated with them.

        draw_color_bar : boolean
            Determines if color bar is drawn.

        color_bar_width : float
            The width of the color bar, measured in relative units of the total
            width of the plotting axis.

        color_bar_height : float
            The height of the color bar, measured in relative units of the
            total height of the plotting axis.

        color_bar_loc : string
            The location of the color bar. Can be 'left', 'right', 'top', or
            'bottom'.

        color_bar_label_loc : string
            The location of the color bar's label relative to the color bar.
            Can be 'left', 'right', 'top', or 'bottom'.

        color_bar_label_font_size : integer
            The font size of the color bar's label.

        color_bar_label_font_color : string
            The font color of the color bar's label.

        save_format : string
            The file format that the image will be saved to. A comprehensive
            list of formats can be found on the imageio docs page:
                https://imageio.readthedocs.io/en/stable/formats/index.html
   
        dpi : integer
            The DPI of the saved image. A higher DPI will result in images
            with a higher resolution.
        """

        args = {'node_size': 100,
                'node_color': None,
                'node_shape': '.',
                'node_border_color': None,
                'node_border_width': None,
                'color_list': None,
                'link_width': 1,
                'link_style': '-',
                'link_arrows': False,
                'link_color': 'black',
                'draw_tanks': True,
                'draw_reservoirs': True,
                'draw_pumps': True,
                'draw_valves': True,
                'draw_links': True,
                'cmap': 'autumn',
                'draw_base_legend': True,
                'draw_discrete_legend': True,
                'base_legend_loc': 'upper right',
                'discrete_legend_loc': 'lower right',
                'base_legend_label_font_size': 15,
                'base_legend_label_color': 'k',
                'discrete_legend_label_font_size': 15,
                'discrete_legend_label_color': 'k',
                'discrete_legend_title_font_size': 17,
                'discrete_legend_title_color': 'k',
                'draw_legend_frame': False,
                'legend_decimal_places': 3,
                'reservoir_size': 150,
                'reservoir_color': 'k',
                'reservoir_shape': epa_res,
                'reservoir_border_color': 'k',
                'reservoir_border_width': 3,
                'tank_size': 200,
                'tank_color': 'k',
                'tank_shape': epa_tank,
                'tank_border_color': 'k',
                'tank_border_width': 2,
                'valve_element': 'node',
                'valve_size': 200,
                'valve_color': 'k',
                'valve_shape': epa_valve,
                'valve_border_color': 'k',
                'valve_border_width': 1,
                'valve_width': 3,
                'valve_line_style': '-',
                'valve_arrows': False,
                'pump_element': 'node',
                'pump_size': 200,
                'pump_color': 'k',
                'pump_shape': epa_pump,
                'pump_border_color': 'k',
                'pump_border_width': 1,
                'pump_width': 3,
                'pump_line_style': '-',
                'pump_arrows': False,
                'base_node_color': 'k',
                'base_node_size': 30,
                'base_link_color': 'k',
                'base_link_width': 1,
                'base_link_line_style': '-',
                'base_link_arrows': False,
                'draw_color_bar': True,
                'color_bar_width': 0.03,
                'color_bar_height': 0.8,
                'color_bar_loc': 'right',
                'color_bar_label_loc': 'right',
                'color_bar_label_font_size': 10,
                'color_bar_label_font_color': 'k',
                'save_format': 'png',
                'dpi': 'figure'}
        args.update(kwargs)
        self.args = args

    def update_style_args(self, **kwargs):
        self.args.update(kwargs)

    def revert_style_args(self, args_list):
        if isinstance(args_list, str):
            args_list = list(args_list)
        for key in args_list:
            del self.args[key]
        args = {'node_size': 100,
                'node_shape': '.',
                'node_border_color': None,
                'node_border_width': None,
                'color_list': None,
                'link_width': 1,
                'link_style': '-',
                'link_arrows': False,
                'draw_tanks': True,
                'draw_reservoirs': True,
                'draw_pumps': True,
                'draw_valves': True,
                'draw_links': True,
                'cmap': 'autumn',
                'draw_base_legend': True,
                'base_legend_loc': 'upper right',
                'discrete_legend_loc': 'best',
                'base_legend_label_font_size': 15,
                'base_legend_label_color': 'k',
                'discrete_legend_label_font_size': 15,
                'discrete_legend_label_color': 'k',
                'discrete_legend_title_font_size': 17,
                'discrete_legend_title_color': 'k',
                'draw_legend_frame': False,
                'legend_decimal_places': 3,
                'draw_discrete_legend': True,
                'reservoir_size': 150,
                'reservoir_color': 'k',
                'reservoir_shape': epa_res,
                'reservoir_border_color': 'k',
                'reservoir_border_width': 3,
                'tank_size': 200,
                'tank_color': 'k',
                'tank_shape': epa_tank,
                'tank_border_color': 'k',
                'tank_border_width': 2,
                'valve_element': 'node',
                'valve_size': 200,
                'valve_color': 'k',
                'valve_shape': epa_valve,
                'valve_border_color': 'k',
                'valve_border_width': 1,
                'valve_width': 3,
                'valve_line_style': '-',
                'valve_arrows': False,
                'pump_element': 'node',
                'pump_size': 200,
                'pump_color': 'k',
                'pump_shape': epa_pump,
                'pump_border_color': 'k',
                'pump_border_width': 1,
                'pump_width': 3,
                'pump_line_style': '-',
                'pump_arrows': False,
                'base_node_color': 'k',
                'base_node_size': 30,
                'base_link_color': 'k',
                'base_link_width': 1,
                'base_link_line_style': '-',
                'base_link_arrows': False,
                'draw_color_bar': True,
                'color_bar_width': 0.03,
                'color_bar_height': 0.8,
                'save_format': 'png',
                'dpi': 'figure'}
        args.update(self.args)
        self.args = args
        