'''
Created on May 14, 2015

@author: mucx
'''

from gimpfu import *
import math
    
class GimpImageManager():
    def __init__(self):
        pass
    
    def insert_image_tiled(self, tile_size, resolution, tile, parent, pos):
        
        width = resolution[0]
        height = resolution[1]

        tiles_in_x = int(math.ceil(float(width)/float(tile_size)))
        tiles_in_y = int(math.ceil(float(height)/float(tile_size)))        
        
        tiles = self.create_layer_group(parent, pos)  
        
        for i in range(0, tiles_in_x):
            x = i * tile_size
            
            for j in range(0, tiles_in_y):
                y = j * tile_size
                
                layer = pdb.gimp_file_load_layer(self.image, tile)
                
                pdb.gimp_image_insert_layer(self.image, layer, tiles, -1)
                pdb.gimp_layer_set_offsets(layer, x , y)
        
        layer = pdb.gimp_layer_new_from_visible(self.image, self.image, "image")
        
    def create_image(self, resolution):
        
        image = pdb.gimp_image_new(
           resolution[0],
           resolution[1],
           RGB
        )
        self.image = image
        
    def create_layer(self, resolution, name, parent, pos):
        layer = pdb.gimp_layer_new(
            self.image, 
            resolution[0], 
            resolution[1],
            RGBA_IMAGE,
            name,
            100, 
            NORMAL_MODE
        )
        pdb.gimp_image_insert_layer(self.image, layer, parent, pos)
        
        # pdb.gimp_edit_fill(layer, BACKGROUND_FILL)
        
        return layer
        
    def create_layer_group(self, parent, pos):
        group = pdb.gimp_layer_group_new(self.image)
        pdb.gimp_image_insert_layer(self.image, group, parent, pos)
        
        return group
        
    def create_layer_image(self, parent, background_img, pos):
        
        layer = pdb.gimp_file_load_layer(self.image, background_img)
        pdb.gimp_image_insert_layer(self.image, layer, parent, pos)
        
    def reset_context(self):
        pdb.gimp_context_set_defaults()
        pdb.gimp_context_push()        
        pdb.gimp_context_set_background((255,255,255,255))
        
    def set_context(self, line_style):
        
        pdb.gimp_context_set_paint_method('gimp-paintbrush')
        pdb.gimp_context_pop()
        pdb.gimp_context_set_brush(line_style[0])
        pdb.gimp_context_set_brush_size(line_style[1])
        pdb.gimp_context_set_dynamics(line_style[3])
        pdb.gimp_context_set_foreground((
            line_style[2][0],
            line_style[2][1],
            line_style[2][2]                
        ))
        # pdb.gimp_context_set_opacity(line_style[3]) # Not working...?
        pdb.gimp_context_push()
        
    def draw_vectors(self, layer):
        for vector in self.image.vectors:
            pdb.gimp_edit_stroke_vectors(layer, vector)                    
            pdb.gimp_image_remove_vectors(self.image, vector)
            
    def simplify_selection(self):
        # Grow and shrink selection to even out small selections
        # Not used for rendering, test only
        pdb.gimp_selection_shrink(self.image, 2)
        pdb.gimp_selection_grow(self.image, 2)
        pdb.gimp_selection_grow(self.image, 2)
        pdb.gimp_selection_shrink(self.image, 2)
        
    def save_image(self, out_path, drawable, create_png, create_xcf):

        if not create_png and not create_xcf:
            print "Nothing to save..."
        else:
            if (create_png):
                out_path += ".png"
                pdb.gimp_file_save(
                    self.image, 
                    drawable,
                    out_path,
                    out_path
                )
            
            if (create_xcf):            
                out_path += ".xcf"
                pdb.gimp_file_save(
                    self.image, 
                    drawable,
                    out_path,
                    out_path
                )
            
    def close_image(self):
        
        pdb.gimp_image_delete(self.image)
        pdb.gimp_context_pop()
        
    def create_gimp_image(self, resolution, out_path, create_png, create_xcf):
        
        self.create_image(resolution)        
        
        layer = self.create_layer(resolution, "layer", None, 0)
        
        self.save_image(out_path, layer, create_png, create_xcf)
        
    def import_vectors(self, svg_path_str):
        pdb.gimp_vectors_import_from_string(
            self.image, 
            svg_path_str, 
            -1, 1, 1,
        )
        
    def select_vectors(self):
        for vector in self.image.vectors:
            pdb.gimp_image_select_item(self.image, CHANNEL_OP_ADD, vector)                        
            pdb.gimp_image_remove_vectors(self.image, vector)
            
    def apply_vectors_as_mask(self, mask_image, group_polygon,
                              resolution, layer_name):
        # Creating a layer group for vector and raster layers
        vector_raster_group = self.create_layer_group(group_polygon, 0)
        
        # Creating vector layer
        layer_vector = self.create_layer(resolution, layer_name,
                                         vector_raster_group, 0) 
        
        # Adding background image to use the mask on
        layer_mask_image = pdb.gimp_file_load_layer(self.image, mask_image)
        pdb.gimp_image_insert_layer(self.image, layer_mask_image, 
                                    vector_raster_group, 1)
        
        # TO DO: Check why duplicate for loop?
        # Drawing and selecting vectors in GIMP layer
        for vector in self.image.vectors:
            pdb.gimp_edit_stroke_vectors(layer_vector, vector)                   
            
        # Selecting vectors in GIMP layer
        self.select_vectors(self.image)
        
        # Apply mask of collected vectors on background image
        mask = pdb.gimp_layer_create_mask(layer_mask_image, 4)
        pdb.gimp_layer_add_mask(layer_mask_image, mask)
        
        pdb.gimp_selection_clear(self.image)