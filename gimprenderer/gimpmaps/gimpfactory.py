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
    
    def create_gimp_image(self, resolution, out_path):
        image = pdb.gimp_image_new(
           resolution[0],
           resolution[1],
           RGB
        )
        
        layer = pdb.gimp_layer_new(
                    image, resolution[0], resolution[1],
                    RGBA_IMAGE,
                    "layer",
                    100, NORMAL_MODE
        )
        pdb.gimp_image_insert_layer(image, layer, None, 0)
        
        out_path_xcf = out_path + ".xcf"   
        pdb.gimp_xcf_save(
            0,
            image,
            layer,
            out_path_xcf,
            out_path_xcf
        )