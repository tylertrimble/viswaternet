====================
Warning Messages
====================

Since VisWaterNet relies on several other packages, and these packages display warnings regarding changes in future package versions, missing data in the input file, etc., we decided not to suppress warning messages. Here, we have compiled a number of common warning messages we run into when using VisWaterNet. 

.. code:: python

    UserWarning: Not all curves were used in "/viswaternet/CTown.inp"; added with type None, units conversion left to user warnings.warn('Not all curves were used in "{}"; added with type None, units conversion left to user'.format(self.wn.name))
    
WNTR displays this warning when the .INP input file contains curves (e.g., to model pump behavior) or patterns (e.g., describing the time-varying demand at junctions) that are not assigned to pumps or junctions. This 

