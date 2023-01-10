# -*- coding: utf-8 -*-
"""
The viswaternet.drawing.animate module facilitates the creation of .gif files
animating data across timesteps.
"""
import numpy as np
import matplotlib.pyplot as plt
import imageio
import os
from viswaternet.network import processing
from viswaternet.drawing import discrete, continuous
from viswaternet.utils import unit_conversion

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
    """Builds .gif file animating network data across timesteps.
    
    Arguments
    ---------
    ax : axes._subplots.AxesSubplot
        Matplotlib axes object.
    
    function : viswaternet
        One of the general viswaternet drawing functions.
        
        .. rubric:: Usable Functions
    
        ================================= ==
            plot_basic_elements
            plot_discrete_nodes
            plot_discrete_links
            plot_continuous_nodes
            plot_continuous_links
            plot_unique_data
        ================================= ==
        
    data_type : string
        The type of data that the excel data is (Unique, continuous, or discrete.)
        
    parameter_type : string
        Type of parameter (nodal, link)
        
    fps : integer
        Framerate that the .gif file will be generated with.
        
    first_timestep : integer
        The starting timestep of the .gif file.
        
    last_timestep : integer
        The last timestep of the .gif file.
        
    unit : string
        The time unit that will be reported for each frame of the .gif file.
        
        .. rubric:: Time Units

        ====================  ====================================
        Default               :math:`s`
        min                   :math:`min`
        hr                    :math:`hr`
        day                   :math:`day`
        ====================  ====================================
    
    kwargs : Any
        Any arguments for the plotting function passed into the function argument
        can be passed into animate_plot.
    """
    
    model=self.model
    timesteps = int(
        model["wn"].options.time.duration / model["wn"].options.time.report_timestep
    )
    values = range(timesteps)
    if last_timestep is not None:
        values = values[first_timestep:last_timestep]

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
            for value in np.min(parameter_results,axis=0):
                if value < -1e-5:
                    if kwargs.get("vmin", None) is None:
                        kwargs["vmin"] = -np.max(np.max(parameter_results,axis=0))
                    if kwargs.get("vmax", None) is None:
                        kwargs["vmax"] = np.max(np.max(parameter_results,axis=0))
                    break
                else:
                    if kwargs.get("vmin", None) is None:
                        kwargs["vmin"] = np.min(np.min(parameter_results,axis=0))
                    if kwargs.get("vmax", None) is None:
                        kwargs["vmax"] = np.max(np.max(parameter_results,axis=0))
    if data_type == "discrete":
        kwargs["disable_interval_deleting"] = True

        if kwargs.get("intervals", None) is None:
            if parameter_type == "link":
                parameter_results, link_list = processing.get_parameter(
                    self, "link", kwargs.get("parameter"), kwargs.get("value", None)
                )
            if parameter_type == "node":
                parameter_results, node_list = processing.get_parameter(
                    self, "node", kwargs.get("parameter"), kwargs.get("value", None)
                )
            kwargs["intervals"] = np.linspace(
                np.min(np.min(parameter_results,axis=0),axis=0),
                np.max(np.max(parameter_results,axis=0),axis=0),
                kwargs.get("num_intervals", 5),
            )
            print(len(kwargs["intervals"]))
    for value in values:

        function(ax, value=value, **kwargs)

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
        if (data_type=='continuous'):
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
