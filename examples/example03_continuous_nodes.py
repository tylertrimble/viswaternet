"""
This example demonstrates how to plot node data by assigning node color according to a colorbar.
"""

# Import libraries
import viswaternet as vis
import matplotlib.pyplot as plt

# Initialize VisWaterNet model
model = vis.VisWNModel('Networks/CTown.inp')
style = vis.NetworkStyle(node_size=200,
                         draw_tanks=False,  # do not draw tanks on the plot
                         dpi=400)
model.plot_continuous_nodes(parameter="pressure",
                            value=10,
                            style=style)
plt.show()
style_2 = vis.NetworkStyle(node_size=200,
                         draw_tanks=False,  # do not draw tanks on the plot
                         dpi=400,
                         cmap='Greens')
model.plot_continuous_nodes(parameter="pressure",
                            value=11,
                            style=style_2)
plt.show()
#%%
style.revert_style_args(cmap='Greens')
model.plot_continuous_nodes(parameter="pressure",
                            value=12,
                            style=style)
plt.show()
