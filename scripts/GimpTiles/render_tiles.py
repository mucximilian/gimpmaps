# -*- coding: utf-8 -*-

from PgsvgTiles.TileRenderer import TileRenderer

zoom_min = 12
zoom_max = 14

zoom_levels = range(zoom_min,zoom_max+1) # last number is excluded

bbox_ul = [1275000, 6131500]
bbox_lr = [1289700, 6118200]

bbox = [bbox_ul, bbox_lr]

# This is needed to calculate the tile buffer which is brushsize/2
# Should be an even number for better calculcation results
brush_size = 12
tile_size = 256

out_dir = ( "/media/data/daten/studium/master/module/master_thesis/data" 
                + "/rendering/results/")

tile_renderer = TileRenderer(bbox, zoom_levels, brush_size, tile_size, out_dir)
