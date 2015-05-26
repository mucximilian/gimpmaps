'''
Created on May 13, 2015

@author: mucx
'''

import svgwrite
from gimpfu import *
from abc import ABCMeta, abstractmethod

from svgsketch import hachurizer

from gimpmaps.renderermap import MapRenderer
from tilerenderer import TileRenderer
from gimpmodule import GimpImageManager

class RendererGimp(object):
    '''
    A renderer to create a single PNG map. An editable GIMP XCF file can be 
    created along with the PNG result.
    '''
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self):
        '''
        Constructor
        '''
        
        pass
    
    def draw_features_line(
            self, gimp, parent, line_styles, bbox, resolution
        ):
        """
        Drawing the line features as GIMP images and saving to PNG and/or XCF
        """
        
        self.conn_osm = self.connect_to_osm_db()
        
        # Creating layer groups for the feature type groups 
        group_line = gimp.create_layer_group(parent, -1)        

        for style_line in line_styles:
                        
            sql_selection = style_line.get_selection_tags()
            line_style = style_line.get_line_style()
            
            # Style settings
            # TO DO: emulate brush dynamics?????
            gimp.set_context(line_style)

            # Import SVG data into SVG drawing from database
            svg_geoms = self.get_svg_features(
                bbox,
                resolution, 
                style_line
            )
            
            for svg_commands in svg_geoms:
                         
                svg_path = svgwrite.path.Path(svg_commands)
                svg_path_str = svg_path.tostring()
                
                # Adding vectors for stroking of lines, outlines/mask
                gimp.import_vectors(svg_path_str)
        
            # Creating image layer for geometry feature
            layer = gimp.create_layer(resolution, 
                                      sql_selection, group_line, 
                                      0)  
            
            # Drawing vectors into GIMP layer
            gimp.draw_vectors(layer)
            
        self.conn_osm.close()
        
    def draw_features_polygon(
            self, gimp, parent, polygon_styles, bbox, resolution, mask
        ):
        """
        Drawing the geometry features as GIMP images and saving to PNG and/or XCF
        """
        
        self.conn_osm = self.connect_to_osm_db()
        
        # Creating layer groups for the feature type groups       
        group_polygon = gimp.create_layer_group(parent, -1)

        for style_polygon in polygon_styles:
            
            sql_selection = style_polygon.get_selection_tags()
            line_style = style_polygon.get_line_style()
            
            # Style settings
            # TO DO: emulate brush dynamics?????
            gimp.set_context(line_style)
            
            # TO DO: Import from style
            spacing = 10
            angle = 30
            
            # Import SVG data into SVG drawing from database
            svg_geoms = self.get_svg_features(
                bbox,
                resolution, 
                style_polygon
            )
            for svg_commands in svg_geoms:
                
                svg_path = svgwrite.path.Path(svg_commands)
                svg_path_str = svg_path.tostring()
        
                # Import vectors to GIMP image
                if (mask):                    
                    # Adding vectors for stroking of lines, outlines/mask
                    gimp.import_vectors(svg_path_str)
                else:
                    # Creating hachure vectors
                    # TO DO: Adding outlines
                    svg_renderer = hachurizer.Hachurizer(spacing, angle)                    

                    hachure = svg_renderer.get_svg_hachure(svg_path)
                    if (hachure is not None):                   
                        gimp.import_vectors(hachure)
                    else:
                        continue
                    
            # Drawing polygon feature_styles                
            if (mask):
                # Adding background image to use the mask on
                # TO DO: Get img path from style file
                mask_image = "img/" + style_polygon.get_image_data()[0]
                gimp.apply_vectors_as_mask(
                    self, mask_image, group_polygon, resolution, sql_selection
                )
                            
            else :
                
                # Creating image layer for geometry feature
                layer = gimp.create_layer(resolution, sql_selection,
                                          group_polygon, 0) 
                
                # Drawing vectors into GIMP layer
                gimp.draw_vectors(layer)
            
        self.conn_osm.close()
        
    def draw_text(
            self, gimp, parent, text_styles, bbox, resolution, 
            draw_outline, draw_buffer
        ):
        
        self.conn_osm = self.connect_to_osm_db()
        
        # Creating layer groups for the feature type groups       
        group_polygon_text = gimp.create_layer_group(parent, -1)
        
        for style_text in text_styles:
            
            sql_selection = style_text.get_selection_tags()
            line_style = style_text.get_line_style()
            text_style = style_text.get_text_style()
            
            # Style settings
            # TO DO: emulate brush dynamics?????
            gimp.set_context(line_style)
                        
            # Import SVG data into SVG drawing from database
            text_points = self.get_text(
                bbox,
                resolution, 
                style_text
            )
            for text_point in text_points:
                
                group_text_point = gimp.create_layer_group(
                    group_polygon_text,
                    -1
                )
                
                text_layer = gimp.create_layer(resolution, 
                                      sql_selection, group_text_point, 
                                      -1)  
                
                gimp.set_foreground(text_style[2])
                
                gimp.draw_text(text_point, text_style)
                
       
