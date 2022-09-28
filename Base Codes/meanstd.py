# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 12:57:31 2022

@author: Tyler
"""

import visnet010 as vis
import matplotlib.pyplot as plt
import os
import numpy as np

#Initialize model
model = vis.initialize_model('Networks\CTown.inp')

#Special Labels
fig, ax = plt.subplots(figsize=(10,15))

mean,element_list = vis.get_parameter(model,'node',parameter='pressure',value='mean')

standard_deviation,element_list = vis.get_parameter(model,'node',parameter='pressure',value='stddev')

max_size=300
min_size=100

minParameter = np.min(standard_deviation)
maxParameter = np.max(standard_deviation)

normalizedParameter = np.copy(standard_deviation)



for counter,parameter in enumerate(standard_deviation):
    
    normalizedParameter[counter] = ((max_size - min_size)*((parameter - minParameter)/(maxParameter - minParameter))) + min_size


node_size = normalizedParameter

vis.plot_unique_data(model,ax,parameter='custom_data',parameter_type='node',data_type='continuous',custom_data_values=[element_list,mean],node_size=node_size)