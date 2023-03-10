"""
This example demonstrates how VisWaterNet can be used to highlight the distinct pipe diameters present in a water distribution network by modifying both link color and width.
"""

# Import libraries
import viswaternet as vis
import matplotlib.pyplot as plt
import numpy as np

# Initialize VisWaterNet model
model = vis.VisWNModel('Networks/CTown.inp')  

# Plot unique pipe diameters
model.plot_unique_data(parameter = "diameter", 
                       unit = "in", 
                       interval_link_width_list = np.linspace(1,7,10),
                       cmap = "Blues", 
                       legend_loc_2 = "upper left", 
                       legend_title = "Pipe Diameter (in)", font_size = 12,
                       legend_sig_figs = 0, 
                       pump_color = "red", 
                       pump_width = 2,
                       save_name = 'figures/example8', dpi=400)  

plt.show()
