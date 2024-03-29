"""
This example demonstrates how VisWaterNet can be used to illustrate the different nodal demand patterns present in a water distribution network.
"""

# Import libraries
import viswaternet as vis
import matplotlib.pyplot as plt

# Initialize VisWaterNet model
model = vis.VisWNModel('Networks/CTown.inp')

model.plot_unique_data(parameter = "demand_patterns", cmap = 'tab10',
                       node_size = 200,
                       discrete_legend_loc = 'lower left', 
                       legend_title = 'Demand Patterns',
                       discrete_legend_title_font_size = 13, discrete_legend_label_font_size = 13,
                       label_list = ['Pattern 1', 'Pattern 2', 'Pattern 3',
                                     'Patten 4', 'Pattern 5', 'No Pattern'],
                      savefig = True, save_name = 'figures/example7', dpi = 400)
plt.show()

