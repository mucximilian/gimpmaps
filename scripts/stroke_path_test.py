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

	pdb.gimp_context_set_background((255,255,255,255))

	# layer = gimp.Layer(image, "layer", image.width, image.height, 
	# 	RGBA_IMAGE, 100, NORMAL_MODE)
	# image.add_layer(layer)

	layer = pdb.gimp_layer_new(image, width, height, RGBA_IMAGE,
		"layer", 100, NORMAL_MODE)
	pdb.gimp_image_insert_layer(image, layer, None, 0)
	#pdb.gimp_image_set_active_layer(image, layer)
	
	pdb.gimp_edit_fill(layer, BACKGROUND_FILL)

	pdb.gimp_vectors_import_from_string(image,
		'<path d="M 100,100 120,50 170,150"/>',
		-1, 1, 1, )
	pdb.gimp_vectors_import_from_string(image,
		'<path d="M 0,100 20,100 70,120"/>',
		-1, 1, 1, )
	pdb.gimp_vectors_import_from_string(image,
		'<path d="M 50,230 200,230"/>',
		-1, 1, 1, )
	pdb.gimp_vectors_import_from_string(image,
		'<path d="M 50,200 200,200"/>',
		-1, 1, 1, )
	
	vectors = image.vectors

	print "vectors=" + str(len(vectors))

	############################################################################
	# Brush Settings
	brush_size = 10
	brush = "GIMP Brush #7"
	# brush_dynamics = "Dynamics Off"
	brush_dynamics = "Det1"
	
	pdb.gimp_context_set_brush(brush)
	pdb.gimp_context_set_dynamics(brush_dynamics)
	pdb.gimp_context_set_brush_size(brush_size)

	pdb.gimp_context_set_foreground((128,0,128,255))

	pdb.gimp_context_push()

	# draw = pdb.gimp_image_get_active_drawable(image)

	# Edit/Stroke/Path
	print "vectors:" + str(len(vectors))

	# TO DO: emulate brush dynamics?????
	for vector in vectors:
		print "stroking vector"
		pdb.gimp_edit_stroke_vectors(layer, vector)
		# pdb.gimp_edit_stroke_vectors(draw, vector)		

	print "saving..."
	out_dir = os.getcwd()
    
	out_time = datetime.datetime.now()
	date_str = out_time.strftime('%Y%m%d_%H%M')   
	out_file = "/script_test_" + date_str + ".png"
	out_path = out_dir + out_file

	print "file: " + out_path

	pdb.file_png_save_defaults(
		image, 
		layer,
		out_path,
		out_path
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