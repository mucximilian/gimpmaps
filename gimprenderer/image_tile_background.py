#! /usr/bin/env python
from gimpfu import *

from gimpmaps.gimpmodule import GimpImageManager

def run():
    
    resolution = [1200,1200]
    
    gimp = GimpImageManager()
    gimp.image_create(resolution)
    
    # Creating a parent layer group for all the layer (groups) added later
    parent = gimp.create_layer_group(None, 0)
    
    image = "buildings.png"
    
    gimp.image_insert_tiled(resolution, image, parent, -1)
    
    gimp.image_save("test.png", parent, create_xcf = True)

register(
    "image_tile_background", 
    "", 
    "", 
    "Max Hartl", 
    "Max Hartl", 
    "2015",
    "<Toolbox>/Scripts/image_tile_background", "",
    [],
    [],
    run
)
main()