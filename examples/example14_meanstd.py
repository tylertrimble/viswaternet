"""
This example demonstrates how one can use VisWaterNet to visualize two different summary measures within a single plot.
Here, we plot the mean value (color) and standard deviation (size) of nodal pressure.
"""

# Import libraries
import viswaternet as vis
import matplotlib.pyplot as plt

# Initialize VisWaterNet model
model = vis.VisWNModel('Networks/CTown.inp')  

fig, ax = plt.subplots(figsize=(11,11))
ax.set_frame_on(False) 
# Obtain mean and standard deviation measures corresponding to each node
#Get mean pressure at each node
mean, elmnt_list = model.get_parameter("node",parameter="pressure",value="mean")
#Get standard deviation at  each node
stddev, elmnt_list = model.get_parameter("node",parameter="pressure",value="stddev")
#Bin standard deviation values
binnedParameter, interval_names = model.bin_parameter(stddev, elmnt_list, 4)
#Set bin_sizes and create node_sizes array
interval_sizes = [150, 250, 350, 450]
node_sizes = [None]*len(elmnt_list)
#Set node_sizes according to bin_sizes
for interval_name, size in zip(interval_names, interval_sizes):
    for element in binnedParameter[interval_name]:
        node_sizes[elmnt_list.index(element)]=size
        
# Plot continuous mean data and pass custom node_sizes to correspong to standard deviation
model.plot_unique_data(ax = ax, parameter = "custom_data",
                       parameter_type = "node", data_type = "continuous",    
                       custom_data_values = [elmnt_list,mean],    
                       color_bar_title = "Mean Pressure (m)",
                       cmap = "winter_r", node_size = node_sizes,
                       element_size_intervals = 4,
                       element_size_legend_title="Standard Deviation (m)",
                       element_size_legend_loc="lower left",
                       element_size_legend_labels=interval_names)
#Called in the case that interactive plotting isn't enabled
plt.show()