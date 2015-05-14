'''
Created on May 13, 2015

@author: mucx
'''

import svgwrite

from gimpfu import *

from svgsketch import hachurizator

from renderer import Renderer
from tilerenderer import TileRenderer

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
        
    def draw(self, feature_styles, bbox, resolution, out_path = ""):

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
        
        mask = False
        
        self.create_image(image, parent, 
                          feature_styles, bbox, resolution, 
                          mask)
        
        self.conn_osm.close()
        
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
            
        pdb.gimp_image_delete(image)
        pdb.gimp_context_pop()
        
    def create_image(self, image, parent, 
                      feature_styles, bbox, resolution, 
                      mask):
        """
        Drawing the feature_styles as GIMP images and saving to PNG and/or XCF
        """
        
        # Creating a layer group for the feature type groups 
        group_line = pdb.gimp_layer_group_new(image)
        group_polygon = pdb.gimp_layer_group_new(image)
        
        pdb.gimp_image_insert_layer(image, group_line, parent, 0)
        pdb.gimp_image_insert_layer(image, group_polygon, parent, 1)  
        
        layer_pos_group = 0
        
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
        
class TileRendererGimp(TileRenderer, RendererGimp):
    """
    This subclass of tilerenderersvg implements different 'setup' and
    'draw_features' methods for the creation of GIMP tiles as PNG and (if 
    defined in the 'create_xcf' variable) as XCF files as well.
    """
    
    def __init__(self, 
                 bbox, zoom_levels, tile_size, out_dir, map_style_id, 
                 create_xcf):
        super(TileRendererGimp, self).__init__(bbox, zoom_levels, tile_size,
                                               out_dir, map_style_id, 
                                               "tiles_gimp")

        self.create_xcf = create_xcf
        
    def draw(self, feature_styles, bbox, resolution, out_path = ""):

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
        
        mask = False
        
        self.create_image(image, parent, 
                          feature_styles, bbox, resolution, 
                          mask)
        
        self.conn_osm.close()
        
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
            
                    
        pdb.gimp_image_delete(image)
        pdb.gimp_context_pop()