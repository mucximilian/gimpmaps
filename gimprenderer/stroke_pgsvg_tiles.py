#! /usr/bin/env python
import inspect, os
from gimpfu import *

from gimpmaps.tiles import tilerenderergimp

"""
Run this file from the bash script provided in the directory above.
"""

def run():
    zoom_min = 12
    zoom_max = 12

    zoom_levels = range(zoom_min,zoom_max+1) # last number is excluded

    # Defining bounds of selection to render
    bbox_ul = [1275000, 6131500]
    bbox_lr = [1289700, 6118200]
    
#     bbox_ul = [1250000, 6160000]
#     bbox_lr = [1310000, 6080000]
    
    bbox = [bbox_ul, bbox_lr]

    # Defining the pixel size of the output map tiles
    tile_size = 256
       
    map_style = 1
    create_xcf = True
    
    tile_renderer = tilerenderergimp.TileRendererGimp(
		bbox, 
		zoom_levels,
		tile_size,
		None, # out_dir undefined, default used
        map_style,
        create_xcf
    )
    
    tile_renderer.render_tiles()

register(
	"stroke_pgsvg_tiles", 
	"Creating map tiles from an OpenStreetMap PostGIS database", 
	"Creating map tiles from an OpenStreetMap PostGIS database", 
	"Maximilian Hartl", 
	"Maximilian Hartl", 
	"April 2015",
	"<Toolbox>/Scripts/StrokePgsvg''Tiles", "",
	[],
	[],
	run
	)
main()