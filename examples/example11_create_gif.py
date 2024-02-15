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

model.animate_plot(function = model.plot_unique_data,
                   parameter="excel_data",
                   data_file = "Excel/node_numerical_data_random.xlsx",
                   parameter_type = 'node',
                   data_type = 'continuous',
                   excel_columns = [0,list(range(1,35))],
                   ax=ax, cmap = 'coolwarm',
                   time_unit = 'hr', fps = 7, color_bar_title = 'Flowrate [m3/s]',
                   save_name = 'figures/example11',file_format='mp4')    
plt.show()