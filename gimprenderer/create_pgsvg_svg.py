#! /usr/bin/env python

from gimpfu import *

from gimpmaps.renderersvgxcf import MapRendererSvgXcf

"""
Run this file from the bash script provided in the directory above.
"""

def run(config_file):
    
    renderer = MapRendererSvgXcf(config_file)    
    renderer.render()

register(
	"create_pgsvg_svg", 
	"Creating map tiles from an OpenStreetMap PostGIS database", 
	"Creating map tiles from an OpenStreetMap PostGIS database", 
	"Maximilian Hartl", 
	"Maximilian Hartl", 
	"2015",
	"<Toolbox>/Scripts/CreatePgsvgSvg", 
    "",
	[
        (PF_STRING, "config_file", "Configuration file", 0)
    ],
	[],
	run
	)
main()