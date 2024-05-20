"""
This example demonstrates how to plot link data by assigning link color according to a colorbar.
"""

# Import libraries
import viswaternet as vis
import matplotlib.pyplot as plt

# Initialize VisWaterNet model
model = vis.VisWNModel('Networks/CTown.inp')
style = vis.NetworkStyle(cmap='coolwarm',
                         link_width=(2, 6),  # this argument varies link widths to match the associated data
                         dpi=400)
model.plot_continuous_links(parameter="flowrate", value='mean',
                            style=style)

plt.show()
