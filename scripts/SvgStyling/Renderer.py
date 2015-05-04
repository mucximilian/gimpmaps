'''
Created on Apr 28, 2015

@author: mucx
'''

from shapely.geometry import LineString
from shapely.geometry import MultiLineString
from shapely.geometry import Polygon
from shapely.geometry.polygon import LinearRing

import math

class Renderer(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        
    def createPolygonHachure(self, path):
        """
        Creating a SVG hachure for a polygon
        """
        
        # Creating a (Multi-)Polygon consisting of an array of points
        polygon = self.createMultiPolygonFromSvgPath(path)
        
        hachure_lines = self.createHachureLines(polygon)
        
        hachure = self.createHachureSvg(hachure_lines)
        
        return hachure
    
    def createMultiPolygonFromSvgPath(self, path):
        """
        Returning a multipolygon array from a SVG path input
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
        
        # Creating shapely polygon from outline and remaining polygons
        polygon = Polygon(exterior, multipolygon)

        return polygon
    
    def createHachureLines(self, polygon):
        """
        Returning hachure as an array of lines 
        """
        
        bbox = polygon.bounds
        
        print(bbox)
               
        # Creating the bounding box hachure lines
        lines = self.calculateHachureLines(bbox, 20, 30)
        
        self.createSvgMultiline(lines)
        
        # Calculating the intersection of hachure lines and polygon
        intersection = list(polygon.intersection(lines))
        
        print len(intersection)

        # Filter and randomize hachure lines
        # TO DO: function
        # hachure_lines = randomizeLines(intersection)
        hachure_lines = None
        
        multiline = MultiLineString(hachure_lines)
        print multiline
        
        multiline_svg = self.createSvgMultiline(intersection)
        
        return multiline_svg
    
    def createSvgMultiline(self, multiline):
        """
        Returning a multilinestring as a SVG multiline  
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
        
        print multiline_svg
        return multiline_svg
    
    def calculateHachureLines(self, bbox, spacing, angle):
        
        if (angle > 180 or angle == 90):
            print "Angle '" + str(angle) + "' is too large or 90 degrees"                
            return
        
        angle = 180 - angle # Necessary as SVG coordinates are flipped
        
        # Calculating the x-shift of the hachure start point as half of the 
        # spacing or half of the remainder of the division x-length/spacing
        x_length = bbox[2]-bbox[0]
        
        spacing_mod = x_length%spacing
        
        if (spacing_mod == 0):
            spacing_rel = spacing
        else:
            spacing_rel = spacing_mod
            
        spacing_start = spacing_rel/2;
        
        # Calculating the integer count of spacings in x-length
        spacing_count_int = int(x_length//spacing)
        
        print "spacing start = " + str(spacing_start)
        print "spacing count = " + str(spacing_count_int)
        print "spacing = " + str(spacing)
        
        bbox_anglespacing = self.calculateAngleSpacingBounds(
            bbox,
            spacing_start,
            spacing,
            angle
        )
        
        print bbox_anglespacing
                
        # Create lines with respect to the x-shift calculated before
        lines = []
        
        position_x = bbox_anglespacing[0]
        while (position_x <= bbox_anglespacing[2]):
            point_1 = (position_x, bbox_anglespacing[1])
            point_2 = self.calculateLinePointX(
                point_1,
                bbox_anglespacing[3],
                angle
            )
            
            line = LineString([point_1, point_2])
            lines.append(line)
            position_x += spacing
            
        multiline = MultiLineString(lines)
        return multiline
    
    def calculateLinePointY(self, point, x, angle):
        """
        Calculating the point coordinates on a linear line with known X
        """
        
        y = point[1] + math.tan(math.radians(angle)) * (x - point[0])
        return (x, y)
        
    def calculateLinePointX(self, point, y, angle):
        """
        Calculating the point coordinates on a linear line with known Y
        """
        
        x = (1/math.tan(math.radians(angle)))*(point[0] * math.tan(math.radians(angle))- point[1] + y)
        return (x, y)
        
    def calculateAngleSpacingBounds(self, bbox, start, spacing, angle):
                
        # Calculating the x length of a hachure line      
        hachure_x = abs((bbox[3] - bbox[1]) * math.tan(math.radians(90-angle)))

        print hachure_x
        # Calculating the oversize that needs to be added to the bounds to fit
        # to all hachure lines  
        oversize = self.exapandSpacingSteps(
            spacing,
            start,
            hachure_x,
            0
        )
        print oversize
        if (angle < 90):    
            return (bbox[0] - oversize, bbox[1], bbox[2], bbox[3])
        else:
            return (bbox[0], bbox[1], bbox[2] + oversize, bbox[3])
    
    def exapandSpacingSteps(self, spacing, start, hachure_x, oversize):
        diff = oversize - start
        if (diff < hachure_x):
            oversize += spacing
            # Recursive call
            return self.exapandSpacingSteps(
                spacing, 
                start,
                hachure_x,
                oversize
            )
        else:
            return abs(oversize - start)        