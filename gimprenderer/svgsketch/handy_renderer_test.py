'''
Created on Jun 5, 2015

@author: mucx
'''

import sketching
import svgmodule

handy_renderer = sketching.HandyRenderer(1234)

line = [[100,100],[1600,650]]

lines1 = []
lines2 = []

points1 = []
points2 = []
points_m = []
points_n = []

line_cnt = 1000

for i in range (0, line_cnt):

    lines = handy_renderer.line(line, 2.0)
    
    line1 = handy_renderer.catmull_rom_bezier(lines[0])
    line2 = handy_renderer.catmull_rom_bezier(lines[1])
    
    lines1.append(line1)
    lines2.append(line2)
    
    points1.append(line1[0])
    points2.append(line1[9])
    points_n.append(line1[3])
    points_m.append(line1[6])
    
    points1.append(line2[0])
    points2.append(line2[9])
    points_n.append(line2[3])
    points_m.append(line2[6])

filename = "results/handy_test_" + str(line_cnt) + "l"
drawing = svgmodule.Drawing(filename)

style = svgmodule.StyleLine(0.2, "blue", "none")
drawing.add_path_bezier_group(lines1, style)
style = svgmodule.StyleLine(0.2, "orange", "none")
drawing.add_path_bezier_group(lines2, style)

style = svgmodule.StyleCircle(5, "none", "grey", 1)
drawing.add_circle_group(points1, style)
style = svgmodule.StyleCircle(5, "none", "grey", 1)
drawing.add_circle_group(points2, style)
style = svgmodule.StyleCircle(5, "none", "green", 1)
drawing.add_circle_group(points_n, style)
style = svgmodule.StyleCircle(5, "none", "yellow", 1)
drawing.add_circle_group(points_m, style)

drawing.create("fit")

drawing.save()

# print handy_renderer.line_as_wkt(lines[0])
# print handy_renderer.line_as_wkt(lines[1])

# line = [[100,200],[250,180],[400,220]]

# print handy_renderer.catmull_rom_to_bezier(line)