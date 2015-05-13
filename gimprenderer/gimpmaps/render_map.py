'''
Created on May 11, 2015

@author: mucx
'''

from gimpmaps import renderergimp

ul_x = 1275000
ul_y = 6131500
lr_x = 1289700
lr_y = 6118200

scale = 10000
map_style_id = 1
create_xcf = False

bbox = [[ul_x, ul_y], [lr_x, lr_y]]
    
gimp_renderer = renderergimp.RendererGimp(
    bbox, 
    scale,
    None, # out_dir undefined, default used
    map_style_id,
    create_xcf
)

gimp_renderer.render_map()