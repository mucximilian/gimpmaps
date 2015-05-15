#! /usr/bin/env python
from gimpfu import *
import os

def run():
	brush_size = 6
	brush = "Chalk 03"
	# brush = "GIMP Brush #7"
	# brush_dynamics = "Dynamics Off"
	brush_dynamics = "Det3"

	pdb.gimp_context_set_background((255,255,255,255))
	
	width = 256
	height = 256

	image = pdb.gimp_image_new(width, height, RGB)
	
	background = pdb.gimp_layer_new(image, width, height, RGBA_IMAGE,
		"layer", 100, NORMAL_MODE)
	pdb.gimp_image_insert_layer(image, background, None, -1)	
	pdb.gimp_edit_fill(background, BACKGROUND_FILL)
	
	text_group = pdb.gimp_layer_group_new(image)
	pdb.gimp_image_insert_layer(image, text_group, None, -1)
	
	# layer_text = pdb.gimp_text_layer_new(image, "Text", "Arial", 20, UNIT_PIXEL)
	
	text_layer = pdb.gimp_layer_new(image, width, height, RGBA_IMAGE,
							"text_layer", 100, NORMAL_MODE)
	pdb.gimp_image_insert_layer(image, text_layer, text_group, -1)
	
	text = "Blag"
	
	pdb.gimp_context_set_foreground((200,200,200,100))
	
	text_fill = pdb.gimp_text_fontname(
						image,
						text_layer, # Drawable for floating sel or None for text
						50,
						50,
						text,
						0,
						True,
						100,
						UNIT_PIXEL,
						"Arial"
						)
	
	print pdb.gimp_text_get_extents_fontname(text,
						100,
						UNIT_PIXEL,
						"Arial"
						)
	
	vectors = pdb.gimp_vectors_new_from_text_layer(image, text_fill)	
	pdb.gimp_image_insert_vectors(image, vectors, None, 0)
	
	pdb.gimp_context_set_brush((brush))
	pdb.gimp_context_set_opacity((50))
	pdb.gimp_context_set_dynamics(brush_dynamics)
	pdb.gimp_context_set_brush_size(brush_size)
	pdb.gimp_context_set_foreground((200,200,200,100))
	pdb.gimp_context_push()
	
	pdb.gimp_floating_sel_anchor(text_fill)
	
	pdb.gimp_context_set_foreground((128,0,128,50))
	
	text_layer_stroke = pdb.gimp_layer_new(image, width, height, RGBA_IMAGE,
							"text_layer_stroke", 100, NORMAL_MODE)
	pdb.gimp_image_insert_layer(image, text_layer_stroke, text_group, -1)

	for vector in image.vectors:
		pdb.gimp_edit_stroke_vectors(text_layer_stroke, vector)

	out_file = os.getcwd() + "/gimpmaps/results/test/stroke_text_path_test.xcf"
	pdb.gimp_file_save(
        image, 
        text_group,
        out_file,
        out_file
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