# -*- coding: utf-8 -*-
"""
Created on Sun Oct  2 21:14:38 2022

@author: Tyler
"""
import numpy as np
import matplotlib.pyplot as plt
import imageio
import os
from visnetwork.network import processing
from visnetwork.drawing import discrete, continuous
from visnetwork.utils import unit_conversion

cbar = 0


def animate_plot(
    self,
    ax,
    function,
    data_type,
    parameter_type,
    fps=3,
    first_timestep=0,
    last_timestep=None,
    gif_save_name="gif",
    unit='s',
    **kwargs
):
    model=self.model
    timesteps = int(
        model["wn"].options.time.duration / model["wn"].options.time.report_timestep
    )
    values = range(timesteps)
    if last_timestep is not None:
        values = values[first_timestep:last_timestep]
    print(function is discrete.plot_discrete_links)
    filenames = []
    if data_type == "continuous":
        if kwargs.get("vmin", None) is None or kwargs.get("vmax", None) is None:
            if parameter_type == "link":
                parameter_results, link_list = processing.get_parameter(
                    self, "link", kwargs.get("parameter"), kwargs.get("value", None)
                )
            if parameter_type == "node":
                parameter_results, node_list = processing.get_parameter(
                    self, "node", kwargs.get("parameter"), kwargs.get("value", None)
                )
            for value in np.min(parameter_results):
                if value < -1e-5:
                    if kwargs.get("vmin", None) is None:
                        kwargs["vmin"] = -np.max(np.max(parameter_results))
                    if kwargs.get("vmax", None) is None:
                        kwargs["vmax"] = np.max(np.max(parameter_results))
                    break
                else:
                    if kwargs.get("vmin", None) is None:
                        kwargs["vmin"] = np.min(np.min(parameter_results))
                    if kwargs.get("vmax", None) is None:
                        kwargs["vmax"] = np.max(np.max(parameter_results))
    if data_type == "discrete":
        kwargs["disable_bin_deleting"] = True

        if kwargs.get("bins", None) is None:
            if parameter_type == "link":
                parameter_results, link_list = processing.get_parameter(
                    self, "link", kwargs.get("parameter"), kwargs.get("value", None)
                )
            if parameter_type == "node":
                parameter_results, node_list = processing.get_parameter(
                    self, "node", kwargs.get("parameter"), kwargs.get("value", None)
                )
            kwargs["bins"] = np.linspace(
                np.min(np.min(parameter_results)),
                np.max(np.max(parameter_results)),
                kwargs.get("bin_edge_num", 5),
            )
            print(len(kwargs["bins"]))
    for value in values:

        function(self, ax, value=value, **kwargs)

        handles, labels = [], []
        time=value*model["wn"].options.time.report_timestep
        time = unit_conversion(time, "time", unit)
        plt.legend(
            handles,
            labels,
            title="Timestep "+str(time)+" "+unit,
            loc="lower left",
            frameon=False,
        )

        plt.savefig(model["image_path"] + "/" + str(value) + ".png")

        filenames = np.append(
            filenames, model["image_path"] + "/" + str(value) + ".png"
        )
        ax.clear()
        if (
            function == continuous.plot_continuous_links
            or function == continuous.plot_continuous_nodes
        ):
            cbar.remove()
    # builds gif
    with imageio.get_writer(
        model["image_path"] + "/" + gif_save_name + ".gif", mode="I", fps=fps
    ) as writer:

        for filename in filenames:

            image = imageio.imread(filename)

            writer.append_data(image)
        for filename in set(filenames):

            os.remove(filename)
