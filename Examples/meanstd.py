# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 12:57:31 2022

@author: Tyler
"""

import visnet as vis
import matplotlib.pyplot as plt

#Initialize model
model = vis.network.initialize_model('Networks\CTown.inp')

#Special Labels
fig, ax = plt.subplots(figsize=(10,15))

mean,element_list = vis.network.get_parameter(model,'node',parameter='pressure',value='mean')

standard_deviation,element_list = vis.network.get_parameter(model,'node',parameter='pressure',value='stddev')

min_size=50
max_size=500

node_size = vis.utils.normalize_parameter(model,standard_deviation,min_size,max_size)

vis.drawing.plot_unique_data(model,ax,parameter='custom_data',parameter_type='node',data_type='continuous',custom_data_values=[element_list,mean],node_size=node_size,color_bar_title='Mean Pressure',cmap='winter')
