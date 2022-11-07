import visnet as vis
import wntr
import matplotlib.pyplot as plt


# Define figure to be drawn to
fig, ax = plt.subplots(figsize=(12, 12))

# Disables frame around figure
ax.set_frame_on(False)
wn = wntr.network.WaterNetworkModel(r"Networks/CTown.inp")
wn.options.quality.parameter = "TRACE"
wn.options.quality.trace_node = "T1"
model = vis.visnet_model(r"Networks/CTown.inp", network_model=wn)
#Plots trace quality parameter
model.plot_discrete_nodes(
    ax,
    parameter="quality",value="max",
    legend_loc_2="lower left",legend_title="Max Trace from T1 (%)",
    valves=False,pumps=False,
    legend_sig_figs=0
)
#Draws label over tank T1
model.draw_label(
    ax,
    labels=["T1"],nodes=["T1"],
    x_coords=[0],y_coords=[150],
    draw_arrow=False,label_font_size=9,
)
plt.show()
