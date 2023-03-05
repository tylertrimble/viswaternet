"""
In this example, we demonstrate how VisWaterNet can be used to display custom data. We generate data corresponding to each node
in the file "example5_nodalerror_generation.py" and visualize it here. Since the dataset includes both positive and negative values, the colorbar is centered at 0.

"""

# Import libraries
import viswaternet as vis
import matplotlib.pyplot as plt

# Import custom data to be plotted from separate .py file
from example5_nodalerror_generation import wn,error_list,element_list

# Initialize VisWaterNet model
model = vis.VisWNModel(r"Networks/CTown.inp", network_model=wn)

# Plot custom data 
model.plot_unique_data(
    parameter="custom_data",node_size=200,line_widths=1,
    edge_colors="k",parameter_type="node",data_type="continuous",
    custom_data_values=[element_list, error_list],
    color_bar_title="Error (%)",cmap="bwr",draw_color_bar=True)

#Called in the case that interactive plotting isn't enabled
plt.show()
