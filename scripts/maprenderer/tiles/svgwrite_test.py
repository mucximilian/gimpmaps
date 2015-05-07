# -*- coding: utf-8 -*-

import svgwrite

dwg = svgwrite.Drawing(height=100, width=100)

path = dwg.path(d='M 11610 -256 l -24 309 22 2 -3 75 -20 -1')

print path.tostring()