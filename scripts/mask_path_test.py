#! /usr/bin/env python
from gimpfu import *
import os
import datetime

def run():
    
    # Setting up the image and a layer group
    width = 256
    height = 256
    image = pdb.gimp_image_new(width, height, RGB)
    pdb.gimp_context_set_background((255,255,255,255))
    parent = pdb.gimp_layer_group_new(image)
    pdb.gimp_image_insert_layer(image, parent, None, 0)         

    # Adding a background image layer
    layer_1 = pdb.gimp_file_load_layer(image, "scripts/img/hachure1.png")
    pdb.gimp_image_insert_layer(image, layer_1, parent, 0)

    # Adding layer to stroke a vector path into
    layer_2 = pdb.gimp_layer_new(
        image,
        width,
        height,
        RGBA_IMAGE,
        "stroke_layer",
        100,
        NORMAL_MODE
    )
    pdb.gimp_image_insert_layer(image, layer_2, parent, -1)
    pdb.gimp_vectors_import_from_string(image,
        '<path d="M 100,100 120,50 170,150"/>',
        -1, 1, 1, )
    vectors = image.vectors
    print "vectors=" + str(len(vectors))

    # Stroke brush settings
    brush_size = 35
    brush = "GIMP Brush #7"
    brush_dynamics = "Det3"	
    pdb.gimp_context_set_brush(brush)
    pdb.gimp_context_set_dynamics(brush_dynamics)
    pdb.gimp_context_set_brush_size(brush_size)
    pdb.gimp_context_set_foreground((128,0,128,255))
    pdb.gimp_context_push()

    # Stroking
    for vector in vectors:
        print "stroking vector"
        pdb.gimp_edit_stroke_vectors(layer_2, vector)

    # Saving
    print "saving..."
    out_dir = os.getcwd()
    out_time = datetime.datetime.now()
    date_str = out_time.strftime('%Y%m%d_%H%M')
    out_file = "/mask_path_test_" + date_str + ".png"
    out_path = out_dir + out_file

    print "file: " + out_path

    pdb.file_png_save_defaults(
        image, 
        parent,
        out_path,
        out_path
    )

register(
    "mask_path_test", 
    "", 
    "", 
    "Max Hartl", 
    "Max Hartl", 
    "2015",
    "<Toolbox>/Scripts/MaskPathTest", "",
    [],
    [],
    run
)
main()