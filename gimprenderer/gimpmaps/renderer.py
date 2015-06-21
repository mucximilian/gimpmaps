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
import json

from abc import ABCMeta, abstractmethod

from gimpmaps import styles, sketchadapter

class Renderer(object):
    '''
    An abstract metaclass that provides the basic functionality for map and tile 
    creation.
    '''
    
    __metaclass__ = ABCMeta
    
    log_line = "###############################################################"
       
    @abstractmethod
    def __init__(self, config_file):
        """
        Constructor
        """
        
        self.config_file = config_file
        
    def setup(self):
        """
        Setting the instance variables and defining logfile and the result
        directory.
        """
        
        self.set_filepath() # setting self.filepath        
        
        self.set_from_config()
        
        self.t_start = datetime.datetime.now()
        self.t_form = datetime.datetime.now().strftime('%Y%m%d_%H%M')
        
        
        # Checking and setting the output directory for the image and log file
        self.out_dir += self.type + "_" + self.t_form + "/"
        if not os.path.exists(self.out_dir):
            os.makedirs(self.out_dir)  
        self.start_logging(self.t_start, self.t_form, self.out_dir + self.type)           

        # Copying the HTML file to view the tiles in the browser for GIMP tiles
        if(self.type == "tiles_gimp"):           
            os.system (
                "cp %s %s" % (
                    self.filepath + "/results/index.html",
                    self.out_dir + "index.html"
                )
            )
        
    ############################################################################
        
    def set_from_config(self):
        """
        Setting the instance variables
        """
        
        self.read_file_config(self.config_file) # setting self.config   
        
        # Setting instance variables
        self.set_style_path() # self.style_path
        self.set_out_dir() # self.out_dir
        self.set_bbox() # self.bbox
        self.set_database() # self.database
        self.set_create_xcf() # Setting self.create_xcf  
        
    def set_out_dir(self):        
        out_dir = self.config["out_dir"]
        
        if (out_dir is None):        
            self.out_dir = self.filepath + "/results/"     
        else:
            self.out_dir = out_dir
        
    def set_bbox(self):        
        self.bbox = self.config["map"]["bounding_box"]
        
    def set_create_xcf(self):        
        self.create_xcf = self.config["map"]["create_xcf"]
        
    def set_database(self):        
        self.database = self.config["osm_db"]
        
    def set_style_path(self):
        """
        Setting style path relative (if not defindend in config) or absolute
        as instance variable.
        """
        style_path = self.config["style"]["style_path"]
        
        if (style_path is None):        
            style_path = self.filepath + "/styles/"            

        style_path += self.config["style"]["style_name"]
        
        self.style_path = style_path  
        
    ############################################################################
    
    def read_file_config(self, config_file):
        """
        Reading the provided config file and storing the dictionary with the
        object.
        """
        
        filepath = ""
        
        print self.filepath
        
        if (config_file.startswith("/")):
            filepath = config_file
        else:
            filepath = self.filepath + "/conf/"  + config_file      
            
        read_file = open(filepath, "r")            
        json_config = json.load(read_file)
        
        self.config = json_config
        
    def read_file_style(self):        
        
        style_file = self.style_path + "/style.json"
        
        read_file = open(style_file, "r")        
        json_style = json.load(read_file)
        
        return json_style
    
    def set_filepath(self):
        filepath = os.path.dirname(
            os.path.abspath(
                inspect.getfile(
                    inspect.currentframe()
                )
            )
        )
        self.filepath = filepath
        
    def connect_to_osm_db(self):
        """
        Establishing a connection to the database storing the OSM data.
        """
        
        conn = psycopg2.connect(
            "dbname=%s user=%s password=%s host=%s port=%s" % (
                self.database["db_name"],
                self.database["user"],
                self.database["password"],
                self.database["host"],
                5432)
            
        )
                    
        return conn
    
    def finish(self):
        
        self.finish_logging(self.t_start)
        
        print "Finished processing"
    
    ############################################################################
    
    def create_svg_image(self, feature_styles, bbox, resolution, out_file):
        """
        Drawing function for SVG image files
        """
        
        self.conn_osm = self.connect_to_osm_db()
        
        # Create SVG file name with extension
        dwg = svgwrite.Drawing(
            out_file + ".svg",
            size=(resolution[0],resolution[1])
        )
        
        for feature_style in feature_styles["lines"]:
            
            grp_lines = dwg.g() # Creating SVG Group
            
            logging.info("##### Reading line geometry")
            
            svg_geoms = self.get_svg_features(
                bbox,
                resolution, 
                feature_style
            )           
    
            # Adding vectors to the group
            for svg_commands in svg_geoms:
                
                logging.info("##### Sketching line geometry")
                
                line_sketched = sketchadapter.sketch_line_path(svg_commands)
                grp_lines.add(line_sketched)
                
            dwg.add(grp_lines)
        
        for feature_style in feature_styles["polygons"]:
            
            grp_hachures = dwg.g() # Creating SVG Group
            grp_outlines = dwg.g() # Creating SVG Group
            
            logging.info("##### Reading polygon geometry")
            svg_geoms = self.get_svg_features(
                bbox,
                resolution, 
                feature_style
            )
    
            # Adding vectors to the group
            for svg_commands in svg_geoms:
                
                logging.info("##### Sketching polygon hachures")
                hachures = sketchadapter.sketch_polygon_hachure(svg_commands)                
                if hachures is not None:
                             
                    for hachure in hachures:
                         
                        if (hachure is not None):                                    
                            grp_hachures.add(hachure)
                                     
                        else:
                            continue
                        
                logging.info("##### Sketching polygon outlines")
                outlines = sketchadapter.sketch_polygon_outline(svg_commands)                
                if outlines is not None:
                             
                    for outline in outlines:
                         
                        if (outline is not None):                            
                            grp_outlines.add(outline)
                            
                        else:
                            continue
                
            dwg.add(grp_hachures)
            dwg.add(grp_outlines)
         
        # Saving SVG file
        print "Creating SVG: " + out_file + ".svg ..."
        dwg.save()        
        print "Done!"
        
        self.conn_osm.close()
        
    ############################################################################
    
    def get_feature_styles(self, zoom_level):
        """
        Getting feature styles and tags of all geometry types for a zoom level.
        """
    
        zoom_style = {}
    
        # Reading the style file from the config
        style_config = self.read_file_style()        
        features = style_config["features"]        
        
        # LINES
        features_lines = features["lines"]
        
        lines = []
        for line in features_lines:
            
            zoom_min = line["zoom_min"]
            zoom_max = line["zoom_max"]
            
            if (zoom_level >= zoom_min and zoom_level <= zoom_max):
                style_object = styles.StyleObjectLine(
                    2,
                    line["osm_tags"],
                    line["z_order"],
                    line["stroke_line"]["brush"],
                    line["stroke_line"]["brush_size"],
                    line["stroke_line"]["color"],
                    line["stroke_line"]["dynamics"]
                )
          
                lines.append(style_object)
                
                logging.info(style_object.string_style())
                
        # Sorting lines by z-order
        lines.sort(key=lambda x: x.z_order, reverse=True)
                
        zoom_style["lines"] = lines

        # POLYGONS
        features_polygons = features["polygons"]

        polygons = []
        for polygon in features_polygons:
            
            zoom_min = polygon["zoom_min"]
            zoom_max = polygon["zoom_max"]
            
            if (zoom_level >= zoom_min and zoom_level <= zoom_max):
                style_object = styles.StyleObjectPolygon(
                    3,
                    polygon["osm_tags"],
                    polygon["z_order"],
                    polygon["stroke_line"]["brush"],
                    polygon["stroke_line"]["brush_size"],
                    polygon["stroke_line"]["color"],
                    polygon["stroke_line"]["dynamics"],
                    polygon["stroke_hachure"]["brush"],
                    polygon["stroke_hachure"]["brush_size"],
                    polygon["stroke_hachure"]["color"],
                    polygon["stroke_hachure"]["dynamics"],
                    polygon["image"],
                )
              
                polygons.append(style_object)
    
                logging.info(style_object.string_style())
                
        # Sorting polygons by z-order
        polygons.sort(key=lambda x: x.z_order, reverse=True)
            
        zoom_style["polygons"] = polygons

        return zoom_style
    
    def get_text_styles(self, zoom_level):
        """
        Getting text styles and tags of all geometry types type for a zoom 
        level.
        """
    
        zoom_style = {}
    
        # Reading the style file from the config
        style_config = self.read_file_style()        
        text = style_config["text"]
        
        # POINTS
        # TO DO: Add point text styles     
        
        # POLYGONS
        text_polygons = text["polygons"]
        
        polygons = []
        for polygon in text_polygons:
            
            zoom_min = polygon["zoom_min"]
            zoom_max = polygon["zoom_max"]
            
            if (zoom_level >= zoom_min and zoom_level <= zoom_max):
                style_object = styles.StyleObjectText(
                    3,
                    polygon["osm_tags"],
                    polygon["z_order"],
                    polygon["stroke_line"]["brush"],
                    polygon["stroke_line"]["brush_size"],
                    polygon["stroke_line"]["color"],
                    polygon["stroke_line"]["dynamics"],
                    polygon["font"],
                    polygon["font_size"],
                    polygon["color"],
                    polygon["effect"]["name"],
                    polygon["effect"]["buffer_size"],
                    polygon["effect"]["buffer_color"]
                )
              
                polygons.append(style_object)
    
                logging.info(style_object.string_style())
                
        # Sorting polygons by z-order
        polygons.sort(key=lambda x: x.z_order, reverse=True)

        zoom_style["polygons"] = polygons
        
        return zoom_style
        
    def get_bg_img(self, zoom_level):
        """
        Getting the background image for a zoom level.
        """

        # Reading the style file from the config
        style_config = self.read_file_style()        
        bg_imgs = style_config["background"]        
        
        images = []
        for bg_img in bg_imgs:
            
            zoom_min = bg_img["zoom_min"]
            zoom_max = bg_img["zoom_max"]
            
            if (zoom_level >= zoom_min or zoom_level <= zoom_max):
                
                img = bg_img["image"]
                img_path = self.style_path + "/img/" + img
                images.append(img_path)

        image = images[0]
        
        # TO DO:
        # Implement checking for multiple or no results

        return image
    
    ############################################################################
    def get_svg_features(self, bbox, resolution, style_feature):
        """
        Returning a list of SVG commands to draw a geometry feature
        """
        
        svg_geometries = []
        
        sql_selection = style_feature.get_selection_tags()
        
        # TO DO: Check selection tags for format and escape column names
        
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
            params = (
                bbox[0][0], bbox[0][1], bbox[1][0], bbox[1][1],
                resolution[0], resolution[1],
                bbox[0][0], bbox[0][1], bbox[1][0], bbox[1][1],
                resolution[0], resolution[1],
                line_style[1]
                )
            
            curs_osm.execute(sql, params)               
        elif (style_feature.geom_type == 3):   
                        
            sql = """
            SELECT * FROM (
                SELECT svg FROM (
                    SELECT
                        gimpmaps_scale_svg_polygon(
                            ST_GeometryN(
                                ST_Union(way),generate_series(
                                    1,ST_NumGeometries(ST_Union(way))
                                )
                            ), 
                            %s, %s, %s, %s, 
                            %s, %s, %s
                        ) AS svg
                    FROM 
                        planet_osm_polygon
                    WHERE 
                        way 
                        &&
                        gimpmaps_get_bbox(
                            %s, %s, %s, %s, 
                            %s, %s, %s
                        )
                    AND 
                        ST_Area(way) > (%s * %s) ^ 2
                    AND 
                    (""" + sql_selection + """)
                )t    
            ) x 
            WHERE coalesce(svg, '') <> ''
            """
            
            params = (
                bbox[0][0], bbox[0][1], bbox[1][0], bbox[1][1],
                resolution[0], resolution[1],
                line_style[1],
                bbox[0][0], bbox[0][1], bbox[1][0], bbox[1][1],
                resolution[0], resolution[1],
                line_style[1], line_style[1], line_style[1]
            )           
                
            # Get SVG tile geometry from database
            curs_osm.execute(sql, params)
            
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
    
    def get_text(self, bbox, resolution, style_feature):
        
        text_points = []
        
        sql_selection = style_feature.get_selection_tags()
        
        # Query text in tile from database               
        curs_osm = self.conn_osm.cursor()
        
        sql = """
            SELECT 
                name,
                gimpmaps_scale_text_polygon_point(
                    way, 
                    %s, %s, %s, %s, 
                    %s, %s
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
            WHERE (""" + sql_selection + ")"
            
        # Get SVG tile geometry from database
        curs_osm.execute(sql, (
            bbox[0][0], bbox[0][1], bbox[1][0], bbox[1][1],
            resolution[0], resolution[1],
            bbox[0][0], bbox[0][1], bbox[1][0], bbox[1][1],
            resolution[0], resolution[1],
            0 # Tile bbox buffer. TO DO: Determine by text length?
            )
        )
        
        # Getting text points and displaying count
        # TO DO: Fix in SQL query: no row number even with empty result
        for row in curs_osm.fetchall():
            
            logging.info(row[0])
            
            # Escape if no SVG geometry is provided               
            if (row[0] == None or row[0] ==''): 
                continue # Skipping empty rows              
            
            text_points.append([row[0], [row[1][0], -row[1][1]]])
            
        out = "      " + sql_selection + " (" + str(len(text_points)) + ")"
        logging.info(out)
        print(out)
        
        return text_points  
    
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
        logging.info(Renderer.log_line)
        logging.info("Start of GIMP processing at " + str(t_start))
        logging.info(Renderer.log_line)
        
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
        logging.info(Renderer.log_line)
    
    def finish_logging(self, t_start):      
        
        t_end = datetime.datetime.now()
        delta_t = t_end - t_start
        
        logging.info(Renderer.log_line)
        logging.info("End of Gimp Tile processing at " + str(t_end))
        logging.info("Processing took " + 
            str(delta_t.total_seconds()) +
            " seconds"
        )
        logging.info(Renderer.log_line)