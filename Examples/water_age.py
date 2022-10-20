import visnet.network as visinit
import visnet.drawing as visplot
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import os

model = visinit.initialize_model(r"Networks\CTown.inp")

cwd = os.getcwd()
model["image_path"] = cwd + "\Images"

fig, ax = plt.subplots(figsize=(12, 12))

ax.set_frame_on(False)

visplot.plot_discrete_nodes(
    model,
    ax,
    parameter="quality",
    value=112,
    unit="hr",
    bin_edge_num=5,
    bin_size_list=[100, 150, 250, 400], #Node sizes
    bin_border_list=["k", "k", "k", "k"],
    bin_border_width_list=[1, 1, 1, 1],
    cmap='Blues',
    legend_loc_2="lower left",
    legend_title="Water Age (hr) at 28 Hours",
    font_color="k",
    legend_title_font_size="16",
    legend_sig_figs=0, #No decimal places
    pumps=False,
    valves=False,
)
plt.show()
