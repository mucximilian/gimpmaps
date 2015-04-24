#! /usr/bin/env python
from gimpfu import *
import os

import datetime
import math


origin_x = -(2 * math.pi * 6378137 / 2.0)
origin_y = 2 * math.pi * 6378137 / 2.0

def run():
	image = pdb.gimp_image_new(256, 256, RGB)
	pdb.gimp_context_set_background((255,255,255,255))
	
	# Creating a 'top' layer group that will contain all the
	# layer groups added in the following steps
	group_top = pdb.gimp_layer_group_new(image)
	pdb.gimp_image_insert_layer(image, group_top, None, 0)
	
	############################################################################
	# LAYER 1
	layer_1 = pdb.gimp_layer_new(
	    image, 256, 256,
	    RGBA_IMAGE,
	    "layer_1",
	    100, NORMAL_MODE
	)
	pdb.gimp_image_insert_layer(image, layer_1, group_top, 0)
	
	pdb.gimp_context_set_defaults()
	pdb.gimp_context_push()
	pdb.gimp_context_pop()
	pdb.gimp_context_set_brush("GIMP Brush #7")
	pdb.gimp_context_set_brush_size(20)
	pdb.gimp_context_set_dynamics("Det3")
	pdb.gimp_context_set_foreground((128,0,128,255))
	pdb.gimp_context_push()
	
	pdb.gimp_vectors_import_from_string(image,
		'<path d="M 100,100 120,50 170,150"/>',
		-1, 1, 1, )
	pdb.gimp_vectors_import_from_string(image,
		'<path d="M 0,100 20,100 70,120"/>',
		-1, 1, 1, )
	
	for vector in image.vectors:
		print "stroking vector"
		pdb.gimp_edit_stroke_vectors(layer_1, vector)
		pdb.gimp_image_remove_vectors(image, vector)
		
	############################################################################
	# LAYER 2
	layer_2 = pdb.gimp_layer_new(
	    image, 256, 256,
	    RGBA_IMAGE,
	    "layer_2",
	    100, NORMAL_MODE
	)
	pdb.gimp_image_insert_layer(image, layer_2, group_top, 1)
	
	pdb.gimp_context_pop()
	pdb.gimp_context_set_brush("GIMP Brush #7")
	pdb.gimp_context_set_brush_size(5)
	pdb.gimp_context_set_dynamics("Det3")
	pdb.gimp_context_set_foreground((64,64,128,255))
	pdb.gimp_context_push()
	
	
	pdb.gimp_vectors_import_from_string(image,
		'<path d="M 50,230 200,230"/>',
		-1, 1, 1, )
	pdb.gimp_vectors_import_from_string(image,
		'<path d="M 50,200 200,200"/>',
		-1, 1, 1, )
	
	for vector in image.vectors:
		print "stroking vector"
		pdb.gimp_edit_stroke_vectors(layer_2, vector)
		pdb.gimp_image_remove_vectors(image, vector)
	
	############################################################################
	# BACKGROUND
	background = pdb.gimp_layer_new(                    
	    image, 256, 256,
	    RGBA_IMAGE, "background", 100, NORMAL_MODE
	)    
	pdb.gimp_image_insert_layer(image, background, group_top, 2)
	
	pdb.gimp_edit_fill(background, BACKGROUND_FILL)
	
	############################################################################
	# SAVING
	out_dir = os.getcwd()
	out_time = datetime.datetime.now()
	date_str = out_time.strftime('%Y%m%d_%H%M')   
	out_file = "/script_test_layer_" + date_str
	out_path = out_dir + out_file
	
	out_path_xcf = out_path + ".xcf"   
	pdb.gimp_xcf_save(
	    0,
	    image,
	    group_top,
	    out_path_xcf,
	    out_path_xcf
	)

register(
	"stroke_path_layer_test", 
	"", 
	"", 
	"Max Hartl", 
	"Max Hartl", 
	"2015",
	"<Toolbox>/Scripts/StrokePathLayerTest", "",
	[],
	[],
	run
	)
main()