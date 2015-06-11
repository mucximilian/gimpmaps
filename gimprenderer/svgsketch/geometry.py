'''
Created on Jun 11, 2015

@author: mucx
'''

# TO DO: Adding Class Point?

from __future__ import division

import math
import abc
import sys

class Geometry(object):
    """
    An abstract class defining the base geometry object
    """
    _metaclass__  = abc.ABCMeta
 
    def __init__(self):
        """
        Constructor
        """

class Line(Geometry):
    """
    An abstract class defining the connection between two points
    """
    _metaclass__  = abc.ABCMeta
 
    def __init__(self, coordinates):
        """
        :param coordinates: A list of coordinate tuples
        """
        
        # Check that line consists only of two points
        if len(coordinates) > 2:
            sys.exit("Too many points for simple line - interrupted.")
        else:
            self.coords = coordinates
        
    def as_wkt(self, line):
        """
        Returns an list of coordinate pair arrays in WKT notation.
        """
        
        line_wkt = "LINESTRING ("        
        for p in self.coords:
            line_wkt += str(p[0]) + " " + str(p[1]) + ", "            
        line_wkt = line_wkt[:-2] + ")"
        
        return line_wkt
    
    @abc.abstractmethod
    def length(self):
        raise NotImplementedError
    
class LineSimple(Line):
    
    def __init__(self, coordinates):
        """
        :param coordinates: A list of coordinate tuples
        """
        
        super(LineSimple, self).__init__(coordinates)
        
    def length(self):
        """
        Calculates the distance between the two line points using the
        pythagorean theorem.
        """
        
        d_x = math.fabs(self.coords[0][0] - self.coords[1][0])
        d_y = math.fabs(self.coords[0][1] - self.coords[1][1])
        
        l = math.sqrt(d_x**2 + d_y**2)
        
        return l
    
    def get_line_equation_params(self):
        """
        Identifies the line equation y = mx + b for a line which is determined 
        by two points.
        
        :param line: Line class determining a line by two points (coordinate 
        tuple array)
        """
        
        x1 = self.coords[0][0]
        y1 = self.coords[0][1]
        x2 = self.coords[1][0]
        y2 = self.coords[1][1]
        
        m = (y1 - y2)/(x1 - x2)
        
        b = y1 - m * x1
        
        return [m,b]
    
    def calculate_point_at_line_pos(self, t):
        """
        Calculating the point at the position t * AB on the line from point A
        to point B.
        """
        
        x = (1-t) * self.coords[0][0] + t * self.coords[1][0];
        y = (1-t) * self.coords[0][1] + t * self.coords[1][1];
        
        return [x,y]
    
class LineString(Line):
    
    def __init__(self, coordinates):
        """
        :param coordinates: A list of coordinate tuples
        """
        
        self.coords = coordinates
        
    def length(self):
        return 0
    
    def simple_bezier(self, linepoints, t = 1.0):
        """
        Returns a Bezier curve in SVG from a sequence of points and control 
        points in an array.
        """
        
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
        
        curve = []
        curve.append([linepoints[0][0], linepoints[0][1]])
        curve.append([linepoints[0][0], linepoints[0][1]])
            
        for i in range(1, len(linepoints)-1):  
            
            points = [linepoints[i-1], linepoints[i], linepoints[i+1]]
            
            controlpoints = get_control_points(points, t)
            
            curve.append([controlpoints[0][0], controlpoints[0][1]])
            curve.append([linepoints[i][0], linepoints[i][1]])
            curve.append([controlpoints[1][0], controlpoints[1][1]])
            
        last = len(linepoints)-1
        
        curve.append([linepoints[last][0], linepoints[last][1]])
        curve.append([linepoints[last][0], linepoints[last][1]])
        
        return curve
    
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