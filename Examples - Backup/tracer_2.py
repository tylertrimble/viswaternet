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

# Define figure to be drawn to
fig, ax = plt.subplots(figsize=(12, 12))  

# Disables frame around figure
ax.set_frame_on(False)

wn.options.quality.trace_node = "T3"
model = visinit.initialize_model(r'Networks/CTown.inp',network_model=wn)
visplot.plot_discrete_nodes(model, 
                         ax, 
                         parameter='quality',
                         value='max',
                         legend_loc_2='lower left',
                         legend_title='Max Trace (%)',
                         valves=False,
                         pumps=False,
                         disable_bin_deleting=True)
plt.show()