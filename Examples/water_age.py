import visnet.network as visinit
import visnet.drawing as visplot
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import os

# Run EPANET2.0 Simulation and store results
model = visinit.initialize_model(r"Networks\CTown.inp")  

# Define figure to be drawn to
fig, ax = plt.subplots(figsize=(12, 12))  

# Disables frame around figure
ax.set_frame_on(False)

visplot.plot_discrete_nodes(
    model,
    ax,
    parameter="quality",
    value='max',
    unit="hr",
    bin_edge_num=5,
    bins=[0,6,12,24],
    bin_size_list=[100, 150, 250, 400], #Node sizes
    bin_border_list=["k", "k", "k", "k"],
    bin_border_width_list=[1, 1, 1, 1],
    cmap='Greens',
    legend_loc_2="lower left",
    legend_title="Max Water Age (hr)",
    font_color="k",
    legend_title_font_size="16",
    legend_sig_figs=0, #No decimal places
    pumps=False,
    valves=False,
)
plt.show()
