#!/usr/bin/env python

# Draws a 150 px radius circle centered in an 800x600 px image
# Adapted from a scheme script-fu contributed by Simon Budig

from gimpfu import *

def draw_circle():

  width = 600
  height = 600

  image = pdb.gimp_image_new(width, height, RGB)

  layer = gimp.Layer(image, "layer", image.width, image.height,
    RGBA_IMAGE, 100, NORMAL_MODE)
  image.add_layer(layer)

  gimp.set_foreground(0, 0, 0)
  pdb.gimp_context_set_brush("Circle (03)")  
  
  vectors = pdb.gimp_vectors_new(image, "circle")
  pdb.gimp_image_add_vectors(image, vectors, -1)
  pdb.gimp_vectors_bezier_stroke_new_ellipse(vectors, 400, 300, 150, 150, 0)
  pdb.gimp_image_set_active_vectors(image, vectors)
  
  print "stroking"
  pdb.gimp_edit_stroke_vectors(layer, vectors)
  pdb.gimp_displays_flush()

  out_path ="/home/mucx/Pictures/test.png"

  print "saving"
  pdb.file_png_save_defaults(
    image, 
    layer,
    out_path,
    out_path
  )
  
register(
    "python-fu-draw-circle",
    N_("Draw a circle"),
    "Simple example of stroking a circular path",
    "Simon Budig",
    "Simon Budig",
    "2007",
    N_("_Draw Circle"),
    "RGB*, GRAY*",
    [],
    [],
    draw_circle,
    menu="<Image>/Python-fu"
    )

main()