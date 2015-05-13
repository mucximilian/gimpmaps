'''
Created on May 11, 2015

@author: mucx

'''

import psycopg2
import logging
import datetime
import os
import inspect
import svgwrite

from abc import ABCMeta
from gimpfu import *

from gimpmaps import styles

class Renderer(object):
    '''
    An abstract metaclass that handles the map creation
    '''
    
    __metaclass__ = ABCMeta
    
    log_line = "###########################################################"
    
    def setup(self, out_dir):
        """
        Defining the log file and the results directory
        """
        
        t_start = datetime.datetime.now()
        t_form = datetime.datetime.now().strftime('%Y%m%d_%H%M')
                
        filepath = os.path.dirname(
            os.path.abspath(
                inspect.getfile(
                    inspect.currentframe()
                )
            )
        )
        
        # Check and set log directory
        log_dir = filepath + "/log/"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)     
        self.start_logging(t_start, t_form, log_dir + self.type)
        
        # Create a directory containing the date and time
        if (self.out_dir is None):
            self.out_dir = filepath + "/results/"
            
        self.out_dir += self.type + "_" + t_form + "/"
        if not os.path.exists(self.out_dir):
            os.makedirs(self.out_dir)
        
        # Copying the HTML file to view the tiles in the browser for GIMP tiles
        if(self.type == "tiles_gimp"):           
            os.system (
                "cp %s %s" % (
                    filepath + "/results/index.html",
                    self.out_dir + "index.html"
                )
            )
            
        # Setting the directory for background images
        self.img_dir = filepath + "/img/"
            
        return t_start

    def render(self):
        """
        Rendering function. Defines the structure for subclasses. 
        'draw_features' is defined in subclasses with appropriate logic.
        """
        
        t_start = self.setup(self.out_dir)
        
        zoom = self.get_zoom_level_for_scale(self.scale)
        resolution = self.calculate_resolution()
        
        self.log_map_data(zoom, resolution)
        
        feature_styles = self.get_feature_styles(zoom)
        
        out_file = self.out_dir + "map_"
        
        self.draw_features(feature_styles,
                           self.bbox,
                           resolution,
                           out_file)
        
        self.finish(t_start)   
        
    ############################################################################        
    def calculate_resolution(self):
                
        bbox_width = abs(self.bbox[0][0] - self.bbox[1][0])
        bbox_height = abs(self.bbox[0][1] - self.bbox[1][1])
        
        map_width = self.get_pixel_size(bbox_width/self.scale, 300)
        map_height = self.get_pixel_size(bbox_height/self.scale, 300)
        
        return [map_width, map_height]
    
    def get_pixel_size(self, size_cm, dpi):
        size_inch = size_cm * 2.54
        size_pixel = int(round(size_inch * dpi))
        
        return size_pixel
    
    def get_zoom_level_for_scale(self, scale):        
        
        """
        Returning the appropriate zoom level for a given scale
        See scales here: http://wiki.openstreetmap.org/wiki/Zoom_levels
        """
        zoom = 0
        
        if (scale <= 0):
            print "Invalid scale"
            exit
        elif(scale > 0 and scale <= 1000):
            zoom = 19
        elif(scale > 0 and scale <= 2000):
            zoom = 18
        elif(scale > 0 and scale <= 4000):
            zoom = 17
        elif(scale > 0 and scale <= 8000):
            zoom = 16
        elif(scale > 0 and scale <= 15000):
            zoom = 15
        elif(scale > 0 and scale <= 35000):
            zoom = 14
        elif(scale > 0 and scale <= 70000):
            zoom = 13
        elif(scale > 0 and scale <= 150000):
            zoom = 12
        elif(scale > 0 and scale <= 250000):
            zoom = 11
        elif(scale > 0 and scale <= 500000):
            zoom = 10
        elif(scale > 0 and scale <= 1000000):
            zoom = 9
        elif(scale > 0 and scale <= 2000000):
            zoom = 8
        elif(scale > 0 and scale <= 4000000):
            zoom = 7
        elif(scale > 0 and scale <= 10000000):
            zoom = 6
        elif(scale > 0 and scale <= 15000000):
            zoom = 5
        elif(scale > 0 and scale <= 35000000):
            zoom = 4
        elif(scale > 0 and scale <= 70000000):
            zoom = 3
        elif(scale > 0 and scale <= 150000000):
            zoom = 2
        elif(scale > 0 and scale <= 250000000):
            zoom = 1
        elif(scale > 0 and scale <= 500000000):
            zoom = 0
        
        return zoom
        
    ############################################################################
    def get_feature_styles(self, zoom_level):
        """
        Get style and tag info of all feature of a type for a zoom level.
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
        
        sql = "SELECT * FROM get_tags_and_style(%s, %s)"                            
        curs_zoom.execute(sql, (self.map_style_id, zoom_level))
        
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
    
    ############################################################################
    def get_svg_features(self, bbox, resolution, style_feature):
        """
        Returning a list of SVG commands to draw a geometry feature
        """
        
        svg_geometries = []
        
        sql_selection = style_feature.get_selection_tags()
        line_style = style_feature.get_line_style()
        
        # Query svg tiles from database               
        curs_osm = self.conn_osm.cursor()
        
        if (style_feature.geom_type == 2):
            
            sql = """
                SELECT 
                    gimpmaps_scale_svg_line(
                        way, 
                        %s, %s, %s, %s, 
                        %s, %s
                    ) AS svg
                FROM (
                    SELECT
                        *
                    FROM planet_osm_line 
                    WHERE ST_Intersects ( 
                        way, 
                        gimpmaps_get_bbox(
                            %s, %s, %s, %s, 
                            %s, %s,
                            %s
                        ) 
                    )
                ) t
                WHERE (""" + sql_selection + ")"
                
            # Get SVG tile geometry from database
            curs_osm.execute(sql, (
                bbox[0][0], bbox[0][1], bbox[1][0], bbox[1][1],
                resolution[0], resolution[1],
                bbox[0][0], bbox[0][1], bbox[1][0], bbox[1][1],
                resolution[0], resolution[1],
                line_style[1]
                )
            )               
        elif (style_feature.geom_type == 3):   
                        
            sql = """
            SELECT * FROM (
                SELECT
                    gimpmaps_scale_svg_polygon(
                        way,
                        %s, %s, %s, %s,
                        %s, %s,
                        %s
                    ) AS svg
                FROM (
                    SELECT
                        *
                    FROM planet_osm_polygon 
                    WHERE ST_Intersects ( 
                        way, 
                        gimpmaps_get_bbox(
                            %s, %s, %s, %s,
                            %s, %s,
                            %s
                        ) 
                    )
                ) t
                WHERE
                    """ + sql_selection + """
            ) x 
            WHERE coalesce(svg, '') <> ''"""                
                
            # Get SVG tile geometry from database
            curs_osm.execute(
                sql, 
                (
                bbox[0][0], bbox[0][1], bbox[1][0], bbox[1][1],
                resolution[0], resolution[1],
                line_style[1],
                bbox[0][0], bbox[0][1], bbox[1][0], bbox[1][1],
                resolution[0], resolution[1],
                line_style[1]
                )
            )    
            
        # Getting vectors and displaying count
        # TO DO: Fix in SQL query: no row number even with empty result
        for row in curs_osm.fetchall():
            
            # Escape if no SVG geometry is provided               
            if (row[0] == None or row[0] ==''): 
                continue # Skipping empty rows              
            
            svg_geometries.append(row[0])
            
        out = "      " + sql_selection + " (" + str(len(svg_geometries)) + ")"
        logging.info(out)
        print(out)
        
        return svg_geometries
    
    ############################################################################
    def finish(self, t_start):
        
        self.finish_logging(t_start)
        
        print "Finished processing"
    
    ############################################################################
    # Logging functions
    def start_logging(self, t_start, t_form, log_dir):
        
        # logging setup
        logging.basicConfig(
            format = '%(message)s',
            # filename = os.getcwd() + "/log/gimp_rendering_" + t_form + ".log",
            filename = log_dir + "_" + t_form + ".log",
            filemode = 'w',
            level = logging.INFO
        )            
        logging.info(self.log_line)
        logging.info("Start of GIMP processing at " + str(t_start))
        logging.info(self.log_line)
        
        return t_start
    
    def log_map_data(self, zoom, resolution):
        logging.info("scale: " + str(self.scale))
        logging.info("zoom level: " + str(zoom))
        logging.info("bbox ul x: " + str(self.bbox[0][0]))
        logging.info("bbox ul y: " + str(self.bbox[0][1]))
        logging.info("bbox lr x: " + str(self.bbox[1][0]))
        logging.info("bbox lr y: " + str(self.bbox[1][1]))
        logging.info("map width in px: " + str(resolution[0]))
        logging.info("map height in px: " + str(resolution[1]))
        logging.info(self.log_line)
    
    def finish_logging(self, t_start):      
        
        t_end = datetime.datetime.now()
        delta_t = t_end - t_start
        
        logging.info(self.log_line)
        logging.info("End of Gimp Tile processing at " + str(t_end))
        logging.info("processing duration: " + 
            str(delta_t.total_seconds()) +
            " seconds"
        )
        logging.info(self.log_line)
        
    def connect_to_osm_db(self):
        """
        Establishing a connection to the database storing the OSM data
        """
        
        conn = psycopg2.connect(
            'dbname=osm_muc '
            'user=gis '
            'password=gis '
            'host=localhost '
            'port=5432'
        )
        
        return conn
    
class RendererSvg(Renderer):
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
        
    def draw_features(self, feature_styles, bbox, resolution, out_path = ""):
        """
        Drawing function for SVG image files   
        """
        
        self.conn_osm = self.connect_to_osm_db()
        
        # Create SVG file name with extension
        dwg = svgwrite.Drawing(
            out_path + ".svg",
            height = resolution[0],
            width = resolution[1]
        )
        
        for feature_style in feature_styles:
            
            svg_geoms = self.get_svg_features(
                bbox,
                resolution, 
                feature_style
            )
    
            # Drawing vectors
            for svg_commands in svg_geoms:            
                dwg.add(dwg.path(d=svg_commands))
            
        dwg.save()
        print "creating SVG: " + out_path + ".svg"
        
        self.conn_osm.close()
        
class RendererGimp(Renderer):
    '''
    This is a renderer to create a GIMP image from map data in a provided 
    bounding box with a specified styling
    '''

    def __init__(self, bbox, scale, out_dir, map_style_id, create_xcf):
        '''
        Constructor
        '''
        
        self.bbox = bbox
        self.scale = scale
        self.out_dir = out_dir
        self.map_style_id = map_style_id
        self.create_xcf = create_xcf
        self.type = "map_gimp"
        
    def draw_features(self, feature_styles, bbox, resolution, out_path = ""):
        """
        Drawing the feature_styles as GIMP images and saving to PNG and/or XCF
        """
        
        self.conn_osm = self.connect_to_osm_db()
       
        # Create GIMP image with layer group
        image = pdb.gimp_image_new(
           resolution[0],
           resolution[1],
           RGB
        )
        
        # Resetting GIMP image context
        pdb.gimp_context_set_defaults()
        pdb.gimp_context_push()        
        pdb.gimp_context_set_background((255,255,255,255))
        
        # Creating a 'top' layer group that will contain all the
        # layer groups added in the following steps
        parent = pdb.gimp_layer_group_new(image)
        pdb.gimp_image_insert_layer(image, parent, None, 0)
        
        # Create a layer group for the feature type groups 
        group_line = pdb.gimp_layer_group_new(image)
        group_polygon = pdb.gimp_layer_group_new(image)
        
        pdb.gimp_image_insert_layer(image, group_line, parent, 0)
        pdb.gimp_image_insert_layer(image, group_polygon, parent, 1)
        
        layer_pos_group = 0       
        
        mask = False
        
        # Geometry feature loop END
        for feature_style in feature_styles:
                        
            sql_selection = feature_style.get_selection_tags()
            line_style = feature_style.get_line_style()
            
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
            
            spacing = float(line_style[1]*2) # hachure spacing
            angle = 30 # hachure angle

            # Import SVG data into SVG drawing from database
            svg_geoms = self.get_svg_features(
                bbox,
                resolution, 
                feature_style
            )
            for svg_commands in svg_geoms:
                         
                svg_path = svgwrite.path.Path(svg_commands)
                svg_path_str = svg_path.tostring()
        
                # Import vectors to GIMP image
                if (not mask and feature_style.geom_type == 3):                    
                    # Creating hachure vectors
                    # TO DO: Adding outlines
                    svg_renderer = hachurizator.Hachurizator(spacing, angle)                    

                    hachure = svg_renderer.get_svg_hachure(svg_path)
                    if (hachure is not None):                   
                        pdb.gimp_vectors_import_from_string(
                            image, 
                            hachure, 
                            -1, 1, 1,
                        )
                    else:
                        continue
                else:
                    # Adding vectors for stroking of lines, outlines/mask
                    pdb.gimp_vectors_import_from_string(
                        image, 
                        svg_path_str, 
                        -1, 1, 1,
                    )
                               
            # Drawing line feature_styles
            if (feature_style.geom_type == 2):
                
                # Creating image layer for geometry feature
                layer = pdb.gimp_layer_new(
                    image, resolution[0], resolution[1],
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
            
            # Drawing polygon feature_styles
            elif (feature_style.geom_type == 3):
                
                if (mask):
                
                    # Creating a layer group for vector and raster layers
                    vector_raster_group = pdb.gimp_layer_group_new(image)
                    pdb.gimp_image_insert_layer(image,
                                                vector_raster_group, 
                                                group_polygon,
                                                0)
                    
                    # Creating vector layer
                    layer_vector = pdb.gimp_layer_new(
                        image, resolution[0], resolution[1],
                        RGBA_IMAGE,
                        sql_selection,
                        100, NORMAL_MODE
                    )
                    pdb.gimp_image_insert_layer(image, layer_vector, 
                                                vector_raster_group, 0
                                            )
                    
                    # Adding background image to use the mask on
                    mask_image = "img/" + feature_style.get_image_data()[0]
                    layer_mask_image = pdb.gimp_file_load_layer(image, 
                                                                mask_image)
                    pdb.gimp_image_insert_layer(image, layer_mask_image, 
                                                vector_raster_group, 1)
                    
                    # TO DO: Check why duplicate for loop?
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
                        image, resolution[0], resolution[1],
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
            
            # Incrementing current layer position
            layer_pos_group =+ layer_pos_group + 1
                
        # Background image        
        background = pdb.gimp_file_load_layer(image, 
            self.img_dir + "texture_blackboard.png"
        )
        pdb.gimp_image_insert_layer(image, background, parent, 2)            
        
        # pdb.gimp_edit_fill(background, BACKGROUND_FILL)
                      
        # Save images as PNG and XCF
        out_path_png = out_path + ".png"
        pdb.file_png_save_defaults(
            image, 
            parent,
            out_path_png,
            out_path_png
        )
        
        if (self.create_xcf):
        
            out_path_xcf = out_path + ".xcf"   
            pdb.gimp_xcf_save(
                0,
                image,
                parent,
                out_path_xcf,
                out_path_xcf
            )
        
        self.conn_osm.close()
            
        pdb.gimp_image_delete(image)
        pdb.gimp_context_pop()