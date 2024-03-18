"""
This example demonstrates how to plot node data by assigning node color based on intervals of data.
"""

# Import libraries
import viswaternet as vis
import matplotlib.pyplot as plt

# Initialize VisWaterNet model
model = vis.VisWNModel('Networks/CTown.inp')

model.plot_discrete_nodes(parameter = "demand", value = 10, 
                          num_intervals = 3,
                          unit = 'CMH',
                          discrete_legend_loc = 'upper left', 
                          discrete_legend_label_font_size = 15,
                          discrete_legend_label_color = 'interval_color', # match text color to color assigned to interval
                          legend_decimal_places = 1,
                          savefig = True, save_name = 'figures/example5', dpi=400)
plt.show()
