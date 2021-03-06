#! /usr/bin/env python

from gimpfu import *

from gimpmaps.renderergimp import TileRendererGimp

"""
Run this file from the bash script provided in the directory above.
"""

def run(config_file):
    
    tile_renderer = TileRendererGimp(config_file)    
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
