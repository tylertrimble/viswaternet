# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 12:22:40 2022

@author: Tyler
"""

import visnet as vis
import matplotlib.pyplot as plt

#Initialize model
model = vis.network.initialize_model('Networks\CTown.inp')

fig, ax = plt.subplots(figsize=(10,15))
#Removes border from figure
plt.box(False)
#Draws distinct elevation.
vis.drawing.plot_discrete_nodes(model,ax,5,parameter='elevation',savefig=False,
                                legend_loc_1='upper left',
                                legend_loc_2='lower left')

vis.drawing.draw_nodes(model,ax,['J511','J411'],
               node_size=[150,150],
               node_color='#00FFFF',
               node_shape='o',
               edge_colors='k',
               line_widths=2)
vis.drawing.draw_label(model, ax,
               labels = ['Sensor 1','Sensor 2'],
               x_coords = [400,-500],
               y_coords = [150,10],
               nodes = ['J511','J411'])