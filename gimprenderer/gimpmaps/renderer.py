'''
Created on May 11, 2015

@author: mucx

'''

import inspect, os
import psycopg2
import logging
import datetime

from abc import ABCMeta

from gimpmaps import styles

class Renderer(object):
    '''
    An abstract metaclass that handles the map creation
    '''
    
    __metaclass__ = ABCMeta
    
    log_line = "###########################################################"
    
    ############################################################################
    def render_map(self):
        
        zoom = self.get_zoom_level(bbox, resolution)
        
        feature_styles = self.get_feature_styles(zoom)
        
        self.draw_features(feature_styles, bbox, out_path)
        
        
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
        curs_zoom.execute(sql, (self.map_style, zoom_level))
        
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
    def get_svg_features(self, bbox, style_feature):
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
                    get_scaled_svg_line(
                        way, 
                        %s, %s, %s, %s, 
                        %s
                    ) AS svg
                FROM (
                    SELECT
                        *
                    FROM planet_osm_line 
                    WHERE ST_Intersects ( 
                        way, 
                        get_tile_bbox(
                            %s, %s, %s, %s, 
                            %s, %s
                        ) 
                    )
                ) t
                WHERE (""" + sql_selection + ")"
                
            # Get SVG tile geometry from database
            curs_osm.execute(sql, (
                bbox[0], bbox[1], bbox[2], bbox[3],
                self.tile_size,
                bbox[0], bbox[1], bbox[2], bbox[3],
                self.tile_size, line_style[1]
                )
            )               
        elif (style_feature.geom_type == 3):   
                        
            sql = """
            SELECT * FROM (
                SELECT
                    get_scaled_svg_polygon(
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
                        get_tile_bbox(
                            %s, %s, %s, %s,
                            %s, %s
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
                    bbox[0], bbox[1], bbox[2], bbox[3],
                    self.tile_size, line_style[1],
                    bbox[0], bbox[1], bbox[2], bbox[3],
                    self.tile_size, line_style[1]
                )
            )    
            
        # Getting vectors and displaying count
        # TO DO: Fix in SQL query: no row number even with empty result
        i = 1
        for row in curs_osm.fetchall():
            
            if (row[0] == None or row[0] ==''): 
                continue # Skipping empty rows              
            
            svg_geometries.append(row[0])
            i += 1
            
        out = "      " + sql_selection + " (" + str(i) + ")"
        logging.info(out)
        print(out)
        
        return svg_geometries
    
    ############################################################################
    def finish(self, t_start):
        
        self.finish_logging(t_start)
        
        print "Finished processing"
    
    ############################################################################
    # Logging functions
    def start_logging(self, t_start, t_form, log_file):
        
        # logging setup
        logging.basicConfig(
            format = '%(message)s',
            # filename = os.getcwd() + "/log/gimp_rendering_" + t_form + ".log",
            filename = log_file + t_form + ".log",
            filemode = 'w',
            level = logging.INFO
        )            
        logging.info(self.log_line)
        logging.info("Start of Gimp Tile processing at " + str(t_start))
        logging.info(self.log_line)
        
        return t_start
    
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