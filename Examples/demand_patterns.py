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

fig, ax = plt.subplots(figsize=(12,12))

ax.set_frame_on(False);

visplot.plot_unique_data(
    model,
    ax,
    parameter="demand_patterns",
    bin_size_list=[300,300,300,300,300,300],
    bin_label_list=['Pattern 1','Pattern 2','Pattern 3','Pattern 4','Pattern 5', 'No Pattern'],
    cmap="Dark2",
    legend_loc_2="lower left",
    legend_title="Demand Patterns",
    font_color="k",
    legend_sig_figs=3,
    pumps=False,  # Disable pump plotting
    valves=False,
)

plt.show()