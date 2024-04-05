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
model.plot_basic_elements(ax, 
                          pump_size=200,
                          reservoir_size=500,
                          tank_color = 'g', 
                          base_legend_loc = 'lower left', 
                          savefig = True, save_name = 'figures/example2', dpi=400)
plt.show()
