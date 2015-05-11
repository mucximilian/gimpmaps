'''
Created on May 11, 2015

@author: mucx
'''

import svgwrite
import os
import inspect 

from gimpmaps.tiles import tilerenderer
from svgsketch import hachurizator

class TileRendererSvg(tilerenderer.TileRenderer):
    '''
    classdocs
    '''
    
    def __init__(self, bbox, zoom_levels, tile_size, out_dir, map_style):
        self.bbox = bbox
        self.zoom_levels = zoom_levels
        self.tile_size = tile_size
        self.out_dir = out_dir
        self.map_style = map_style
        
    def setup(self, t_start, t_form):
        """
        Defining the log file and the results directory
        """
        
        filepath = os.path.dirname(
            os.path.abspath(
                inspect.getfile(
                    inspect.currentframe()
                )
            )
        )
        
        log_file = filepath + "/../log/svg_rendering_"     
        self.start_logging(t_start, t_form, log_file)
        
        # Create a directory containing the date and time
        self.out_dir += "svg_" + t_form + "/"
        if not os.path.exists(self.out_dir):
            os.makedirs(self.out_dir)
        
    def draw_features(self, feature_styles, tile_bbox, out_path):
        """
        Drawing function for SVG image files   
        """
        
        self.conn_osm = self.connect_to_osm_db()
        
        # Create SVG file name with extension
        dwg = svgwrite.Drawing(
            out_path + ".svg",
            height = self.tile_size,
            width = self.tile_size
        )
        
        for feature_style in feature_styles:
            
            svg_geoms = self.get_svg_features(
                tile_bbox, 
                feature_style
            )
    
            # Drawing vectors
            for svg_commands in svg_geoms:            
                dwg.add(dwg.path(d=svg_commands))
            
        dwg.save()
        print "creating SVG: " + out_path + ".svg"
        
        self.conn_osm.close()
