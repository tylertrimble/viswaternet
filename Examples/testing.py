# -*- coding: utf-8 -*-
"""
Created on Sat Oct  8 16:36:38 2022

@author: Tyler
"""
import visnetwork.network as visinit
import visnet.drawing as visplot

import matplotlib.pyplot as plt
import os
#Initialize model
model = visinit.initialize_model('Networks\CTown.inp')

#Define the file path for images. By default, this is the location where the python file is located.
#Because of how Jupyter Notebook works, a relative path from the notebook can not be obtained.
cwd = os.getcwd()
model['image_path'] = cwd + '\Images'
#Defines a matplotlib figure and axis. The user can customize the size of the plot in this way.

fig, ax = plt.subplots(figsize = (9,15))
plt.title("Pipe Diameters for CTown Network")
#Removes border from figure
plt.box(False)
#Creates discrete nodes plot of elevation. Doesn't draw reservoirs, tanks, pumps or valves
visplot.plot_discrete_nodes(model,ax,5,parameter='pressure',
                        value=6,
                        savefig=False, 
                        legend=True,
                        legend_title= 'Elevation Groups')
#%%
def test_func(**kwargs):
    return kwargs