'''
Created on May 12, 2015

@author: mucx
'''

import svgwrite

class RendererSvg(object):
    '''
    classdocs
    '''


    def __init__(self, bbox, scale, out_dir, map_style_id):
        '''
        Constructor
        '''
        
        self.bbox = bbox
        self.scale = scale
        self.out_dir = out_dir
        self.map_style_id = map_style_id
        self.type = "map_svg"
        
    def draw_features(self, feature_styles, bbox_tile, out_path):
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
                bbox_tile, 
                feature_style
            )
    
            # Drawing vectors
            for svg_commands in svg_geoms:            
                dwg.add(dwg.path(d=svg_commands))
            
        dwg.save()
        print "creating SVG: " + out_path + ".svg"
        
        self.conn_osm.close()