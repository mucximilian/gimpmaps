'''
Created on Apr 28, 2015

@author: mucx
'''
import shapely

class Renderer(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        
    def createPolygonHachure(self, path):
        
        # Creating a (MUlti-)Polygon consisting of an array of points
        polygon = self.createMultiPolygonFromSvgPath(path)
        
        hachure_lines = self.createHachureLines(polygon)
        
        hachure = self.createHachureSvg(hachure_lines)
        
        return hachure
    
    def createMultiPolygonFromSvgPath(self, path):
        
        multipolygon = []
        
        # Getting the "d" string of the SVG path
        path_str = path.commands[0]
        
        # Split path into single polygons
        multipolygon_str = path_str.split("Z");        
        multipolygon_str.pop() # Remove last item from list which is empty
        
        for polygon_str in multipolygon_str:
            
            polygon = []
            
            polygon_str = polygon_str.strip() # Trim whitespaces
            
            # Split polygon into single points
            points_str = polygon_str.split(" ");           
            points_str.remove('L')
            points_str.remove('M')
            
            # Appending point pairs (coordinates) to an array (polygon)
            for i in range(0, len(points_str), 2):
                polygon.append([points_str[i], points_str[i+1]])
                
            # Appending the created polygon to an array (multipolygon)
            multipolygon.append(polygon)
        
        print multipolygon
        return multipolygon
    
    def createHachureLines(self, polygon):
        hachure_lines = None
        
        # Returning hachure as an array of lines 
        return hachure_lines
    
    def createHachureSvg(self, hachure_lines):
        hachure = None
        
        # Return a hachure as a SVG multiline
        return hachure