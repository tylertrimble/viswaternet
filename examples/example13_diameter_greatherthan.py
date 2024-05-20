"""
This example demonstrates how to use the plot_discrete_links function to show binary differences.
"""

import viswaternet as vis
import matplotlib.pyplot as plt

model = vis.VisWNModel('Networks/CTown.inp')
style = vis.NetworkStyle(link_width=[3, 5],
                         color_list=['k', 'r'], cmap="Blues",
                         discrete_legend_loc="lower left",
                         pump_color="mediumseagreen",
                         dpi=400)
model.plot_discrete_links(parameter="diameter", unit="in",
                          num_intervals=2, intervals=[0, 11.999],
                          label_list=["< 12", ">= 12"],
                          discrete_legend_title="Pipe Diameter (in)",
                          style=style)
plt.show()
