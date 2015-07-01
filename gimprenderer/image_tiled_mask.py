#! /usr/bin/env python
from gimpfu import *

from gimpmaps.gimpmodule import GimpImageManager

path_1 = '<path d="M 30 30 L 220 30 230 210 20 240 Z"/>'

def run():
    
    gimp = GimpImageManager()
    gimp.image_create([256,256])
    
    # Creating a parent layer group for all the layer (groups) added later
    parent = gimp.create_layer_group(None, 0)
    
    image = "test_tile.png"
    
    gimp.vectors_import(path_1)
    
    gimp.vectors_as_mask(image, parent, [256,256], 1, 1)
    
    gimp.image_save("test.png", parent, create_xcf = True)

register(
    "image_tiled_mask", 
    "", 
    "", 
    "Max Hartl", 
    "Max Hartl", 
    "2015",
    "<Toolbox>/Scripts/image_tiled_maskd", "",
    [],
    [],
    run
)
main()