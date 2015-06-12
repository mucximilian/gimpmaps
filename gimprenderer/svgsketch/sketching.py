'''
Created on Jun 5, 2015

@author: mucx
'''

from __future__ import division

import math
import random

class SketchRenderer(object):
    '''
    classdocs
    '''

    def __init__(self, seed):
        '''
        Constructor
        '''
        self.seed = seed
           
    def displace_points_handy(self, line, r):
        """
        Does what the Handy renderer is supposed to do (according to paper)
        """
        
        point_a = self.displace_point(line[0], r)
        point_b = self.displace_point(line[1], r)
        point_m = self.displace_point_orthogonal(line, r)
        point_n = self.displace_point_orthogonal_area(line, r)
        
        line_sketch = [point_a, point_m, point_n, point_b]
        
        return line_sketch
    
    def displace_point(self, point, r, method = "square"):
        """
        Displaces a point, r defines the radius within which the point 
        coordinates are randomly perturbed (with a uniform random deviate).
        
        Note: The random seed should be set outside of the function.
        """
        
        # random.seed(r * self.seed)
        
        coords_new = None
        
        if (method == "circle"):
            angle = random.random() * (2 * math.pi)
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
    
    def displace_point_orthogonal(self, line, r):
        """
        Displaces a point, r defines the radius within which the point 
        coordinates are randomly perturbed (with a uniform random deviate)
        """
        
        m = self.calculate_point_at_line_pos(line, 0.5)
        
        print m
        
        # TO DO:
        # Calculate point that is within r on a orthogonal line through m 
        
        x = 0
        y = 0
        
        return [x,y]
    
    def displace_point_orthogonal_area(self, line, r):
        """
        Displaces a point, r defines the radius within which the point 
        coordinates are randomly perturbed (with a uniform random deviate)
        """
        
        n = line.calculate_point_at_line_pos(0.75)
        
        print n
        
        # TO DO:
        # Calculate point that is within r and orthogonal to a 10 % section of
        # the line around n
        
        x = 0
        y = 0
        
        return [x,y]
    
    def polygon(self, polygon, angle_disjoin = 135.0):
        """
        Disjoins polygon linestrings into segments at vertices where the angle 
        between the lines from the vertex to the vertex behind and the vertex 
        to the vertex ahead exceeds a given threshold. Returns the calculated
        line segments as an array.
        
        :param polygon: Input geometry, array of lines (arrays of coordinates)
        :param angle_disjoin: Threshold angle for disjoin in degree.
        """
        
        def get_three_point_angle(points):
            """
            Calculates the angle between the lines from a vertex to the vertex 
            behind and the vertex to the vertex ahead.
            
            :param points: Coordinate array, containing three points 
            (vertex behind, vertex, vertex ahead)
            """
            
            p0 = points[0] # point_behind
            p1 = points[1] # point_center
            p2 = points[2] # point_ahead
            
            a = (p1[0] - p0[0])**2 + (p1[1] - p0[1])**2
            b = (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2
            c = (p2[0] - p0[0])**2 + (p2[1] - p0[1])**2
            
            angle = math.acos((a + b - c) / math.sqrt(4 * a * b)) * 180/math.pi
        
            return angle
        
        outline_segments = []
        
        for line in polygon:
            
            print line
            print "###"
            
            segment = []
            segment.append(line[0])
            
            for i in range(1, len(line) -1):
                
                points = []
                
                points.append(line[i - 1])
                points.append(line[i])
                points.append(line[i + 1])
                
                angle = self.get_three_point_angle(points)
                
                # Continue segment
                if (angle >= angle_disjoin):
                    segment.append(line[i])
                    
                # Finish segment and create new one
                else:
                    segment.append(line[i])                    
                    outline_segments.append(segment)
                    
                    segment = []
                    segment.append(line[i])
                
            segment.append(line[0])                    
            outline_segments.append(segment)
            
        return outline_segments
    
    def line_jitter_bezier(self, line, d_rel = 10.0, d_abs = None):
        """
        Calculates random control points for a jittered line.
        
        :param line: The LineString to apply the jittering to.
        """
        
        d = None        
        if d_abs is not None:
            d = d_abs
        else:
            d = line.length() / d_rel
        
        random.seed(line.length() * self.seed)
        
        controlpoints = []
        controlpoints.append(line.coords[0])
        
        self.get_random_control_point((line.coords[0], line.coords[1]), d)
        
        for i in range(1, len(line.coords) -1):
            
            point_behind = line.coords[i - 1]
            point = line.coords[i]
            point_ahead = line.coords[i + 1]
                            
            cp1 = self.get_random_control_point((point, point_behind), d)            
            cp2 = self.get_random_control_point((point, point_ahead), d)
            
            controlpoints.append(cp1)
            controlpoints.append(cp2)
            
        controlpoints.append(line.coords[-1])
            
        return controlpoints
    
    def get_random_control_point(self, line, d):
        """
        Computes the point that is on the straight line between P0 and P1 and
        the distance d away from.
        
        :param line: A tuple that contains both points. 
        """
        
        point1 = self.get_point_shifted(line, d)
        print point1
        point2 = self.add_point_to_line((point1, line[1]))
        print point2
        cp = self.displace_point(point2, d)
        
        return cp
    
    def get_point_shifted(self, line, d):
        """
        Computes the point that is on the straight line between P0 and P1 and
        the distance d away from.
        
        :param line: A tuple that contains both points. 
        """ 
        
        x = line[1][0] - line[0][0]
        y = line[1][1] - line[0][1]        
        vector = (x,y)
        l = math.sqrt(x**2 + y**2)    
        
        shift = tuple((d / l) * x for x in vector)
                
        point_shifted = tuple(sum(t) for t in zip(line[0], shift))
        
        return point_shifted        
    
    def line_jitter_bezier_test(self, line):
        """
        Creates a jittered line as described here:
        
        http://stackoverflow.com/a/6373008/3854098 
        http://jsfiddle.net/GfGVE/9/
        
        :param line: The LineString to apply the jittering to.
        """
        
        random.seed(line.length() * self.seed)
        
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
            
            print neg
                
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
            
    def add_points_to_line(self, line, n = 1, method = "equal"):
        """
        Adds a specified number of points to a line between two points using
        the selected method.
        
        :param line: geometry.LineSimple between two points (coordinate tuple
        array)
        """
        
        a = min(line.coords) # Get point with smaller x value as point a
        b = max(line.coords)
            
        points_on_line = []
        
        # Distribute points equally
        if method == "equal":
            
            for i in range(0, n + 1):
            
                d = (line.length() / (n + 1)) * i
            
                point = self.get_point_shifted((a, b), d)                
                points_on_line.append(point)
        
        # Distribute points randomly  
        elif method == "uniform" or method == "equal_uniform":            
        
            random.seed(line.length() * self.seed)
        
            # - just random
            if method == "uniform":
        
                for _ in range(0, n + 1):
                    
                    d = line.length() * random.random()
            
                    point = self.get_point_shifted((a, b), d)                
                    points_on_line.append(point)        
            
            # - randomly within equal partitions        
            elif method == "equal_uniform":
                
                # Determine the break points for the segments
                breaks = []
                for i in range(1, n):
                    d_part = line.length() / n * i
                    point = self.get_point_shifted((a, b), d_part)
                    breaks.append(point)
                
                # Now rondom points between the segments are computed
                points_on_line.append(
                    self.add_random_point_to_line((a, breaks[0]))
                )                
                for i in range(0, n - 2):                   
                    points_on_line.append(
                        self.add_random_point_to_line(
                            (breaks[i], breaks[i + 1])
                        )
                    )                    
                points_on_line.append(
                    self.add_random_point_to_line((breaks[-1], b))
                )
            
        # Inserting new points in the original line
        line_new = [a]
        line_new += sorted(points_on_line)
        line_new += [b]
        
        return line_new
    
    def add_random_point_to_line(self, line):
        """
        Computes the point that is on the straight line between P0 and P1 and
        the distance d away from.
        
        :param line: A tuple that contains both points. 
        """ 
        
        d_x = math.fabs(line[0][0] - line[1][0])
        d_y = math.fabs(line[0][1] - line[1][1])
        
        d = math.sqrt(d_x**2 + d_y**2)
        d_rand = random.random() * d
        
        point = self.get_point_shifted(line, d_rand)
        
        return point
        
    
class HandyRenderer(SketchRenderer):
    '''
    This class is a customized and simplified copy of the HandyRenderer.java 
    class which contains the geometry processing logic of the Handy Processing 
    library developed by Jo Wood.
    
    http://www.gicentre.net/software/#/handy/
    '''

    def __init__(self, seed, roughness = 1.0, bowing = 1.0):
        '''
        Constructor
        '''
        super(HandyRenderer, self).__init__(seed)
        
        self.bowing = bowing
        self.roughness = roughness
    
    def line(self, line, max_offset):
        """
        Clone of the function:
        
        void line(float x1, float y1, float x2, float y2, float maxOffset)
        """
        
        x1 = line.coords[0][0]
        y1 = line.coords[0][1]
        x2 = line.coords[1][0]
        y2 = line.coords[1][1]

        # Ensure random perturbation is no more than 10% of line length.
        lenSq = (x1-x2)*(x1-x2) + (y1-y2)*(y1-y2)
        offset = max_offset

        if (max_offset * max_offset * 100 > lenSq):
            offset = math.sqrt(lenSq)/10.0

        half_offset = offset/2
        
        random.seed(line.length * self.seed)
        
        divergePoint = 0.2 + random.random() * 0.2

        # This is the midpoint displacement value to give slightly bowed lines.
        midDispX = self.bowing * max_offset * (y2-y1) / 200.0
        midDispY = self.bowing * max_offset * (x1-x2) / 200.0

        midDispX = self.get_offset(-midDispX, midDispX)
        midDispY = self.get_offset(-midDispY, midDispY)

        # Calculating line 1           
        line1 = self.get_displaced_linepoints(x1, y1, x2, y2, 
                                              midDispX, midDispY, 
                                              divergePoint, offset)
        
        # Calculating line 2
        line2 = self.get_displaced_linepoints(x1, y1, x2, y2, 
                                              midDispX, midDispY, 
                                              divergePoint, half_offset)
                    
        return [line1, line2]
        
    def get_offset(self, minVal, maxVal):
        """
        Clone of the function:
        
        float getOffset(float minVal, float maxVal)
        
        Should be called only from the 'line' function for secure random seed.
        """
             
        offset = self.roughness * (random.random() * (maxVal - minVal) + minVal)
             
        return offset
    
    def get_displaced_linepoints(self, x_a, y_a, x_b, y_b, 
                     midDispX, midDispY, divergePoint, offset):
        """
        This is part of the line function in the original Java code and was put
        separately for readability reasons.
        """
        
        x0 = x_a + self.get_offset(-offset, offset)
        y0 = y_a + self.get_offset(-offset, offset)
        p0 = [x0, y0]
        
        x1 = midDispX + x_a + (x_b-x_a) * divergePoint + self.get_offset(-offset, offset)
        y1 = midDispY + y_a + (y_b-y_a) * divergePoint + self.get_offset(-offset, offset)
        p1 = [x1, y1]
        
        x2 = midDispX + x_a + 2 * (x_b-x_a) * divergePoint + self.get_offset(-offset, offset)
        y2 = midDispY + y_a + 2 * (y_b-y_a) * divergePoint + self.get_offset(-offset, offset)
        p2 = [x2, y2] 
        
        x3 = + x_b + self.get_offset(-offset, offset)
        y3 = + y_b + self.get_offset(-offset, offset)
        p3 = [x3, y3]
        
        # Note:
        # self.get_offset(...) cannot be substituted to a variable as the
        # random function inside it needs to be called each time
        
        line = [p0, p1, p2, p3]
        
        return line