"""
This example demonstrates how to plot link data by assigning link color according to a colorbar.
"""

# Import libraries
import viswaternet as vis
import matplotlib.pyplot as plt

# Initialize VisWaterNet model
model = vis.VisWNModel('Networks/CTown.inp')

model.plot_continuous_links(parameter = "flowrate", value = 'mean', cmap = 'coolwarm', 
                            min_width = 2, max_width = 6, save_name = 'figures/example4', dpi=400)

plt.show()

