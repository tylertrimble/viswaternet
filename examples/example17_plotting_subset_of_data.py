"""
In this example, we plot a subset of our custom generated data.
"""

# Import libraries
import viswaternet as vis
import matplotlib.pyplot as plt
import wntr
import random


wn = wntr.network.WaterNetworkModel('Networks/CTown.inp')
sim = wntr.sim.EpanetSimulator(wn)
results = sim.run_sim()

link_num_data = []
node_num_data = []
link_cat_data = []
node_cat_data = []

random.seed(1)
    
# Generate random numerical and categorical data for each node
for junction_name, junction in wn.junctions():
    node_num_data.append(random.uniform(20.0, 40.0))    
    if junction.demand_timeseries_list[0].base_value < 0.0007:
        node_cat_data.append('Low demand')
    elif junction.demand_timeseries_list[0].base_value < 0.001  and  junction.demand_timeseries_list[0].base_value >= 0.0007:
        node_cat_data.append('Medium demand')
    else:
        node_cat_data.append('High demand')

# Initialize VisWaterNet model
model = vis.VisWNModel('Networks/CTown.inp')
style = vis.NetworkStyle(node_size = 200,
                         base_link_width = 1,
                         base_link_color = "purple",
                         cmap = "bwr",
                         base_node_size = 50,
                         base_node_color = 'k',
                         dpi=400)
model.plot_unique_data(parameter = "custom_data",
                       parameter_type = "node", data_type = "continuous",    
                       custom_data_values = [wn.junction_name_list[:100], node_num_data[:100]],
                       color_bar_title = "Error (%)",
                       style=style) 
plt.show()