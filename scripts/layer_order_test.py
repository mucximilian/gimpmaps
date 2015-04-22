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
    
    group_1 = pdb.gimp_layer_group_new(image)
    group_2 = pdb.gimp_layer_group_new(image)
    
    pdb.gimp_image_insert_layer(image, group_1, None, 0)         
    pdb.gimp_image_insert_layer(image, group_2, None, 1)         

    # Adding layer layers
    layer_1 = pdb.gimp_layer_new(
        image,
        width,
        height,
        RGBA_IMAGE,
        "layer_1",
        100,
        NORMAL_MODE
    )
    pdb.gimp_image_insert_layer(image, layer_1, group_1, 0)
    
    layer_2 = pdb.gimp_layer_new(
        image,
        width,
        height,
        RGBA_IMAGE,
        "layer_2",
        100,
        NORMAL_MODE
    )
    pdb.gimp_image_insert_layer(image, layer_2, group_1, 1)
    
    layer_3 = pdb.gimp_layer_new(
        image,
        width,
        height,
        RGBA_IMAGE,
        "layer_3",
        100,
        NORMAL_MODE
    )
    pdb.gimp_image_insert_layer(image, layer_3, group_1, 2)
    
    layer_4 = pdb.gimp_layer_new(
        image,
        width,
        height,
        RGBA_IMAGE,
        "layer_4",
        100,
        NORMAL_MODE
    )
    pdb.gimp_image_insert_layer(image, layer_4, group_1, 3)
    
    layer_5 = pdb.gimp_layer_new(
        image,
        width,
        height,
        RGBA_IMAGE,
        "layer_5",
        100,
        NORMAL_MODE
    )
    pdb.gimp_image_insert_layer(image, layer_5, group_1, 4)
    
    layer_6 = pdb.gimp_layer_new(
        image,
        width,
        height,
        RGBA_IMAGE,
        "layer_6",
        100,
        NORMAL_MODE
    )
    pdb.gimp_image_insert_layer(image, layer_6, group_2, 0)
    
    layer_7 = pdb.gimp_layer_new(
        image,
        width,
        height,
        RGBA_IMAGE,
        "layer_7",
        100,
        NORMAL_MODE
    )
    pdb.gimp_image_insert_layer(image, layer_7, group_2, 1)
    
    layer_8 = pdb.gimp_layer_new(
        image,
        width,
        height,
        RGBA_IMAGE,
        "layer_8",
        100,
        NORMAL_MODE
    )
    pdb.gimp_image_insert_layer(image, layer_8, group_2, 2)


    # Saving
    print "saving..."
    
    out_dir = os.getcwd()
    
    out_time = datetime.datetime.now()
    date_str = out_time.strftime('%Y%m%d_%H%M')
    
    out_file = "/layer_order_" + date_str
    out_path = out_dir + out_file
    out_path_xcf = out_path + ".xcf"
    
    print "file: " + out_path_xcf
    
    pdb.gimp_xcf_save(
        0,
        image,
        image,
        out_path_xcf,
        out_path_xcf
    )

register(
    "layer_order_test", 
    "", 
    "", 
    "Max Hartl", 
    "Max Hartl", 
    "2015",
    "<Toolbox>/Scripts/LayerOrderTest", "",
    [],
    [],
    run
)
main()