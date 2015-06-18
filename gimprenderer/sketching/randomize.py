'''
Created on Jun 18, 2015

@author: mucx
'''

from __future__ import division
import math
import random

import sketch
from geometry import LineSimple, LineString

seed = 1
seed_loop = 1
        
def line_handy(line, r):
    """
    Does what the Handy renderer is supposed to do (according to paper).
    
    http://www.gicentre.net/software/#/handy/
    
    :param line: Tuple of two coordinate pairs determining the line points.
    """
    
    line = LineSimple(line)
    
    point_a = displace_point(line[0], r)
    point_b = displace_point(line[1], r)
    
    l = line.length()
    
    d_m = random.uniform(-1, 1) * (l / 200)
    m = line.point_at_pos(0.5)
    point_m = displace_point_orthogonal(line.coords, m, d_m)
    
    # Calculating a position that is +/- 10% away from the point at 75% of l
    pos = random.uniform(0.65,0.85)
    d_n = random.uniform(-1, 1) * r
    n = line.point_at_pos(pos)
    point_n = displace_point_orthogonal(line.coords, n, d_n)
    
    line_sketch = [point_a, point_m, point_n, point_b]
    
    return line_sketch

def displace_point(point, r, method = "circle"):
    """
    Displaces a point, r defines the radius within which the point 
    coordinates are randomly perturbed (with a uniform random deviate).
    
    Note: The random seed should be set outside of the function.
    
    :param point: Tuple of x and y coordinates.
    """
    
    # random.seed(r * seed)
    
    coords_new = None
    
    if (method == "circle"):
        
        angle = random.random() * 360
        distance = random.random() * r
        
        x = point[0] + (math.cos(math.radians(angle)) * distance)
        y = point[1] + (math.sin(math.radians(angle)) * distance)
        
        coords_new = (x,y)
        
    elif(method == "square"):
        
        d_x = random.uniform(-r, r)
        d_y = random.uniform(-r, r)
        
        x = d_x + point[0]
        y = d_y + point[1]
        
        coords_new = (x,y)
    
    return coords_new

def displace_point_orthogonal(line, p, d):
    """
    Displaces a point from a line orthogonally within a distance d.
    
    :param line: The line the point should be orthogonally displaced from
    :param p: A point on the line from where to dispalce orthogonally
    :param d: Distance the point is displaced
    """
    
    line = LineSimple(line)
    
    v = line.vector_orthogonal()
    
    shift = [(p[0], p[1]), (v[0] + p[0], v[1] + p[1])]
    shift_line = LineSimple(shift)
    
    p_displaced = shift_line.point_shifted(d)
    
    return p_displaced
    
def add_points_to_line(line, n = 1, method = "equal"):
    """
    
    Note: The direction of the new line is always from min X to max X
    """
    
    line_new = []
    
    points_new = get_random_points_on_line(line, n, method)        
    
    line_new += [line[0]]
    line_new += points_new
    line_new += [line[1]]
    
    return line_new    
    
