=======
Getting Started 
=======

To get started, import both viswaternet and matplotlib.pyplot:

.. code:: python

    import viswaternet as vis
    import matplotlib.pyplot as plt

Next, initialize a matplotlib figure and viswaternet model. For example purposes we use the CTown network included in the Examples folder:

.. code:: python

    fig, ax = plt.subplots(figsize=(12, 12))
    model = vis.VisWNModel('Networks/CTown.inp')
    
Finally, call on any of the plotting functions with the argument inputs of your choice. For example, the following line of code generates a discrete plot for maximum nodal pressure in units of psi:

.. code:: python

    model.plot_discrete_nodes(ax, parameter="pressure", value='max', unit="psi")

If the plot does not show up after you run the script, it is possible that your IDE does not support interactive plotting (e.g., IDLE) or interactive mode is off. To see the plot, add the following line to display the figures: 

.. code:: python

    plt.show()

A range of examples to understand the different VisWaterNet plotting functions can be found in the `Example Applications`_ section in the documentation and in the the `Examples`_ folder.

.. _`Example Applications`: https://viswaternet.readthedocs.io/en/latest/examples.html
.. _`Examples`: https://github.com/tylertrimble/viswaternet/tree/master/Examples
