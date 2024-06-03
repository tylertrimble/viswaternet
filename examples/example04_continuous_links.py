"""
This example demonstrates how to plot link data by assigning link color according to a colorbar.
"""

# Import libraries
import viswaternet as vis
import matplotlib.pyplot as plt

# Initialize VisWaterNet model
model = vis.VisWNModel('Networks/CTown.inp')
style = vis.NetworkStyle(cmap='coolwarm',
                         link_width=(2, 6),
                         color_bar_width=0.8,
                         color_bar_height=0.03,
                         color_bar_loc='top',
                         color_bar_label_loc='top',
                         color_bar_label_font_size=14,
                         color_bar_label_font_color='b',
                         dpi=400)
model.plot_continuous_links(parameter="flowrate", value='mean',
                            style=style)

plt.show()
