'''
Created on May 21, 2015

@author: mucx
'''

from __future__ import division
from abc import ABCMeta, abstractmethod

from renderer import Renderer

class MapRenderer(Renderer):
    '''
    An abstract metaclass that handles the map rendering
    '''
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, config_file):
        '''
        Constructor
        '''
        
        super(MapRenderer, self).__init__(config_file)
    
    def render(self):
        """
        Rendering function, called from subclasses for the basic rendering.
        'draw_features' is defined in back in the subclasses.
        """
        
        self.setup()
        
        self.set_scale()
        
        # Zoom level needed to determine styling
        zoom = self.get_zoom_level_for_scale()
        resolution = self.calculate_resolution()
        
        self.log_map_data(zoom, resolution)
        
        out_path = self.out_dir + self.type
        
        self.draw(
            zoom,
            self.bbox,
            resolution,
            out_path
        )
        
        self.finish()
        
    ############################################################################
    
    def set_scale(self):
        self.scale = self.config["map"]["image"]["scale"]
        
    def calculate_resolution(self):
        """
        Calculating the size of the resulting image in pixel based on the 
        bounding box and the scale.
        """
                
        bbox_width = abs(self.bbox[0][0] - self.bbox[1][0])
        bbox_height = abs(self.bbox[0][1] - self.bbox[1][1])
        
        map_width = self.get_pixel_size(bbox_width)
        map_height = self.get_pixel_size(bbox_height)
        
        return [map_width, map_height]
    
    def get_pixel_size(self, size_m, dpi = 300):
        """
        Calculating the pixel size of a length given in meter using the scale 
        and desired DPI (e.g. 300 for print).        
        """
        
        size_cm = size_m/self.scale
        
        size_inch = size_cm * 2.54
        
        size_pixel = int(round(size_inch * dpi))
        
        return size_pixel
    
    def get_zoom_level_for_scale(self):       
        """
        Returning the appropriate zoom level for a given scale
        See scales here: http://wiki.openstreetmap.org/wiki/Zoom_levels
        """
        
        zoom = 0
        
        if (self.scale <= 0):
            print "Invalid scale"
            exit
        elif(self.scale > 0 and self.scale <= 1000):
            zoom = 19
        elif(self.scale > 0 and self.scale <= 2000):
            zoom = 18
        elif(self.scale > 0 and self.scale <= 4000):
            zoom = 17
        elif(self.scale > 0 and self.scale <= 8000):
            zoom = 16
        elif(self.scale > 0 and self.scale <= 15000):
            zoom = 15
        elif(self.scale > 0 and self.scale <= 35000):
            zoom = 14
        elif(self.scale > 0 and self.scale <= 70000):
            zoom = 13
        elif(self.scale > 0 and self.scale <= 150000):
            zoom = 12
        elif(self.scale > 0 and self.scale <= 250000):
            zoom = 11
        elif(self.scale > 0 and self.scale <= 500000):
            zoom = 10
        elif(self.scale > 0 and self.scale <= 1000000):
            zoom = 9
        elif(self.scale > 0 and self.scale <= 2000000):
            zoom = 8
        elif(self.scale > 0 and self.scale <= 4000000):
            zoom = 7
        elif(self.scale > 0 and self.scale <= 10000000):
            zoom = 6
        elif(self.scale > 0 and self.scale <= 15000000):
            zoom = 5
        elif(self.scale > 0 and self.scale <= 35000000):
            zoom = 4
        elif(self.scale > 0 and self.scale <= 70000000):
            zoom = 3
        elif(self.scale > 0 and self.scale <= 150000000):
            zoom = 2
        elif(self.scale > 0 and self.scale <= 250000000):
            zoom = 1
        elif(self.scale > 0 and self.scale <= 500000000):
            zoom = 0
        
        return zoom
        
class MapRendererSvg(MapRenderer):
    '''
    A renderer to create a single SVG map. A GIMP image with the corresponding
    dimensions is created along with the SVG result.
    '''

    def __init__(self, config_file):
        '''
        Constructor
        '''
        
        super(MapRendererSvg, self).__init__(config_file)
        
        self.type = "map_svg"
        
    def draw(self, zoom, bbox, resolution, out_file):
        
        feature_styles = self.get_feature_styles(zoom)
        
        self.create_svg_image(feature_styles, self.bbox, resolution, out_file)