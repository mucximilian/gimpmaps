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
        
        polygon = self.createMultiPolygonFromSvgPath(path)
        
        hachure = self.createHachure(polygon)
        
        return hachure
    
    def createMultiPolygonFromSvgPath(self, path):
        polygon = None
        
        return polygon
    
    def createHachure(self, polygon):
        hachure = None
        
        return hachure