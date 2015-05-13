'''
Created on May 11, 2015

@author: mucx
'''

import math
import os
import logging

from abc import ABCMeta

from gimpmaps import renderer

class TileRenderer(renderer.Renderer):
    '''
    An abstract metaclass that handles the tiling
    '''
    
    __metaclass__ = ABCMeta
    
    origin_x = -(2 * math.pi * 6378137 / 2.0)
    origin_y = 2 * math.pi * 6378137 / 2.0
         
    def render(self):
        """
        Basic tile rendering function. Loops over the specified bounding box in
        different zoom levels.
        """
        
        t_start = self.setup(self.out_dir)       
        
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
            feature_styles = self.get_feature_styles(zoom)
            
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
                    
                    self.draw_features(feature_styles, 
                                       tile_bbox, 
                                       self.tile_size, 
                                       out_path)               
        
        self.finish(t_start)
    
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
        tile_size_m = tile_size_0 / int(math.pow(2, zoom))
        tiles_count = tiles_count_x * tiles_count_y
        
        tiling_data= [
            [tile_ul[0],tile_ul[1]],
            [tile_lr[0],tile_lr[1]],
            [tiles_count_x, tiles_count_y],
            tile_size_m
        ]
        
        print "------------------------------------------"
        print "zoom = " + str(zoom)
        print "tile_ul = " + str(tile_ul)
        print "tile_lr = " + str(tile_lr)
        print "tile_size = " + str(tile_size_m)
        print "tiles in x = " + str(tiles_count_x)
        print "tiles in y = " + str(tiles_count_y)
        print "tiles count = " + str(tiles_count)
        
        return tiling_data  
    
    def calculate_tile_bbox(self, x, y, tile_size):    
        """
        Calculating the tile coordinates from the tile size    
        """
        
        ul_x = self.origin_x + x * tile_size
        ul_y = self.origin_y - y * tile_size
        lr_x = ul_x + tile_size
        lr_y = ul_y - tile_size
        return [[ul_x, ul_y], [lr_x, lr_y]]
                   
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
               indent + indent + str(tile_bbox[0][0]) + ",\n" +
               indent + indent + str(tile_bbox[0][1]) + ",\n" +
               indent + indent + str(tile_bbox[1][0]) + ",\n" +
               indent + indent + str(tile_bbox[1][1]))
        print out
        return out
    
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
        logging.info("-------------------------------------")
        
    def log_tiling_data_info_x(self, x, tiling_data):
        out = self.print_tiling_data_info_x(x, tiling_data)
        logging.info(out)
        
    def log_tiling_data_info_y(self, x, y, tiling_data):
        out = self.print_tiling_data_info_y(x, y, tiling_data)
        logging.info(out)
        
    def log_tile_bbox_info(self, tile_bbox):
        out = self.print_tile_bbox_info(tile_bbox)
        logging.info(out)
        
class TileRendererSvg(TileRenderer, renderer.RendererSvg):
    '''
    classdocs
    '''
    
    def __init__(self, bbox, zoom_levels, tile_size, out_dir, map_style_id):
        self.bbox = bbox
        self.zoom_levels = zoom_levels
        self.tile_size = [tile_size, tile_size]
        self.out_dir = out_dir
        self.map_style_id = map_style_id
        self.type = "tiles_svg"        
        
class TileRendererGimp(TileRenderer, renderer.RendererGimp):
    """
    This subclass of tilerenderersvg implements different 'setup' and
    'draw_features' methods for the creation of GIMP tiles as PNG and (if 
    defined in the 'create_xcf' variable) as XCF files as well.
    """
    
    def __init__(self, 
                 bbox, zoom_levels, tile_size, out_dir, map_style_id, create_xcf):
        self.bbox = bbox
        self.zoom_levels = zoom_levels
        self.tile_size = [tile_size, tile_size]
        self.out_dir = out_dir
        self.map_style_id = map_style_id
        self.create_xcf = create_xcf
        self.type = "tiles_gimp"