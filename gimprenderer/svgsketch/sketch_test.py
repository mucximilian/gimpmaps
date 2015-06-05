'''
Created on Jun 5, 2015

@author: mucx
'''

from sketching import SketchRenderer

sketch_renderer = SketchRenderer(1232)
# 
# line = [[100,100],[500,200]]
# 
# line_sketch = sketch_renderer.add_sketch_points(line, 1)
# 
# print sketch_renderer.create_bezier_path(line_sketch)

print sketch_renderer.displace_point_circle([1,1], 1)