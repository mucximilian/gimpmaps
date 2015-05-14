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
        
        # Create GIMP image with layer group
        image = self.create_image(resolution)
        
        # Resetting GIMP image context
        self.reset_context()
        
        # Creating a parent layer group for all the layer (groups) added later
        parent = self.create_layer_group(image, None, 0)
        
        self.draw_features(image, parent, 
                          feature_styles, bbox, resolution, 
                          False)
    
        self.draw_text()
        # Background image
        # TO DO: Get background from style database
        self.create_layer_image(image, parent, "texture_blackboard.png", 2)           
                      
        # Save images as PNG and XCF
        self.save_image(out_path, image, parent, True, self.create_xcf)
        
        self.close_image(image)
        
    def draw_features(self, image, parent, 
                      feature_styles, bbox, resolution, 
                      mask):
        """
        Drawing the feature_styles as GIMP images and saving to PNG and/or XCF
        """
        
        self.conn_osm = self.connect_to_osm_db()
        
        # Creating layer groups for the feature type groups 
        group_line = self.create_layer_group(image, parent, 0)        
        group_polygon = self.create_layer_group(image, parent, 1)
        
        layer_pos_group = 0
        
        for feature_style in feature_styles:
                        
            sql_selection = feature_style.get_selection_tags()
            line_style = feature_style.get_line_style()
            
            # Style settings
            # TO DO: emulate brush dynamics?????
            self.set_context(line_style)
            
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
                layer = self.create_layer(image, resolution, 
                                          sql_selection, group_line, 
                                          layer_pos_group)  
                
                # Drawing vectors into GIMP layer
                self.draw_vectors(image, layer)
            
            # Drawing polygon feature_styles
            elif (feature_style.geom_type == 3):
                
                if (mask):
                
                    # Creating a layer group for vector and raster layers
                    vector_raster_group = self.create_layer_group(image, 
                                                                  group_polygon,
                                                                  0)
                    
                    # Creating vector layer
                    layer_vector = self.create_layer(self, image, resolution, 
                                                     sql_selection,
                                                     vector_raster_group, 0) 
                    
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
                    
                    # Apply mask of collected vectors on background image
                    mask = pdb.gimp_layer_create_mask(layer_mask_image, 4)
                    pdb.gimp_layer_add_mask(layer_mask_image, mask)
                    
                    pdb.gimp_selection_clear(image)
                    
                else :
                    
                    # Creating image layer for geometry feature
                    layer = self.create_layer(image, resolution, sql_selection,
                                              group_line, layer_pos_group) 
                    
                    # Drawing vectors into GIMP layer
                    self.draw_vectors(image, layer)             
            
            # Incrementing current layer position
            layer_pos_group =+ layer_pos_group + 1
            
        self.conn_osm.close()
            
    def draw_text(self):
        print "bla"
        
    def create_image(self, resolution):
        
        image = pdb.gimp_image_new(
           resolution[0],
           resolution[1],
           RGB
        )
        return image
        
    def create_layer(self, image, resolution, name, parent, pos):
        layer = pdb.gimp_layer_new(
            image, 
            resolution[0], 
            resolution[1],
            RGBA_IMAGE,
            name,
            100, 
            NORMAL_MODE
        )
        pdb.gimp_image_insert_layer(image, layer, parent, pos)
        
        # pdb.gimp_edit_fill(layer, BACKGROUND_FILL)
        
        return layer
        
    def create_layer_group(self, image, parent, pos):
        group = pdb.gimp_layer_group_new(image)
        pdb.gimp_image_insert_layer(image, group, parent, pos)
        
        return group
        
    def create_layer_image(self, image, parent, background_img, pos):
        
        background = self.img_dir + background_img
        
        layer = pdb.gimp_file_load_layer(image, background)
        pdb.gimp_image_insert_layer(image, layer, parent, pos)
        
        return background
        
    def reset_context(self):
        pdb.gimp_context_set_defaults()
        pdb.gimp_context_push()        
        pdb.gimp_context_set_background((255,255,255,255))
        
    def set_context(self, line_style):
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
        
    def draw_vectors(self, image, layer):
        for vector in image.vectors:
            pdb.gimp_edit_stroke_vectors(layer, vector)                    
            pdb.gimp_image_remove_vectors(image, vector)
            
    def simplify_selection(self, image):
        # Grow and shrink selection to even out small selections
        pdb.gimp_selection_shrink(image, 2)
        pdb.gimp_selection_grow(image, 2)
        pdb.gimp_selection_grow(image, 2)
        pdb.gimp_selection_shrink(image, 2)
        
    def save_image(self, out_path, image, drawable, create_png, create_xcf):

        if not create_png and not create_xcf:
            print "Nothing to save"
        else:
            if (create_png):
                out_path += ".png"
                pdb.gimp_file_save(
                    image, 
                    drawable,
                    out_path,
                    out_path
                )
            
            if (create_xcf):            
                out_path += ".xcf"
                pdb.gimp_file_save(
                    image, 
                    drawable,
                    out_path,
                    out_path
                )
            
    def close_image(self, image):
        
        pdb.gimp_image_delete(image)
        pdb.gimp_context_pop()
        
    def create_gimp_image(self, resolution, out_path, create_png, create_xcf):
        
        image = self.create_image(resolution)        
        
        layer = self.create_layer(image, resolution, "layer", None, 0)
        
        self.save_image(out_path, image, layer, create_png, create_xcf)
        
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
        
        # Create GIMP image with layer group
        image = self.create_image(resolution)
        
        # Resetting GIMP image context
        self.reset_context()
        
        # Creating a parent layer group for all the layer (groups) added later
        parent = self.create_layer_group(image, None, 0)
        
        self.draw_features(image, parent, 
                          feature_styles, bbox, resolution, 
                          False)
    
        # Background image
        # TO DO: Get background from style database
        self.create_layer_image(image, parent, "texture_blackboard.png", 2)           
                      
        # Save images as PNG and XCF
        self.save_image(out_path, image, parent, True, self.create_xcf)
        
        self.close_image(image)