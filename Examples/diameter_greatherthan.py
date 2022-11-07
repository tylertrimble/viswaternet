# -*- coding: utf-8 -*-
"""
Created on Sat Oct 22 16:03:53 2022

@author: Tyler
"""

import visnet as vis
import matplotlib.pyplot as plt

# Run EPANET2.0 Simulation and store results
model = vis.visnet_model(r"Networks/CTown.inp")  

# Define figure to be drawn to
fig, ax = plt.subplots(figsize=(12, 12))  

# Disables frame around figure
ax.set_frame_on(False)


model.plot_discrete_links(
    ax, 
    parameter="diameter", 
    unit="in", 
    num_intervals=2,
    intervals=[0,11.999],
    interval_label_list=["< 12",">= 12"],
    interval_link_width_list=[1,5],
    color_list=['k','r'],
    cmap="Blues", #Controls link widths
    legend_loc_2="lower left", #Location of legend with intervals
    legend_title="Pipe Diameter (in)",
    legend_sig_figs=0, #Whole numbers only
    pump_color="mediumseagreen", 
    pump_width=5, #In Pixels
)
plt.show()
