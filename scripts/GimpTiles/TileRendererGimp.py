# -*- coding: utf-8 -*-
"""
********************************************************************************
TileRendererGimp
                              -------------------
        begin                : 2015-03-28
        copyright            : (C) 2015 by Maximilian Hartl
        email                : mucximilian@gmail.com
        
    
********************************************************************************

********************************************************************************
*                                                                              *
*   This program is free software; you can redistribute it and/or modify       *
*   it under the terms of the GNU General Public License as published by       *
*   the Free Software Foundation; either version 2 of the License, or          *
*   (at your option) any later version.                                        *
*                                                                              *
********************************************************************************
"""
import psycopg2
import svgwrite
import os
import logging
import datetime

from gimpfu import *
from TileRenderer import TileRenderer

import StyleObjects

class TileRendererGimp(TileRenderer):
    def __init__(self, bbox, zoom_levels, tile_size, out_dir):
        
        t_start = datetime.datetime.now()
        t_form = datetime.datetime.now().strftime('%Y%m%d_%H%M')
        
        # logging setup
        logging.basicConfig(
            filename = os.getcwd() + "/log/gimp_rendering_" + t_form + ".log",
            filemode = 'w',
            level = logging.INFO
        )            
        log_line = "###########################################################"
        logging.info(log_line)
        logging.info("Start of Gimp Tile processing at " + str(t_start))
        logging.info(log_line)
        
        # Defining database connection for different zoom level styles
        conn_zoom = psycopg2.connect(
            'dbname=gimp_osm_styles '
            'user=gis '
            'password=gis '
            'host=localhost '
            'port=5432'
        )
        
        # Create a directory containing the date and time
        result_dir = out_dir
        out_dir += "tiles_" + t_form + "/"
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
            
        # Copying the HTML file to view the tiles in the browser
        os.system ("cp %s %s" % (
                                   result_dir + "index.html",
                                   out_dir + "index.html")
                   )
        
        ########################################################################
        # Zoom level loop
        for zoom in zoom_levels:
            
            tiling_data = self.get_tiling_data(bbox, zoom)
            self.log_tiling_data_info_zoom(zoom, tiling_data) 
    
            # Checking for a zoom directory, creating it if not existing
            out_dir_zoom = out_dir + str(zoom) + "/"
            if not os.path.exists(out_dir_zoom):
                os.makedirs(out_dir_zoom)
            
            # Get OSM tags and styles for zoom level
            features_line = self.get_feature_styles(zoom, conn_zoom,
                                                    "line")
            features_polygon = self.get_feature_styles(zoom, conn_zoom,
                                                       "polygon")
            
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
                    
                    self.log_tiling_data_info_y(x, y, tiling_data)
                                    
                    tile_bbox = self.calculate_tile_bbox(x, y, tiling_data[3])        
                                        
                    conn_osm = psycopg2.connect(
                        'dbname=osm_muc '
                        'user=gis '
                        'password=gis '
                        'host=localhost '
                        'port=5432'
                    )

                    ############################################################
                    # Drawing geometry features
                    
                    # Create GIMP image with layer group
                    image = pdb.gimp_image_new(tile_size, tile_size, RGB)
                    pdb.gimp_context_set_background((255,255,255,255))
                    
                    group_top = pdb.gimp_layer_group_new(image)
                    
                    # Lines
                    self.draw_features(tile_bbox, tile_size,
                                       image, 
                                       conn_osm, 
                                       features_line,
                                       group_top, 0)
                    
                    # Polygons
                    self.draw_features(
                                       tile_bbox, tile_size,
                                       image, 
                                       conn_osm,
                                       features_polygon,
                                       group_top, 1)

                    # Background
                    background = pdb.gimp_layer_new(                    
                        image, tile_size, tile_size,
                        RGBA_IMAGE, "background", 100, NORMAL_MODE
                    )    
                    pdb.gimp_image_insert_layer(image, background,
                                                group_top, 2)
                    
                    pdb.gimp_edit_fill(background, BACKGROUND_FILL)
                    
                    # Assign the Y value as the file name
                    out_path = out_dir_zoom_x + str(y)
                    out = "saving file: " + out_path
                    print out                     
                    
                    # Save images as PNG and XCF
                    out_path_png = out_path + ".png"
                    pdb.file_png_save_defaults(
                        image, 
                        group_top,
                        out_path_png,
                        out_path_png
                    )
                    
                    out_path_xcf = out_path + ".xcf"   
                    pdb.gimp_xcf_save(
                        0,
                        image,
                        group_top,
                        out_path_xcf,
                        out_path_xcf
                    )
                    
                    conn_osm.close()
                    
                    pdb.gimp_image_delete(image)
                     
                # Y-direction loop END
                ################################################################
            
            # Y-direction loop END
            ####################################################################
                
        # Zoom-level loop END
        ########################################################################
        
        conn_zoom.close()       
        
        t_end = datetime.datetime.now()
        delta_t = t_end - t_start
        
        logging.info(log_line)
        logging.info("End of Gimp Tile processing at " + str(t_end))
        logging.info("processing duration: " + 
            str(delta_t.total_seconds()) +
            " seconds"
        )
        logging.info(log_line)
        
      
    ############################################################################
    # Get style and tag info of all feature of a type for a zoom level
    def get_feature_styles(self, zoom_level, conn_zoom, feature_type):
        curs_zoom = conn_zoom.cursor()
        
        sql = "SELECT * FROM get_" + feature_type + "_tags_and_style(%s)"                            
        curs_zoom.execute(sql, (zoom_level,))
        
        # Store feature data in an array
        features = []        
        if (feature_type == "line"):        
            for row in curs_zoom.fetchall():
                style_object = StyleObjects.StyleObjectLine(
                    "line", row[1], row[2],
                    row[3], row[4], row[5], row[6], row[7]
                )
                features.append(style_object)
                logging.info("selected OSM " + feature_type 
                    + " features: " + str(row[1]))
        elif (feature_type == "polygon"):
            for row in curs_zoom.fetchall():
                style_object = StyleObjects.StyleObjectPolygon(
                    "polygon", row[1], row[2],
                    row[3], row[4], row[5], row[6], row[7],
                    row[8], row[9]
                )
                features.append(style_object)
                logging.info("selected OSM " + feature_type 
                    + " features: " + str(row[1]))
        
        curs_zoom.close()
        
        return features
        
    ############################################################################
    # Logging functions
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
        
    def draw_features(self, tile_bbox, tile_size, image, 
                           conn_osm, features_line, 
                           group_top, layer_pos):
        
        # Create a layer group for the feature
        feature_group = pdb.gimp_layer_group_new(image)
        pdb.gimp_image_insert_layer(image, feature_group, group_top, layer_pos)       
        
        layer_pos_group = 0
        
        for style_feature in features_line:
                        
            sql_selection = style_feature.get_selection_tags()
            line_style = style_feature.get_line_style()
            
            # Get svg tiles from database                    
            curs_osm = conn_osm.cursor()
            sql = """
                SELECT 
                    ROW_NUMBER() OVER (ORDER BY osm_id) AS id,
                    svg
                FROM (
                    SELECT
                        get_scaled_svg(
                            way,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s
                        ) AS svg,
                        *
                    FROM planet_osm_line  
                    WHERE ST_Intersects ( 
                        way, 
                        get_tile_bbox(
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s
                        ) 
                    )
                ) t
                WHERE (""" + sql_selection + ")"      
                
            # Get SVG tile geometry from database
            curs_osm.execute(sql, (
                tile_bbox[0], tile_bbox[1], tile_bbox[2], tile_bbox[3],
                tile_size,
                tile_bbox[0], tile_bbox[1], tile_bbox[2], tile_bbox[3],
                tile_size,
                line_style[1]
                )
            )
            
            # Create image layer for geometry feature
            layer = pdb.gimp_layer_new(
                image, tile_size, tile_size,
                RGBA_IMAGE,
                sql_selection,
                100, NORMAL_MODE
            )
            pdb.gimp_image_insert_layer(image, layer, 
                                        feature_group, layer_pos_group
                                    )                   
            
            # Style settings
            pdb.gimp_context_set_brush(line_style[0])
            pdb.gimp_context_set_brush_size(line_style[1])
            pdb.gimp_context_set_dynamics(line_style[4])
            pdb.gimp_context_set_foreground((
                line_style[2][0],
                line_style[2][1],
                line_style[2][2],
                line_style[3]
            ))
            pdb.gimp_context_push()
        
            # Create temporary SVG drawing from geometry features
            dwg = svgwrite.Drawing(
                height = tile_size,
                width = tile_size
            )
        
            # Import SVG data into SVG drawing from database
            for row in curs_osm.fetchall():
                path = dwg.path(d=row[1])
                path_str = path.tostring()
                
                logging.info(path)
                logging.info(path_str)
        
                pdb.gimp_vectors_import_from_string(
                    image, 
                    path_str, 
                    -1, 1, 1,
                )
                
                # TO DO:
                # Import from modified string (hachure)
        
            out = "      vectors: " + str(len(image.vectors))
            print out
            logging.info(out)
            
            # Draw vectors into GIMP image layer
            # TO DO: emulate brush dynamics?????
            for vector in image.vectors:
                pdb.gimp_edit_stroke_vectors(layer, vector)
                
                # TO DO:
                # Polygon drawing
                # Masking
                
                pdb.gimp_image_remove_vectors(image, vector)
            
            curs_osm.close()
            
            # Incrementing current layer position
            layer_pos_group =+ layer_pos_group + 1

        # Geometry feature loop END
        ############################################################
        pdb.gimp_image_insert_layer(image, feature_group, None, 0)
        