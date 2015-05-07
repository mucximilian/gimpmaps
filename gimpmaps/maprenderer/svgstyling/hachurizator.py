'''
Created on Apr 28, 2015

@author: mucx
'''

from shapely.geometry import LineString
from shapely.geometry import MultiLineString
from shapely.geometry import Polygon
from shapely.geometry import Point
from shapely.geometry.polygon import LinearRing

import math
import svgwrite
from shapely.geometry.multilinestring import MultiLineString

class Hachurizator(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        
    def get_svg_hachure(self, path):
        """
        Returns a SVG hachure for the specified polygon input path
        """
        
        # TO DO: Check if input is polygon!
        
        # Creating a (Multi-)Polygon consisting of an array of points        
        polygon = self.multipolygon_from_svgpath(path)
        
        hachure_lines = self.create_hachure_lines(polygon)
        
        hachure = svgwrite.path.Path(hachure_lines)
        
        return hachure
    
    def multipolygon_from_svgpath(self, path):
        """
        Returning a Shapely multipolygon array from a SVG path input
        """
        
        multipolygon = []
        
        # Getting the "d" string of the SVG path
        path_str = path.commands[0]
        
        # Split path into single polygons
        multipolygon_str = path_str.split("Z");        
        multipolygon_str.pop() # Remove last item from list which is empty
        
        for polygon_str in multipolygon_str:
            
            polygon_points = []           
            
            polygon_str = polygon_str.strip() # Trim whitespaces
            
            # Split polygon into single points
            points_str = polygon_str.split(" ");           
            points_str.remove('L')
            points_str.remove('M')
            
            # Appending point pairs (coordinates) to an array (polygon)
            for i in range(0, len(points_str), 2):
                polygon_points.append(
                    [float(points_str[i]), float(points_str[i+1])]
                )
                
            # Adding first point again
            polygon_points.append([float(points_str[0]), float(points_str[1])])
            
            # Appending the created polygon to an array (multipolygon)
            multipolygon.append(polygon_points)
            
        # Extracting the first polygon as outline from the multipolygon array
        exterior = multipolygon.pop(0)
        
        # Creating Shapely polygon from outline and remaining polygons
        polygon = Polygon(exterior, multipolygon)

        return polygon
    
    def create_hachure_lines(self, polygon):
        """
        Returning hachure as an array of lines 
        """
               
        # Creating the bounding box hachure lines
        lines = self.calculate_bbox_hachure(polygon.bounds, 8, 10)     
        
        intersections = []
        
        for line in lines:

            # Calculating the intersection of hachure lines and polygon
            self.calculateIntersection(line, polygon, intersections)
        
        # TO DO check if can be deleted as type is checked earlier now
        for item in intersections:
            if (type(item) == Point):
                intersections.remove(item)

        # Filter and randomize hachure lines
        # TO DO: function
        # hachure_lines = randomizeLines(intersection)
        #hachure_lines = None
        
        #multiline = MultiLineString(hachure_lines)
        #print multiline
        
        multiline_svg = self.create_svg_multilinepath(intersections)
                
        return multiline_svg
    
    def create_svg_multilinepath(self, multiline):
        """
        Returning a Shapely multilinestring as a SVG multiline path string
        """
        
        multiline_svg = ""
        
        for line in multiline:
            multiline_svg += "M "
            
            i = 0
            
            for point in line.coords:
                
                multiline_svg += (
                    str(round(point[0],2)) + " " + 
                    str(round(point[1],2)) + " ")
                
                if (i == 0):
                    multiline_svg += "L "
                
                i += 1     

        return multiline_svg
    
    def calculate_bbox_hachure(self, bbox, spacing, angle):
        """
        Returning the hachure lines of a specified bounding box, calculated 
        based on given spacing and angle
        """
        
        # Check if provided angle is valid
        if (angle > 180 or angle == 90 or angle == 0):
            print "Angle '" + str(angle) + "' is too large or 90 degrees"                
            return
        
        angle = 180 - angle # Necessary as SVG coordinates are flipped
               
        bbox_anglespacing = self.calculate_hachure_bounds(
            bbox,
            spacing,
            angle
        )
                
        # Creating lines with respect to the x-shift calculated before
        lines = []        
        position_x = bbox_anglespacing[0] + (spacing/2) # 
        while (position_x <= bbox_anglespacing[2]):
            point_1 = (position_x, bbox_anglespacing[1])
            point_2 = self.calculate_line_point_x(
                point_1,
                bbox_anglespacing[3],
                angle
            )            
            line = LineString([point_1, point_2])
            lines.append(line)
            position_x += spacing
            
        multiline = MultiLineString(lines)
        
        print self.create_svg_multilinepath(multiline)
        
        return multiline
    
    def calculate_line_point_y(self, point, x, angle):
        """
        Calculating the coordinates of a point on a linear line containing the 
        provided point with known X
        """
        
        y = point[1] + math.tan(math.radians(angle)) * (x - point[0])
        return (x, y)
        
    def calculate_line_point_x(self, point, y, angle):
        """
        Calculating the coordinates of a point on a linear line containing the 
        provided point with known Y
        """
        
        x = (1/math.tan(math.radians(angle)))*(point[0] 
                * math.tan(math.radians(angle))- point[1] + y)
        return (x, y)
        
    def calculate_hachure_bounds(self, bbox, spacing, angle):
        """
        Calculating a new bounding box for the hachure lines based on the angle
        """
                
        # Calculating the x difference of one hachure line using the formula:
        # opposite side = adjacent side * tan(alpha)
        hachure_x = abs((bbox[3] - bbox[1]) * math.tan(math.radians(90-angle)))

        # Calculating the oversize that needs to be added to the bounds to fit
        # to all hachure lines  
        oversize = math.floor(hachure_x / spacing) * spacing
        
        # Add oversize in minus or plus direction, depending on angle direction
        bbox_anglespacing = None
        if (angle < 90):    
            bbox_anglespacing = (bbox[0] - oversize, bbox[1], bbox[2], bbox[3])
        else:
            bbox_anglespacing = (bbox[0], bbox[1], bbox[2] + oversize, bbox[3])
        
        print "-------------"
        print bbox
        print spacing
        print hachure_x
        print oversize
        print bbox_anglespacing
        print "-------------"
        
        return bbox_anglespacing
        
    def calculateIntersection(self, line, polygon, intersections):
        intersection = polygon.intersection(line)
        
        if (type(intersection) == LineString):
            print "linestring"
            intersections.append(intersection)
        elif(type(intersection) == MultiLineString):
            print "multilinestring"
            for linestring in intersection:
                self.calculateIntersection(linestring, polygon, intersections)
        
        
        
        
    """
        intersection = polygon.intersection(line)
            #print (type(intersection))
            if (type(intersection) == LineString):
                print "linestring"
                intersection_result = polygon.intersection(line)
                print(type(intersection_result))
                intersections.append(intersection_result)
            elif (type(intersection) == MultiLineString):
                for linestring in intersection:
                    print "multilinestring"
                    intersection_result = polygon.intersection(linestring)
                    print(type(intersection_result))
                    intersections.append(intersection_result)
        """