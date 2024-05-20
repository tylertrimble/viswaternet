"""
This example demonstrates how VisWaterNet can be used to highlight the distinct pipe diameters present in a water distribution network by modifying both link color and width.
"""

# Import libraries
import viswaternet as vis
import matplotlib.pyplot as plt
import numpy as np

# Initialize VisWaterNet model
model = vis.VisWNModel('Networks/CTown.inp')  
style = vis.NetworkStyle(cmap='Blues',
                         discrete_legend_loc='upper left',
                         discrete_legend_label_font_size=12,
                         legend_decimal_places=0,
                         link_width=np.linspace(1, 7, 10),
                         pump_color="red",
                         valve_color='orange',
                         dpi=400)
# Plot unique pipe diameters
model.plot_unique_data(parameter = "diameter", 
                       unit = "in", 
                       discrete_legend_title = "Pipe Diameter (in)", 
                       savefig = True,
                       style=style)  

plt.show()
