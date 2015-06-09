'''
Created on Jun 9, 2015

@author: mucx
'''

import svgmodule

drawing = svgmodule.Drawing("test")

point_group_1 = []
point_group_1.append([123,234])
point_group_1.append([133,254])
point_group_1.append([143,244])

style1 = svgmodule.StyleCircle(5, "none", "yellow", 5)
drawing.add_circle_group(point_group_1, style1)

point_group_2 = []
point_group_2.append([463,784])
point_group_2.append([533,954])
point_group_2.append([613,814])

style2 = svgmodule.StyleCircle(5, "none", "red", 5)
drawing.add_circle_group(point_group_2, style2)

path_group = []
path_group.append(
    [
        [784,546],
        [923,489],
        [1101,399]
    ]
)
path_group.append(
    [
        [744,446],
        [933,389],
        [1001,299]
    ]
)

style = svgmodule.StyleLine(1, "orange", "none")
drawing.add_path_group(path_group, style)

bez_group = []
bez_group.append(
    [
        [1100, 1200],
        [1100, 1200],
        [1150.0, 1100.0],
        [1200, 1100],
        [1250.0, 1100.0],
        [1300, 1200],
        [1300, 1200]
    ]
)
bez_group.append(
    [
        [1100, 1200],
        [1108, 1191],
        [1183, 1100.0],
        [1200, 1100],
        [1216, 1100.0],
        [1291, 1191],
        [1300, 1200]
    ]
)

style = svgmodule.StyleLine(1, "red", "none")
drawing.add_path_bezier_group(bez_group, style)

bez = [
    [100, 200],
    [108, 191],
    [183, 100.0],
    [200, 100],
    [216, 100.0],
    [291, 191],
    [300, 200]
]

style = svgmodule.StyleLine(1, "red", "none")
drawing.add_path_bezier(bez, style)

drawing.create("fit")

drawing.save()