'''
Created on Apr 28, 2015

@author: mucx
'''
import Renderer
import shapely
import svgwrite

path_d = ("M 100 50 L 100 200 250 200 250 50 Z " +
    "M 150 100 L 200 100 200 150 150 150 Z")

print(path_d)

my_path = svgwrite.path.Path(path_d)

svg_renderer = Renderer.Renderer(my_path)

# svg_hachure = svg_renderer.hachurizePolygon()