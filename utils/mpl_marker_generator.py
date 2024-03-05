# -*- coding: utf-8 -*-
"""
Created on Sat Feb 17 01:03:57 2024

@author: tyler
"""
import matplotlib as mpl
from svgpath2mpl import parse_path
from svgpathtools import svg2paths2
paths, attributes, svg_attributes = svg2paths2('pump.svg')
pump_marker = parse_path(attributes[0]['d'])
pump_marker.vertices -= pump_marker.vertices.mean(axis=0)

pump_marker = pump_marker.transformed(mpl.transforms.Affine2D().rotate_deg(180))
pump_marker = pump_marker.transformed(mpl.transforms.Affine2D().scale(-1,1))
vertices = pump_marker.vertices
codes = pump_marker._codes