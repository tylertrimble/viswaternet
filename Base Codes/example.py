# -*- coding: utf-8 -*-
"""
Example with CTown.inp showing first few functions
"""
import wdn_viz_003 as wdn

model = wdn.initializeModel('CTown.inp')

wdn.createBasicPlot(model, savefig=True, saveName = 'Basic')
wdn.createFlowRatePlot(model, savefig=True)
wdn.createDemandPatternPlot(model, savefig=True, saveName = 'DemandPatterns')
wdn.plotDistinctNodes(model,parameter='elevation',savefig=True, legendTitle= 'Elevation Groups', saveName = 'ElevationMap')
wdn.plotDistinctNodes(model,parameter='elevation',bins=[25,50,75,100,125,150],binSizeList = [100,125,150,175,200,225], binShapeList = ['.','v','8','D','1','p'], cmap=None,colorList=['#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'],savefig=True, legendTitle= 'Elevation Groups', saveName = 'ElevationMap2')