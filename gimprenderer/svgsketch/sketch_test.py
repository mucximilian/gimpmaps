'''
Created on Jun 5, 2015

@author: mucx
'''

import sketching

handy_renderer = sketching.HandyRenderer(1234)

# line = [[100,100],[500,200]]
# 
# line_sketch = handy_renderer.add_sketch_points(line, 1)
# 
# print handy_renderer.to_bezier_curve(line_sketch)
#
# print handy_renderer.displace_point_circle([1,1], 1)

# print handy_renderer.calculate_point_at_line_pos([[1,1],[4,2]], 0.75)

lines = handy_renderer.line([[100,100],[400,200]], 2.0)

# print handy_renderer.line_as_wkt(ls[0])
# print handy_renderer.line_as_wkt(ls[1])
# 
# print handy_renderer.create_bezier_path(ls[0])

# line = [[100,200],[250,220],[400,180],[550,200]]

line1_svg = handy_renderer.line_as_svg(lines[0])
line1_bez = handy_renderer.catmull_rom_to_bezier(lines[0])

line2_svg = handy_renderer.line_as_svg(lines[1])
line2_bez = handy_renderer.catmull_rom_to_bezier(lines[1])

print line1_svg
print line1_bez
print line2_svg
print line2_bez

print handy_renderer.as_svg_path(line1_svg)
print handy_renderer.as_svg_path(line1_bez)
print handy_renderer.as_svg_path(line2_svg)
print handy_renderer.as_svg_path(line2_bez)

# line = [[100,200],[250,180],[400,220]]

# print handy_renderer.catmull_rom_to_bezier(line)