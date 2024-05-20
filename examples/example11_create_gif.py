"""
This example demonstrates how to plot and save time-varying data as GIFs
"""

# Import libraries
import viswaternet as vis
import matplotlib.pyplot as plt

# Initialize VisWaterNet model
model = vis.VisWNModel('Networks/CTown.inp')

# Initialize a Matplotlib figure and axis.
fig, ax = plt.subplots(figsize=(11, 11))
ax.set_frame_on(False)
style = vis.NetworkStyle(link_width=(2, 4),
                         cmap='coolwarm',
                         pump_color='green',
                         dpi=400)
model.animate_plot(function=model.plot_continuous_links,  # the "function" argument takes in what kind of viswaternet function you would like to see in your animated plot
                   ax=ax,
                   parameter='flowrate',
                   last_timestep=24,
                   # arguments specific to animated plots
                   time_unit='hr', fps=7, color_bar_title='Flowrate [m3/s]',
                   save_name='figures/example11', save_format='gif',
                   style=style)
plt.show()
