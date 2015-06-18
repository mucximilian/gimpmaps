'''
Created on Jun 18, 2015

@author: mucx
'''

from __future__ import division
import math
import random

from geometry import LineSimple

seed = 1
seed_loop = 1

def reset_seed_loop():    
    global seed_loop 
    seed_loop = 1
    return

def random_beta(a = 5, b = 5):
    
    x = random.betavariate(a, b)
    return x

def random_uniform():
    
    x = random.random()
    return x

def random_uniform_int(a = -1, b = 1):
    
    x = random.uniform(a, b)
    return x
        
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
    
    d_m = random_uniform_int() * (l / 200)
    point_m = line.point_orthogonal(0.5, d_m)
    
    # Calculating a position that is +/- 10% away from the point at 75% of l
    pos = random_uniform_int(0.65, 0.85)
    d_n = random_uniform_int() * r
    point_n = line.point_orthogonal(pos, d_n)
    
    line_sketch = [point_a, point_m, point_n, point_b]
    
    return line_sketch

def displace_point(point, r, method = "circle"):
    """
    Displaces a point, r defines the radius within which the point 
    coordinates are randomly perturbed (with a uniform random deviate).
    
    Note: The random seed should be set outside of the function.
    
    :param point: Tuple of x and y coordinates.
    """
    
    # random.seed(r * seed * seed_loop)
    
    coords_new = None
    
    if (method == "circle"):
        
        angle = random_uniform() * 360
        distance = random_uniform() * r
        
        x = point[0] + (math.cos(math.radians(angle)) * distance)
        y = point[1] + (math.sin(math.radians(angle)) * distance)
        
        coords_new = (x,y)
        
    elif(method == "square"):
        
        d_x = random_uniform_int(-r, r)
        d_y = random_uniform_int(-r, r)
        
        x = d_x + point[0]
        y = d_y + point[1]
        
        coords_new = (x,y)
    
    return coords_new   
    
def random_points_on_line(line, n = 1, method = "equal"):
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
        
    points_on_line = []
    
    if n == 0:
        return points_on_line
    
    # Distribute points equally
    if method == "equal":
        
        for i in range(0, n):
        
            d = (length / (n + 1)) * (i + 1)
        
            point = line.point_shifted(d)                
            points_on_line.append(point)
    
    # Distribute points randomly  
    elif (method == "uniform" or
        method == "equal_uniform" or
        method == "equal_beta"):            
    
        random.seed(line.length() * seed * seed_loop)
    
        # - just random
        if method == "uniform":
    
            for _ in range(0, n):
                
                d = length * random_uniform()
        
                point = line.point_shifted(d)                
                points_on_line.append(point)        
        
        # - randomly within equal segments        
        elif method == "equal_uniform" or method == "equal_beta":
            
            # Computing the start and end points of the equal segments
            segment_points = [line.coords[0]]
            
            for i in range(0, n - 1):
                
                d_part = (length / (n + 1)) * (i + 1)
                point = line.point_shifted(d_part)
                segment_points.append(point)
                
            segment_points.append(line.coords[1])
            
            # Now random points on the segments are added
            if method == "equal_uniform":
                method = "uniform"
            else:
                method = "beta"
                        
            for i in range(0, len(segment_points) - 1): 
                                  
                points_on_line.append(
                    random_point_on_line(
                        (segment_points[i], segment_points[i + 1], method)
                    )
                )
        
    # Inserting new points in the original line
    # points_on_line = sorted(points_on_line)
    
    return points_on_line
    
def random_point_on_line(line, method = "beta"):
    """
    Computes the point that is on the straight line between P0 and P1 and
    the distance d away from P0 and P1.
    
    :param line: Tuple of two coordinate pairs determining the line points.
    :return:
    """ 
    
    line = LineSimple(line)
    
    d = line.length()
    p = None
    
    if (method == "uniform"):
        p = random_uniform * d
    elif (method == "beta"):
        p = random_beta() * d
    
    point = line.point_shifted(p)
    
    return point

def jitter_line_bezier(line):
    """
    Creates a jittered line as described here:
    
    http://stackoverflow.com/a/6373008/3854098 
    http://jsfiddle.net/GfGVE/9/
    
    :param line: Tuple of two coordinate pairs determining the line points.
    """
    
    line = LineSimple(line)
    
    random.seed(line.length() * seed * seed_loop)
    
    curve = []
    curve.append(line.coords[0])
    
    for i in range(0, len(line.coords) -1):
        
        p0_x = line.coords[i][0]
        p0_y = line.coords[i][1]
        p1_x = line.coords[i+1][0]
        p1_y = line.coords[i+1][1]

        diff_y = p1_y - p0_y;
        
        # so the y value can go positive or negative from the typical   
        neg = random_uniform() - 0.5; 
            
        cp1 = (
            -neg + p0_x + ((random_uniform() - 0.5) * diff_y / 8),
            p0_y + 0.3 * diff_y
        )
        cp2 = (
            -neg + p0_x + ((random_uniform() - 0.5) * diff_y / 8),
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
        rand = math.cos(2 * math.pi * random_uniform()) * math.sqrt(-2 * math.log(random_uniform()))
        
        return round((rand * range1) + mean)
    
    def randomizeUniform (range_in = 100, mean = 0.0):
        rand = random_uniform() * range_in;
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
    
    random.seed(line.length() * seed * seed_loop)

    cp1 = None
    cp2 = None
    
    if method == "orthogonal":
        
        # pos = random_uniform()
        pos = 0.5
        
        m = line.point_at_line_pos(pos)
        
        line1 = LineSimple([line.coords[0], m])
        
        line2 = LineSimple([m ,line.coords[1]])
        
        d1 = random_uniform_int() * d
        d2 = random_uniform_int() * d
        
        cp1 = line1.point_orthogonal(random_beta(4,1), d1)
        cp2 = line2.point_orthogonal(random_beta(1,4), d2)
        
        cp1 = line1.point_orthogonal(random_uniform(), d1)
        cp2 = line2.point_orthogonal(random_uniform(), d2)
    
    elif method == "circular":        
        # Displacing point circular around the center of the line
        # A----(-*-)----B
        if d >= line_length_half:           
            point = line.point_shifted(line_length_half)
            cp1 = displace_point(point, line_length_half)
            cp2 = displace_point(point, line_length_half)
        
        # Displacing the point circular on a random position that is on a line
        # which is an inside segment of the original line but the distance d 
        # away from both endpoints.
        # A-(-----)-B
        else:
            point1 = line.point_shifted(d)
            
            line_reverse = LineSimple(line.coords[::-1])       
            point2 = line_reverse.point_shifted(d)
            
            point = random_point_on_line((point1, point2))
            cp1 = displace_point(point, d)
            cp2 = displace_point(point, d)
            
        
    controlpoints = (cp1, cp2)
                
    return controlpoints