def get_random_points_on_line(line, n = 1, method = "equal"):
    """
    Computes a specified number of points on a line between two points 
    using the selected method. Returns the computed points in an array
    which can be added to the line then.
    
    :param line: Tuple of two coordinate pairs determining the line points.
    """
    
    line = LineSimple(line)
    length = line.length()
    
    # Determine start and end point by ordering after X and Y coordinates
    # Used to combine with the points computed later which are also sorted
    # a = min(line.coords)
    # b = max(line.coords)
    
    a = line.coords[0]
    b = line.coords[1]
        
    points_on_line = []
    
    if n == 0:
        return points_on_line
    
    # Distribute points equally
    if method == "equal":
        
        for i in range(0, n):
        
            d = (length / (n + 1)) * (i + 1)
        
            point = sketch.point_shifted((a, b), d)                
            points_on_line.append(point)
    
    # Distribute points randomly  
    elif (method == "uniform" or
        method == "equal_uniform" or
        method == "equal_normlike"):            
    
        random.seed(length * seed)
    
        # - just random
        if method == "uniform":
    
            for _ in range(0, n):
                
                d = length * random.random()
        
                point = sketch.point_shifted((a, b), d)                
                points_on_line.append(point)        
        
        # - randomly within equal segments        
        elif method == "equal_uniform":
            
            # Computing the start and end points of the equal segments
            segment_points = [a]
            for i in range(0, n - 1):
                d_part = (length / (n + 1)) * (i + 1)
                point = sketch.point_shifted((a, b), d_part)
                segment_points.append(point)
            segment_points.append(b)
            
            # Now random points between the segments are added               
            for i in range(0, len(segment_points) - 1):                   
                points_on_line.append(
                    get_random_point_on_line(
                        (segment_points[i], segment_points[i + 1])
                    )
                )
        
        # Distribute points normal distribution like on segment 
        elif method == "equal_normlike":
            print "'equal_normlike' not yet implemented"
        
    # Inserting new points in the original line
    # points_on_line = sorted(points_on_line)
    
    return points_on_line
    
def get_random_point_on_line(line):
    """
    Computes the point that is on the straight line between P0 and P1 and
    the distance d away from P0 and P1.
    
    :param line: Tuple of two coordinate pairs determining the line points.
    """ 
    
    line = LineSimple(line)
    
    d = line.length()
    d_rand = random.random() * d
    
    point = line.point_shifted(d_rand)
    
    return point

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
    point1 = displace_point(a, r, method = "circle")
    point2 = displace_point(b, r, method = "circle")
    
    line_new = [point1, point2]
    
    return line_new

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
            
            point = displace_point(line.coords[i], d, "circle")
            
            line_jittered.append(point)             
        
    elif method == "bezier":
    
        controlpoints = []
        
        for i in range(0, len(line.coords) - 1):
            
            a = line.coords[i]
            b = line.coords[i + 1]
                        
            controlpoints += random_controlpoints((a, b), d)
        
        line_jittered = line.get_curve(controlpoints)
        
    elif method == "displace_bezier":
        # TO DO: Add displacing
    
        controlpoints = []
        
        for i in range(0, len(line.coords) - 1):
            
            a = line.coords[i]
            b = line.coords[i + 1]
                        
            controlpoints += random_controlpoints((a, b), d)
        
        line_jittered = line.get_curve(controlpoints)
        
    return line_jittered  

def jitter_line_bezier(line):
    """
    Creates a jittered line as described here:
    
    http://stackoverflow.com/a/6373008/3854098 
    http://jsfiddle.net/GfGVE/9/
    
    :param line: Tuple of two coordinate pairs determining the line points.
    """
    
    line = LineSimple(line)
    
    random.seed(line.length() * seed)
    
    curve = []
    curve.append(line.coords[0])
    
    for i in range(0, len(line.coords) -1):
        
        p0_x = line.coords[i][0]
        p0_y = line.coords[i][1]
        p1_x = line.coords[i+1][0]
        p1_y = line.coords[i+1][1]

        diff_y = p1_y - p0_y;
        
        # so the y value can go positive or negative from the typical   
        neg = random.random() - 0.5; 
            
        cp1 = (
            -neg + p0_x + ((random.random() - 0.5) * diff_y / 8),
            p0_y + 0.3 * diff_y
        )
        cp2 = (
            -neg + p0_x + ((random.random() - 0.5) * diff_y / 8),
            p0_y + 0.6 * diff_y
        )
        p = (p1_x, p1_y)
        
        curve.append(cp1)
        curve.append(cp2)
        curve.append(p)
        
    return curve

