'''
Created on May 11, 2015

@author: mucx
'''

import psycopg2
import svgwrite
import os
import logging
import math

from gimpmaps.tiles import tilerenderer
from svgsketch import hachurizator

class TileRendererSvg(tilerenderer.TileRenderer):
    '''
    classdocs
    '''
    
    origin_x = -(2 * math.pi * 6378137 / 2.0)
    origin_y = 2 * math.pi * 6378137 / 2.0
    
    def __init__(self, bbox, zoom_levels, tile_size, out_dir, style):
        self.bbox = bbox
        self.zoom_levels = zoom_levels
        self.tile_size = tile_size
        self.out_dir = out_dir
        
    def setup(self, t_start, t_form):
        
        log_file = "../../../log/svg_rendering_"     
        self.start_logging(t_start, t_form, log_file)
        
        # Create a directory containing the date and time
        self.out_dir += "svg_" + t_form + "/"
        if not os.path.exists(self.out_dir):
            os.makedirs(self.out_dir)
        
    def draw_features(self, features, tile_bbox, out_path):
        """
        Drawing function for SVG image files   
        """
        
        conn_osm = psycopg2.connect(
            'dbname=osm_muc '
            'user=gis '
            'password=gis '
            'host=localhost '
            'port=5432'
        )        
        
        # Create SVG file name with extension
        dwg = svgwrite.Drawing(
            out_path + ".svg",
            height = self.tile_size,
            width = self.tile_size
        )
        print "creating SVG: " + out_path + ".svg"
        
        for style_feature in features:
                        
            sql_selection = style_feature.get_selection_tags()
            line_style = style_feature.get_line_style()
            
            curs_osm = conn_osm.cursor()
            
            if (style_feature.geom_type == 2):        
                sql = """
                SELECT 
                    ROW_NUMBER() OVER () AS id,
                    get_scaled_svg_line(
                        way, %s, %s, %s, %s, %s
                    ) AS svg
                FROM (
                    SELECT
                        *
                    FROM planet_osm_line 
                    WHERE ST_Intersects ( 
                        way, 
                        get_tile_bbox(
                            %s, %s, %s, %s, %s, %s
                        ) 
                    )
                ) t
                WHERE (""" + sql_selection + ")"
            elif (style_feature.geom_type == 3):
                sql = """
                SELECT 
                    ROW_NUMBER() OVER () AS id,
                    get_scaled_svg_polygon(
                        ST_Union(way), %s, %s, %s, %s, %s
                    ) AS svg
                FROM (
                    SELECT
                        *
                    FROM planet_osm_polygon
                    WHERE ST_Intersects ( 
                        way, 
                        get_tile_bbox(
                            %s, %s, %s, %s, %s, %s
                        ) 
                    )
                ) t
                WHERE (""" + sql_selection + ")"            
        
            curs_osm.execute(sql, (
                tile_bbox[0], tile_bbox[1], tile_bbox[2], tile_bbox[3],
                self.tile_size,
                tile_bbox[0], tile_bbox[1], tile_bbox[2], tile_bbox[3],
                self.tile_size,
                line_style[1]
                )
            )     
    
            # Drawing vectors and displaying count
            i = 1
            for row in curs_osm.fetchall():
                
                if (row[1] == None or row[1] ==''): continue                
                dwg.add(dwg.path(d=row[1]))
                i += 1
                
            out = "      " + sql_selection + " (" + str(i) + ")"
            logging.info(out)
            print(out)
            
        dwg.save()
