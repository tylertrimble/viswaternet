"""
In this example, we plot a subset of our custom generated data.
"""

# Import libraries
import viswaternet as vis
import matplotlib.pyplot as plt
import wntr
import random

# Generate data

wn = wntr.network.WaterNetworkModel('Networks/CTown.inp')
sim = wntr.sim.EpanetSimulator(wn)
results = sim.run_sim()

link_num_data = []
node_num_data = []
link_cat_data = []
node_cat_data = []

random.seed(1)

# Links
for index, pipe_name in enumerate(wn.pipe_name_list):
    if index < 50:
        link_num_data.append(random.uniform(2.5, 10.0))   
    else:
        link_num_data.append(random.uniform(17.0, 20.0)) 
    if (results.link['flowrate'].loc[:,pipe_name] < 0).any():
        link_cat_data.append('Reverse flow')
    else:
        link_cat_data.append('No reverse flow')
    

# Initialize VisWaterNet model
model = vis.VisWNModel('Networks/CTown.inp')
style = vis.NetworkStyle(node_size = 200,
                         base_link_width = 1,
                         base_link_color = "green",
                         cmap = "coolwarm",
                         base_node_size = 50,
                         base_node_color = 'k',
                         link_width = 2, 
                         discrete_legend_loc = 'lower left',
                         dpi=400)
# Initialize a Matplotlib figure and axis.
fig, ax = plt.subplots(1,2,figsize=(22,11))
ax[0].set_frame_on(False) 
ax[1].set_frame_on(False) 

# Plot data with equal intervals defined across the full range of data
model.plot_unique_data(ax=ax[0], parameter = "custom_data", 
                       parameter_type = "link", data_type = "discrete",    
                       custom_data_values = [wn.pipe_name_list[:100], link_num_data[:100]],
                       color_bar_title = "Error (%)", 
                       disable_interval_deleting = False,
                       style=style) 

# Do not include empty intervals (i.e., intervals with no data points)
model.plot_unique_data(ax=ax[1], parameter = "custom_data",
                       parameter_type = "link", data_type = "discrete",    
                       custom_data_values = [wn.pipe_name_list[:100], link_num_data[:100]],
                       color_bar_title = "Error (%)",
                       disable_interval_deleting = True,
                       style=style) 

# Save figure
fig.tight_layout()
fig.savefig('figures/example18', dpi=400)
plt.show()