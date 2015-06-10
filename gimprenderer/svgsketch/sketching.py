'''
Created on Jun 5, 2015

@author: mucx
'''

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
        random.seed(seed)
        
    def simple_bezier(self, linepoints, t = 1.0):
        """
        Returns a Bezier curve in SVG from a sequence of points and control 
        points in an array.
        """
        
        curve = []
        curve.append([linepoints[0][0], linepoints[0][1]])
        curve.append([linepoints[0][0], linepoints[0][1]])
            
        for i in range(1, len(linepoints)-1):  
            
            points = [linepoints[i-1], linepoints[i], linepoints[i+1]]
            
            controlpoints = self.get_control_points(points, t)
            
            curve.append([controlpoints[0][0], controlpoints[0][1]])
            curve.append([linepoints[i][0], linepoints[i][1]])
            curve.append([controlpoints[1][0], controlpoints[1][1]])
            
        last = len(linepoints)-1
        
        curve.append([linepoints[last][0], linepoints[last][1]])
        curve.append([linepoints[last][0], linepoints[last][1]])
        
        return curve
        
    def get_control_points(self, points, t = 1.0):
        """
        Given three consecutive points on a line (P0, P1, P2), this function 
        calculates the Bezier control points of P1 using the technique 
        explained by Rob Spencer.
        
        Source: http://scaledinnovation.com/analytics/splines/aboutSplines.html
        """
    
        x0 = points[0][0]
        y0 = points[0][1]
        x1 = points[1][0]
        y1 = points[1][1]
        x2 = points[2][0]
        y2 = points[2][1]
        
        d01 = math.sqrt(math.pow(x1 - x0, 2) + math.pow(y1 - y0, 2))
        d12 = math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))
        
        fa = t * d01 / (d01 + d12) # scaling factor for triangle Ta
        fb = t * d12 / (d01 + d12) # ditto for Tb, simplifies to fb=t-fa
        
        p1x = x1 - fa * (x2 - x0) # x2-x0 is the width of triangle T
        p1y = y1 - fa * (y2 - y0) # y2-y0 is the height of T
        p2x = x1 + fb * (x2 - x0)
        p2y = y1 + fb * (y2 - y0)  
        
        return [[p1x,p1y],[p2x,p2y]];
        
    def catmull_rom_bezier(self, linepoints, t = 1.0):
        """
        Returns a SVG Bezier curve of a line with the given points.
        
        Source: http://schepers.cc/getting-to-the-point
        
        Catmull-Rom to Cubic Bezier conversion matrix 
        0       1       0       0
        -1/6    1      1/6      0
        0      1/6      1     -1/6
        0       0       1       0
            
        """
        curve = []
        curve.append([linepoints[0][0], linepoints[0][1]])
        
        point_count = len(linepoints)
        
        for i in range(0, point_count-1):
            
            # Creating an array of relevant knot points
            p = []
            
            if ( 0 == i ):
                p.append([linepoints[i][0], linepoints[i][1]])
                p.append([linepoints[i][0], linepoints[i][1]])
                p.append([linepoints[i+1][0], linepoints[i+1][1]])
                p.append([linepoints[i+2][0], linepoints[i+2][1]])
            elif (len(linepoints) - 2 == i ):
                p.append([linepoints[i-1][0], linepoints[i-1][1]])
                p.append([linepoints[i][0], linepoints[i][1]])
                p.append([linepoints[i+1][0], linepoints[i+1][1]])
                p.append([linepoints[i+1][0], linepoints[i+1][1]])
            else:
                p.append([linepoints[i-1][0], linepoints[i-1][1]])
                p.append([linepoints[i][0], linepoints[i][1]])
                p.append([linepoints[i+1][0], linepoints[i+1][1]])
                p.append([linepoints[i+2][0], linepoints[i+2][1]])
    
            # Calculating the bezier points from the knot points
            bp = [];
            
            # This assignment is for readability only
            x0 = p[0][0]
            y0 = p[0][1]
            x1 = p[1][0]
            y1=  p[1][1]
            x2 = p[2][0]
            y2 = p[2][1]
            x3 = p[3][0]
            y3=  p[3][1]
            
            # Using the factor t as "tension control"           
            f = (1 / t) * 6
            
            bp.append([x1, y1])
            bp.append([
                    ((-x0 + f*x1 + x2) / f),
                    ((-y0 + f*y1 + y2) / f)
            ])
            bp.append([
                    ((x1 + f*x2 - x3) / f),
                    ((y1 + f*y2 - y3) / f)
            ])
            bp.append([x2, y2])
            
            curve.append([bp[1][0], bp[1][1]])
            curve.append([bp[2][0], bp[2][1]])
            curve.append([bp[3][0], bp[3][1]])
        
        return curve
           
    def add_sketch_points(self, line, r):
        
        point_a = self.displace_point_circle(line[0], r)
        point_b = self.displace_point_circle(line[1], r)
        point_m = self.displace_point_orthogonal(line, r)
        point_n = self.displace_point_orthogonal_area(line, r)
        
        line_sketch = [point_a, point_m, point_n, point_b]
        
        return line_sketch
    
    def displace_point_circle(self, point, r):
        """
        Displaces a point, r defines the radius within which the point 
        coordinates are randomly perturbed (with a uniform random deviate)
        """
        
        angle = random.random() * (2 * math.pi)
        distance = random.random() * r
        
        print math.radians(angle)
        
        x = point[0] + (math.cos(math.radians(angle)) * distance)
        y= point[1] + (math.sin(math.radians(angle)) * distance)
        
        return [x,y]
    
    def displace_point_orthogonal(self, line, r):
        """
        Displaces a point, r defines the radius within which the point 
        coordinates are randomly perturbed (with a uniform random deviate)
        """
        
        m = self.calculate_point_at_line_pos(line, 0.5)
        
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
        
        n = self.calculate_point_at_line_pos(line, 0.75)
        
        # TO DO:
        # Calculate point that is within r and orthogonal to a 10 % section of
        # the line around n
        
        x = 0
        y = 0
        
        return [x,y]
    
    def calculate_point_at_line_pos(self, line, t):
        """
        Calculating the mid point of a line consisting of two points
        """
        
        x = (1-t)*line[0][0] + t*line[1][0];
        y = (1-t)*line[0][1] + t*line[1][1];
        
        return [x,y]
    
    def line_as_wkt(self, line):
        """
        Returns an array of coordinate pair arrays in WKT notation.
        """
        
        line_wkt = "LINESTRING ("        
        for p in line:
            line_wkt += str(p[0]) + " " + str(p[1]) + ", "            
        line_wkt = line_wkt[:-2] + ")"
        
        return line_wkt
    
    def polygon(self, polygon, angle_disjoin = 135.0):
        """
        Disjoins polygon linestrings into segments at vertices where the angle 
        between the lines from the vertex to the vertex behind and the vertex 
        to the vertex ahead exceeds a given threshold. Returns the calculated
        line segments as an array.
        
        :param polygon: Input geometry, array of lines (arrays of coordinates)
        :param angle_disjoin: Threshold angle for disjoin in degree.
        """
        
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
                
    def get_three_point_angle(self, points):
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
        
        x1 = line[0][0]
        y1 = line[0][1]
        x2 = line[1][0]
        y2 = line[1][1]

        # Ensure random perturbation is no more than 10% of line length.
        lenSq = (x1-x2)*(x1-x2) + (y1-y2)*(y1-y2)
        offset = max_offset

        if (max_offset * max_offset * 100 > lenSq):
            offset = math.sqrt(lenSq)/10.0

        half_offset = offset/2
        
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