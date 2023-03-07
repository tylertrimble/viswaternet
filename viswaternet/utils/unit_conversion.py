"""
The viswaternet.utils.unit_conversion module contains a function for converting
units from WNTR's base SI units.

.. rubric:: Base Demand, Demand, and Flowrate Units

====================  ====================================  ====================
    Default           :math:`m^3\\,/\\,s`                     Metric
    LPS               :math:`L\\,/\\,s`                       Metric
    LPM               :math:`L\\,/\\,min`                     Metric
    MLD               :math:`ML\\,/\\,day`                    Metric
    CMH               :math:`m^3\\,\\,hr`                     Metric
    CMD               :math:`m^3\\,/\\,day`                   Metric
    CFS               :math:`ft^3\\,/\\,s`                    USC
    GPM               :math:`gal\\,/\\,min`                   USC
    MGD               :math:`10^6\\,gal\\,/\\,day`             USC
    IMGD              :math:`10^6\\,Imp.\\,gal\\,/\\,day`       USC
    AFD               :math:`acre\\cdot\\,ft\\,/\\,day`         USC
====================  ====================================  ====================

.. rubric:: Diameter, Elevation, Head, and Length Units

====================  ====================================  ====================
    Default           :math:`m`                             Metric
    cm                :math:`cm`                            Metric
    ft                :math:`ft`                            USC
    in                :math:`in'`                           USC
====================  ====================================  ====================

.. rubric:: Presure Units

====================  ====================================  ====================
    Default           :math:`m`                             Metric
    psi               :math:`psi`                           USC
====================  ====================================  ====================

.. rubric:: Velocity Units

====================  ====================================  ====================
    Default           :math:`m/s`                           Metric
    ft/s              :math:`ft/s`                          USC
====================  ====================================  ====================

.. rubric:: Time, Quality (Water Age) Units

====================  ====================================  ====================
    Default           :math:`s`                             N/A
    min               :math:`min`                           N/A
    hr                :math:`hr`                            N/A
    day               :math:`day`                           N/A
====================  ====================================  ====================

"""


def unit_conversion(parameter_results, parameter, new_unit):
    """Convert network datapoints from base SI WNTR units to some new unit.

    Arguments
    ---------

    parameter_results : array-like
        Network data to be converted.

    parameter : string
        The parameter that the data represents.

        .. rubric:: Nodal Parameters

        ======================= =====
        base_demand             Nodal
        demand                  Nodal
        elevation               Nodal
        head                    Nodal
        pressure                Nodal
        quality                 Nodal
        diameter                Link
        flowrate                Link
        velocity                Link
        quality                 Link
        time                    N/A
        ======================= =====

    new_unit : string
        The unit that the network data is to be converted to.

    Returns
    -------
    float,array-like
        The network data converted into new units

    """
    conversion_factors = {
        "base_demand": {
            "LPS": 1000,
            "LPM": 60000,
            "MLD": 86.4,
            "CMH": 3600,
            "CMD": 86400,
            "CFS": 35.31467,
            "GPM": 15850.32314,
            "MGD": 22.82447,
            "IMGD": 13198.15490,
            "AFD": 70.04562,
        },
        "demand": {
            "LPS": 1000,
            "LPM": 60000,
            "MLD": 86.4,
            "CMH": 3600,
            "CMD": 86400,
            "CFS": 35.31467,
            "GPM": 15850.32314,
            "MGD": 22.82447,
            "IMGD": 13198.15490,
            "AFD": 70.04562,
        },
        "diameter": {"ft": 3.28084, "in": 39.37008, "cm": 100},
        "elevation": {"ft": 3.28084, "in": 39.37008, "cm": 100},
        "flowrate": {
            "LPS": 1000,
            "LPM": 60000,
            "MLD": 86.4,
            "CMH": 3600,
            "CMD": 86400,
            "CFS": 35.31467,
            "GPM": 15850.32314,
            "MGD": 22.82447,
            "IMGD": 13198.15490,
            "AFD": 70.04562,
        },
        "head": {"ft": 3.28084, "in": 39.37008, "cm": 100},
        "length": {"ft": 3.28084, "in": 39.37008, "cm": 100},
        "pressure": {"psi": 1.42197},
        "velocity": {"ft/s": 3.28084},
        "quality": {"min": 1/60, "hr": 1/3600, "day": 1/86400},
        "time": {"s": 1, "min": 1/60, "hr": 1/3600, "day": 1/86400}
    }
    parameter_results = parameter_results * \
        conversion_factors[parameter][new_unit]
    return parameter_results
