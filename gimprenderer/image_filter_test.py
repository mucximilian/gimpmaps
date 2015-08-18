#! /usr/bin/env python
from gimpfu import *
import os, inspect

from gimpmaps.gimpmodule import GimpImageManager

def run():
    
    filepath = os.path.dirname(
        os.path.abspath(
            inspect.getfile(
                inspect.currentframe()
            )
        )
    )
    
    resolution = [256,256]
    
    gimp = GimpImageManager()
    gimp.image_create(resolution)
    
    # Creating a parent layer group for all the layer (groups) added later
    parent = gimp.create_layer_group(None, 0)
    
    image = filepath + "/../../test/gimp/filter/tile2.png"
    
    layer = gimp.image_insert(resolution, image, parent, -10, -10)
    
    pdb.plug_in_oilify(gimp.image, layer, 10, 0)
    
    layer = pdb.gimp_image_flatten(gimp.image)
    
    gimp.image_save("tile2.png", layer, create_xcf = False)

register(
    "image_filter_test", 
    "", 
    "", 
    "Max Hartl", 
    "Max Hartl", 
    "2015",
    "<Toolbox>/Scripts/image_filter_test", "",
    [],
    [],
    run
)
main()