'''
Created on Jun 5, 2015

@author: mucx
'''

from __future__ import division
import math

import randomize
from geometry import LineSimple, LineString
        




############################################################################
# Interface functions    

def jitter_line(line, d = 10.0, method = "displace"):
    """
    Creates a jittered version of a Line (LineSimple or LineString) using 
    an absolute distortion value (in image units). Depending on the 
    distortion d, random points are added to the line segments (lines 
    connecting two points). After that, the line points are distorted 
    either using circular point displacement ("displace"), random Bezier 
    control points ("bezier") or both techniques ("displace_bezier").
    
    :param line: List of coordinate pairs determining the line
    :param d: Jitter distortion of the line in absolute image units
    :param method: Method used for jittering ("displace", "bezier" or
    "displace_bezier")
    
    TO DO: Adding a relative_displacement d_rel?
    """
    
    randomize.seed = 1
    
    line = LineString(line)
    
    line_points = []
    
    line_points.append(line.coords[0]) # Adding the first point        
    for i in range(0, len(line.coords) - 1):
        
        a = line.coords[i]
        b = line.coords[i + 1]
        
        line_seg = LineSimple([a,b])
        
        # Adding ceil(length/[10d|d^2])-1 points to the line segment
        seg_breaks = int(math.floor(line_seg.length() / (d * d))) - 1
                 
        if seg_breaks > 0:
            points = randomize.add_points_to_line(
                line_seg.coords, seg_breaks, "equal_uniform"
            )
            # Check the direction of the segment and flip if necessary
            if points[0] == a:
                line_points += points[1:-1]
            else:
                line_points += reversed(points[1:-1])
                
        line_points.append(line.coords[i + 1]) # Adding segment end point
    
    line_jittered = randomize.jitter_linestring(line_points, d, method)
    
    return line_jittered

############################################################################
# SVG functions

def line(linestring):
    
    # parse SVG
    
    # jtter line
    
    # return SVG
    
    pass

def polygon_outline(linestring):
    
    # parse SVG
    
    # disjoin polygon
    
    # jtter lines
    
    # return SVG
    
    pass

def polygon_hachure(linestring):
    
    # parse SVG
    
    # create hachure lines
    
    # randomize hachure lines
    
    # return SVG
    
    pass