# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 23:38:12 2022

@author: Tyler
"""
import wntr

import random
import matplotlib.pyplot as plt

wn = wntr.network.WaterNetworkModel(r"Networks/CTown.inp")

#Generation of error data
random.seed(1)
error_list = []
element_list = wn.junction_name_list
for _, junc in wn.junctions():
    try:
        pat = junc.demand_timeseries_list[0].pattern.name
        if pat == "DMA2_pat" or pat == "DMA5_pat" or pat == "DMA3_pat":
            error_list.append(0)
        else:
            error_list.append(random.uniform(-8, 5))
    except AttributeError:
        error_list.append(0)