# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 18:01:36 2022

@author: Tyler
"""

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

fig, ((ax1,ax2,ax3,ax4),(ax5,ax6,ax7,ax8)) = plt.subplots(nrows=2,ncols=4,figsize=(25,25))
ax_list=[ax1,ax2,ax3,ax4,ax5,ax6,ax7,ax8]
timesteps=[0,1,2,3,4,5,6,7]
colors=[(0.6, 0.75, 1), (0, 0.20, 0.5)]
cmap = LinearSegmentedColormap.from_list('DarkBlues', colors, N=100)

wn.options.quality.trace_node = 'R1'
model = visinit.initialize_model(r'Networks\CTown.inp',network_model=wn)

for axes,timestep in zip(ax_list,timesteps):
    axes.set_title("Tracer From R1 at " + str(timestep*15) + " Minutes")
    visplot.plot_continuous_links(model, 
                             axes, 
                             parameter='quality',
                             value=timestep,
                             unit='hr',
                             vmin=0,
                             vmax=0.03,
                             cmap=cmap,
                             color_bar_title='Tracer (%)',
                             legend=False,
                             pumps=False,
                             tank_size=50,
                             tank_border_width=1,
                             reservoirs=True,
                             valves=False)
    visplot.draw_label(model,axes,labels=["T1"],x_coords=[0],y_coords=[150],nodes=["T1"],draw_arrow=False,label_font_size=9)
    
plt.show()