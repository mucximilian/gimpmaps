#! /usr/bin/env python
from gimpfu import *
import os
import datetime

def run():
	brush_size = 6
	brush = "GIMP Brush #7"
	# brush = "GIMP Brush #7"
	# brush_dynamics = "Dynamics Off"
	brush_dynamics = "Det3"

	pdb.gimp_context_set_background((255,255,255,255))
	pdb.gimp_context_set_foreground((128,0,128,255))
	
	width = 256
	height = 256

	image = pdb.gimp_image_new(width, height, RGB)
	
	parent = pdb.gimp_layer_group_new(image)
	pdb.gimp_image_insert_layer(image, parent, None, 0)
	
	text_layer = pdb.gimp_text_layer_new(image, "Text", "Arial", 60, UNIT_PIXEL)
	pdb.gimp_image_insert_layer(image, text_layer, parent, 0)
	
	layer = pdb.gimp_layer_new(image, width, height, RGBA_IMAGE,
		"layer", 100, NORMAL_MODE)
	pdb.gimp_image_insert_layer(image, layer, parent, 1)
	
	pdb.gimp_edit_fill(layer, BACKGROUND_FILL)
	
	vectors = pdb.gimp_vectors_new_from_text_layer(image, text_layer)	
	print vectors
	pdb.gimp_image_insert_vectors(image, vectors, None, 0)
	

	out_dir = os.getcwd()
	out_time = datetime.datetime.now()
	date_str = out_time.strftime('%Y%m%d_%H%M')
	out_file = "/stroke_text_path_test_" + date_str
	out_path = out_dir + out_file
	out_path_xcf = out_path + ".xcf"
	print "file: " + out_path_xcf
	pdb.gimp_xcf_save(
	    0,
	    image,
	    parent,
	    out_path_xcf,
	    out_path_xcf
	)

register(
	"stroke_path_text_layer_test", 
	"", 
	"", 
	"Max Hartl", 
	"Max Hartl", 
	"2015",
	"<Toolbox>/Scripts/StrokePathTextLayerTest", "",
	[],
	[],
	run
	)
main()