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
		"layer", 100, NORMAL_MODE)
	pdb.gimp_image_insert_layer(image, layer, parent, 0)
	
	pdb.gimp_vectors_import_from_string(image,
		'<path d="M 100,100 L 120,50 170,150"/>',
		-1, 1, 1, )
	pdb.gimp_vectors_import_from_string(image,
		'<path d="M 0,100 L 20,100 70,120"/>',
		-1, 1, 1, )
	pdb.gimp_vectors_import_from_string(image,
		'<path d="M 50,230 L 200,230"/>',
		-1, 1, 1, )
	pdb.gimp_vectors_import_from_string(image,
		'<path d="M 50,200 L 200,200"/>',
		-1, 1, 1, )
	
	vectors = image.vectors

	print "vectors=" + str(len(vectors))

	############################################################################
	# Brush Settings
	brush_size = 16
	brush = "GIMP Brush #7"
	# brush_dynamics = "Dynamics Off"
	brush_dynamics = "Det1"
	
	pdb.gimp_context_set_brush(brush)
	pdb.gimp_context_set_opacity((100))
	pdb.gimp_context_set_dynamics(brush_dynamics)
	pdb.gimp_context_set_brush_size(brush_size)
	pdb.gimp_context_set_foreground((128,0,128,50))
	pdb.gimp_context_set_background((255,255,255,100))

	pdb.gimp_context_push()

	#pdb.gimp_paintbrush(layer,100,4,[10, 10, 200, 10],0,0)
	#pdb.gimp_paintbrush(layer,200,4,[10, 10, 200, 10],0,0)
	
	# TO DO: emulate brush dynamics?????
	for vector in vectors:
		pdb.gimp_edit_stroke_vectors(layer, vector)
		
	# Background
	background = pdb.gimp_layer_new(                    
        image, 256, 256,
        RGBA_IMAGE, "background", 100, NORMAL_MODE
    )    
	pdb.gimp_image_insert_layer(image, background,
                                parent, 1)    
	pdb.gimp_edit_fill(background, BACKGROUND_FILL)

	print "saving..."
	out_dir = os.getcwd() + "/../results"
	out_time = datetime.datetime.now()
	date_str = out_time.strftime('%Y%m%d_%H%M')   
	out_file = "/stroke_opacity_test_" + date_str
	out_path_png = out_dir + out_file + ".png"

	pdb.file_png_save_defaults(
		image, 
		parent,
		out_path_png,
		out_path_png
	)
	
	out_path_xcf = out_dir + out_file + ".xcf"
	pdb.gimp_xcf_save(
        0,
        image,
        parent,
        out_path_xcf,
        out_path_xcf
    )
	
	print "END"

register(
	"stroke_path_test", 
	"", 
	"", 
	"Max Hartl", 
	"Max Hartl", 
	"2015",
	"<Toolbox>/Scripts/StrokePathTest", "",
	[],
	[],
	run
	)
main()