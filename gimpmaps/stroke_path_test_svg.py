#! /usr/bin/env python
from gimpfu import *
import os

def run():
	brush_size = 20
	brush = "GIMP Brush #7"
	brush_dynamics = "Det1"

	pdb.gimp_context_set_background((255,255,255,255))
	pdb.gimp_context_set_foreground((128,0,128,255))
	
	width = 256
	height = 256

	image = pdb.gimp_image_new(width, height, RGB)
	
	parent = pdb.gimp_layer_group_new(image)
	pdb.gimp_image_insert_layer(image, parent, None, 0)

	layer = pdb.gimp_layer_new(image, width, height, RGBA_IMAGE,
		"layer", 100, NORMAL_MODE)
	pdb.gimp_image_insert_layer(image, layer, parent, 0)
	
	pdb.gimp_edit_fill(layer, BACKGROUND_FILL)

# 	pdb.gimp_vectors_import_from_string(image,
# 		('<svg height="256" width="256">' +
# 		'<path d="M 100,150 120,100 170,200"/>' + 
# 		'</svg>'), # WORKING
# 		#'<path d="M 100,150 120,100 170,200"/>', # WORKING
# 		# "M 100,150 120,100 170,200", # NOT WORKING
# 		-1, 1, 1, )
	
	pdb.gimp_vectors_import_from_string(image,
		("""
		<g>
		<path fill-rule="evenodd" fill="#66cc99" stroke="#555555" stroke-width="2.0" opacity="0.6" d="M 197.0,69.0 L 198.0,65.0 L 202.0,65.0 L 204.0,63.0 L 200.0,56.0 L 202.0,49.0 L 199.0,48.0 L 198.0,46.0 L 215.0,37.0 L 219.0,39.0 L 216.0,40.0 L 218.0,47.0 L 218.0,49.0 L 211.0,52.0 L 215.0,75.0 L 202.0,76.0 L 197.0,71.0 L 197.0,69.0 z" />
		</g>
"""), # WORKING
		#'<path d="M 100,150 120,100 170,200"/>', # WORKING
		# "M 100,150 120,100 170,200", # NOT WORKING
		-1, 1, 1, )

	pdb.gimp_context_push()

	pdb.gimp_context_set_brush(brush)
	pdb.gimp_context_set_dynamics(brush_dynamics)
	pdb.gimp_context_set_brush_size(brush_size)
	pdb.gimp_context_push()
	
	print len(image.vectors)

	# Edit/Stroke/Path
	for vector in image.vectors:
		pdb.gimp_edit_stroke_vectors(layer, vector)

	out_file = os.getcwd() + ("/script_test_svg_br_" + str(brush_size))

	pdb.file_png_save_defaults(
		image, 
		parent,
		out_file + ".png",
		out_file + ".png"
	)
	
	pdb.gimp_xcf_save(
	    0,
	    image,
	    parent,
	    out_file + ".xcf",
		out_file + ".xcf"
	)

register(
	"stroke_path_test_svg", 
	"", 
	"", 
	"Max Hartl", 
	"Max Hartl", 
	"2015",
	"<Toolbox>/Scripts/StrokePathTestSVG", "",
	[],
	[],
	run
	)
main()