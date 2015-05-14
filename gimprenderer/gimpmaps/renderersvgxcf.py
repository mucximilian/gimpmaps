'''
Created on May 14, 2015

@author: mucx
'''

from renderer import Renderer
from gimphelper import gimprenderer

class RendererSvgXcf(Renderer):
    '''
    A class to create a single SVG map. This class is kept separate from the 
    other SVG Render classes as it usses the GIMP-Fu module which can only be 
    accessed from a GIMP session.
    '''

    def __init__(self, bbox, scale, out_dir, map_style_id, create_xcf):
        '''
        Constructor
        '''
        
        self.bbox = bbox
        self.scale = scale
        self.out_dir = out_dir
        self.map_style_id = map_style_id
        self.type = "map_svg"
        
    def draw(self, feature_styles, bbox, resolution, out_file):
        
        self.create_svg_image(feature_styles,
                           self.bbox,
                           resolution,
                           out_file)
                  
        gimp_renderer = gimprenderer.RendererGimp(self.bbox, self.scale,
                                                  out_file, self.map_style_id,
                                                  True)
        gimp_renderer.create_gimp_image(resolution, out_file, True, True)