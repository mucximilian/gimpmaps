#! /usr/bin/env python
from gimpfu import *

from GimpTiles.TileRendererGimp import TileRendererGimp

def run():
	zoom_min = 12
	zoom_max = 13

	zoom_levels = range(zoom_min,zoom_max+1) # last number is excluded

	bbox_ul = [1275000, 6131500]
	bbox_lr = [1289700, 6118200]

	bbox = [bbox_ul, bbox_lr]

	tile_size = 256

	out_dir = ( "/media/data/daten/studium/master/module/master_thesis/data" 
                + "/rendering/results/20150413/")

	tile_renderer = TileRendererGimp(
		bbox, 
		zoom_levels,
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
	"<Toolbox>/Scripts/StrokePgsvgTiles", "",
	[],
	[],
	run
	)
main()