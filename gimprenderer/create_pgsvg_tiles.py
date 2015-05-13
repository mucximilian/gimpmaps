#! /usr/bin/env python

from gimpfu import *

from gimpmaps import gimprenderer

"""
Run this file from the bash script provided in the directory above.
"""

def run(zoom_min, zoom_max,
        ul_x, ul_y, lr_x, lr_y, 
        tile_size, map_style_id,
        create_xcf):
    
    bbox = [[ul_x, ul_y], [lr_x, lr_y]]
    zoom_levels = range(zoom_min,zoom_max+1) # last number is excluded
    
    tile_renderer = gimprenderer.TileRendererGimp(
		bbox, 
		zoom_levels,
		tile_size,
		None, # out_dir undefined, default used
        map_style_id,
        create_xcf
    )
    
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
        (PF_INT, "zoom_min", "Zoom Min", 0),
        (PF_INT, "zoom_max", "Zoom Min", 0),
        (PF_INT32, "ul_x", "Upper Left X", 0),
        (PF_INT32, "ul_y", "Upper Left Y", 0),  
        (PF_INT32, "lr_x", "Lower Right X", 0),  
        (PF_INT32, "lr_y", "Lower Right Y", 0),
        (PF_INT, "tile_size", "Tile Size", 256),  
        (PF_INT, "map_style_id", "Map Style ID", 0),  
        (PF_BOOL, "create_xcf", "Create XCFs", False)
     ],
	[],
	run
	)
main()