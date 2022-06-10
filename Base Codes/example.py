# -*- coding: utf-8 -*-
"""
Example with CTown.inp showing first few functions
"""
import wdn_viz_001 as wdn

model = wdn.initializeModel('CTown.inp')

flow_rates = wdn.createFlowRatePlot(model,savefig=True)
