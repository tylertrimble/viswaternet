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

wn = wntr.network.WaterNetworkModel(r'Networks/CTown.inp')
model = visinit.initialize_model(r'Networks/CTown.inp',network_model=wn)

wn.options.quality.parameter = 'TRACE'

fig, ax= plt.subplots(figsize=(12,12))

wn.options.quality.trace_node = "T3"
model = visinit.initialize_model(r'Networks/CTown.inp',network_model=wn)

visplot.plot_discrete_nodes(model, 
                         ax, 
                         parameter='quality',
                         value='max',
                         unit='hr',
                         bin_edge_num=2,
                         bins=[0,0.00001],
                         bin_label_list=['No', 'Yes'],
                         color_list=['k','r'],
                         legend_loc_2='lower left',
                         legend_title='Trace From T3',
                         valves=False,
                         pumps=False,
                         disable_bin_deleting=True)
visplot.draw_label(model,
                   ax,
                   labels=['T3'],
                   x_coords=[0],
                   y_coords=[-150],
                   nodes=['T3'],
                   draw_arrow=False,
                   label_font_size=9
                   )
plt.show()