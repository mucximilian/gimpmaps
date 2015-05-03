'''
Created on Apr 28, 2015

@author: mucx
'''

from shapely.geometry import LineString
from shapely.geometry import Polygon
from shapely.geometry.polygon import LinearRing

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
        
        line = [(50, 0), (300, 250)]
        shapely_line = LineString(line)
        
        # lines = calculateHachureLines(bbox, spacing, angle)
        
        intersection = list(polygon.intersection(shapely_line))
        print intersection
        
        print intersection[0]
        print intersection[1]

        #prep_poly = prep(polygon)
        #hits = filter(prepared_polygon.intersects, points)
        
        hachure_lines = None
        
        return hachure_lines
    
    def createHachureSvg(self, hachure_lines):
        """
        Returning a hachure as a SVG multiline
        """
        
        hachure = None
        
        return hachure