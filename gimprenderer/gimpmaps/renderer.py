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
import operator

from abc import ABCMeta, abstractmethod

from gimpmaps import styles

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
        
        # Checking and setting log directory
        log_dir = self.filepath + "/log/"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)     
        self.start_logging(self.t_start, self.t_form, log_dir + self.type)           
            
        # Checking and setting the output directory
        self.out_dir += self.type + "_" + self.t_form + "/"
        if not os.path.exists(self.out_dir):
            os.makedirs(self.out_dir)
        
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
        Setting style path relative (if not defindend inf config) or absolute
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
            'dbname=osm_muc '
            'user=gis '
            'password=gis '
            'host=localhost '
            'port=5432'
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
            height = resolution[0],
            width = resolution[1]
        )
        
        for feature_style in feature_styles["lines"]:
            
            grp = dwg.g() # Creating SVG Group
            
            svg_geoms = self.get_svg_features(
                bbox,
                resolution, 
                feature_style
            )
    
            # Adding vectors to the group
            for svg_commands in svg_geoms:            
                grp.add(dwg.path(d=svg_commands))
                
            dwg.add(grp)
         
        # Saving SVG file    
        dwg.save()
        print "creating SVG: " + out_file + ".svg"
        
        self.conn_osm.close()
        
    ############################################################################
    
    def get_feature_styles(self, zoom_level):
        """
        Getting feature styles and tags of all geometry types for a zoom level.
        """
    
        features = {}
    
        # Reading the style file from the config
        style_config = self.read_file_style()    
        
        zoom_level = style_config["zoom_levels"][str(zoom_level)]
        features_lines = sorted(
            zoom_level["features"]["lines"],
            key=operator.itemgetter('z_order'),
            reverse=True
        )
        
        lines = []
        for line in features_lines:
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
            
        features["lines"] = lines
                
        features_polygons = zoom_level["features"]["polygons"]
        
        polygons = []
        for polygon in features_polygons:
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
            
        features["polygons"] = polygons

        return features
    
    def get_text_styles(self, zoom_level):
        """
        Getting text styles and tags of all geometry types type for a zoom 
        level.
        """
    
        features = []
        
        # Reading the style file from the config
        style_config = self.read_file_style()    
        
        zoom_level = style_config["zoom_levels"][str(zoom_level)]
        features_polygons = zoom_level["text"]["polygons"]
        
        for polygon in features_polygons:
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
                polygon["color"]
            )
          
            features.append(style_object)

            logging.info(style_object.string_style())

        return features
    
    def get_bg_img(self, zoom_level):
        """
        Getting the background image for a zoom level.
        """
        
        style_config = self.read_file_style()    
        
        zoom_level = style_config["zoom_levels"][str(zoom_level)]
        img = zoom_level["background"]
        
        img_path = self.style_path + "/img/" + img

        return img_path
    
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
        logging.info("processing duration: " + 
            str(delta_t.total_seconds()) +
            " seconds"
        )
        logging.info(Renderer.log_line)