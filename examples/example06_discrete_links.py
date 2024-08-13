"""
This example demonstrates how to plot link data by assigning link color based on intervals of data.
"""

# Import libraries
import viswaternet as vis
import matplotlib.pyplot as plt

# Initialize VisWaterNet model
model = vis.VisWNModel('Networks/CTown.inp')
style = vis.NetworkStyle(discrete_legend_loc = 'lower left',
                        legend_decimal_places = 0,
                        dpi=400)

model.plot_discrete_links(parameter = 'velocity', value = 'max', 
                          unit = 'ft/s',
                          intervals = [0,2,6,10],
                          savefig = True, save_name = 'figures/example06',
                          style=style)
plt.show()
