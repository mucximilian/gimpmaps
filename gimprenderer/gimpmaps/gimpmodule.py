'''
Created on May 14, 2015

@author: mucx
'''

from gimpfu import *
import math
    
class GimpImageManager():
    def __init__(self):
        pass
    
    def image_insert_tiled(self, resolution, image, parent, pos):
        
        # TO DO: Get tile_size from image
        tile_size = 256
        
        width = resolution[0]
        height = resolution[1]

        tiles_in_x = int(math.ceil(float(width)/float(tile_size)))
        tiles_in_y = int(math.ceil(float(height)/float(tile_size)))        
        
        tiles = self.create_layer_group(parent, pos)
        
        layer_count = 0
        
        for i in range(0, tiles_in_x):
            x = i * tile_size
            
            for j in range(0, tiles_in_y):
                y = j * tile_size
                
                layer_image = pdb.gimp_file_load_layer(self.image, image)
                
                pdb.gimp_image_insert_layer(self.image, layer_image, tiles, -1)
                pdb.gimp_layer_set_offsets(layer_image, x , y)
                
                if layer_count > 0:
                    pdb.gimp_image_merge_down(self.image, layer_image,
                                              CLIP_TO_IMAGE)
                    
                layer_count += 1
                
        # Set layer id as variable to access it again for label mask
        self.background = self.get_active_layer()
        
        # TO DO:
        # PDB function merge layer group??
        # layer = pdb.gimp_layer_new_from_visible(self.image, self.image, "image")
        
    def image_insert(self, image, tile_part_x, tile_part_y, parent, pos):
        
        x_off = - tile_part_x * 256
        y_off = - tile_part_y * 256
        
        layer_image = pdb.gimp_file_load_layer(self.image, image)
                
        pdb.gimp_image_insert_layer(self.image, layer_image, parent, -1)
        pdb.gimp_layer_set_offsets(layer_image, x_off , y_off)
        
        pdb.gimp_layer_resize_to_image_size (layer_image)
        
        return layer_image
        
    def image_create(self, resolution):
        
        image = pdb.gimp_image_new(
           resolution[0],
           resolution[1],
           RGB
        )
        self.image = image
        
    def image_save(self, out_path, drawable, create_png = True, create_xcf = False):

        if not create_png and not create_xcf:
            print "Nothing to save..."
        else:
            if (create_png):
                out = out_path + ".png"
                pdb.gimp_file_save(
                    self.image, 
                    drawable,
                    out,
                    out
                )
            
            if (create_xcf):            
                out = out_path + ".xcf"
                pdb.gimp_file_save(
                    self.image, 
                    drawable,
                    out,
                    out
                )
            
    def image_close(self):
        
        pdb.gimp_image_delete(self.image)
        pdb.gimp_context_pop()
        
    def create_gimp_image(self, resolution, out_path, create_png, create_xcf):
        
        self.image_create(resolution)        
        
        layer = self.create_layer(resolution, "layer", None, 0)
        
        self.image_save(out_path, layer, create_png, create_xcf)
        
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
        
    def remove_layer(self, layer):
        pdb.gimp_image_remove_layer(self.image, layer)
        
    def get_active_layer(self):
        active_layer = pdb.gimp_image_get_active_layer(self.image)
        return active_layer
        
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
        
    def set_foreground(self, color):
        pdb.gimp_context_set_foreground((color[0],color[1],color[2],100))
        
    def draw_labels(self, group_polygon_text, text_points, style_text,
                   resolution):
        """
        This functions draws text labels (containing of a text and two 
        coordinates for the placement) in an image using the specified effect.
        
        The available effects are:
        
        text
        text_buffercolor
        text_buffermask
        text_outline
        text_outline_buffermask
        text_outline_buffercolor
        outline_text
        outline
        outline_buffercolor
        outline_buffermask
        """
        
        effect = style_text.effect
        
        print type(effect)
        print type(style_text.font)
        
        # Create text layer with 100 px buffer around original image
        # TO DO: Adding buffer as configuration parameter?
        img_buffer = 200
        resolution_new = [
            resolution[0] + img_buffer,
            resolution[0] + img_buffer
        ]
        
        # Draw buffer mask first (as label background)
        if (effect =="text_buffermask" or 
            effect == "text_outline_buffermask" or
            effect == "outline_buffermask"):
            
            self.draw_textbuffer_mask(
                group_polygon_text, 
                text_points, style_text,
                resolution
            )
        
        for text_point in text_points:
                    
            # Check if point is on the image as outliers crash selection 
            if (self.text_point_is_in_image(text_point, resolution)):     
    
                group_label = self.create_layer_group(group_polygon_text, -1)
                     
                line_style = style_text.get_line_style()
                text_style = style_text.get_text_style()
                               
                text_layer = self.create_layer(resolution_new, text_point[0], 
                                               group_label, -1)        
                pdb.gimp_layer_translate (text_layer, -100, -100)   
                
                if (effect == "text" or 
                    effect == "text_buffermask"):
                    
                    text = self.draw_text(text_point, text_style, text_layer)
                    
                    pdb.gimp_floating_sel_anchor(text)
                    
                elif(effect == "text_buffercolor"):
                    
                    text = self.draw_text(text_point, text_style, text_layer)
                    
                    self.draw_textbuffer_color(text, resolution, text_point, 
                                               group_label, style_text)
                    
                elif(effect == "text_outline" or
                    effect == "text_outline_buffermask"):
                    
                    text = self.draw_text(text_point, text_style, text_layer)
                
                    self.draw_text_outline(text, resolution_new, group_label, 
                                           line_style, text_point[0])
                    
                    pdb.gimp_floating_sel_anchor(text)
                    
                elif(effect == "outline_text"):
                    
                    text = self.draw_text(text_point, text_style, text_layer)
                
                    self.draw_text_outline(text, resolution_new, group_label, 
                                           line_style, text_point[0])
                    
                    pdb.gimp_image_raise_item(self.image, text_layer)
                    
                    pdb.gimp_floating_sel_anchor(text)
                    
                elif(effect == "text_outline_buffercolor"):
                    
                    text = self.draw_text(text_point, text_style, text_layer)
                    
                    self.draw_textbuffer_color(text, resolution, text_point,
                                               group_label, style_text)
                    
                    self.draw_text_outline(text, resolution, group_label, 
                                           line_style, text_point[0])
                    
                    pdb.gimp_floating_sel_anchor(text)
                    
                elif(effect == "outline" or
                     effect == "outline_buffermask"):
                    
                    text = self.draw_text(text_point, text_style, text_layer)
                
                    self.draw_text_outline(text, resolution, group_label,
                                           line_style, text_point[0])
                    
                    self.remove_layer(text_layer)
                
                elif(effect == "outline_buffercolor"):
                    
                    text = self.draw_text(text_point, text_style, text_layer)
                
                    self.draw_text_outline(text, resolution, group_label, 
                                           line_style, text_point[0])
                    
                    self.draw_textbuffer_color(text, resolution, text_point, 
                                               group_label, style_text)
                    
                    self.remove_layer(text_layer)
                    
    def text_point_is_in_image(self, point, resolution):
        """
        Function to check whether a point is on the image canvas or not.
        Points lying completely outside the image canvas crash the selction
        resulting e.g. in a image entirely filled with the buffer color.
        """
        
        if (point[1][0] >= 0 and point[1][0] <= resolution[0] and
            point[1][1] >= 0 and point[1][1] <= resolution[1]):
            
            return True
        else:
            return False
                
    def draw_text(self, text_point, text_style, text_layer):
        """
        Basic text rendering function. Draws the provided text into a layer and
        returns the text.
        """
        
        self.set_foreground(text_style[2])
        
        text = pdb.gimp_text_fontname(
            self.image,
            text_layer, # Drawable for floating sel or None for text
            text_point[1][0],
            text_point[1][1], # SVG x coordinates are flipped!
            text_point[0],
            0,
            True,
            text_style[1],
            UNIT_PIXEL,
            text_style[0]
        )
        
        return text
    
    def draw_textbuffer_color(self, text, resolution, text_point, 
                              group_text, style_text):
        """
        This function calculates a buffer around the text using the text 
        outline vectors and fills the buffer with color.
        """
        
        vectors = pdb.gimp_vectors_new_from_text_layer(self.image, text)    
        pdb.gimp_image_insert_vectors(self.image, vectors, None, 0)
        
        self.vectors_select()
        
        buffer_size = style_text.buffer_size
        buffer_color = style_text.buffer_color
        
        pdb.gimp_selection_grow(self.image, buffer_size)      
        
        text_layer_stroke = self.create_layer(
            resolution,
            "Buffer " + text_point[0],
            group_text,
            1
        )
        
        self.fill_selection(text_layer_stroke, buffer_color)
        
    def draw_textbuffer_mask(self, group_polygon_text, text_points,
                             style_text, resolution):
        """
        This function calculates a buffer around the text using the text 
        outline vectors and uses it as a mask on the background image.
        """
        
        group_label = self.create_layer_group(group_polygon_text, -1)
        
        text_style = style_text.get_text_style()
        
        buffer_size = style_text.buffer_size            
        
        for text_point in text_points:
            
            # Check if point is on the image as outliers crash selection 
            if (text_point[1][0] > 0 and text_point[1][1] > 0):
            
                text_layer = self.create_layer(resolution, text_point[0], 
                                           group_label, -1)            
                text = self.draw_text(text_point, text_style, text_layer)
            
                vectors = pdb.gimp_vectors_new_from_text_layer(self.image, text)    
                pdb.gimp_image_insert_vectors(self.image, vectors, None, 0)
                    
                self.remove_layer(text_layer)
            
        self.vectors_select()
                
        pdb.gimp_selection_grow(self.image, buffer_size)
        
        bg_copy = pdb.gimp_layer_copy(self.background, 1)
        
        pdb.gimp_image_insert_layer(self.image, bg_copy, group_label, -1)
                
        mask = pdb.gimp_layer_create_mask(bg_copy, 4)
        pdb.gimp_layer_add_mask(bg_copy, mask)
        
        pdb.gimp_selection_clear(self.image)
        
    def draw_text_outline(self, text, resolution_new, text_group, 
                          line_style, label):
        """
        This function calculates the text outline vectors and strokes them
        using a provided line style.
        """
        
        vectors = pdb.gimp_vectors_new_from_text_layer(self.image, text)    
        pdb.gimp_image_insert_vectors(self.image, vectors, None, 0)
        
        # pdb.gimp_floating_sel_anchor(text)        
        
        text_layer_stroke = self.create_layer(
            resolution_new,
            "Outline " + label,
            text_group,
            -1
        )
        
        self.set_context(line_style)    
        self.vectors_draw(text_layer_stroke)        
    
    def get_text_extent(self, text_point, text_style):
        """
        Calculating the bounds of a text label with provided style parameters.
        """
        extent = pdb.gimp_text_get_extents_fontname(
            text_point[0],
            text_style[1],
            UNIT_PIXEL,
            text_style[0]
        )
        return extent
    
    def fill_selection(self, layer, color):
        
        self.set_foreground(color)        
        pdb.gimp_edit_fill(layer, FOREGROUND_FILL)            
        pdb.gimp_selection_clear(self.image)
            
    def simplify_selection(self):
        """
        Grow and shrink selection to even out small selections
        Not used for rendering, test only
        """
        pdb.gimp_selection_shrink(self.image, 2)
        pdb.gimp_selection_grow(self.image, 2)
        pdb.gimp_selection_grow(self.image, 2)
        pdb.gimp_selection_shrink(self.image, 2)
        
    def vectors_import(self, svg_path_str):
        pdb.gimp_vectors_import_from_string(
            self.image, 
            svg_path_str, 
            -1, 1, 1,
        )
        
    def vectors_select(self):
        
        for vector in self.image.vectors:
            
            pdb.gimp_image_select_item(self.image, CHANNEL_OP_ADD, vector)                        
            pdb.gimp_image_remove_vectors(self.image, vector)
            
    def vectors_draw(self, layer):
        
        for vector in self.image.vectors:
                     
            pdb.gimp_edit_stroke_vectors(layer, vector)                    
            pdb.gimp_image_remove_vectors(self.image, vector)
            
    def vectors_as_mask(self, mask_image, parent,
                              resolution,
                              tile_part_x = 0, tile_part_y = 0):
        
        # Adding background image to use the mask on
        layer_image = self.image_insert(mask_image,
                                        tile_part_x, tile_part_y, 
                                        parent, 1)        
            
        # Selecting vectors in GIMP layer
        self.vectors_select()
        
        # Apply mask of collected vectors on background image
        mask = pdb.gimp_layer_create_mask(layer_image, 4)
        pdb.gimp_layer_add_mask(layer_image, mask)
        
        pdb.gimp_selection_clear(self.image)