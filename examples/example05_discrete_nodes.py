"""
This example demonstrates how to plot node data by assigning node color based on intervals of data.
"""

# Import libraries
import viswaternet as vis
import matplotlib.pyplot as plt

# Initialize VisWaterNet model
model = vis.VisWNModel('Networks/CTown.inp')

model.plot_discrete_nodes(parameter = "demand", value = 10, num_intervals = 3,
                          discrete_legend_label_font_color = 'interval_color',
                          discrete_legend_loc = 'upper left', unit = 'CMH',
                          save_name = 'figures/example5', dpi=400)
plt.show()