class MapRendererGimp(MapRenderer, RendererGimp):
    '''
    A renderer to create a single PNG map. An editable GIMP XCF file can be 
    created along with the PNG result.
    '''
    
    def __init__(self, config_file):
        '''
        Constructor
        '''
        
        super(MapRendererGimp, self).__init__(config_file)
        
        self.type = "map_gimp"
        
    def draw(self, zoom, bbox, resolution, out_path):
               
        # Creating a GIMP Manager instance and an image
        gimp = GimpImageManager()
        gimp.create_image(resolution)
        
        # Resetting GIMP image context
        gimp.reset_context()
        
        # Creating a parent layer group for all the layer (groups) added later
        parent = gimp.create_layer_group(None, 0)
        
        # Background image
        bg_image = self.get_bg_img(zoom) 
        gimp.insert_image_tiled(256, resolution, bg_image, parent, -1)        
        
        # Drawing features
        feature_styles = self.get_feature_styles(zoom)
        
        ## Polygon features
        self.draw_features_polygon(
            gimp, parent, feature_styles["polygons"], bbox, resolution, False
        )
        
        ## Line features
        self.draw_features_line(
            gimp, parent, feature_styles["lines"], bbox, resolution
        )
        
        # Drawing the text
        text_styles = self.get_text_styles(zoom)
        self.draw_text(
            gimp, parent, text_styles, bbox, resolution, True, False
        )  
                      
        # Save images as PNG and XCF
        gimp.save_image(out_path, parent, True, self.create_xcf)
        
        gimp.close_image()
        
    
        
class TileRendererGimp(TileRenderer, RendererGimp):
    """
    This subclass of TileRenderer implements different 'setup' and
    'draw_features' methods for the creation of GIMP tiles as PNG and (if 
    defined in the 'create_xcf' variable) as XCF files as well.
    """
    
    def __init__(self, config_file):

        super(TileRendererGimp, self).__init__(config_file)
        
        self.type = "tiles_gimp"
        
    def draw(self, styles, bbox, resolution, out_path):   
        
        # Creating a GIMP Manager instance and an image
        gimp = GimpImageManager()
        gimp.create_image(resolution)
        
        # Resetting GIMP image context
        gimp.reset_context()
        
        # Creating a parent layer group for all the layer (groups) added later
        parent = gimp.create_layer_group(None, 0)
        
        # Background image
        bg_image = styles["background_img"]
        gimp.create_layer_image(parent, bg_image, -1)
        
        # Drawing polygon features
        self.draw_features_polygon(
            gimp, parent, styles["features"]["polygons"], bbox, resolution, False
        )  
        
        # Drawing line features
        self.draw_features_line(
            gimp, parent, styles["features"]["lines"], bbox, resolution
        )      
                      
        # Save images as PNG and XCF
        gimp.save_image(out_path, parent, True, self.create_xcf)
        
        gimp.close_image()