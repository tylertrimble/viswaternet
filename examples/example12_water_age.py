"""
This example demonstrates how to plot EPANET simulation results
"""

import viswaternet as vis
import matplotlib.pyplot as plt

# Create visnet model
model = vis.VisWNModel('Networks/CTown.inp')
style = vis.NetworkStyle(node_size=[100, 150, 250, 350, 450],
                         node_border_color='k',
                         node_border_width=1,
                         cmap='Greens', discrete_legend_loc="lower left",
                         discrete_legend_title_font_size="16",
                         legend_decimal_places=0,
                         dpi=400)
# Plot maximum water age in hours
model.plot_discrete_nodes(parameter="quality", value='max', unit="hr",
                          intervals=[0, 6, 12, 24, 48],
                          style=style)
plt.show()
