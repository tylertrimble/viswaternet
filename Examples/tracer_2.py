# -*- coding: utf-8 -*-
"""
Created on Sat Oct  8 17:18:55 2022

@author: Tyler
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Oct  8 16:36:38 2022

@author: Tyler
"""
import visnet.network as visinit
import visnet.drawing as visplot

import wntr

import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import os

wn = wntr.network.WaterNetworkModel(r'Networks\CTown.inp')
model = visinit.initialize_model(r'Networks\CTown.inp',network_model=wn)
wn.options.quality.parameter = 'TRACE'
cwd = os.getcwd()
model['image_path'] = cwd + '\Images'

fig, ((ax1,ax2,ax3,ax4),(ax5,ax6,ax7,ax8)) = plt.subplots(nrows=2,ncols=4,figsize=(25,25))
ax_list=[ax1,ax2,ax3,ax4,ax5,ax6,ax7]
x_coords=[0,0,0,0,-100,0,0]
y_coords=[150,-150,-150,150,100,100,120]
tanks = sorted(model['tank_names'])

colors=[(0.6, 0.75, 1), (0, 0.20, 0.5)]
cmap = LinearSegmentedColormap.from_list('DarkBlues', colors, N=100)

for axes,tank,x_coord,y_coord in zip(ax_list,tanks,x_coords,y_coords):
    wn.options.quality.trace_node = 'T1'
    model = visinit.initialize_model(r'Networks\CTown.inp',network_model=wn)
            
    axes.set_title("Tracer From " + tank + " at 28 Hours")
    visplot.plot_continuous_links(model, 
                             axes, 
                             parameter='quality',
                             value=111,
                             unit='hr',
                             vmin=0,
                             vmax=0.03,
                             cmap=cmap,
                             color_bar_title='Tracer (%)',
                             legend=False,
                             pumps=False,
                             tank_shape='h',
                             tank_color='b',
                             tank_size=50,
                             tank_border_color='k',
                             tank_border_width=1,
                             reservoirs=False,
                             valves=False)
    visplot.draw_label(model,axes,labels=[tank],x_coords=[x_coord],y_coords=[y_coord],nodes=[tank],draw_arrow=False,label_font_size=9)
    
wn.options.quality.trace_node = 'R1'
model = visinit.initialize_model(r'Networks\CTown.inp',network_model=wn)

ax8.set_title("Tracer From R1 at 28 Hours")
visplot.plot_continuous_links(model, 
                         ax8, 
                         parameter='quality',
                         value=111,
                         unit='hr',
                         cmap=cmap,
                         vmin=0,
                         vmax=0.3,
                         color_bar_title='Tracer (%)',
                         legend=False,
                         pumps=False,
                         tank_shape='h',
                         tank_color='b',
                         tank_size=50,
                         tank_border_color='k',
                         tank_border_width=1,
                         reservoir_color='b',
                         reservoir_size=50,
                         reservoir_border_color='k',
                         reservoir_border_width=2,
                         valves=False,
                         tanks=False)
visplot.draw_label(model,ax8,labels=["R1"],x_coords=[0],y_coords=[150],nodes=["R1"],draw_arrow=False,label_font_size=9)
plt.show()