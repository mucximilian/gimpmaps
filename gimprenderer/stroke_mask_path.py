#! /usr/bin/env python
from gimpfu import *
import os
import datetime

path_1 = '<path d="M 30 30 l 50 -5 5 40 -30 10 z"/>'
path_2 = '<path d="M 150 120 l 50 -10 5 50 -40 10 z"/>'
path_3 = '<path d="M 93 180 l 1 -9 2 -5 2 -5 2 -6 1 -0 2 1 3 1 -0 1 0 0 4 0 0 0 0 7 4 -0 0 0 3 -1 1 3 -4 1 0 2 -0 2 -0 4 -1 6 -12 -1 z"/>'
path_4 = '<path d="M 118 245 L 120 244 120 244 121 244 123 243 124 243 131 242 131 243 131 243 131 245 133 245 133 245 133 245 133 244 132 244 133 244 133 244 133 244 133 243 133 243 134 244 135 244 135 244 134 244 133 243 134 242 134 242 135 241 135 248 133 248 133 248 133 249 133 251 121 253 121 253 120 253 120 253 120 253 119 252 119 247 Z M 119 249 L 119 249 125 248 125 248 124 248 124 247 120 248 120 249 Z M 121 244 L 121 247 124 246 124 247 124 247 124 246 124 246 124 245 123 245 123 244 Z"/>'
path_5 = '<path d="M -30 -30 L 30 -10 20 20 -20 10 z"/>'

def run():
    
    # Setting up the image and a layer group
    width = 256
    height = 256
    image = pdb.gimp_image_new(width, height, RGB)
    pdb.gimp_context_set_background((255,255,255,255))
    parent = pdb.gimp_layer_group_new(image)
    pdb.gimp_image_insert_layer(image, parent, None, 0)
    
    # Adding layer to stroke a vector path into
    stroke_layer = pdb.gimp_layer_new(
        image,
        width,
        height,
        RGBA_IMAGE,
        "stroke_layer",
        100,
        NORMAL_MODE
    )
    pdb.gimp_image_insert_layer(image, stroke_layer, parent, 0)
    
    # Adding a background image layer
    out_dir = os.getcwd()
    mask_layer = pdb.gimp_file_load_layer(image, out_dir + 
                                       "/img/hachure_grey_08.png")
    pdb.gimp_image_insert_layer(image, mask_layer, parent, 1)

    # Adding vectors
    pdb.gimp_vectors_import_from_string(image,
        path_5,
        -1, 1, 1, )
    pdb.gimp_vectors_import_from_string(image,
        path_2,
        -1, 1, 1, )
    pdb.gimp_vectors_import_from_string(image,
        path_4,
        -1, 1, 1, )
    
    # Set stroking style context
    pdb.gimp_context_set_brush("GIMP Brush #7")
    pdb.gimp_context_set_brush_size(12)
    pdb.gimp_context_set_dynamics("Det3")
    pdb.gimp_context_set_foreground((0, 123, 234, 255))
    pdb.gimp_context_push()

    print "vectors=" + str(len(image.vectors))
    # Stroking
    for vector in image.vectors:
        
        print "stroking vector"
        pdb.gimp_edit_stroke_vectors(stroke_layer, vector)
        
    for vector in image.vectors:
        
        print "selecting vector"        
        pdb.gimp_image_select_item(image, CHANNEL_OP_ADD, vector)
    
    mask = pdb.gimp_layer_create_mask(mask_layer, 4)
    pdb.gimp_layer_add_mask(mask_layer, mask)
    
    pdb.gimp_selection_clear(image)
    
    # Background
    background = pdb.gimp_layer_new(                    
        image, 256, 256,
        RGBA_IMAGE, "background", 100, NORMAL_MODE
    )    
    pdb.gimp_image_insert_layer(image, background,
                                parent, 2)
    
    pdb.gimp_edit_fill(background, BACKGROUND_FILL)

    # Saving
    print "saving..."
    out_dir = os.getcwd()
    out_time = datetime.datetime.now()
    date_str = out_time.strftime('%Y%m%d_%H%M')
    out_file = "/stroke_mask_path_test_" + date_str
    out_path = out_dir + out_file
    out_path_xcf = out_path + ".xcf"
    print "file: " + out_path_xcf
    pdb.gimp_xcf_save(
        0,
        image,
        parent,
        out_path_xcf,
        out_path_xcf
    )

register(
    "stroke_mask_path", 
    "", 
    "", 
    "Max Hartl", 
    "Max Hartl", 
    "2015",
    "<Toolbox>/Scripts/StrokeMaskPath", "",
    [],
    [],
    run
)
main()