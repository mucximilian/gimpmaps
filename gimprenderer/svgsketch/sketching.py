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
        
    def get_control_points(self, points, t):
        """
        Calculates the control points of a point P1 between the points P0 and 
        P2 based on the technique developed by Rob Spencer:
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
    
    def create_bezier_path(self, line):
            
        path_m = "M " + str(line[0][0]) + "," + str(line[0][1])
        
        path_c = " C " + str(line[0][0]) + "," + str(line[0][1])
            
        for i in range(1, len(line)-1):
            
            print "calculating control points"     
            
            points = [line[i-1], line[i], line[i+1]]
            
            cps = self.get_control_points(points, 1)
            
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
        
        m = self.calculate_midpoint(line)
        
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
        
        n = self.calculate_quarterpoint(line)
        
        # TO DO:
        # Calculate point that is within r and orthogonal to a 10 % section of
        # the line around n
        
        x = 0
        y = 0
        
        return [x,y]
    
    def calculate_midpoint(self, line):
        """
        Calculating the mid point of a line consisting of two points
        """
        
        x = (line[0][0] + line[1][0]) / 2
        y = (line[0][1] + line[1][1]) / 2
        
        return [x,y]
    
    def calculate_quarterpoint(self, line):
        """
        Calculating the mid point of a line consisting of two points
        """
        
        x = (line[0][0] + line[1][0]) / 8
        y = (line[0][1] + line[1][1]) / 8
        
        return [x,y]