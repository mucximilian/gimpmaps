#! /usr/bin/env python
from gimpfu import *
import os
import math

def run():
    
    # Setting up the image and a layer group
    width = 600
    height = 600
    image = pdb.gimp_image_new(width, height, RGB)
    
    pdb.gimp_context_set_background((255,255,255,255))

    # Adding a background image layer
    img = "gimpmaps/img/texture_blackboard.png"
    
    tile_size = 256
    
    tiles_in_x = int(math.ceil(float(width)/float(tile_size)))
    tiles_in_y = int(math.ceil(float(height)/float(tile_size)))
    
    background = pdb.gimp_layer_group_new(image)
    pdb.gimp_image_insert_layer(image, background, None, -1)    
    
    for i in range(0, tiles_in_x):
        x = i * tile_size
        for j in range(0, tiles_in_y):
            y = j * tile_size
            layer = pdb.gimp_file_load_layer(image, img)
            pdb.gimp_image_insert_layer(image, layer, background, -1)
            pdb.gimp_layer_set_offsets(layer, x , y)
    
    layer = pdb.gimp_layer_new_from_visible(image, image, "layer")
    # pdb.gimp_image_insert_layer(image, layer, None, -1)

    # Saving
    print "saving..."
    out_file = os.getcwd() + "/gimpmaps/results/test/background_tile.xcf"
    print "file: " + out_file

    pdb.gimp_file_save(
        image, 
        layer,
        out_file,
        out_file
    )

register(
    "background_tile", 
    "", 
    "", 
    "Max Hartl", 
    "Max Hartl", 
    "2015",
    "<Toolbox>/Scripts/BackgroundTile", "",
    [],
    [],
    run
)
main()