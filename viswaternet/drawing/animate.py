# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import imageio
from viswaternet.network import processing
from viswaternet.utils import unit_conversion, convert_excel
def animate_plot(
        self,
        function,
        ax=None,
        fps=3,
        first_timestep=0,
        last_timestep=None,
        save_name="animation",
        save_format="mp4",
        time_unit='s',
        **kwargs):
    """
    Builds .gif file animating network data across timesteps.
    
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
    model = self.model
    if ax is None:
        if ax is None:
            fig, ax = plt.subplots(figsize=self.figsize)
            ax.set_frame_on(self.axis_frame)
    frames = []
    if function == self.plot_unique_data:
        parameter_type = kwargs.get("parameter_type", None)
        data_type = kwargs.get("data_type", None)
        try:
            custom_data_values = kwargs.get("custom_data_values")
            data_values = pd.Series(custom_data_values[1],
                                    custom_data_values[0])
        except TypeError:
            excel_columns = kwargs.get("excel_columns", None)
            element_list, results = convert_excel(
                self, kwargs.get("data_file", None),
                parameter_type,
                data_type,
                excel_columns[0],
                excel_columns[1])
            # data_values.append(data['results'])
            data_values = results
        timesteps = data_values.shape[1]
        values = range(timesteps)
        if last_timestep is not None:
            values = values[first_timestep:last_timestep]
        if data_type == "continuous":
            if kwargs.get("vmin", None) is None \
                    or kwargs.get("vmax", None) is None:
                kwargs["vmin"], kwargs["vmax"] = make_vmin_vmax(data_values,
                                                                kwargs)
        if data_type == 'discrete':
            kwargs["disable_interval_deleting"] = True
            if kwargs.get("intervals", None) is None:
                kwargs["intervals"] = make_intervals(data_values, kwargs)
        data_values = [data_values[i].tolist() 
                       for i in data_values.columns]
    else:
        timesteps = int(
            model["wn"].options.time.duration
            / model["wn"].options.time.report_timestep)
        values = range(timesteps)
        if last_timestep is not None:
            values = values[first_timestep:last_timestep]
    if function == self.plot_continuous_nodes \
            or function == self.plot_discrete_nodes:
        parameter_type = 'node'
    elif function == self.plot_continuous_links \
            or function == self.plot_discrete_links:
        parameter_type = 'link'
    if function == self.plot_continuous_nodes \
            or function == self.plot_continuous_links:
        if kwargs.get("vmin", None) is None \
                or kwargs.get("vmax", None) is None:
            parameter_results, element_list = processing.get_parameter(
                self,
                parameter_type,
                kwargs.get("parameter"), kwargs.get("value", None))
            kwargs["vmin"], kwargs["vmax"] = make_vmin_vmax(parameter_results,
                                                            kwargs)
            parameter_results = parameter_results.transpose()
    if function == self.plot_discrete_nodes \
            or function == self.plot_discrete_links:
        kwargs["disable_interval_deleting"] = True
        if kwargs.get("intervals", None) is None:
            parameter_results, element_list = processing.get_parameter(
                self, parameter_type, kwargs.get(
                    "parameter"), kwargs.get("value", None))
            kwargs["intervals"] = make_intervals(parameter_results, kwargs)
        parameter_results = parameter_results.transpose()
    for value in values:
        plt.ioff()
        fig = ax.get_figure()
        if function == self.plot_unique_data:
            try:
                kwargs["custom_data_values"] = [custom_data_values[0],
                                                custom_data_values[1][value]]
            except Exception:
                kwargs["custom_data_values"] = [element_list,
                                           data_values[value]]
                kwargs["parameter"] = 'custom_data'
            function(ax=ax, savefig=False, **kwargs)
        else:
            kwargs["value"] = [parameter_results.iloc[:,value],
                               element_list]
            function(ax=ax, savefig=False, **kwargs)
        handles, labels = [], []
        time = value*model["wn"].options.time.report_timestep
        time = unit_conversion(time, "time", time_unit)
        ax.legend(
            handles,
            labels,
            title="Timestep "+str(time)+" "+time_unit,
            loc="lower left",
            frameon=False)
        fig.canvas.draw()
        mat = np.array(fig.canvas.renderer._renderer)
        frames.append(mat)
        try:
            if function == self.plot_continuous_nodes \
                    or function == self.plot_continuous_links \
                    or data_type == 'continuous':
                fig.axes[1].remove()
        except Exception:
            if function == self.plot_continuous_nodes \
                    or function == self.plot_continuous_links:
                fig.axes[1].remove()
        ax.clear()
    if save_format == "gif" or save_format == "GIF":
        imageio.mimsave(save_name+"."+save_format,
                        frames,
                        format='GIF',
                        fps=fps)

    else:
        imageio.mimsave(save_name+"."+save_format,
                        frames,
                        format='FFMPEG',
                        fps=fps,
                        quality=8,
                        ffmpeg_log_level='quiet')

def make_vmin_vmax(parameter, kwargs):
    for value in np.min(parameter, axis=0):
        if value < -1e-5:
            if kwargs.get("vmin", None) is None:
                vmin = - \
                    np.max(np.max(parameter, axis=0))
            if kwargs.get("vmax", None) is None:
                vmax = np.max(
                    np.max(parameter, axis=0))
            break
        else:
            if kwargs.get("vmin", None) is None:
                vmin = np.min(
                    np.min(parameter, axis=0))
            if kwargs.get("vmax", None) is None:
                vmax = np.max(
                    np.max(parameter, axis=0))
    return vmin, vmax


def make_intervals(parameter, kwargs):
    intervals = np.linspace(
        np.min(np.min(parameter, axis=0), axis=0),
        np.max(np.max(parameter, axis=0), axis=0),
        kwargs.get("num_intervals", 5)).tolist()
    return intervals
