"""
This example demonstrates how to plot link data by assigning link color according to a colorbar.
"""

# Import libraries
import viswaternet as vis
import matplotlib.pyplot as plt

# Initialize VisWaterNet model
model = vis.VisWNModel('Networks/CTown.inp')

model.plot_continuous_links(parameter = "flowrate", value = 'mean', 
                            cmap = 'coolwarm', 
                            link_width=(4,10), # this argument varies link widths to match the data associated with them
                            include
                            #save_name = 'figures/example4', dpi=400, savefig=True)

plt.show()
