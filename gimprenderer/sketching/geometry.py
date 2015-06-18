'''
Created on Jun 11, 2015

@author: mucx

# TO DO:
- Adding classes:
    - Point?
    - Polygon
    
- Multipolygon support
    
'''

from __future__ import division
from abc import ABCMeta, abstractmethod

import math
import sys

class Geometry(object):
    """
    An abstract class defining the base geometry object
    """
    
    __metaclass__ = ABCMeta
 
    @abstractmethod
    def __init__(self):
        """
        Constructor
        """

class Line(Geometry):
    """
    An abstract class defining the connection between points
    """
    __metaclass__  = ABCMeta
 
    def __init__(self, coordinates):
        """
        :param coordinates: A list of lne point coordinate tuples.
        """
        
        # Check that line consists only of two points
        if len(coordinates) > 2:
            print coordinates
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
    
    @abstractmethod
    def length(self):
        raise NotImplementedError
    
class LineSimple(Line):
    """
    A class defining the straight connection between two points. The point
    that is closer to the origin as the first point.
    """
    
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
    
    def vector(self):
        
        x = self.coords[1][0] - self.coords[0][0]
        y = self.coords[1][1] - self.coords[0][1]
        
        return (x, y)
    
    def vector_orthogonal(self):
        """
        Calculates an orthogonal vector to the line using the dot product.
        Two vectors are orthogonal when their dot product is zero.
        """
        
        v1 = self.vector()
        
        v2 = None
            
        try:
            v2_y = -v1[0] / v1[1]
            v2 = (1, v2_y)
        except ZeroDivisionError:   
            v2 = (0, 1)
        
        return v2
    
    def get_delta(self):
        """
        Returns the x or y distance between the two line points based on the
        equation parameter (which determines the ascent of the line)
        """
        
        delta = None
        
        eq_params = self.get_line_equation_params()
        if eq_params is not None:
            delta = self.coords[0][0] - self.coords[1][0] # delta x
        else:
            delta = self.coords[0][1] - self.coords[1][1] # delta y
            
        return delta
    
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
        
        delta_x = x1 - x2
        delta_y = y1 - y2
        
        if (delta_x == 0):
            return None # Vertical line
        else:
            m = (delta_y)/(delta_x)            
            b = y1 - m * x1
            
            return [m,b]
    
    def point_at_line_pos(self, p, reverse = False):
        """
        Calculating the point at the position t * AB on the line from point A
        to point B.
        
        :param: Relative position between A and B (0 is at A, 0.5 middle, 1 is at B)
        :param reverse: False, position between A and B, True between B and A.
        Default is False
        """
        
        a = self.coords[0]
        b = self.coords[1]
        
        p1 = None
        p2 = None        
        if reverse:
            p1 = b
            p2 = a
        else:
            p1 = a
            p2 = b    
        
        x = (1-p) * p1[0] + p * p2[0];
        y = (1-p) * p1[1] + p * p2[1];
        
        return (x,y)
    
    def point_orthogonal(self, pos, d):
        """
        Displaces a point P which is located on a line at a relative position d 
        between A and B orthogonally within a distance d.
        .
        
        :param pos: Relative position of the point between A and B (0...1)
        :param d: Distance the point is displaced orthogonally
        """
        
        p = self.point_at_line_pos(pos)
        
        v = self.vector_orthogonal()
    
        shift = [(p[0], p[1]), (v[0] + p[0], v[1] + p[1])]
        shift_line = LineSimple(shift)
        
        p_displaced = shift_line.point_shifted(d)
        
        return p_displaced
    
    def point_shifted(self, d):
        """
        Computes the point that is on the straight line between A and B and
        the distance d away from B.
        
        :param line: Tuple of two coordinate pairs determining the line points.
        """ 
        
        line_vector = self.vector()        
        length = self.length()
        
        shift = tuple((d / length) * x for x in line_vector)
                
        point_shifted = tuple(sum(t) for t in zip(self.coords[0], shift))
        
        return point_shifted
    
    def line_scale(self, d_abs = None, d_rel = None):
        """
        Equally scaling (extending or shortening at both endpoints) the line
        either with using a relative or absolute value. Returns the new
        endpoints as a tuple.
        
        :param d_abs: Scaling 
        :param d_rel:
        """
        
        d = 0
        if (d_abs is not None and d_rel is None):
            d = d_abs
        elif (d_rel is not None and d_abs is None):
            d = d_rel * self.length()
        else:
            d = d_abs
            print "Two d values provied for line scaling - absolute value used"
        
        a_new = self.point_shifted(-d)
        
        # Using reversed line coordinates
        coords_reversed = self.coords[::-1]
        line_reversed = LineSimple(coords_reversed)        
        b_new = line_reversed.point_shifted(-d) 
        
        return (a_new, b_new)
    
