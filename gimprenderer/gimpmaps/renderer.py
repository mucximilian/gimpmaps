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

from gimpmaps import styles
from svgsketch import hachurizator

class Renderer(object):
    '''
    An abstract metaclass that handles the map creation
    '''
    
    __metaclass__ = ABCMeta
    
    log_line = "###########################################################"
    img_dir = None
    conn_osm = None
    
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
        
        out_file = self.out_dir + self.type
        
        self.draw(feature_styles,
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
        conn_zoom_style = psycopg2.connect(
            'dbname=gimp_osm_styles '
            'user=gis '
            'password=gis '
            'host=localhost '
            'port=5432'
        )
        
        curs_zoom = conn_zoom_style.cursor()
        
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
    
    def create_svg_image(self, feature_styles, bbox, resolution, out_path = ""):
        """
        Drawing function for SVG image files
        """
        
        # Create SVG file name with extension
        dwg = svgwrite.Drawing(
            out_path + ".svg",
            height = resolution[0],
            width = resolution[1]
        )
        
        for feature_style in feature_styles:
            
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
        print "creating SVG: " + out_path + ".svg"
        
class RendererSvg(Renderer):
    '''
    A class to create a single SVG map
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
        
    def draw(self, feature_styles, bbox, resolution, out_file):
        
        self.conn_osm = self.connect_to_osm_db()
        
        self.create_svg_image(feature_styles, self.bbox, resolution, out_file)
        
        self.conn_osm.close()                              