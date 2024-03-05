"""
This example demonstrates user-generated data stored in lists.
The data points in error_list correspond to the node names in the same indices in element_list
"""

import viswaternet as vis
import matplotlib.pyplot as plt

from example10_nodalerror_generation import wn,error_list,element_list

#Create water network model
model = vis.VisWNModel('Networks/CTown.inp', network_model=wn)

#Plot custom data generated in nodalerror_generation.py
model.plot_unique_data(parameter = "custom_data", node_size = 200,
                       node_border_width = 1, node_border_color = "k",
                       parameter_type = "node", data_type = "continuous",    
                       custom_data_values = [element_list, error_list],
                       color_bar_title = "Error (%)", cmap = "bwr",
                       save_name = 'figures/example10', dpi = 400)
plt.show()
