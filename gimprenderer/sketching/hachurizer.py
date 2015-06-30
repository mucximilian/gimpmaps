'''
Created on Apr 28, 2015

@author: mucx
'''

from __future__ import division

from shapely.geometry import LineString
from shapely.geometry import MultiLineString
from shapely.geometry import Polygon
from shapely.geometry import MultiPolygon

import shapely
import math

class Hachurizer(object):
    '''
    classdocs
    '''

    def __init__(self, spacing, angle):
        '''
        Constructor
        '''
        
        self.spacing = spacing
        self.angle = angle
        
    def get_svg_hachure(self, path):
        """
        Returns a SVG hachure for the specified polygon input path
        """
        
        # TO DO: Check if input is polygon!
        
        # Creating a (Multi-)Polygon consisting of an array of points        
        polygon = self.multipolygon_from_svgpath(path)
        
        hachure_lines = self.create_hachure_lines(polygon)
                      
        # multiline_svg = self.create_svg_multilinepath(intersections)
        
        if (len(hachure_lines) == 0):            
            print "No hachures created for polygon with given parameters"
            return None
        else:
            # lines = MultiLineString(hachure_lines)
            # hachure = lines.svg()  
            # return hachure
            hachure_lines_simple = []
            
            for line in hachure_lines:
                hachure_lines_simple.append(list(line.coords))
                
            return hachure_lines_simple 
            
    
    def multipolygon_from_svgpath(self, path):
        """
        Returning a Shapely multipolygon array from a SVG path input
        """
        
        multipolygon_list = []
        
        # Getting the "d" string of the SVG path
        path_str = path.commands[0]
        
        # Split path into single polygons
        path_str_polygons = path_str.split("Z");
        
        # Removing last item from list which is empty due to split
        path_str_polygons.pop()    
        
        # Getting first SVG polygon string as exterior (outline)
        exterior = self.create_coordlist_from_string(path_str_polygons.pop(0))
        exterior_polygon = Polygon(exterior)        

        # Adding all polygons to a list of polygons
        polygons = []
        for polygon_str in path_str_polygons:
            polygon_coords = self.create_coordlist_from_string(polygon_str)            
            
            # Appending the created polygon to the multipolygon list            

            # check if polygon is within exterior outline
            # TRUE add as polygon_coords to polygons
            # FALSE add as polygon to multipolygon
            polygon = Polygon(polygon_coords)
            
            if (polygon.within(exterior_polygon)):
                polygons.append(polygon_coords)
            else:
                multipolygon_list.append(polygon)            

        polygon = Polygon(exterior, polygons)
        multipolygon_list.insert(0, polygon)
            
        # Extracting the first polygon as outline from the multipolygon array
        #exterior = multipolygon.pop(0)
        
        # Creating Shapely polygon from outline and remaining polygons
        #polygon = Polygon(exterior, multipolygon)
        
        multipolygon = MultiPolygon(multipolygon_list)
        return multipolygon
    
    def create_coordlist_from_string(self, polygon_str):
        """
        Returning a list of coordinates representing the input SVG polygon
        string
        """
        
        # Array for the coordinates (x/y points) of the polygon
        polygon_coords = []           
        
        polygon_str = polygon_str.strip() # Trim whitespaces
        
        # Split SVG polygon string into single points
        points_str = polygon_str.split(" ");           
        points_str.remove('L')
        points_str.remove('M')
        
        # Appending coordinates to polygon coordinates array
        for i in range(0, len(points_str), 2):
            polygon_coords.append(
                [float(points_str[i]), float(points_str[i+1])]
            )
            
        # Adding first coordinate again
        polygon_coords.append([float(points_str[0]), float(points_str[1])])
        
        return polygon_coords
    
    def create_hachure_lines(self, polygon):
        """
        Returning hachure as an array of lines 
        """
               
        # Creating the bounding box hachure lines
        lines = self.calculate_bbox_hachure(polygon.bounds)     
        
        intersections = []
        
        for line in lines:
            # Calculating the intersection of hachure lines and polygon
            self.calculateIntersection(line, polygon, intersections)

        # Filter and randomize hachure lines
        # TO DO:
        # hachure_lines = randomizeLines(intersection)

        multiline = MultiLineString(intersections)
               
        return multiline
    
    def create_svg_multilinepath(self, multiline):
        """
        Converts a Shapely multilinestring into a SVG multiline path string.
        Deprecated, Shapely .svg() function used now.
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
    
    def calculate_bbox_hachure(self, bbox):
        """
        Returning the hachure lines of a specified bounding box, calculated 
        based on given spacing and angle
        """
        
        # Check if provided angle is valid
        if (self.angle > 180 or self.angle == 90 or self.angle == 0):
            print "Angle '" + str(self.angle) + "' is too large or 90 or 0 degrees"                
            return
        
        angle = 180 - self.angle # Necessary as SVG coordinates are flipped
               
        bbox_anglespacing = self.calculate_hachure_bounds(
            bbox,
            self.spacing,
            angle
        )
                
        # Creating lines with respect to the x-shift calculated before
        lines = []        
        position_x = bbox_anglespacing[0] + (self.spacing/2) # 
        while (position_x <= bbox_anglespacing[2]):
            point_1 = (position_x, bbox_anglespacing[1])
            point_2 = self.calculate_line_point_x(
                point_1,
                bbox_anglespacing[3],
                angle
            )            
            line = LineString([point_1, point_2])
            lines.append(line)
            position_x += self.spacing
            
        multiline = MultiLineString(lines)
        
        # print self.create_svg_multilinepath(multiline)
        
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
        
        return bbox_anglespacing
        
    def calculateIntersection(self, line, polygon, intersections):
        """
        Returning the intersecting lines of a polygon an the hachure lines
        """
        
        try:        
            intersection = polygon.intersection(line)
            
            if (type(intersection) == LineString):
                # Only consider lines which are at least as big as the brush size
                if (intersection.length >= self.spacing/2):
                    intersections.append(intersection)
            
            # Recursive function call to split up multilinestrings 
            elif(type(intersection) == MultiLineString):
                for linestring in intersection:
                    self.calculateIntersection(linestring,
                                               polygon,
                                               intersections)
        except shapely.geos.TopologicalError:
            print "INVALID GEOMETRY:"
            print polygon.svg()