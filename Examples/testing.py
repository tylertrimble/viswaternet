# -*- coding: utf-8 -*-
"""
Created on Sat Oct  8 16:36:38 2022

@author: Tyler
"""
import visnet.network as visinit
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
#Removes border from figure
plt.box(False)
#Creates discrete nodes plot of elevation. Doesn't draw reservoirs, tanks, pumps or valves
visplot.plot_discrete_nodes(model, ax, parameter='elevation',font_size=11,legend_title='Elevation (ft)',legend_title_font_size=17)
#%%
def test_func(**kwargs):
    return kwargs