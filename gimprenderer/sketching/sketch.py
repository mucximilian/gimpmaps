'''
Created on Jun 5, 2015

@author: mucx
'''

from __future__ import division
import math
import random

import randomize
from geometry import LineSimple, LineString

seed = 1

def add_points_to_line(line, n = 1, method = "equal"):
    """
    Note: The direction of the new line is always from min X to max X
    """
    
    line_new = []
    
    points_new = randomize.random_points_on_line(line, n, method)        
    
    line_new += [line[0]]
    line_new += points_new
    line_new += [line[1]]
    
    return line_new

def displace_line(line, r):
    """
    Displaces the two end points of a line. If the specified radius is
    larger than the line length, the points are displaced by half of the
    original line length.
    """
    
    line = LineSimple(line)
    
    a = line.coords[0]
    b = line.coords[1]
    
    length = line.length()
    
    if (length <= r):
        r =  length/2               
            
    random.seed(length + seed)
    point1 = randomize.displace_point(a, r, method = "circle")
    point2 = randomize.displace_point(b, r, method = "circle")
    
    line_new = [point1, point2]
    
    return line_new

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
            points = add_points_to_line(
                line_seg.coords, seg_breaks, "equal_uniform"
            )
            # Check the direction of the segment and flip if necessary
            if points[0] == a:
                line_points += points[1:-1]
            else:
                line_points += reversed(points[1:-1])
                
        line_points.append(line.coords[i + 1]) # Adding segment end point
    
    line_jittered = jitter_linestring(line_points, d, method)
    
    return line_jittered

def jitter_linestring(line, d = 10.0, method = "simple"):
    """
    Creates a jittered version of a Line (LineSimple or LineString) using 
    an absolute distortion value (in image units). The line points are 
    distorted either using circular point displacement ("displace"), 
    random Bezier control points ("bezier") or both techniques 
    ("displace_bezier").
    
    The function 'jitter_line' calls this function after additional random 
    points have been computed and added to the input geometry.
    
    :param line: List of coordinate pairs determining the line
    :param d: Jitter distortion of the line in absolute image units
    :param method: Method used for jittering ("displace", "bezier" or
    "displace_bezier")
    """
    
    line_jittered = []
    
    line = LineString(line)
    
    if method == "simple":
        
        for i in range(0, len(line.coords)):
                
            seed_loop = i * seed
            random.seed(seed_loop)
            
            point = randomize.displace_point(line.coords[i], d, "circle")
            
            line_jittered.append(point)             
        
    elif method == "bezier":
    
        controlpoints = []
        
        for i in range(0, len(line.coords) - 1):
            
            a = line.coords[i]
            b = line.coords[i + 1]
                        
            controlpoints += randomize.random_controlpoints((a, b), d)
        
        line_jittered = line.get_curve(controlpoints)
        
    elif method == "displace_bezier":
        # TO DO: Add displacing
    
        controlpoints = []
        
        for i in range(0, len(line.coords) - 1):
            
            a = line.coords[i]
            b = line.coords[i + 1]
                        
            controlpoints += randomize.random_controlpoints((a, b), d)
        
        line_jittered = line.get_curve(controlpoints)
        
    return line_jittered  

############################################################################
# Interface functions

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