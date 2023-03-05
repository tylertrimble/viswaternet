"""
This example demonstrates how VisWaterNet's disrete plotting capabilties can be utilized to highlight specific properties for network elements. 
Here, all links with diameter >= 12 inches are colored red and have link width 5 pixels. All other links are black and have width 1 pixel.
"""

# Import libraries
import viswaternet as vis
import matplotlib.pyplot as plt

# Initialize VisWaterNet model
model = vis.VisWNModel(r"Networks/CTown.inp")  

# Plot links with diameters < 12 and >= 12 inches
model.plot_discrete_links(
    parameter="diameter", 
    unit="in", 
    num_intervals=1,
    intervals=[0,11.999],
    interval_label_list=["< 12",">= 12"],
    interval_link_width_list=[1,5],
    color_list=['k','r'],
    cmap="Blues", # Controls link widths
    legend_loc_2="lower left", # Location of legend with intervals
    legend_title="Pipe Diameter (in)",
    legend_sig_figs=0, # Whole numbers only
    pump_color="mediumseagreen", 
    pump_width=5) # In pixels

#Called in the case that interactive plotting isn't enabled
plt.show()
