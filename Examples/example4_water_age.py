"""
This example demonstrates how VisWaterNet can visualize water distribution network simulation results. 
Here, we plot the maximum water age (throughout the simulation duration) at each node.
"""

# Import libraries
import viswaternet as vis
import matplotlib.pyplot as plt

# Initialize VisWaterNet model
model = vis.VisWNModel(r"Networks/CTown.inp")  

# Initialize plot
fig, ax = plt.subplots(figsize=(12, 12))  

# Hide frame on plot
ax.set_frame_on(False)

# Plot maximum water age in hours
model.plot_discrete_nodes(
    ax,
    parameter="quality",value='max',unit="hr", # The "value" parameter can take in a time step multiplier or one of the following: mean, min, max, range
    num_intervals=5,intervals=[0,6,12,24,48],
    interval_node_size_list=[100,150,250,350,450], # Node sizes corresponding to each interval
    interval_node_border_color_list=['k','k','k','k','k'],
    interval_node_border_width_list=[1,1,1,1,1],
    cmap='Greens',legend_loc_2="lower left",
    legend_title="Max Water Age (hr)",font_color="k",
    legend_title_font_size="16",
    legend_sig_figs=0) # No decimal places

plt.show()
