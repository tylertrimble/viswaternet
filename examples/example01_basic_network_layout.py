"""
This example demonstrates the basic plotting fuctionality that the function plot_basic_elements provides, without any additional data attached to each element of the network.
The plot_basic_elements function generates a view of the network layout, depicting the locations of nodes (junctions, tanks, and reservoirs) and links (pipes, pumps, and valves).
"""

# Import libraries
import viswaternet as vis
import matplotlib.pyplot as plt

# Initialize VisWaterNet model
model = vis.VisWNModel('Networks/CTown.inp')

# Plot basic network layout 
model.plot_basic_elements()
plt.show()
