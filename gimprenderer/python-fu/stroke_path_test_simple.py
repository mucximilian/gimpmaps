#! /usr/bin/env python
from gimpfu import *
import os

def run():
	brush_size = 20
	brush = "GIMP Brush #7"
	# brush = "GIMP Brush #7"
	# brush_dynamics = "Dynamics Off"
	brush_dynamics = "Det3"

	pdb.gimp_context_set_background((255,255,255,255))
	pdb.gimp_context_set_foreground((128,0,128,255))
	
	width = 256
	height = 256

	image = pdb.gimp_image_new(width, height, RGB)

	layer = pdb.gimp_layer_new(image, width, height, RGBA_IMAGE,
		"layer", 100, NORMAL_MODE)
	pdb.gimp_image_insert_layer(image, layer, None, 0)
	
	pdb.gimp_edit_fill(layer, BACKGROUND_FILL)

	pdb.gimp_vectors_import_from_string(image,
		# '<path d="M 223 265 L 223 263 223 252 223 249 223 236"/>',
		'<path d="M 223 9 L 223 7 223 -4 223 -7 223 -20"/>',
		-1, 1, 1, )

	pdb.gimp_context_set_brush(brush)
	pdb.gimp_context_set_dynamics(brush_dynamics)
	pdb.gimp_context_set_brush_size(brush_size)
	pdb.gimp_context_push()

	# Edit/Stroke/Path
	for vector in image.vectors:
		pdb.gimp_edit_stroke_vectors(layer, vector)

	out_file = os.getcwd() + ("/script_test_simple_2_br_" + 
		str(brush_size) + 
		".png")

	pdb.file_png_save_defaults(
		image, 
		layer,
		out_file,
		out_file
	)

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