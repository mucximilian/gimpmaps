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
        
    def get_control_points_simple(self, points, t):
        """
        Calculates the control points of a point P1 between the points P0 and 
        P2 using the technique explained by Rob Spencer:
        
        http://scaledinnovation.com/analytics/splines/aboutSplines.html
        """
    
        x0 = points[0][0]
        y0 = points[0][1]
        x1 = points[1][0]
        y1 = points[1][1]
        x2 = points[2][0]
        y2 = points[2][1]
        
        d01 = math.sqrt(math.pow(x1 - x0, 2) + math.pow(y1 - y0, 2))
        d12 = math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))
        
        fa=t*d01/(d01+d12) # scaling factor for triangle Ta
        fb=t*d12/(d01+d12) # ditto for Tb, simplifies to fb=t-fa
        
        p1x=x1-fa*(x2-x0) # x2-x0 is the width of triangle T
        p1y=y1-fa*(y2-y0) # y2-y0 is the height of T
        p2x=x1+fb*(x2-x0)
        p2y=y1+fb*(y2-y0)  
        
        return [[p1x,p1y],[p2x,p2y]];
    
    def get_control_points_spline(self, points, t):
        """
        Calculates the control points of a point P1 between the points P0 and 
        P2 using the centripetal Catmull-Rom spline:
        
        http://en.wikipedia.org/wiki/Centripetal_Catmull%E2%80%93Rom_spline
        """
        
        pass
    
        # TO DO:
        # Implement Catmull-Rom spline technique here
        
    def catmullRom2bezier(self, points):
        """
        
        
        Source: http://schepers.cc/getting-to-the-point
        """
        
        d = "M "
        d += str(points[0][0]) + "," + str(points[0][0])
        
        point_count = len(points)
        
        print point_count
        
        for i in range(0, point_count-1):
            p = []
            
            if ( 0 == i ):
                p.append([points[i][0], points[i][1]])
                p.append([points[i][0], points[i][1]])
                p.append([points[i+1][0], points[i+1][1]])
                p.append([points[i+2][0], points[i+2][1]])
            elif (len(points) - 2 == i ):
                p.append([points[i-1][0], points[i-1][1]])
                p.append([points[i][0], points[i][1]])
                p.append([points[i+1][0], points[i+1][1]])
                p.append([points[i+1][0], points[i+1][1]])
            else:
                p.append([points[i-1][0], points[i-1][1]])
                p.append([points[i][0], points[i][1]])
                p.append([points[i+1][0], points[i+1][1]])
                p.append([points[i+2][0], points[i+2][1]])
            
            # Catmull-Rom to Cubic Bezier conversion matrix 
            #    0       1       0       0
            #  -1/6      1      1/6      0
            #    0      1/6      1     -1/6
            #    0       0       1       0
            
            bp = [];
            bp.append([p[1][0],  p[1][1]])
            bp.append([
                    ((-p[0][0] + 6*p[1][0] + p[2][0]) / 6),
                    ((-p[0][1] + 6*p[1][1] + p[2][1]) / 6)
            ])
            bp.append([
                    ((p[1][0] + 6*p[2][0] - p[3][0]) / 6),
                    ((p[1][1] + 6*p[2][1] - p[3][1]) / 6)
            ])
            bp.append( [p[2][0], p[2][1] ] )
            
            d += " C " + str(bp[1][0]) + ","
            d += str(bp[1][1]) + " " + str(bp[2][0]) + ","
            d += str(bp[2][1]) + " " + str(bp[3][0]) + ","
            d += str(bp[3][1]) + " "
        
        return d
    
    def create_bezier_path(self, line):
            
        path_m = "M " + str(line[0][0]) + "," + str(line[0][1])
        
        path_c = " C " + str(line[0][0]) + "," + str(line[0][1])
            
        for i in range(1, len(line)-1):  
            
            points = [line[i-1], line[i], line[i+1]]
            
            cps = self.get_control_points_simple(points, 1)
            
            path_c += " " + str(cps[0][0]) + "," + str(cps[0][1])
            path_c += " " + str(line[i][0]) + "," + str(line[i][1])
            path_c += " " + str(cps[1][0]) + "," + str(cps[1][1])
            
        last = len(line)-1
        path_c += " " + str(line[last][0]) + "," + str(line[last][1])
        path_c += " " + str(line[last][0]) + "," + str(line[last][1])
        
        path = path_m + path_c
        
        return path
           
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
    
    def print_line_as_wkt(self, line):
        
        line_wkt = "LINESTRING ("        
        for p in line:
            line_wkt += str(p[0]) + " " + str(p[1]) + ", "            
        line_wkt = line_wkt[:-2] + ")"
        
        print line_wkt
        
    def print_line_as_svg(self, line):
        
        line_svg = "M "        
        for p in line:
            line_svg += str(p[0]) + " " + str(p[1]) + " L"            
        line_svg = line_svg[:-2]
        
        print line_svg
    
