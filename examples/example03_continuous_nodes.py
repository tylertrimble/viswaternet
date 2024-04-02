"""
This example demonstrates how to plot node data by assigning node color according to a colorbar.
"""
# Import libraries
import viswaternet as vis
import matplotlib.pyplot as plt

# Initialize VisWaterNet model
model = vis.VisWNModel('Networks/CTown.inp')

model.plot_continuous_nodes(parameter = "pressure", value = 10, 
                            node_size=200, 
                            save_name = 'figures/example3', dpi=400,
                            include_reservoirs=False)
plt.show()
