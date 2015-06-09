'''
Created on Jun 5, 2015

@author: mucx
'''

import sketching

sketch_renderer = sketching.SketchRenderer(1234)

# line = [[100,200],[250,220],[400,180],[550,200]]
# line_bez = sketch_renderer.to_bezier_curve(line)
# print line_bez

# line = [[100,100],[500,200]]
#  
# line_sketchy = sketch_renderer.add_sketch_points(line, 1)
#  
# print sketch_renderer.to_bezier_curve(line_sketchy)
# 
# print sketch_renderer.displace_point_circle([1,1], 1)
# print sketch_renderer.calculate_point_at_line_pos([[1,1],[4,2]], 0.75)

line = [[1100,1200],[1200,1100],[1300,1200]]
# line = [[500,200],[600,300],[700,200]]

curve1 = sketch_renderer.simple_bezier(line, 0.5)
print curve1
print sketch_renderer.curve_to_svg_bezier(curve1)

curve2 = sketch_renderer.catmull_rom_bezier(line, 0.5)
print curve2
print sketch_renderer.curve_to_svg_bezier(curve2)

    