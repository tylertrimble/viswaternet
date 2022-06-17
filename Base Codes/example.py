# -*- coding: utf-8 -*-
"""
Example with CTown.inp showing first few functions
"""
import wdn_viz_002 as wdn

model = wdn.initializeModel('CTown.inp')

wdn.createBasicPlot(model, savefig=True, saveName = 'Basic')
wdn.createFlowRatePlot(model, savefig=True)
wdn.createDemandPatternPlot(model, savefig=True, saveName = 'DemandPatterns')
binned = wdn.plotDistinctNodes(model,parameter='elevation',savefig=True, legendTitle= 'Elevation Groups', saveName = 'ElevationMap')