def jitter_line_handrawn(line, segments, wobble):
    """
    A python implementation of the core function that is implemented in 
    the Handdrawn RaphaelJS plugin to create jittered lines.
    
    http://handdrawn.clearcove.ca/
    https://github.com/jhund/raphael.handdrawn.js/blob/master/raphael.handdrawn.js
    
    :param line: Tuple of two coordinate pairs determining the line points
    :param segemnts: Number of segments that the line is split into 
    :param wobble: Degree of the jitter effect
    """
    
    def randomizeNormal(range_in = 1.0, mean = 0.0):
        range1 = range_in / 9;
        rand = math.cos(2 * math.pi * random.random()) * math.sqrt(-2 * math.log(random.random()))
        
        return round((rand * range1) + mean)
    
    def randomizeUniform (range_in = 100, mean = 0.0):
        rand = random.random() * range_in;
        return round((rand - (range_in / 2)) + mean);
    
    x = line[0][0]
    y = line[0][1]
    x2 = line[1][0]
    y2 = line[1][1]
    
    points = ['M ' + str(x) + ' ' + str(y)]

    for i in range(1, segments +1):
        
        segmentStartX = x + (x2-x) * (i-1) / segments
        segmentStartY = y + (y2-y) * (i-1) / segments
        segmentEndX = x + (x2-x) * i/segments
        segmentEndY = y + (y2-y) * i/segments
    
        midX1 = int(round(segmentStartX + (segmentStartX - segmentEndX) * -0.3 + randomizeUniform(wobble)))
        midX2 = int(round(segmentStartX + (segmentStartX - segmentEndX) * -0.7 + randomizeUniform(wobble)))
        midY1 = int(round(segmentStartY + (segmentStartY - segmentEndY) * -0.3 + randomizeUniform(wobble)))
        midY2 = int(round(segmentStartY + (segmentStartY - segmentEndY) * -0.7 + randomizeUniform(wobble)))
    
        points.append(
          'C ' + str(midX1) + ' ' + str(midY1) + ' ' + str(midX2) + ' ' + str(midY2) + ' ' + str(segmentEndX) + ' ' + str(segmentEndY)
        );
        
    return ' '.join(points);

def random_controlpoints(line, d, method = "orthogonal"):
    """
    Computes a random point that is on the straight line between P0 and P1 
    and the minimum distance d away from P0 and P1. The distance is 
    capped at half of the line length.
    
    :param line: Tuple of two coordinate pairs determining the line points
    P0 and P1.
    """
    
    # TO DO:
    # - Avoid overlapping controlpoints
    # - Control points alternating on opposite sides of the line 
    # --> smoother line
    
    line = LineSimple(line)
            
    line_length_half = line.length()/2
    
    random.seed(seed * line.length())

    cp1 = None
    cp2 = None
    
    if method == "orthogonal":
        
        # pos = random.random()
        pos = 0.5
        
        m = line.point_at_line_pos(pos)
        
        line1 = LineSimple([line.coords[0], m])
        p1 = line1.point_at_line_pos(random.random())
        
        line2 = LineSimple([m ,line.coords[1]])
        p2 = line2.point_at_line_pos(random.random())
        
        d1 = random.uniform(-1, 1) * d
        d2 = random.uniform(-1, 1) * d
        
        cp1 = displace_point_orthogonal(line.coords, p1, d1)
        cp2 = displace_point_orthogonal(line.coords, p2, d2)
    
    elif method == "circular":        
        # Displacing point circular around the center of the line
        # A----(-*-)----B
        if d >= line_length_half:           
            point = sketch.point_shifted(line.coords, line_length_half)
            cp1 = displace_point(point, line_length_half)
            cp2 = displace_point(point, line_length_half)
        
        # Displacing the point circular on a random position that is on a line
        # which is an inside segment of the original line but the distance d 
        # away from both endpoints.
        # A-(-----)-B
        else:
            point1 = sketch.point_shifted(line.coords, d)            
            point2 = sketch.point_shifted(line.coords[::-1], d)
            
            point = get_random_point_on_line((point1, point2))
            cp1 = displace_point(point, d)
            cp2 = displace_point(point, d)
            
        
    controlpoints = [cp1, cp2]
                
    return controlpoints