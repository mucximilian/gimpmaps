# -*- coding: utf-8 -*-
import psycopg2
import math
import svgwrite
import os
import datetime
import logging

from maprenderer.tiles import styles

class TileRenderer(object):
    
    origin_x = -(2 * math.pi * 6378137 / 2.0)
    origin_y = 2 * math.pi * 6378137 / 2.0
    
    def __init__(self, bbox, zoom_levels, tile_size, out_dir):
        self.bbox = bbox
        self.zoom_levels = zoom_levels
        self.tile_size = tile_size
        self.out_dir = out_dir
        
    def render_tiles(self):
        """
        Basic tile rendering function. Loops over the specified bounding box in
        different zoom levels.
        """
        
        t_start = datetime.datetime.now()
        t_form = datetime.datetime.now().strftime('%Y%m%d_%H%M')
        
        self.setup(t_start, t_form)       
        
        ########################################################################
        # Zoom level loop
        for zoom in self.zoom_levels:
            
            tiling_data = self.get_tiling_data(self.bbox, zoom)
            self.log_tiling_data_info_zoom(zoom, tiling_data) 
    
            # Checking for a zoom directory, creating it if not existing
            out_dir_zoom = self.out_dir + str(zoom) + "/"
            if not os.path.exists(out_dir_zoom):
                os.makedirs(out_dir_zoom)
            
            # Get OSM tags and styles for zoom level
            features = self.get_feature_styles(zoom)
            
            ####################################################################            
            # X-direction loop
            for x in range(tiling_data[0][0], tiling_data[1][0] + 1):
                
                self.log_tiling_data_info_x(x, tiling_data)                
                
                # Checking for a X directory in zoom directory, 
                # creating it if not existing
                out_dir_zoom_x = out_dir_zoom + str(x) + "/"
                if not os.path.exists(out_dir_zoom_x):
                    os.makedirs(out_dir_zoom_x)
    
                ################################################################
                # Y-direction loop
                for y in range(tiling_data[0][1], tiling_data[1][1] + 1):
                                    
                    tile_bbox = self.calculate_tile_bbox(x, y, tiling_data[3])
                    
                    self.log_tiling_data_info_y(x, y, tiling_data)                    
                    self.log_tile_bbox_info(tile_bbox)       
                                    
                    # Assign the Y value as the file name                       
                    out_path = out_dir_zoom_x + str(y)
                    
                    self.draw_features(features, tile_bbox, out_path)
                    
                # Y-direction loop END
                ################################################################
            
            # Y-direction loop END
            ####################################################################
                
        # Zoom-level loop END
        ########################################################################                  
        
        self.finish(t_start, t_form)
    
    def get_tile_of_point(self, point_ul, zoom):
        """
        Get UL and LR coordinates of tile containing a given point at zoom level 
        """
        
        # Calculate tile size for zoom level
        tiles_xy = int(math.pow(2, zoom))
        tile_size_0 = 2 * self.origin_y
        tile_size_new = tile_size_0/tiles_xy
        
        # Get coordinates
        X_ul = int(math.floor((point_ul[0] - self.origin_x) / tile_size_new))
        X_lr = int(math.floor((self.origin_y - point_ul[1]) / tile_size_new))
        
        tile_ul_lr = [X_ul, X_lr]
        
        return tile_ul_lr
        
    def get_tiling_data(self, bbox, zoom):
        """
        Get UL and LR coordinates of tile containing a given point at zoom level
        
        Returns tiling data array:
        [0][0] = tile ul x
        [0][1] = tile ul y
        [1][0] = tile lr x
        [1][1] = tile lr y
        [2][0] = tiles in x
        [2][1] = tiles in y
        [3] = tile size in CRS units (meter)
        """
        
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
        
    def get_feature_styles(self, zoom_level):
        """
        Get style and tag info of all feature of a type for a zoom level
        """
        
        # Defining database connection for different zoom level styles
        conn_zoom = psycopg2.connect(
            'dbname=gimp_osm_styles '
            'user=gis '
            'password=gis '
            'host=localhost '
            'port=5432'
        )
        
        curs_zoom = conn_zoom.cursor()
        
        sql = "SELECT * FROM get_tags_and_style(%s)"                            
        curs_zoom.execute(sql, (zoom_level,))
        
        # Store feature data in an array
        features = []               
        for row in curs_zoom.fetchall():
            
            if (row[1] == 2):
                style_object = styles.StyleObjectLine(
                    row[1], # geometry type
                    row[2], # tags
                    row[3], # z order
                    row[4], # brush
                    row[5], # brush_size
                    row[6], # color
                    row[7], # opacity_brush
                    row[8]  # dynamics
                )
                features.append(style_object)

                logging.info(style_object.string_style())
                
            elif (row[1] == 3):
                
                print row
                
                style_object = styles.StyleObjectPolygon(
                    row[1], # geometry type
                    row[2], # tags
                    row[3], # z order
                    row[4], # brush
                    row[5], # brush_size
                    row[6], # color
                    row[7], # opacity_brush
                    row[8], # dynamics
                    row[9], # image
                    row[10] # image opacity
                )
                features.append(style_object)
                
                logging.info(style_object.string_style())
            
        curs_zoom.close()
        
        return features         
    
    def calculate_tile_bbox(self, x, y, tile_size):    
        """
        Calculating the tile coordinates from the tile size    
        """
        
        ul_x = self.origin_x + x * tile_size
        ul_y = self.origin_y - y * tile_size
        lr_x = ul_x + tile_size
        lr_y = ul_y - tile_size
        return [ul_x, ul_y, lr_x, lr_y]
    
    def setup(self, t_start, t_form):
        
        log_file = "../../log/svg_rendering_"     
        self.start_logging(t_start, t_form, log_file)
        
        # Create a directory containing the date and time
        self.out_dir += "svg_" + t_form + "/"
        if not os.path.exists(self.out_dir):
            os.makedirs(self.out_dir)
    
    def finish(self, t_start, t_form):
        
        self.finish_logging(t_start, t_form)
        
        print "Finished processing"
                   
    ############################################################################
    # Printing functions
    def print_tiling_data_info_x(self, x, tiling_data):
        indent = "  "
        out = (indent + "row " 
            + str(x + tiling_data[2][0] - tiling_data[1][0]) + "/" 
            + str(tiling_data[2][0]) + " (" + str(x) + ")")
        print out
        return out
        
    def print_tiling_data_info_y(self, x, y, tiling_data):
        indent = "  "
        out = indent + indent + "tile " + str(x) + "/" + str(y)
        print out
        return out
    
    def print_tile_bbox_info(self, tile_bbox):
        indent = "  "
        out = (indent + indent + "tile bbox:\n" + 
               indent + indent + str(tile_bbox[0]) + ",\n" +
               indent + indent + str(tile_bbox[1]) + ",\n" +
               indent + indent + str(tile_bbox[2]) + ",\n" +
               indent + indent + str(tile_bbox[3]))
        print out
        return out
    
    ############################################################################
    # Logging functions
    def start_logging(self, t_start, t_form, log_file):
        
        log_line = "###########################################################"
        
        # logging setup
        logging.basicConfig(
            format = '%(message)s',
            # filename = os.getcwd() + "/log/gimp_rendering_" + t_form + ".log",
            filename = log_file + t_form + ".log",
            filemode = 'w',
            level = logging.INFO
        )            
        logging.info(log_line)
        logging.info("Start of Gimp Tile processing at " + str(t_start))
        logging.info(log_line)
        
        return t_start
    
    def finish_logging(self, t_start, t_form):
        
        log_line = "###########################################################"
        
        t_end = datetime.datetime.now()
        delta_t = t_end - t_start
        
        logging.info(log_line)
        logging.info("End of Gimp Tile processing at " + str(t_end))
        logging.info("processing duration: " + 
            str(delta_t.total_seconds()) +
            " seconds"
        )
        logging.info(log_line)
        
    
    def log_tiling_data_info_zoom(self, zoom, tiling_data):
        logging.info("zoom level: " + str(zoom))
        logging.info("tile ul: " + str(tiling_data[0]))
        logging.info("tile lr: " + str(tiling_data[1]))
        logging.info("tiles in x: " + str(tiling_data[2][0]))
        logging.info("tiles in y: " + str(tiling_data[2][1]))
        logging.info("tiles total: "
            + str(tiling_data[2][0] + tiling_data[2][1]))
        
    def log_tiling_data_info_x(self, x, tiling_data):
        out = self.print_tiling_data_info_x(x, tiling_data)
        logging.info(out)
        
    def log_tiling_data_info_y(self, x, y, tiling_data):
        out = self.print_tiling_data_info_y(x, y, tiling_data)
        logging.info(out)
        
    def log_tile_bbox_info(self, tile_bbox):
        out = self.print_tile_bbox_info(tile_bbox)
        logging.info(out)
        
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
