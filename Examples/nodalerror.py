# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 12:57:31 2022

@author: Tyler
"""

import wntr

import visnet.network as visinit
import visnet.drawing as visplot
import random
import matplotlib.pyplot as plt
#Initialize model

#Special Labels
fig, ax = plt.subplots(figsize=(12,12))


wn = wntr.network.WaterNetworkModel(r'Networks\CTown.inp')
model = visinit.initialize_model(r'Networks\CTown.inp',network_model=wn)
random.seed(1)
error_list = []
element_list=wn.junction_name_list
for _, junc in wn.junctions():
    try:
        pat = junc.demand_timeseries_list[0].pattern.name
        if pat == 'DMA2_pat' or pat == 'DMA5_pat' or pat == 'DMA3_pat':
            error_list.append(0)
        else:
            error_list.append(random.uniform(-8,5))
    except AttributeError:
        error_list.append(0)
        
visplot.plot_unique_data(model,
                             ax,
                             parameter='custom_data',
                             node_size=200,
                             line_widths=1,
                             edge_colors='k',
                             parameter_type='node',
                             data_type='continuous',
                             custom_data_values=[element_list,error_list],
                             color_bar_title='Error (%)',
                             cmap='autumn_r')

plt.show()