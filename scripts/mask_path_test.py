#! /usr/bin/env python
from gimpfu import *
import os
import datetime

path_1 = '<path d="M 20 20 l 20 20 5 20 -30 0 z"/>'
path_2 = '<path d="M 100 100 l 30 10 1 10 -20 0 z"/>'
path_3 = '<path d="M 100 240 L 95 250 100 260 120 265 150 260 150 240 120 235 Z ' + 
    'M 120 250 L 124 250 124 246 122 244 120 248 Z"/>'

def run():
    
    # Setting up the image and a layer group
    width = 256
    height = 256
    image = pdb.gimp_image_new(width, height, RGB)
    pdb.gimp_context_set_background((255,255,255,255))
    parent = pdb.gimp_layer_group_new(image)
    pdb.gimp_image_insert_layer(image, parent, None, 0)         

    # Adding a background image layer
    out_dir = os.getcwd()
    layer_1 = pdb.gimp_file_load_layer(image, out_dir + "/img/hachure_grey_08.png")
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
        path_1,
        -1, 1, 1, )
    pdb.gimp_vectors_import_from_string(image,
        path_2,
        -1, 1, 1, )
    vectors = image.vectors
    print "vectors=" + str(len(vectors))

    # Stroking
    for vector in vectors:
        print "selecting vector"
        pdb.gimp_image_select_item(image, CHANNEL_OP_ADD, vector)
    
    mask = pdb.gimp_layer_create_mask(layer_1, 4)
    pdb.gimp_layer_add_mask(layer_1, mask)

    # Saving
    print "saving..."
    out_dir = os.getcwd()
    out_time = datetime.datetime.now()
    date_str = out_time.strftime('%Y%m%d_%H%M')
    out_file = "/mask_path_test_" + date_str
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