#! /usr/bin/env python

from gimpfu import *

from gimpmaps.renderergimp import TileRendererGimp, MapRendererGimp

"""
Run this file from the bash script provided in the directory above.
"""

def run(config_file, map_type):
    
    if map_type == "tiles":        
    
        tile_renderer = TileRendererGimp(config_file)    
        tile_renderer.render()
        
    elif map_type == "map":
        
        gimp_renderer = MapRendererGimp(config_file)    
        gimp_renderer.render()
        
    else:
        
        print "No valid map type provided" 


register(
	"create_gimpmap", 
	"Creating a map or tiles from an OpenStreetMap PostGIS database", 
	"Creating a map or tiles from an OpenStreetMap PostGIS database", 
	"Maximilian Hartl", 
	"Maximilian Hartl", 
	"2015",
	"<Toolbox>/Scripts/CreateGIMPmap", 
    "",
	[
        (PF_STRING, "config_file", "Configuration file", 0),
        (PF_STRING, "map_type", "Type of map to create ('tiles' or 'map')", 0)
    ],
	[],
	run
	)
main()
