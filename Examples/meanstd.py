# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 12:57:31 2022

@author: Tyler
"""

import visnet.network as visinit
import visnet.drawing as visplot
import visnet.utils as visutils

import matplotlib.pyplot as plt
#Initialize model
model = visinit.initialize_model('Networks\CTown.inp')


#Special Labels
fig, ax = plt.subplots(figsize=(20,30))

mean,element_list = visinit.get_parameter(model,
                                          'node',
                                          parameter='pressure',
                                          value='mean')

standard_deviation,element_list = visinit.get_parameter(model,
                                                        'node',
                                                        parameter='pressure',
                                                        value='stddev')

min_size=150
max_size=150

node_size = visutils.normalize_parameter(model,standard_deviation,min_size,max_size)

binnedParameter, bin_names=visinit.bin_parameter(model,standard_deviation,element_list,5)

bin_names=bin_names.tolist()
visplot.plot_unique_data(model,
                             ax,
                             parameter='custom_data',
                             parameter_type='node',
                             data_type='continuous',
                             custom_data_values=[element_list,mean],
                             node_size=node_size,
                             color_bar_title='Mean Pressure',
                             cmap='autumn_r',
                             element_size_bins=4,
                             element_size_legend_title='Standard Deviation',
                             element_size_legend_loc='lower left',
                             element_size_legend_labels=bin_names)


plt.show()