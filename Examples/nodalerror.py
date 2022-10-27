# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 12:57:31 2022

@author: Tyler
"""

import wntr

import visnet.network as visinit
import visnet.drawing as visplot
import random
import matplotlib.pyplot as plt

# Define figure to be drawn to
fig, ax = plt.subplots(figsize=(12, 12))  

# Disables frame around figure
ax.set_frame_on(False)


#Create water network model
wn = wntr.network.WaterNetworkModel(r"Networks/CTown.inp")
model = visinit.initialize_model(r"Networks/CTown.inp", network_model=wn)
#Generation of error data
random.seed(1)
error_list = []
element_list = wn.junction_name_list
for _, junc in wn.junctions():
    try:
        pat = junc.demand_timeseries_list[0].pattern.name
        if pat == "DMA2_pat" or pat == "DMA5_pat" or pat == "DMA3_pat":
            error_list.append(0)
        else:
            error_list.append(random.uniform(-8, 5))
    except AttributeError:
        error_list.append(0)
#Plot nodal error data by treating it as custom data
visplot.plot_unique_data(
    model,ax,
    parameter="custom_data",node_size=200,line_widths=1,
    edge_colors="k",parameter_type="node",data_type="continuous",
    custom_data_values=[element_list, error_list],
    color_bar_title="Error (%)",cmap="bwr",draw_color_bar=True,
)

plt.show()