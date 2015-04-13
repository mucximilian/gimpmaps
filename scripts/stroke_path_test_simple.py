#! /usr/bin/env python
from gimpfu import *

def run():
	"""Stroke SVG Paths"""
	brush_size = 20
	brush = "GIMP Brush #7"
	# brush = "GIMP Brush #7"
	# brush_dynamics = "Dynamics Off"
	brush_dynamics = "Deter1"

	pdb.gimp_context_set_background((255,255,255,255))
	pdb.gimp_context_set_foreground((128,0,128,255))
	
	width = 256
	height = 256

	print "brush/size=" + brush + "/" + str(brush_size)

	image = pdb.gimp_image_new(width, height, RGB)

	# layer = gimp.Layer(image, "layer", image.width, image.height, 
	# 	RGBA_IMAGE, 100, NORMAL_MODE)
	# image.add_layer(layer)

	layer = pdb.gimp_layer_new(image, width, height, RGBA_IMAGE,
		"layer", 100, NORMAL_MODE)
	pdb.gimp_image_insert_layer(image, layer, None, 0)
	
	pdb.gimp_edit_fill(layer, BACKGROUND_FILL)

	pdb.gimp_vectors_import_from_string(image,
		'<path d="M 100,150 120,100 170,200"/>',
		-1, 1, 1, )

	pdb.gimp_context_push()

	pdb.gimp_context_set_brush(brush)
	pdb.gimp_context_set_dynamics(brush_dynamics)
	pdb.gimp_context_set_brush_size(brush_size)

	#pdb.gimp_context_push()

	# Edit/Stroke/Path
	pdb.gimp_edit_stroke_vectors(layer, vector)

	print "saving"
	out_file = "/home/mucx/Pictures/script_test_br" + str(brush_size) + ".png"

	pdb.file_png_save_defaults(
		image, 
		layer,
		out_file,
		out_file
	)
	print "END"

register(
	"stroke_path_test_simple", 
	"", 
	"", 
	"Max Hartl", 
	"Max Hartl", 
	"2015",
	"<Toolbox>/Scripts/StrokePathTestSimple", "",
	[],
	[],
	run
	)
main()