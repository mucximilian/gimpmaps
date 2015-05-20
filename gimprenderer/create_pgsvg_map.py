#! /usr/bin/env python

from gimpfu import *

from gimpmaps import gimprenderer

"""
Run this file from the bash script provided in the directory above.
"""

def run(ul_x, ul_y, lr_x, lr_y, 
        scale,
        map_style_file,
        create_xcf):
    
    bbox = [[ul_x, ul_y], [lr_x, lr_y]]
    
    gimp_renderer = gimprenderer.RendererGimp(
		bbox, 
		scale,
		None, # out_dir undefined, default used
        map_style_file,
        create_xcf
    )
    
    gimp_renderer.render()

register(
	"create_pgsvg_map", 
	"Creating map tiles from an OpenStreetMap PostGIS database", 
	"Creating map tiles from an OpenStreetMap PostGIS database", 
	"Maximilian Hartl", 
	"Maximilian Hartl", 
	"2015",
	"<Toolbox>/Scripts/CreatePgsvgMap", 
    "",
	[
        (PF_INT32, "ul_x", "Upper Left X", 0),
        (PF_INT32, "ul_y", "Upper Left Y", 0),  
        (PF_INT32, "lr_x", "Lower Right X", 0),  
        (PF_INT32, "lr_y", "Lower Right Y", 0),
        (PF_INT, "scale", "Image width", 10000),
        (PF_STRING, "style_file", "Map Style File", 0),  
        (PF_BOOL, "create_xcf", "Create XCFs", False)
    ],
	[],
	run
	)
main()