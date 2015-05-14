'''
Created on May 14, 2015

@author: mucx
'''

from gimpfu import *
import gimprenderer
    
class GimpFactory():
    def __init__(self):
        pass
    
    def gimp_renderer(self, 
                 bbox, zoom_levels, tile_size, out_dir, map_style_id):
        gimp_renderer = gimprenderer.RendererGimp(bbox, zoom_levels, 
                                                  tile_size, out_dir,
                                                  map_style_id)
        return gimp_renderer
    
    def gimp_renderer_tile(self, 
                 bbox, zoom_levels, tile_size, out_dir, map_style_id, 
                 create_xcf):
        
        gimp_renderer = gimprenderer.TileRendererGimp(bbox, zoom_levels, 
                                                      tile_size, out_dir, 
                                                      map_style_id, create_xcf)
        return gimp_renderer