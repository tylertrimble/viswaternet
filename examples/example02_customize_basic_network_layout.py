"""
In this example, we customize the basic network plot by changing the location of the legend, color of the tank marker, and pump line style.
We also draw the plot into a Matplotlib axis, which allows for subplotting and customization of figure size, frames, etc.
"""

# Import libraries
import viswaternet as vis
import matplotlib.pyplot as plt

# Initialize VisWaterNet model
model = vis.VisWNModel('Networks/CTown.inp')

# Initialize a Matplotlib figure and axis.
fig, ax = plt.subplots(figsize=(11,11))
ax.set_frame_on(False) 

# Customize and plot basic network layout 
model.plot_basic_elements(ax, valve_element = 'link', base_legend_loc = 'lower left', tank_color = 'g', 
                          draw_pumps=True)
plt.show()
