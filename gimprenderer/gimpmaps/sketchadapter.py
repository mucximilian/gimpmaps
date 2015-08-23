'''
Created on Jun 18, 2015

@author: mucx

This module 
'''

import svgwrite

import sketching.sketch as sketch
from sketching import hachurizer

def sketch_line_path(path):
    
    linestring = sketch.path_to_linestring(path)
    
    linestring_jittered = sketch.jitter_line(linestring, 1.0, "curve")
    
    linestring_svg = get_curve_commands(linestring_jittered)
    
    path_svg = svgwrite.path.Path(linestring_svg)
    
    return path_svg

def sketch_polygon_outline(path):
    
    # Get as multipolygon
    polygons = sketch.path_to_polygon(path)
    
    polygons_svg = ""
    
    # Operate on sub polygons
    for polygon in polygons:

        segments = sketch.jitter_polygon([polygon], 1.0)
    
        # Creating polygon from jittered segments
        polygon = get_polygon_commands_from_segments(segments)
        
        polygons_svg += polygon + " "
    
    polygon_svg = svgwrite.path.Path(polygons_svg)
    
    return polygon_svg

def sketch_polygon_hachure(path, spacing = 8.0, angle = 35.0):
      
    
    hachurize = hachurizer.Hachurizer(spacing, angle)
    
    polygons = sketch.path_to_polygon(path)
    
    # TO DO: Update function input parameter !!!!!!    
    hachures = hachurize.get_hachure(polygons)
    
    if (hachures is not None):
    
        hachures_handy = sketch.handy_hachures(hachures, 1.0) 
        
        paths_svg = []         
        for hachure in hachures_handy:
             
            hachure_curve = get_curve_commands(hachure)
             
            path_svg = svgwrite.path.Path(hachure_curve)
             
            paths_svg.append(path_svg)
     
        return paths_svg
    
    else:
        
        return None

################################################################################
# Functions from svgmodule.py
# TO DO: Find a better solution here later!

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

def get_polygon_commands(polygon):
    
    rings_svg = map(get_curve_commands, polygon)
    
    svg = ' Z '.join(rings_svg)
    
    return svg

def get_polygon_commands_from_segments(segments):
    
    m = segments[0][0]
    
    svg = "M " + coord_string(m) + " C "
    
    for i in range(0, len(segments) - 1):
        
        for j in range(1, len(segments[i])):
                  
            svg += coord_string(segments[i][j])
            svg += " "
    
    for i in range(0, len(segments[-1]) - 1):
                   
        svg += coord_string(segments[-1][i])
        svg += " "
    
    svg += "Z"
    
    return svg    

def coord_string(point):
    """
    Returns the coordinates of a point in the format of a SVG path string.
    
    :param point: Point coordinates
    """
    
    return str(point[0]) + "," + str(point[1])

    