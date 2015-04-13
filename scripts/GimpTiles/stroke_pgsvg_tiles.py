#! /usr/bin/env python
from gimpfu import *

from PgsvgTiles.TileRendererGimp import TileRendererGimp

def run():
	zoom_min = 12
	zoom_max = 15

	zoom_levels = range(zoom_min,zoom_max+1) # last number is excluded

	bbox_ul = [1275000, 6131500]
	bbox_lr = [1289700, 6118200]

	bbox = [bbox_ul, bbox_lr]

	tile_size = 256
	# Brush Settings
	# Brush size is needed to calculate the tile buffer (half of size)
	# Should be an even number for better calculcation results
	brush_size = 8
	brush = "GIMP Brush #7"
	#brush_dynamics = "Dynamics Off"
	brush_dynamics = "Det1"

	brush_settings = [brush, brush_size, brush_dynamics]

	print brush_settings

	out_dir = ( "/media/data/daten/studium/master/module/master_thesis/data" 
                + "/rendering/results/")

	tile_renderer = TileRendererGimp(
		bbox, 
		zoom_levels,
		brush_settings,
		tile_size,
		out_dir
	)

register(
	"stroke_pgsvg_tiles", 
	"", 
	"", 
	"Max Hartl", 
	"Max Hartl", 
	"2015",
	"<Toolbox>/Scripts/StrokePostGISSvgTiles", "",
	[],
	[],
	run
	)
main()