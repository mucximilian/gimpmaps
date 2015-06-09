'''
Created on Jun 9, 2015

@author: mucx
'''

import svgmodule

drawing = svgmodule.Drawing("test")

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

curve = [
    [100, 200],
    [108, 191],
    [183, 100.0],
    [200, 100],
    [216, 100.0],
    [291, 191],
    [300, 200]
]

style = svgmodule.StyleLine(1, "blue", "none")
drawing.add_path_bezier(curve, style)

print drawing.paths_bezier
print drawing.path_bezier_groups

drawing.create("fit")

drawing.save()