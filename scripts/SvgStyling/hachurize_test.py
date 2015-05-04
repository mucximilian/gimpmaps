'''
Created on Apr 28, 2015

@author: mucx
'''
import Renderer
import svgwrite

path_d = ("M 100 50 L 100 200 250 200 250 50 Z " +
    "M 150 100 L 200 100 200 150 150 150 Z")

path_d = ("M 50 50 L 40 160 140 150 140 100 100 110 100 60 Z")

#print(path_d)

my_path = svgwrite.path.Path(path_d)

svg_renderer = Renderer.Renderer()

polygon = svg_renderer.createMultiPolygonFromSvgPath(my_path)

#print polygon

svg_renderer.createHachureLines(polygon)