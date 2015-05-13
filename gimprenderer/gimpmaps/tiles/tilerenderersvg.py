'''
Created on May 11, 2015

@author: mucx
'''

from gimpmaps.tiles import tilerenderer
from gimpmaps import renderersvg

class TileRendererSvg(tilerenderer.TileRenderer, renderersvg.RendererSvg):
    '''
    classdocs
    '''
    
    def __init__(self, bbox, zoom_levels, tile_size, out_dir, map_style_id):
        self.bbox = bbox
        self.zoom_levels = zoom_levels
        self.tile_size = [tile_size, tile_size]
        self.out_dir = out_dir
        self.map_style_id = map_style_id
        self.type = "tiles_svg"