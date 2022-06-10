# -*- coding: utf-8 -*-
"""
Example with CTown.inp showing first few functions
"""
import wdn_viz_001 as wdn

model = wdn.initializeModel('Net3.inp')

wdn.createBasicPlot(model, savefig=True)
wdn.createFlowRatePlot(model, savefig=True)
wdn.createDemandPatternPlot(model, savefig=True)