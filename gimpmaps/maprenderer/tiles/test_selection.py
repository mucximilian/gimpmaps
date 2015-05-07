# -*- coding: utf-8 -*-
from ZoomSelection import ZoomSelection

zoom_selection_lines = ZoomSelection()        
selection = zoom_selection_lines.lines[5]

for bla in selection:
    print bla["tags"]
    print bla["style"]["brush"]
