# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 12:57:31 2022

@author: Tyler
"""
import visnet.network as visinit
import visnet.drawing as visplot
import matplotlib.pyplot as plt

from nodalerror_generation import wn,error_list,element_list
# Define figure to be drawn to
fig, ax = plt.subplots(figsize=(12, 12))  

# Disables frame around figure
ax.set_frame_on(False)

#Create water network model
model = visinit.initialize_model(r"Networks/CTown.inp", network_model=wn)

#Plot custom data generated in nodalerror_generation.py
visplot.plot_unique_data(
    model,ax,
    parameter="custom_data",node_size=200,line_widths=1,
    edge_colors="k",parameter_type="node",data_type="continuous",
    custom_data_values=[element_list, error_list],
    color_bar_title="Error (%)",cmap="bwr",draw_color_bar=True,
)

plt.show()
