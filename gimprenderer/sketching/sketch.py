'''
Created on Jun 5, 2015

@author: mucx
'''

from __future__ import division
import math

import randomize
from geometry import LineSimple, LineString, Polygon

seed = 1

def add_points_to_line(line, n = 1, method = "equal"):
    """
    Note: The direction of the new line is always from min X to max X
    """
    
    line_new = []
    
    points_new = randomize.add_random_points_to_line(line, n, method)        
    
    line_new += [line[0]]
    line_new += points_new
    line_new += [line[1]]
    
    return line_new

def handy_hachures(hachures, d):
    
    hachures_handy = []
    
    randomize.reset_seed_loop()
    
    for hachure in hachures:
        
        hachure_displaced = randomize.displace_line(hachure, d)
        
        hachure_handy = randomize.line_handy(hachure_displaced, d)
        # hachure_handy = handyrenderer.line(hachure_displaced, d)[0]

        hachures_handy.append(hachure_handy)
        
        randomize.seed_loop += 1
        
    randomize.reset_seed_loop()
        
    return hachures_handy

def jitter_line(line, d = 10.0, method = "curve"):
    """
    Creates a jittered version of a Line (LineSimple or LineString) using 
    an absolute distortion value (in image units). Depending on the 
    distortion d, random points are added to the line segments (lines 
    connecting two points). After that, the line points are distorted 
    either using circular point displacement ("displace"), random Bezier 
    control points ("bezier") or both techniques ("displace_bezier").
    
    IMPORTANT: Do not forget to reset the randomize.seed_loop in the calling
    environment!
    
    :param line: List of coordinate pairs determining the line
    :param d: Jitter distortion of the line in absolute image units
    :param method: Method used for jittering ("displace", "curve" or
    "displace_curve")
    
    TO DO: Adding displace_bezier method
    TO DO: Adding a relative_displacement d_rel?
    """
    
    line = LineString(line)
    
    line_points = []    
    
    # First step: Adding random points
    line_points.append(line.coords[0]) # Adding the first point to result   
    
    # Iteration over all line segments to add random points
    for i in range(0, len(line.coords) - 1):
        
        a = line.coords[i]
        b = line.coords[i + 1]
        
        line_seg = LineSimple([a,b])
        
        # Adding ceil(length/[10d|d^2])-1 points to the line segment
        seg_breaks = int(math.floor(line_seg.length() / (d * d))) - 1
                 
        if seg_breaks > 0:
            
            points = add_points_to_line(
                line_seg.coords, seg_breaks, "equal_beta"
            )
            
            # Check the direction of the segment and flip if necessary
            if points[0] == a:
                line_points += points[1:-1]
            else:
                line_points += reversed(points[1:-1])
                
        line_points.append(line.coords[i + 1]) # Adding segment end point
    
    # Second step: Displacing points
    if method == "displace" or method == "displace_curve":
        line_points_displaced = []
        
        for point in line_points:
            
            point_displaced = randomize.displace_point(point, d)
            line_points_displaced.append(point_displaced)
            
        line_points = line_points_displaced
        
    line = LineString(line_points)
    
    # Third step: Adding random control points
    if method == "curve" or method == "displace_curve":
        
        controlpoints = []
        
        for i in range(0, len(line.coords) - 1):
        
            a = line.coords[i]
            b = line.coords[i + 1]    
                
            controlpoints += randomize.random_controlpoints((a, b), d)
        
        line_jittered = line.get_curve(controlpoints)
    
    return line_jittered

def jitter_polygon(polygon, d = 10.0, method = "displace"):
    
    polygon = Polygon(polygon)
    
    segments = polygon.disjoin(120)
    
    segments_jittered = []
    
    randomize.seed = 1

    for segment in segments:
        
        segment_jittered = jitter_line(segment, 10, "bezier")
        segments_jittered.append(segment_jittered)
          
    return segments_jittered

################################################################################
# Interface functions

def path_to_linestring(path):
    
    coords = path.split(" ");   
    coords.remove('M')
    coords.remove('L')

    linestring = []
    
    for i in range(0, len(coords), 2):
        linestring.append(
            (float(coords[i]), float(coords[i + 1]))
        )
    
    return linestring

def path_to_linearring(path):
    
    linearring = path_to_linestring(path)
    linearring.append(linearring[0])
    
    return linearring
    
def path_to_polygon(path):
    
    polygons_str = path.split("Z");
    polygons_str.pop() # Removing last item from list (empty due to split)
    
    polygons = []
    
    for polygon_str in polygons_str:
        
        polygon_str = polygon_str.strip()
        
        polygon = path_to_linearring(polygon_str)
        polygons.append(polygon)
        
    return polygons