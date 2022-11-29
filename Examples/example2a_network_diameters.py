"""
This example demonstrates how VisWaterNet can be used to highlight the distinct pipe diameters present in a water distribution network by modifying both link color and width.
"""

# Import libraries
import viswaternet as vis
import matplotlib.pyplot as plt
import numpy as np

# Initialize VisWaterNet model
model = vis.VisWNModel(r"Networks/CTown.inp")  

# Initialize plot
fig, ax = plt.subplots(figsize=(12, 12))  

# Hide frame on plot
ax.set_frame_on(False)

# Plot unique pipe diameters
model.plot_unique_data(
    ax, parameter="diameter", 
    unit="in", 
    interval_link_width_list=np.linspace(1,7,10),
    cmap="Blues", # Controls link widths
    legend_loc_2="lower left", # Location of legend with bins
    legend_title="Pipe Diameter (in)",font_size=12,
    legend_sig_figs=0, # Whole numbers only
    pump_color="mediumseagreen", # Customize pump color and width
    pump_width=5 # In Pixels )
    
plt.show()
