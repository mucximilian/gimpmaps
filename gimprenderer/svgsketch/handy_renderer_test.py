'''
Created on Jun 5, 2015

@author: mucx
'''

import sketching

handy_renderer = sketching.HandyRenderer(1234)

line = [[100,100],[400,200]]

lines = handy_renderer.line(line, 2.0)

# print handy_renderer.line_as_wkt(lines[0])
# print handy_renderer.line_as_wkt(lines[1])
# 
# print handy_renderer.catmull_rom_to_bezier(lines[0])
# print handy_renderer.catmull_rom_to_bezier(lines[1])

line1_bez = handy_renderer.catmull_rom_bezier(lines[0])
line2_bez = handy_renderer.catmull_rom_bezier(lines[1])

print line1_bez
print line2_bez

# line = [[100,200],[250,180],[400,220]]

# print handy_renderer.catmull_rom_to_bezier(line)