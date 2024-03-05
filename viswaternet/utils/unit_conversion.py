def unit_conversion(parameter_results, parameter, new_unit):
    cf = {
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
    if isinstance(parameter_results, int):
        parameter_results = parameter_results * cf[parameter][new_unit]
    else:
        parameter_results = \
            [i * cf[parameter][new_unit] for i in parameter_results]
    return parameter_results
