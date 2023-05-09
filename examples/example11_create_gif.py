"""
This example demonstrates how to plot and save time-varying data as GIFs
"""

# Import libraries
import viswaternet as vis
import matplotlib.pyplot as plt

# Initialize VisWaterNet model
model = vis.VisWNModel('Networks/CTown.inp')

# Initialize a Matplotlib figure and axis.
fig, ax = plt.subplots(figsize=(11,11))
ax.set_frame_on(False) 

model.animate_plot(function = model.plot_continuous_links,
                   ax=ax,
                   parameter = 'flowrate', cmap = 'coolwarm', 
                   first_timestep = 0, last_timestep = 40,
                   max_width = 5, min_width = 5, legend = False,
                   time_unit = 'hr', fps = 7, color_bar_title = 'Flowrate [m3/s]',
                   pump_color = 'green', save_name = 'figures/example6',file_format='mp4')    
plt.show()