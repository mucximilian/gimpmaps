#! /usr/bin/env python
from gimpfu import *
import os

def run():
	"""Stroke SVG Paths"""
	
	print "START"
	print pdb.gimp_version()

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
	pdb.gimp_vectors_import_from_string(image,
		'<path d="M 0,100 20,100 70,120"/>',
		-1, 1, 1, )
	
	vectors = image.vectors

	print "vectors=" + str(len(vectors))

	pdb.gimp_image_set_active_vectors(image, vectors)

	# pdb.gimp_context_push()

	print "brush"
	pdb.gimp_context_set_brush(brush)

	print "dynamics"
	pdb.gimp_context_set_dynamics(brush_dynamics)

	print "brush-size"
	pdb.gimp_context_set_brush_size(brush_size)

	pdb.gimp_context_push()

	# Edit/Stroke/Path
	print "vectors:" + str(len(vectors))
	for vector in vectors:
		print "stroking vector"
		# pdb.gimp_edit_stroke_vectors(layer, vector)
		pdb.gimp_edit_stroke_vectors(layer, vector)

	print "saving"
	out_dir = "/media/data/daten/studium/master/module/master_thesis/rendering/gimp/python-fu/results/"
	out_file = "script_test_br" + str(brush_size) + ".png"
	out_path = out_dir + out_file

	pdb.file_png_save_defaults(
		image, 
		layer,
		out_path,
		out_path
	)
	print "END"

register(
	"stroke_path_test_neu", 
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