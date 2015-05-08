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

from gimpfu import *

from maprenderer.tiles import tilerenderer
from maprenderer.svgstyling import hachurizator

class TileRendererGimp(tilerenderer.TileRenderer):
    """
    This subclass of tilerenderer implements different 'setup' and
    'draw_features' methods for the creation of GIMP tiles as PNG and if defined
    in the 'create_xcf' variable also as XCF files. 
    can be defined )
    """
    
    def __init__(self, bbox, zoom_levels, tile_size, out_dir, create_xcf):
        self.bbox = bbox
        self.zoom_levels = zoom_levels
        self.tile_size = tile_size
        self.out_dir = out_dir
        self.create_xcf = create_xcf
        
    def setup(self, t_start, t_form):
        """
        Setting up the logging environment and the output directory. Also 
        copies the 'index.html' file to view the tile result in a web browser
        into the output directory.
        """
        
        log_file = os.getcwd() + "/log/gimp_rendering_"
        self.start_logging(t_start, t_form, log_file)
        
        result_dir = self.out_dir # storing the original directory for later
        
        # Create a directory containing the date and time
        self.out_dir += "tiles_" + t_form + "/"
        if not os.path.exists(self.out_dir):
            os.makedirs(self.out_dir)
            
        # Copying the HTML file to view the tiles in the browser
        os.system ("cp %s %s" % (
                                   result_dir + "index.html",
                                   self.out_dir + "index.html")
                   )      
        
    def draw_features(self, features, tile_bbox, out_path):
        """
        Drawing the features as GIMP images and saving to PNG and/or XCF
        """
        
        conn_osm = psycopg2.connect(
            'dbname=osm_muc '
            'user=gis '
            'password=gis '
            'host=localhost '
            'port=5432'
        )
       
        # Create GIMP image with layer group
        image = pdb.gimp_image_new(
           self.tile_size,
           self.tile_size,
           RGB
        )
        pdb.gimp_context_set_background((255,255,255,255))
        
        # Creating a 'top' layer group that will contain all the
        # layer groups added in the following steps
        group_top = pdb.gimp_layer_group_new(image)
        pdb.gimp_image_insert_layer(image, group_top, None, 0)
        
        # Create a layer group for the feature type groups 
        group_line = pdb.gimp_layer_group_new(image)
        group_polygon = pdb.gimp_layer_group_new(image)
        
        pdb.gimp_image_insert_layer(image, group_line, group_top, 0)
        pdb.gimp_image_insert_layer(image, group_polygon, group_top, 1)
        
        layer_pos_group = 0
        
        # Resetting GIMP image context
        pdb.gimp_context_set_defaults()
        pdb.gimp_context_push()
        
        mask = False
        
        # Geometry feature loop END
        for style_feature in features:
                        
            sql_selection = style_feature.get_selection_tags()
            line_style = style_feature.get_line_style()

            # Query svg tiles from database               
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
                    
                # Get SVG tile geometry from database
                curs_osm.execute(sql, (
                    tile_bbox[0], tile_bbox[1], tile_bbox[2], tile_bbox[3],
                    self.tile_size,
                    tile_bbox[0], tile_bbox[1], tile_bbox[2], tile_bbox[3],
                    self.tile_size,
                    line_style[1]
                    )
                )               
            elif (style_feature.geom_type == 3):   
                
                # TO DO:
                # tile_size/brush_size instead of 100
                
                way_select = "way"
                if (mask):
                    way_select = "ST_Union(way)"
                
                sql = """
                    SELECT 
                        ROW_NUMBER() OVER () AS id,
                        get_scaled_svg_polygon(
                            """ + way_select + """,
                            %s, %s, %s, %s, %s, %s
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
                        AND ST_Area(way) > ((((%s - %s)/(%s / %s))*2)^2)
                    ) t
                    WHERE (""" + sql_selection + ")"   
                    
                # Get SVG tile geometry from database
                curs_osm.execute(sql, (
                    tile_bbox[0], tile_bbox[1], tile_bbox[2], tile_bbox[3],
                    self.tile_size, line_style[1],
                    tile_bbox[0], tile_bbox[1], tile_bbox[2], tile_bbox[3],
                    self.tile_size,
                    line_style[1],
                    tile_bbox[2], tile_bbox[0],
                    self.tile_size, line_style[1]
                    )
                )               
            
            # Style settings
            # TO DO: emulate brush dynamics?????
            pdb.gimp_context_pop()
            pdb.gimp_context_set_brush(line_style[0])
            pdb.gimp_context_set_brush_size(line_style[1])
            pdb.gimp_context_set_dynamics(line_style[4])
            pdb.gimp_context_set_foreground((
                line_style[2][0],
                line_style[2][1],
                line_style[2][2]                
            ))
            pdb.gimp_context_set_opacity(line_style[3]) # Not working...?
            pdb.gimp_context_push()
               
            # Import SVG data into SVG drawing from database
            for row in curs_osm.fetchall():
                # Escape if no SVG geometry is provided
                # TO DO: Fix in SQL query: no row number even with empty result
                if (row[1] == None or row[1] ==''):
                    continue                
                path = svgwrite.path.Path(row[1]) # M 226 176 l -2 -0
                path_str = path.tostring() # <path d="M 226 176 l -2 -0" />
                
                # print "path string = " + path_str
        
                if (not mask and style_feature.geom_type == 3):
                    
                    svg_renderer = hachurizator.Hachurizator()

                    hachure = svg_renderer.get_svg_hachure(path)
                    
                    hachure = svgwrite.path.Path(hachure)
                    
                    if (hachure.tostring() == None or hachure.tostring() ==''):
                        continue
                    
                    pdb.gimp_vectors_import_from_string(
                        image, 
                        hachure.tostring(), 
                        -1, 1, 1,
                    )
                    
                else:
                    pdb.gimp_vectors_import_from_string(
                        image, 
                        path_str, 
                        -1, 1, 1,
                    )
                
                # TO DO:
                # Import from modified string (hachure)
        
            out = ("      " + sql_selection + " (" + str(len(image.vectors)) + ")")
            logging.info(out)
                       
            # Drawing line features
            if (style_feature.geom_type == 2):
                
                # Creating image layer for geometry feature
                layer = pdb.gimp_layer_new(
                    image, self.tile_size, self.tile_size,
                    RGBA_IMAGE,
                    sql_selection,
                    100, NORMAL_MODE
                )
                pdb.gimp_image_insert_layer(image, layer, 
                                            group_line, layer_pos_group
                                        )    
                
                # Drawing vectors into GIMP layer
                for vector in image.vectors:
                    pdb.gimp_edit_stroke_vectors(layer, vector)                    
                    pdb.gimp_image_remove_vectors(image, vector)
            
            # Drawing polygon features
            elif (style_feature.geom_type == 3):
                
                if (mask):
                
                    # Creating a layer group for vector and raster layers
                    vector_raster_group = pdb.gimp_layer_group_new(image)
                    pdb.gimp_image_insert_layer(image,
                                                vector_raster_group, group_polygon,
                                                0)
                    
                    # Creating vector layer
                    layer_vector = pdb.gimp_layer_new(
                        image, self.tile_size, self.tile_size,
                        RGBA_IMAGE,
                        sql_selection,
                        100, NORMAL_MODE
                    )
                    pdb.gimp_image_insert_layer(image, layer_vector, 
                                                vector_raster_group, 0
                                            )
                    
                    # Adding background image to use the mask on
                    mask_image = "img/" + style_feature.get_image_data()[0]
                    layer_mask_image = pdb.gimp_file_load_layer(image, mask_image)
                    pdb.gimp_image_insert_layer(image, layer_mask_image, 
                                                vector_raster_group, 1)
                    
                    # Drawing and selecting vectors in GIMP layer
                    for vector in image.vectors:
                        pdb.gimp_edit_stroke_vectors(layer_vector, vector)                   
                        
                    # Drawing and selecting vectors in GIMP layer
                    for vector in image.vectors:
                        pdb.gimp_image_select_item(image, CHANNEL_OP_ADD, vector)
                        
                        pdb.gimp_image_remove_vectors(image, vector)
                        
                    # Grow and shrink selection to even out small selections
    #                 pdb.gimp_selection_shrink(image, 2)
    #                 pdb.gimp_selection_grow(image, 2)
    #                 pdb.gimp_selection_grow(image, 2)
    #                 pdb.gimp_selection_shrink(image, 2)
                    
                    # Apply mask of collected vectors on background image
                    mask = pdb.gimp_layer_create_mask(layer_mask_image, 4)
                    pdb.gimp_layer_add_mask(layer_mask_image, mask)
                    
                    pdb.gimp_selection_clear(image)
                    
                else :
                    
                    # Creating image layer for geometry feature
                    layer = pdb.gimp_layer_new(
                        image, self.tile_size, self.tile_size,
                        RGBA_IMAGE,
                        sql_selection,
                        100, NORMAL_MODE
                    )
                    pdb.gimp_image_insert_layer(image, layer, 
                                                group_line, layer_pos_group
                                            )    
                    
                    # Drawing vectors into GIMP layer
                    for vector in image.vectors:
                        pdb.gimp_edit_stroke_vectors(layer, vector)                    
                        pdb.gimp_image_remove_vectors(image, vector)              
                    
                
            curs_osm.close()
            
            # Incrementing current layer position
            layer_pos_group =+ layer_pos_group + 1
                
        # Background image       
        background = pdb.gimp_file_load_layer(image, 
                           "img/texture_blackboard.png")
        pdb.gimp_image_insert_layer(image, background,
                                    group_top, 2)            
        # pdb.gimp_edit_fill(background, BACKGROUND_FILL)
                      
        # Save images as PNG and XCF
        out_path_png = out_path + ".png"
        pdb.file_png_save_defaults(
            image, 
            group_top,
            out_path_png,
            out_path_png
        )
        
        if (self.create_xcf):
        
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
        pdb.gimp_context_pop()   