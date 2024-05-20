# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 14:27:17 2024

@author: tyler
"""
from viswaternet.utils.markers import *

class NetworkStyle:
    def __init__(self,
                 **kwargs):
        args = {'node_size': 100,
                        'node_color': None,
                        'node_shape': '.',
                        'node_border_color': None,
                        'node_border_width': None,
                        'color_list': None,
                        'link_width': 1,
                        'link_color': 1,
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
                        'discrete_legend_loc': 'lower right',
                        'base_legend_label_font_size': 15,
                        'base_legend_label_color': 'k',
                        'discrete_legend_label_font_size': 15,
                        'discrete_legend_label_color': 'k',
                        'discrete_legend_title_font_size': 17,
                        'discrete_legend_title_color': 'k',
                        'draw_legend_frame': False,
                        'legend_decimal_places': 3,
                        'element_size_intervals': None,
                        'element_size_legend_title': None,
                        'element_size_legend_loc': None,
                        'element_size_legend_labels': None,
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
                        'element_size_intervals': None,
                        'element_size_legend_title': None,
                        'element_size_legend_loc': None,
                        'element_size_legend_labels': None,
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