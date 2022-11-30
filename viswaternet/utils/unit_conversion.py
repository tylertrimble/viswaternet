"""
The viswaternet.utils.unit_conversion module contains a function for converting
units from WNTR's base SI units.

.. rubric:: Base Demand, Demand, and Flowrate Units

====================  ====================================  ====================
    :attr:'~Default'  :math:'m^3\,/\,s'                     :attr:'Metric'
    :attr:`~LPS`      :math:`L\,/\,s`                       :attr:`Metric`
    :attr:`~LPM`      :math:`L\,/\,min`                     :attr:`Metric`
    :attr:`~MLD`      :math:`ML\,/\,day`                    :attr:`Metric`
    :attr:`~CMH`      :math:`m^3\,\,hr`                     :attr:`Metric`
    :attr:`~CMD`      :math:`m^3\,/\,day`                   :attr:`Metric`
    :attr:`~CFS`      :math:`ft^3\,/\,s`                    :attr:`USC`
    :attr:`~GPM`      :math:`gal\,/\,min`                   :attr:`USC`
    :attr:`~MGD`      :math:`10^6\,gal\,/\,day`             :attr:`USC`
    :attr:`~IMGD`     :math:`10^6\,Imp.\,gal\,/\,day`       :attr:`USC`
    :attr:`~AFD`      :math:`acre\cdot\,ft\,/\,day`         :attr:`USC`
====================  ====================================  ====================

.. rubric:: Diameter, Elevation, Head, and Length Units

====================  ====================================  ====================
    :attr:'~Default'  :math:'m'                             :attr:'Metric'
    :attr:'~cm'       :math:'cm'                            :attr:'Metric'
    :attr:'~ft'       :math:'ft'                            :attr:'USC'
    :attr:'~in'       :math:'in'                            :attr:'USC'
====================  ====================================  ====================

.. rubric:: Presure Units

====================  ====================================  ====================
    :attr:'~Default'  :math:'m'                             :attr:'Metric'
    :attr:'~psi'      :math:'psi'                           :attr:'USC'
====================  ====================================  ====================

.. rubric:: Velocity Units

====================  ====================================  ====================
    :attr:'~Default'  :math:'m/s'                           :attr:'Metric'
    :attr:'~ft/s'     :math:'ft/s'                          :attr:'USC'
====================  ====================================  ====================

.. rubric:: Time, Quality (Water Age) Units

====================  ====================================  ====================
    :attr:'~Default'  :math:'s'                             :attr:'N/A'
    :attr:'~min'      :math:'min'                           :attr:'N/A'
    :attr:'~hr'       :math:'hr'                            :attr:'N/A'
    :attr:'~day'      :math:'day'                           :attr:'N/A'
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
        
        =======================
            :attr:'base_demand'
            :attr:'demand'
            :attr:'elevation'
            :attr:'head'
            :attr:'pressure'
            :attr:'quality'
        =======================
            
        .. rubric:: Nodal Parameters
        
        =======================
            :attr:'diameter'
            :attr:'flowrate'
            :attr:'velocity'
            :attr:'quality'
        =======================
        
        .. rubric:: Other Parameters
        
        =======================
            :attr:'time'
        =======================
      
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
        "quality": {"min":1/60, "hr":1/3600, "day":1/86400},
        "time": {"s":1,"min":1/60, "hr":1/3600, "day":1/86400}
    }
    parameter_results = parameter_results * conversion_factors[parameter][new_unit]
    return parameter_results
