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
                       link_width = np.linspace(1,7,10),
                       cmap = "Blues", 
                       discrete_legend_loc = "upper left", 
                       legend_title = "Pipe Diameter (in)", 
                       discrete_legend_label_font_size = 12,
                       legend_decimal_places = 0, 
                       pump_color = "red", 
                       valve_color = 'orange',
                       savefig = True, save_name = 'figures/example8', dpi=400)  

plt.show()
