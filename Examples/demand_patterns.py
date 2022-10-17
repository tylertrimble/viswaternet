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
import os

model = visinit.initialize_model(r'Networks\CTown.inp')

cwd = os.getcwd()
model['image_path'] = cwd + '\Images'

fig, ax = plt.subplots(figsize=(10,15))
plt.title("Demand Patterns for CTown Network",fontsize=16)

ax.set_frame_on(False);

visplot.plot_unique_data(model, 
                         ax, 
                         parameter='demand_patterns',
                         cmap='tab10',
                         legend_loc_2='lower left',
                         legend_title='Demand Patterns',
                         font_color='k',
                         legend_sig_figs=3,
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