"""
This example demonstrates how VisWaterNet can be used to illustrate the different nodal demand patterns present in a water distribution network.
"""

# Import libraries
import viswaternet as vis
import matplotlib.pyplot as plt

# Initialize VisWaterNet model
model = vis.VisWNModel(r'Networks/CTown.inp')

model.plot_unique_data(
    parameter="demand_patterns",
    interval_node_size_list=[300,300,300,300,300,300],
    interval_label_list=['Pattern 1','Pattern 2','Pattern 3','Pattern 4','Pattern 5', 'No Pattern'],
    cmap="Dark2",
    legend_loc_2="lower left",legend_title="Demand Patterns",font_color="k", legend_sig_figs=3)

#Called in the case that interactive plotting isn't enabled
plt.show()