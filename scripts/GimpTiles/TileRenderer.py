# -*- coding: utf-8 -*-
import psycopg2
import math
import svgwrite
import os

from ZoomSelection import ZoomSelectionLinesType

class TileRenderer(object):
    
    origin_x = -(2 * math.pi * 6378137 / 2.0)
    origin_y = 2 * math.pi * 6378137 / 2.0    
    
    def __init__(self, bbox, zoom_levels, tile_size, out_dir):
        self.bbox = bbox
        self.zoom_levels = zoom_levels
        self.tile_size = tile_size
        self.out_dir = out_dir
        
    def create_tiles(self):
        
        for zoom in self.zoom_levels:
            
            tiling_data = self.get_tiling_data(self.bbox, zoom)
            
            print tiling_data
            
            brush_size = 12
    
            out_dir_zoom = self.out_dir + str(zoom) + "/"
            if not os.path.exists(out_dir_zoom):
                os.makedirs(out_dir_zoom)
            
            indent = "  "
            
            # Define geometry selection query based on zoom level
            zoom_selection_lines = ZoomSelectionLinesType()        
            sql_selection = zoom_selection_lines.roads[zoom]
                        
            # X-direction loop
            for x in range(tiling_data[0][0], tiling_data[1][0] + 1):
                
                print (indent + "row " + str(x + tiling_data[2][0] - tiling_data[1][0]) + "/" +
                    str(tiling_data[2][0]) + " (" + str(x) + ")")
                    
                conn = psycopg2.connect('dbname=osm_muc '
                	'user=gis '
                	'password=gis '
                	'host=localhost '
                	'port=5432')
    
                curs = conn.cursor()
                
                out_dir_zoom_x = out_dir_zoom + str(x) + "/"
                if not os.path.exists(out_dir_zoom_x):
        			os.makedirs(out_dir_zoom_x)
    
                # Y-direction loop
                for y in range(tiling_data[0][1], tiling_data[1][1] + 1):
                                    
                    ul_x = self.origin_x + x * tiling_data[3]
                    ul_y = self.origin_y - y * tiling_data[3]
                    lr_x = ul_x + tiling_data[3]
                    lr_y = ul_y - tiling_data[3]
                                    
                    print indent + indent + "tile " + str(x) + "/" + str(y)
                    
                    sql = """
                        SELECT 
                            ROW_NUMBER() OVER (ORDER BY id) AS id,
                            line_type,
                            svg
                        FROM get_unclipped_svg_tile_collect(%s,%s,%s,%s,%s,%s)
                        WHERE (""" + sql_selection + ")"        

                    curs.execute(sql, (
                        ul_x,
                        ul_y,
                        lr_x,
                        lr_y,
                        brush_size,
                        self.tile_size
                        )
                    )
    
                    # Assign the Y value as the file name
                    out_path = out_dir_zoom_x + str(y)
                    self.save_svg_tiles(out_path, self.tile_size, curs)
                        
                curs.close()
                conn.close()
    
    ############################################################################
    # Get UL and LR coordinates of tile containing a given point at zoom level 
    def get_tile_of_point(self, point_ul, zoom):
        
        # Calculate tile size for zoom level
        tiles_xy = int(math.pow(2, zoom))
        tile_size_0 = 2 * self.origin_y
        tile_size_new = tile_size_0/tiles_xy
        
        # Get coordinates
        X_ul = int(math.floor((point_ul[0] - self.origin_x) / tile_size_new))
        X_lr = int(math.floor((self.origin_y - point_ul[1]) / tile_size_new))
        
        tile_ul_lr = [X_ul, X_lr]
        
        return tile_ul_lr
        
    ############################################################################
    # Get UL and LR coordinates of tile containing a given point at zoom level 
    def get_tiling_data(self, bbox, zoom):
        
        # Determine containing tile for the UL and LR bounds at zoom level
        tile_ul = self.get_tile_of_point(bbox[0], zoom)
        tile_lr = self.get_tile_of_point(bbox[1], zoom)
        
        # Calculate number of tiles within the bounds
        tiles_count_x = tile_lr[0] - tile_ul[0] + 1
        tiles_count_y = tile_lr[1] - tile_ul[1] + 1
        
        tile_size_0 = 2 * self.origin_y
        tile_size = tile_size_0 / int(math.pow(2, zoom))
        tiles_count = tiles_count_x * tiles_count_y
        
        tiling_data= [
            [tile_ul[0],tile_ul[1]],
            [tile_lr[0],tile_lr[1]],
            [tiles_count_x, tiles_count_y],
            tile_size
        ]
        
        print "------------------------------------------"
        print "zoom = " + str(zoom)
        print "tile_ul = " + str(tile_ul)
        print "tile_lr = " + str(tile_lr)
        print "tile_size = " + str(tile_size)
        print "tiles in x = " + str(tiles_count_x)
        print "tiles in y = " + str(tiles_count_y)
        print "tiles count = " + str(tiles_count)
        
        return tiling_data
        
    def save_svg_tiles(self, out_file, tile_size, curs):
        dwg = svgwrite.Drawing(
            out_file + ".svg",
            height = tile_size,
            width = tile_size)
    
        i = 1
        for row in curs.fetchall():
            dwg.add(dwg.path(d=row[2]))
            #print path.tostring()
            i += 1
            
        dwg.save()
        print "        vectors = " + str(i)
        
    ############################################################################
    # Returns selection tags as a string suitable for a SQL 'WHERE' condition
    def get_selection_tags(self, tags):
        selection_string = ""
        count = 0
        for tag in tags:
            if count > 0:
                selection_string += " OR "
            selection_string += tag
            count += 1
            
        return selection_string
