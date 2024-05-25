=======
History
=======
2.1.0 (2024-05-25)
-----------------------
* Added new style object
* Converted all functions to work with style objects

2.0.0 (2024-04-12)
-----------------------
* Added new label customization options
* Added ability to plot valves as links, and pumps as markers
* Added EPANET icons for pumps, valves, reservoirs, and tanks.
* Renamed, consolidated many arguments for clarity and to reduce # of aruments.
* Removed superfluous arguments.
* Added ability to make discrete legend text color align with interval color. 
* Legend label colors can now be changed independently for base legend and discrete legend.
* Title color for discrete legend can now be changed.
* Rewrote code to use data structures more consistently.
* Base links and nodes are now only drawn when necessary when not all nodes/links have data associated with them.
* Added ability to choose to include pump/valve or reservoir/tank data.
* Further improved animate plot speed for excel data plotting
* Animate plot output layout now conforms to normal plotting layout.
* Fixed discrete plotting when empty interval is present.
* Fixed animation issue where color bar label would be cut off.
* Fixed animation of custom data and excel data
* Fixed node size legend not properly showing up
* Fixed case where base elements legend and discrete legend were joined into one legend
* Fixed missing argument passes
* Fixed instances where network elements don't know show up when they should.

1.2.0 (2023-08-01)
------------------
* Overhauled animate_plot function to allow for plotting of custom data and use different file formats
* Plotting custom data now uses new parameter data_file instead of parameter
* Improved initilization time by switching to numpy
* Fixed blank figure appearing before plotting occurs

1.1.0a (2023-03-15)
-------------------
* Fixed colorbar functionality with subplots
* Added ability to customize colorbar size
* Legend/colorbar labels are automatically generated based on parameter/value type
* A default matplotlib figure and axis is created if no axis is specified
* Fixed deprecation issue with matplotlib colormaps
* Updated supported versions of dependecies
* Updated supported python versions 

1.0.0 (2023-02-07)
------------------
* Greatly improved animate_plot() function speed
* Fixed numerous bugs related to excel data plotting
* Added ability to use directional arrows with continuous plots

0.1.5 (2023-01-22)
------------------
* Complete documentation
* Fixed animate plot bugs
* Changed how num_interval parameter works
* Fixed warnings

0.1.4 (2022-12-19)
------------------
* Updated requirements

0.1.3 (2022-12-17)
------------------
* Bug fixes
* Some documentation added

0.1.2 (2022-11-11)
------------------

* Rename package once more to avoid confusion with R package 'visnetwork'.

0.1.1 (2022-11-11)
------------------

* Fix import errors due to package name change.

0.1.0 (2022-11-11)
------------------

* First release on PyPI.


