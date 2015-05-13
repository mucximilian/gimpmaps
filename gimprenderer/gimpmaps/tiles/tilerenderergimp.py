'''
Created on May 11, 2015

@author: mucx
'''

from gimpmaps.tiles import tilerenderer
from gimpmaps import renderergimp

from gimpfu import *


class TileRendererGimp(tilerenderer.TileRenderer, renderergimp.RendererGimp):
    """
    This subclass of tilerenderersvg implements different 'setup' and
    'draw_features' methods for the creation of GIMP tiles as PNG and (if 
    defined in the 'create_xcf' variable) as XCF files as well.
    """
    
    def __init__(self, 
                 bbox, zoom_levels, tile_size, out_dir, map_style_id, create_xcf):
        self.bbox = bbox
        self.zoom_levels = zoom_levels
        self.tile_size = [tile_size, tile_size]
        self.out_dir = out_dir
        self.map_style_id = map_style_id
        self.create_xcf = create_xcf
        self.type = "tiles_gimp"