class HandyRenderer(SketchRenderer):
    '''
    This class is a customized and simplified clone of the HandyRenderer.java 
    class of the Handy Processing library by Jo Wood.
    '''

    def __init__(self, seed):
        '''
        Constructor
        '''
        random.seed(seed)
        
        self.bowing = 1
        self.roughness = 1
    
    def handy_line(self, line, maxOffset):
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
        offset = maxOffset

        if (maxOffset*maxOffset*100 > lenSq):
            offset = math.sqrt(lenSq)/10

        half_offset = offset/2
        
        divergePoint = 0.2 + random.random()*0.2

        # This is the midpoint displacement value to give slightly bowed lines.
        midDispX = self.bowing * maxOffset * (y2-y1)/200
        midDispY = self.bowing * maxOffset * (x1-x2)/200

        midDispX = self.get_offset(-midDispX, midDispX)
        midDispY = self.get_offset(-midDispY, midDispY)

        p1 = [
              x1 + self.get_offset(-offset, offset),
              y1 + self.get_offset(-offset, offset)
            ]
        p2 = [
              midDispX+x1+(x2-x1)*divergePoint + self.get_offset(-offset, offset),
              midDispY+y1+(y2-y1)*divergePoint + self.get_offset(-offset, offset)
            ]
        p3 = [
            midDispX+x1+2*(x2-x1)*divergePoint + self.get_offset(-offset, offset),
            midDispY+y1+2*(y2-y1)*divergePoint + self.get_offset(-offset, offset)
            ] 
        p4 = [
              +x2 + self.get_offset(-offset, offset),
              +y2 + self.get_offset(-offset, offset)
            ]
        
        p12 = [
              x1 + self.get_offset(-half_offset, half_offset),
              y1 + self.get_offset(-half_offset, half_offset)
            ]
        p22 = [
              midDispX+x1+(x2-x1)*divergePoint + self.get_offset(-half_offset, half_offset),
              midDispY+y1+(y2-y1)*divergePoint + self.get_offset(-half_offset, half_offset)
            ]
        p32 = [
            midDispX+x1+2*(x2-x1)*divergePoint + self.get_offset(-half_offset, half_offset),
            midDispY+y1+2*(y2-y1)*divergePoint + self.get_offset(-half_offset, half_offset)
            ] 
        p42 = [
              +x2 + self.get_offset(-half_offset, half_offset),
              +y2 + self.get_offset(-half_offset, half_offset)
            ]
        
        # Note:
        # self.get_offset(...) cannot be substituted to a variable as the
        # random function inside it needs to be called each time
            
        l1 = [p1, p2, p3, p4]
        l2 = [p12, p22, p32, p42]
        
        return [l1, l2]
        
    def get_offset(self, minVal, maxVal):
        """
        Clone of the function:
        
        float getOffset(float minVal, float maxVal)
        """
             
        return self.roughness*(random.random()*(maxVal-minVal)+minVal)        