#! /usr/bin/env python

from gimpfu import *

from gimpmaps import gimprenderer

"""
Run this file from the bash script provided in the directory above.
"""

def run(config_file):
    
    bbox = [[ul_x, ul_y], [lr_x, lr_y]]
    zoom_levels = range(zoom_min,zoom_max+1) # last number is excluded
    
    tile_renderer = gimprenderer.TileRendererGimp(config_file)    
    tile_renderer.render()

register(
	"create_pgsvg_tiles", 
	"Creating map tiles from an OpenStreetMap PostGIS database", 
	"Creating map tiles from an OpenStreetMap PostGIS database", 
	"Maximilian Hartl", 
	"Maximilian Hartl", 
	"2015",
	"<Toolbox>/Scripts/CreatePgsvgTiles", 
    "",
	[
        (PF_STRING, "config_file", "Configuration file", 0)
     ],
	[],
	run
	)
main()