#! /usr/bin/env python
import os
from gimpfu import *

from tiles import tilerenderergimp

def run():
    zoom_min = 12
    zoom_max = 13

    zoom_levels = range(zoom_min,zoom_max+1) # last number is excluded

    # Defining bounds of selection to render
    bbox_ul = [1275000, 6131500]
    bbox_lr = [1289700, 6118200]
    
#     bbox_ul = [1250000, 6160000]
#     bbox_lr = [1310000, 6080000]
    
    bbox = [bbox_ul, bbox_lr]

    # Defining the pixel size of the output map tiles
    tile_size = 256
 
    out_dir = os.getcwd() + "/results/"
    create_xcf = True

    tile_renderer = tilerenderergimp(
		bbox, 
		zoom_levels,
		tile_size,
		out_dir,
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