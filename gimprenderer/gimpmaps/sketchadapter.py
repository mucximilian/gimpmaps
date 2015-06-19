'''
Created on Jun 18, 2015

@author: mucx
'''

import svgwrite

import sketching.sketch as sketch
from sketching import hachurizer

def sketch_line_path(path):
    
    linestring = sketch.path_to_linestring(path)
    
    linestring_jittered = sketch.jitter_line(linestring, 5, "bezier")
    
    linestring_svg = get_curve_commands(linestring_jittered)
    
    path_svg = svgwrite.path.Path(linestring_svg)
    
    return path_svg.tostring()

def sketch_polygon_path(path):
    
    polygon = sketch.path_to_polygon(path)
    
    polygon_jittered = sketch.jitter_polygon(polygon, 5, "bezier")
    
    polygon_commands = get_polygon_commands(polygon_jittered)
    
    path_svg = svgwrite.path.Path(polygon_commands)
    
    return path_svg.tostring()

def sketch_polygon_hachure(path):
    
    svg_path = svgwrite.path.Path(path)    
    
    hachurizer_svg = hachurizer.Hachurizer(10.0, 35.0)
    hachures = hachurizer_svg.get_svg_hachure(svg_path)
    
    if (hachures is not None):
    
        hachures_handy = sketch.handy_hachures(hachures) 
        
        paths_svg = []
         
        for hachure in hachures_handy:
             
            hachure_curve = get_curve_commands(hachure)
             
            path_svg = svgwrite.path.Path(hachure_curve)
             
            paths_svg.append(path_svg.tostring())
     
        return paths_svg
    
    else:
        
        return None

################################################################################
# Functions taken from svgmodule.py, need to find a better solution here later!

def get_polygon_commands(polygon):
    
    rings_svg = map(get_curve_commands, polygon)
    
    svg = ' Z '.join(rings_svg)
    
    return svg

def get_curve_commands(linestring):
    """
    Returns a SVG path representation of an array of points that describe
    a Bezier curve.
    
    :param linestring: The linestring with computed Bezier control points
    """
    
    m = linestring.pop(0)
    
    svg = "M " + coord_string(m) + " C"
    
    for p in linestring:
        svg += " " + coord_string(p)
        
    return svg

def coord_string(point):
    """
    Returns the coordinates of a point in the format of a SVG path string.
    
    :param point: Point coordinates
    """
    
    return str(point[0]) + "," + str(point[1])