class LineString(Line):
    
    def __init__(self, coordinates):
        """
        :param coordinates: A list of coordinate tuples
        """
        
        self.coords = coordinates
        self.curve = None
        
    def length(self):
        
        length_total = 0
        
        for i in range(1, len(self.coords)):
            line = LineSimple([self.coords[i], self.coords[i - 1]])
            length_total += line.length()
            
        return length_total
    
    def simple_bezier(self, t = 1.0):
        """
        Returns a Bezier curve in SVG from a sequence of points and control 
        points in an array.
        """
        
        def get_controlpoints(point_triple, t = 1.0):
            """
            Given three consecutive points on a line (P0, P1, P2), this function 
            calculates the Bezier control points of P1 using the technique 
            explained by Rob Spencer.
            
            Source: http://scaledinnovation.com/analytics/splines/aboutSplines.html
            """
        
            x0 = point_triple[0][0]
            y0 = point_triple[0][1]
            x1 = point_triple[1][0]
            y1 = point_triple[1][1]
            x2 = point_triple[2][0]
            y2 = point_triple[2][1]
            
            d01 = math.sqrt(math.pow(x1 - x0, 2) + math.pow(y1 - y0, 2))
            d12 = math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))
            
            fa = t * d01 / (d01 + d12) # scaling factor for triangle Ta
            fb = t * d12 / (d01 + d12) # ditto for Tb, simplifies to fb=t-fa
            
            p1x = x1 - fa * (x2 - x0) # x2-x0 is the width of triangle T
            p1y = y1 - fa * (y2 - y0) # y2-y0 is the height of T
            p2x = x1 + fb * (x2 - x0)
            p2y = y1 + fb * (y2 - y0)  
            
            return [[p1x,p1y],[p2x,p2y]];
        
        ########################################################################
        
        controlpoints = []
        controlpoints.append([self.coords[0][0], self.coords[0][1]])
            
        for i in range(1, len(self.coords)-1):  
            
            point_triple = [self.coords[i-1], self.coords[i], self.coords[i+1]]
            
            cps_point = get_controlpoints(point_triple, t)
            
            controlpoints.append([cps_point[0][0], cps_point[0][1]])
            controlpoints.append([cps_point[1][0], cps_point[1][1]])
            
        last = len(self.coords)-1
        
        controlpoints.append([self.coords[last][0], self.coords[last][1]])
        
        curve = self._get_curve(controlpoints)
        
        self.curve = curve
        
        return curve
    
    def catmull_rom_bezier(self, t = 1.0):
        """
        Returns a SVG Bezier curve of a line with the given points.
        
        Source: http://schepers.cc/getting-to-the-point
        
        Catmull-Rom to Cubic Bezier conversion matrix 
        0       1       0       0
        -1/6    1      1/6      0
        0      1/6      1     -1/6
        0       0       1       0
            
        """
        controlpoints = []
        
        point_count = len(self.coords)
        
        for i in range(0, point_count-1):
            
            # Creating an array of relevant knot points
            p = []
            
            if ( 0 == i ):
                p.append([self.coords[i][0], self.coords[i][1]])
                p.append([self.coords[i][0], self.coords[i][1]])
                p.append([self.coords[i+1][0], self.coords[i+1][1]])
                p.append([self.coords[i+2][0], self.coords[i+2][1]])
            elif (len(self.coords) - 2 == i ):
                p.append([self.coords[i-1][0], self.coords[i-1][1]])
                p.append([self.coords[i][0], self.coords[i][1]])
                p.append([self.coords[i+1][0], self.coords[i+1][1]])
                p.append([self.coords[i+1][0], self.coords[i+1][1]])
            else:
                p.append([self.coords[i-1][0], self.coords[i-1][1]])
                p.append([self.coords[i][0], self.coords[i][1]])
                p.append([self.coords[i+1][0], self.coords[i+1][1]])
                p.append([self.coords[i+2][0], self.coords[i+2][1]])
    
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
            
            controlpoints.append([bp[1][0], bp[1][1]])
            controlpoints.append([bp[2][0], bp[2][1]])
            
        print controlpoints
            
        curve = self.get_curve(controlpoints)
        
        self.curve = curve
        
        return curve
    
    def get_curve(self, cps):
        """
        Creates a coordinate array of points and control points that can be
        used as a SVG path.
        
        :param cps: An array of control points coordinates.
        """
        
        # Checking every linepoint after the start point for two control points 
        if (len(self.coords) - 1) != (len(cps) / 2):
            print "coords: " + str(len(self.coords))
            print "cps: " + str(len(cps))
            sys.exit("Curve cannot be created - control point error:")
        else:      
            
            # Adding first point  
            curve = [self.coords[0]]
            
            # Adding remaining points
            for i in range(0, len(self.coords) -1):
                
                cp_pos = i * 2
                
                curve.append(cps[cp_pos])
                curve.append(cps[cp_pos + 1])
                curve.append(self.coords[i + 1])
        
        return curve
    
class Polygon(object):
    """
    Classdocs
    """
    
    def __init__(self, linearrings):
        """
        :param coordinates: A list of coordinate tuples
        """
        
        self.linearrings = linearrings
        
    def disjoin(self, angle_disjoin = 135.0):
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
        
        # Get linearrings of multipolygons
        for linearring in self.linearrings:
            
            segment = []
            segment.append(linearring[0])
            
            # Iterate over linearring
            for i in range(1, len(linearring) -1):
                
                points = []
                
                points.append(linearring[i - 1])
                points.append(linearring[i])
                points.append(linearring[i + 1])
                
                angle = get_three_point_angle(points)
                
                # Continue segment
                if (angle >= angle_disjoin):
                    segment.append(linearring[i])
                    
                # Finish segment and create new one
                else:
                    segment.append(linearring[i])                    
                    outline_segments.append(segment)
                    
                    segment = []
                    segment.append(linearring[i])
                
            segment.append(linearring[0])                    
            outline_segments.append(segment)
            
        return outline_segments