'''
Created on Jun 5, 2015

@author: mucx
'''

import sketching

handy_renderer = sketching.HandyRenderer(42)
# 
# line = [[100,100],[500,200]]
# 
# line_sketch = sketch_renderer.add_sketch_points(line, 1)
# 
# print sketch_renderer.create_bezier_path(line_sketch)

# print sketch_renderer.displace_point_circle([1,1], 1)

# print sketch_renderer.calculate_point_at_line_pos([[1,1],[4,2]], 0.75)

ls = handy_renderer.handy_line([[1,1],[40,12]], 1)
# 
# handy_renderer.print_line_as_wkt(ls[0])
# handy_renderer.print_line_as_wkt(ls[1])
# 
# print handy_renderer.create_bezier_path(ls[0])

# line = [[100,200],[250,220],[400,180],[550,200]]

handy_renderer.print_line_as_svg(ls[0])
print handy_renderer.catmullRom2bezier(ls[0])