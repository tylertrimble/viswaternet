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
import visnetwork as vis
import wntr
import matplotlib.pyplot as plt

wn = wntr.network.WaterNetworkModel(r'Networks/CTown.inp')
model = vis.VisnetModel(r'Networks/CTown.inp',network_model=wn)

wn.options.quality.parameter = 'TRACE'

fig, ax= plt.subplots(figsize=(12,12))

wn.options.quality.trace_node = "T3"
model = vis.VisnetModel(r'Networks/CTown.inp',network_model=wn)

model.plot_discrete_nodes(
                         ax, 
                         parameter='quality',
                         value='max',
                         unit='hr',
                         num_intervals=2,
                         intervals=[0,0.00001],
                         interval_label_list=['No', 'Yes'],
                         color_list=['k','r'],
                         legend_loc_2='lower left',
                         legend_title='Trace From T3',
                         valves=False,
                         pumps=False,
                         disable_interval_deleting=True)
model.draw_label(
                   ax,
                   labels=['T3'],
                   x_coords=[0],
                   y_coords=[-150],
                   nodes=['T3'],
                   draw_arrow=False,
                   label_font_size=9
                   )
plt.show()