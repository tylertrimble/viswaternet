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
        'pressure': 'Pressure',
        'velocity': 'Velocity',
        'roughness': 'Roughness',
        'diameter': 'Diameter',
    }
    if parameter == 'base_demand' \
            or parameter == 'demand' \
            or parameter == 'flowrate':
        if unit is None:
            unit = 'CMS'
        unit_titles = {"LPS": "[$LPS$]",
                       "LPM": "[$LPM$]",
                       "MLD": "[$MLD$]",
                       "CMS": "[$m^3/s$]",
                       "CMH": "[$m^3/hr$]",
                       "CMD": "[$m^3/day$]",
                       "CFS": "[$CFS$]",
                       "GPM": "[$GPM$]",
                       "MGD": "[$MGD$]",
                       "IMGD": "[$IMGD$]",
                       "AFD": "[$AFD$]"}
    elif parameter == 'diameter' \
            or parameter == 'elevation' \
            or parameter == 'head' \
            or parameter == 'headloss' \
            or parameter == 'length' \
            or parameter == 'diameter':
        if unit is None:
            unit = 'm'
        unit_titles = {"ft": '[$ft$]',
                       "in": '[$in$]',
                       "m": '[$m$]',
                       'cm': '[$cm$]'}
    elif parameter == 'pressure':
        if unit is None:
            unit = 'm'
        unit_titles = {'m': '[$m$]',
                       'psi': '[$psi$]'}
    elif parameter == 'velocity':
        if unit is None:
            unit = 'm/s'
        unit_titles = {'m/s': '[$m/s$]',
                       'ft/s': '[$ft/s$]'}
    elif parameter == 'time':
        if unit is None:
            unit = None
        unit_titles = {'s': '[$s$]',
                       'min': '[$min$]',
                       'hr': '[$hr$]',
                       'day': '[$day$]'}
    elif parameter == 'quality':
        unit = ' '
        unit_titles = {' ': ' '}
    
    else:
        unit_titles = {None: ''}
    if isinstance(value, int):
        title_label = parameter_titles[parameter] \
                      + " " + unit_titles[unit] \
                      + ' at timestep ' + str(value)
    elif value == 'min':
        title_label = 'Minimum ' \
                      + parameter_titles[parameter] \
                      + " " + unit_titles[unit]
    elif value == 'max':
        title_label = 'Maximum ' \
                      + parameter_titles[parameter] \
                      + " " + unit_titles[unit]
    elif value == 'mean':
        title_label = 'Mean ' \
                      + parameter_titles[parameter] \
                      + " " + unit_titles[unit]
    elif value == 'stddev':
        title_label = 'Standard Deviation of ' \
                      + parameter_titles[parameter] \
                      + " " + unit_titles[unit]
    elif value == 'range':
        title_label = 'Range of ' \
                      + parameter_titles[parameter] \
                      + " " + unit_titles[unit]
    elif value is None:
        title_label = parameter_titles[parameter] + " " + unit_titles[unit]
    else:
        title_label = parameter_titles[parameter] + " " + unit_titles[unit]
    return title_label
