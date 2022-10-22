import visnet.network as visinit
import visnet.drawing as visplot
import matplotlib.pyplot as plt

# Run EPANET2.0 Simulation and store results
model = visinit.initialize_model(r"Networks/CTown.inp")  

# Define figure to be drawn to
fig, ax = plt.subplots(figsize=(12, 12))  

# Disables frame around figure
ax.set_frame_on(False)

mean, element_list = visinit.get_parameter(
    model, "node", parameter="pressure", value="mean"
)
standard_deviation, element_list = visinit.get_parameter(
    model, "node", parameter="pressure", value="stddev"
)

binnedParameter, bin_names = visinit.bin_parameter(
    model, standard_deviation, element_list, 5
)

bin_sizes = [100, 200, 300, 400]
node_sizes = []

for element in element_list:
    for bin_name, size in zip(bin_names, bin_sizes):
        if element in binnedParameter.get(bin_name):
            node_sizes.append(size)
bin_names = bin_names.tolist()
visplot.plot_unique_data(
    model,
    ax,
    parameter="custom_data",
    parameter_type="node",
    data_type="continuous",
    custom_data_values=[element_list, mean],
    color_bar_title="Mean Pressure (m)",
    cmap="gist_heat_r",
    node_size=node_sizes,
    element_size_bins=4,
    element_size_legend_title="Standard Deviation (m)",
    element_size_legend_loc="lower left",
    element_size_legend_labels=bin_names,
)
plt.show()
