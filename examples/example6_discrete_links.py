"""
This example demonstrates how to plot link data by assigning link color based on intervals of data.
"""

# Import libraries
import viswaternet as vis
import matplotlib.pyplot as plt

# Initialize VisWaterNet model
model = vis.VisWNModel('Networks/CTown.inp')

model.plot_discrete_links(parameter = 'velocity', value = 'max', intervals = [0,2,6,10],
                          legend_sig_figs = 0,
                          legend_loc_2 = 'lower left', unit = 'ft/s',
                          save_name = 'figures/example6', dpi=400)
plt.show()