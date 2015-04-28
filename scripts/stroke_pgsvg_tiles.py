#! /usr/bin/env python
import os
from gimpfu import *

from GimpTiles.TileRendererGimp import TileRendererGimp

def run():
    zoom_min = 12
    zoom_max = 14

    zoom_levels = range(zoom_min,zoom_max+1) # last number is excluded

    # Defining bounds of selection to render
    bbox_ul = [1275000, 6131500]
    bbox_lr = [1289700, 6118200]
    bbox = [bbox_ul, bbox_lr]

    # Defining the pixel size of the output map tiles
    tile_size = 256
 
    out_dir = os.getcwd() + "/results/"

    tile_renderer = TileRendererGimp(
		bbox, 
		zoom_levels,
		tile_size,
		out_dir
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