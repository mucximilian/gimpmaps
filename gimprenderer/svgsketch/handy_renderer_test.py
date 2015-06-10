'''
Created on Jun 5, 2015

@author: mucx
'''

import sketching
import svgmodule

def draw_lines():
    
    lines1 = []
    lines2 = []
    
    points1 = []
    points2 = []
    points_m = []
    points_n = []
    
    handy_renderer = sketching.HandyRenderer(seed, roughness, bowing)
    
    for j in range (0, line_count):
    
        lines = handy_renderer.line(line, max_offset)
        
        line1 = handy_renderer.catmull_rom_bezier(lines[0], t)
        line2 = handy_renderer.catmull_rom_bezier(lines[1], t)
        
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
    
    param_str = "_".join(map(str, params))
    line_count_str = str(line_count) + "l"
    filename = "results/handy_test/linetest_" + param_str + "_" + line_count_str
    drawing = svgmodule.Drawing(filename, [1700, 1700])
    
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
    
    drawing.create("fixed_centered", "no_date")
    
    drawing.save()

################################################################################
seed = 1234

roughnesses = [0.5, 2.0, 5.0, 10.0]
bowings = [0.5, 1.0, 2.0, 5.0, 10.0]
max_offsets = [0.5, 1.0, 2.0, 5.0, 10.0]
ts = [0.5, 1.0, 2.0] # The bezier tension

line = [[100.0,100.0],[1600.0,650.0]]

line_counts = [10, 100, 250]

for roughness in roughnesses:
    print "" + str(roughness)
    
    for bowing in bowings:
        print "    " + str(bowing)
        
        for max_offset in max_offsets:
            print "        " + str(max_offset)
            
            for t in ts:
                print "            " + str(t)
                
                params = [seed, roughness, bowing, max_offset, t]
            
                for line_count in line_counts:
                    print "                " + str(line_count)
                    
                    draw_lines()
                
print "Done"

# print handy_renderer.line_as_wkt(lines[0])
# print handy_renderer.line_as_wkt(lines[1])

# line = [[100,200],[250,180],[400,220]]

# print handy_renderer.catmull_rom_to_bezier(line)