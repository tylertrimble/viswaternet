"""
This example demonstrates how to plot and save time-varying custom generated data as GIFs
"""

# Import libraries
import viswaternet as vis
import matplotlib.pyplot as plt

# Initialize VisWaterNet model
model = vis.VisWNModel('Networks/CTown.inp')
style = vis.NetworkStyle(cmap = 'coolwarm',
                         dpi=400)
# Initialize a Matplotlib figure and axis.
fig, ax = plt.subplots(figsize=(11,11))
ax.set_frame_on(False) 

model.animate_plot(function = model.plot_unique_data,
                   
                   ax=ax,
                   
                   parameter="excel_data",
                   data_file = "Excel/node_numerical_data_random.xlsx", excel_columns = [0,list(range(1,35))],
                   parameter_type = 'node',
                   data_type = 'continuous',
                   time_unit = 'hr', fps = 3, color_bar_title = 'Flowrate [m3/s]',
                   save_name = 'figures/example15',save_format='mp4')    
plt.show()