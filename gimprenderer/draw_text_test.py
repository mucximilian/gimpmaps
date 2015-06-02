#! /usr/bin/env python
from gimpfu import *
from gimpmaps import gimpmodule, styles

def run():
    
    resolution = [600, 600]
    
    gimp = gimpmodule.GimpImageManager()
    gimp.create_image(resolution)
    
    text_points = [
                   ["Blabla", [50, -10]],
                   ["Hello World", [130, 150]],
                   ["Foooooooooooooooo", [400, 400]]
                ]
    
    
    style_text = styles.StyleObjectText(
                    3,
                    ["osm_tags"],
                    1,
                    "2. Hardness 075",
                    4,
                    [100,100,100],
                    "Det3",
                    "Arial",
                    32,
                    [200,200,200],
                    "text"
                )
    
    # Creating a parent layer group for all the layer (groups) added later
    parent = gimp.create_layer_group(None, 0)
    
    bg_image = "gimpmaps/styles/chalk/img/texture_blackboard.png"
    gimp.insert_image_tiled(256, resolution, bg_image, parent, -1)
    
    # Resetting GIMP image context
    gimp.reset_context()  
    
    group_polygon_text = gimp.create_layer_group(parent, -1)
        
    gimp.draw_labels(
        group_polygon_text,
        text_points, style_text,
        resolution
    )
        
    gimp.save_image("gimpmaps/results/draw_text_test", parent, True, True)
        
    gimp.close_image()

register(
    "draw_text_test", 
    "", 
    "", 
    "Max Hartl", 
    "Max Hartl", 
    "2015",
    "<Toolbox>/Scripts/DrawTextTest", "",
    [],
    [],
    run
    )
main()