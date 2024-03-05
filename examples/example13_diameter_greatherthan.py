"""
This example demonstrates how to use the plot_discrete_links function to showcase different element attributes.
"""

import viswaternet as vis
import matplotlib.pyplot as plt

model = vis.VisWNModel('Networks/CTown.inp')  

model.plot_discrete_links(parameter = "diameter", unit = "in", 
                          num_intervals = 2, intervals = [0,11.999],
                          label_list = ["< 12", ">= 12"],
                          link_width = [3,5],    
                          color_list = ['k','r'], cmap = "Blues", 
                          discrete_legend_loc="lower left", 
                          legend_title="Pipe Diameter (in)",
                          legend_decimal_places=0, pump_color="mediumseagreen", 
                          pump_width=5, save_name = 'figures/example13', dpi=400)
plt.show()
