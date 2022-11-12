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
import visnet as vis
import matplotlib.pyplot as plt

model = vis.VisnetModel(r'Networks/CTown.inp')

fig, ax = plt.subplots(figsize=(12,12))

ax.set_frame_on(False)
#Plot demand pattern for each node
model.plot_unique_data(
    ax,parameter="demand_patterns",
    interval_node_size_list=[300,300,300,300,300,300],
    interval_label_list=['Pattern 1','Pattern 2','Pattern 3','Pattern 4','Pattern 5', 'No Pattern'],
    cmap="Dark2",
    legend_loc_2="lower left",legend_title="Demand Patterns",font_color="k",
    legend_sig_figs=3,
    pumps=False,valves=False
)

plt.show()