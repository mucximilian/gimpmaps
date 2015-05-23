'''
Created on May 14, 2015

@author: mucx
'''

from gimpmaps.renderermap import MapRenderer
from gimpmodule import GimpImageManager

class MapRendererSvgXcf(MapRenderer):
    '''
    A renderer to create a single SVG map plus a GIMP image with the 
    corresponding dimensions. 
    This class is kept separate from the MapRenderer classes as it usses the
    GIMP-Fu module which can only be accessed from a GIMP session.
    '''

    def __init__(self, config_file):
        '''
        Constructor
        '''
        
        super(MapRendererSvgXcf, self).__init__(config_file)
        
        self.type = "map_svg"
        
    def draw(self, zoom, bbox, resolution, out_file):
        
        feature_styles = self.get_feature_styles(zoom)
        
        self.create_svg_image(feature_styles,
                           self.bbox,
                           resolution,
                           out_file)
                  
        gimp = GimpImageManager()
        gimp.create_gimp_image(resolution, out_file, True, True)