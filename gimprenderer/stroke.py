#! /usr/bin/env python
from gimpfu import *
import os

import datetime
import math


origin_x = -(2 * math.pi * 6378137 / 2.0)
origin_y = 2 * math.pi * 6378137 / 2.0

def run():
	"""Stroke SVG Paths"""
	
	width = 256
	height = 256
	image = pdb.gimp_image_new(width, height, RGB)

	parent = pdb.gimp_layer_group_new(image)
	pdb.gimp_image_insert_layer(image, parent, None, 0)         

	layer = pdb.gimp_layer_new(image, width, height, RGBA_IMAGE,
		"layer", 50, NORMAL_MODE)
	pdb.gimp_image_insert_layer(image, layer, parent, 0)

	############################################################################
	# Brush Settings
	pdb.gimp_context_set_paint_method('gimp-paintbrush')
	pdb.gimp_context_set_brush("GIMP Brush #7")
	pdb.gimp_context_set_dynamics("Fade Script")
	pdb.gimp_context_set_brush_size(16)
	pdb.gimp_context_set_foreground((128,0,128,50))
	pdb.gimp_context_set_background((255,255,255,100))

	pdb.gimp_context_push()

	pdb.gimp_paintbrush(layer,150,4,[10, 10, 200, 10],0,10)
	pdb.gimp_paintbrush(layer,10,6,[10, 50, 50, 60, 200, 40],0,0)
		
	# Background
	background = pdb.gimp_layer_new(                    
        image, 256, 256,
        RGBA_IMAGE, "background", 100, NORMAL_MODE
    )    
	pdb.gimp_image_insert_layer(image, background,
                                parent, 1)    
	pdb.gimp_edit_fill(background, BACKGROUND_FILL)

	out_file = os.getcwd() + "/gimpmaps/results/test/stroke_test.png"
	print "saving..."
	print out_file
	
	pdb.file_png_save_defaults(
		image, 
		parent,
		out_file,
		out_file
	)

register(
	"stroke_test", 
	"", 
	"", 
	"Max Hartl", 
	"Max Hartl", 
	"2015",
	"<Toolbox>/Scripts/StrokeTest", "",
	[],
	[],
	run
	)
main()