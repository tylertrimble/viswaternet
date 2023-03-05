def label_generator(parameter, value, unit=None):


    parameter_titles = {
        "base_demand": 'Base Demand',
        'elevation': 'Elevation',
        'emitter_coefficient': 'Emitter Coefficient',
        'initial_quality': "Initial Quality",
        'head': "Head",
        "demand": 'Demand',
        'leak_demand': 'Leak Demand',
        'leak_area': 'Leak Area',
        'leak_discharge_coeff': 'Leak Discharge Coefficient',
        'quality': 'Quality',
        'length': 'Length',
        'minor_loss': 'Minor Loss',
        'bulk_coeff': 'Bulk Reaction Coefficient',
        'wall_coeff': 'Wall Reaction Coefficient',
        'flowrate': 'Flowrate',
        'headloss': 'Headloss',
        'friction_factor': 'Friction Factor',
        'reaction_rate': 'Reaction Rate',
        'pressure': 'Pressure'
    }
    if parameter == 'base_demand' or parameter == 'demand' or parameter == 'flowrate':
        if unit is None:
            unit = 'CMS'
        unit_titles = {"LPS": "[L/s]",
                       "LPM": "[L/min]",
                       "MLD": "[million L/s]",
                       "CMS": "[m^3/s]",
                       "CMH": "[m^3/hr]",
                       "CMD": "[m^3/day]",
                       "CFS": "[ft^3/s]",
                       "GPM": "[gal/min]",
                       "MGD": "[million gal/min]",
                       "IMGD": "[million imperial gal/min]",
                       "AFD": "[acre-ft/day]"}

    if parameter == 'diameter' or parameter == 'elevation' or parameter == 'head' or parameter == 'length':
        if unit is None:
            unit = 'm'
        unit_titles = {"ft": '[ft]',
                       "in": '[in]',
                       "m": '[m]',
                       'cm': '[cm]'}

    if parameter == 'pressure':
        if unit is None:
            unit = 'm'

        unit_titles = {'m': '[m]',
                       'psi': '[psi]'}

    if parameter == 'velocity':
        if unit is None:
            unit = 'm/s'

        unit_titles = {'m/s': '[m/s]',
                       'ft/s': '[ft/s]'}

    if parameter == 'quality' or parameter == 'time':
        if unit is None:
            unit = 's'

        unit_titles = {'s': '[s]',
                       'min': '[min]',
                       'hr': '[hr]',
                       'day': '[day]'}
    
    if isinstance(value, int):
        title_label = parameter_titles[parameter] + " " + unit_titles[unit] + " at timestep " + str(value)
        
    if value=='min':
        title_label = 'Minimum ' + parameter_titles[parameter] + " " + unit_titles[unit]
        
    if value=='max':
        title_label = 'Maximum ' + parameter_titles[parameter] + " " + unit_titles[unit]
        
    if value=='mean':
        title_label = 'Mean ' + parameter_titles[parameter] + " " + unit_titles[unit]
    
    if value=='stddev':
        title_label = 'Standard Deviation of ' + parameter_titles[parameter] + " " + unit_titles[unit]
        
    if value=='range':
        title_label = 'Range of ' + parameter_titles[parameter] + " " + unit_titles[unit]
        
    if value is None:
        title_label = parameter_titles[parameter] + " " + unit_titles[unit]
    return title_label
