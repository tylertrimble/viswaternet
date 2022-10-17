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
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import os

model = visinit.initialize_model(r'Networks\CTown.inp')

cwd = os.getcwd()
model['image_path'] = cwd + '\Images'

fig, ax = plt.subplots(figsize=(10,15))
plt.title("Water Age for CTown Network",fontsize=16)

ax.set_frame_on(False);

colors=[(0.6, 0.75, 1), (0, 0.20, 0.5)]
cmap = LinearSegmentedColormap.from_list('DarkBlues', colors, N=4)

visplot.plot_discrete_nodes(model, 
                         ax, 
                         parameter='quality',
                         value=111,
                         unit='hr',
                         bin_edge_num=5,
                         bins=[0,30,60,90,120],
                         bin_size_list=[100,150,250,400],
                         bin_border_list=['k','k','k','k'],
                         bin_border_width_list=[1,1,1,1],
                         cmap=cmap,
                         legend_loc_2='lower left',
                         legend_title='Water Age (hr) at 28 Hours',
                         font_color='k',
                         legend_title_font_size='16',
                         legend_sig_figs=0,
                         pumps=False,
                         tank_shape='h',
                         tank_color='b',
                         tank_border_color='k',
                         tank_border_width=2,
                         reservoir_color='b',
                         reservoir_size=150,
                         reservoir_border_color='k',
                         reservoir_border_width=3,
                         valves=False)
plt.show()