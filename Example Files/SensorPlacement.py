# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 12:22:40 2022

@author: Tyler
"""

import visnet010 as vis
import matplotlib.pyplot as plt
import os
#Initialize model
model = vis.initialize_model('Networks\CTown.inp')

#Special Labels
fig, ax = plt.subplots(figsize=(10,15))
#Removes border from figure
plt.box(False)
#Draws distinct elevation.
vis.plot_discrete_nodes(model,ax,5,parameter='elevation')

#Plots red square with black outline at specific nodes
vis.draw_nodes(model,['J511','J411'],
               node_size=[150,150],
               node_color='#00FFFF',
               node_shape='o',
               edge_colors='k',
               line_widths=2)
vis.draw_label(model, ax,
               labels = ['Sensor 1','Sensor 2'],
               x_coords = [400,-500],
               y_coords = [150,10],
               nodes = ['J511','J411'])