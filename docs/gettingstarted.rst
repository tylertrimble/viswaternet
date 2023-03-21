=======
Getting Started 
=======

To get started, import VisWaterNet:

.. code:: python

    import viswaternet as vis

Next, initialize a VisWaterNet model. For example purposes, we use the CTown network included in the Examples folder:

.. code:: python

    model = vis.VisWNModel('Networks/CTown.inp')
    
Finally, call on any of the plotting functions with the argument inputs of your choice. For example, the following line of code generates a discrete plot for maximum nodal pressure in units of psi:

.. code:: python

    model.plot_discrete_nodes(ax, parameter="pressure", value='max', unit="psi")

If the plot does not show up after you run the script, it is possible that your IDE does not support interactive plotting (e.g., IDLE) or interactive mode is off. To see the plot, add the following line to display the figures: 

.. code:: python

    plt.show()

Since several VisWaterNet function arguments rely on Matplotlib visualization inputs, it is recommended to visit the `Matplotlib docs`_ to view customization options for `colors`_, `colorbars`_, `node markers`_, `line styles`_, etc.


A range of examples to understand the different VisWaterNet plotting functions can be found in the `Example Applications`_ section in the documentation and in the the `Examples`_ folder.

.. _`Matplotlib docs`: https://matplotlib.org/stable/index.html
.. _`colors`: https://matplotlib.org/stable/gallery/color/named_colors.html
.. _`colorbars`: https://matplotlib.org/stable/tutorials/colors/colormaps.html#sphx-glr-tutorials-colors-colormaps-py
.. _`node markers`: https://matplotlib.org/stable/gallery/lines_bars_and_markers/marker_reference.html
.. _`line styles`: https://matplotlib.org/stable/gallery/lines_bars_and_markers/linestyles.html
.. _`Example Applications`: https://viswaternet.readthedocs.io/en/latest/examples.html
.. _`Examples`: https://github.com/tylertrimble/viswaternet/tree/main/examples
